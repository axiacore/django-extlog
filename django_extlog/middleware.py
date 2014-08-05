from django.db.models import signals
from django.utils.functional import curry
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session

from django_extlog.models import ExtLog


class AuditLoggingMiddleware(object):
    ip_address = None

    def process_request(self, request):
        if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated():
                user = request.user
            else:
                user = None

            session = request.session.session_key
            self.ip_address = request.META.get('REMOTE_ADDR', None)
            update_post_save_info = curry(
                self._update_post_save_info,
                user,
                session,
            )
            update_post_delete_info = curry(
                self._update_post_delete_info,
                user,
                session,
            )

            signals.post_save.connect(
                update_post_save_info,
                dispatch_uid=(self.__class__, request,),
                weak=False
            )
            signals.post_delete.connect(
                update_post_delete_info,
                dispatch_uid=(self.__class__, request,),
                weak=False
            )

    def process_response(self, request, response):
        signals.post_save.disconnect(dispatch_uid=(self.__class__, request,))
        signals.post_delete.disconnect(dispatch_uid=(self.__class__, request,))
        return response

    def _save_to_log(self, instance, action, user):

        content_type = ContentType.objects.get_for_model(instance)
        if content_type.app_label != 'django_extlog' and user:
            ExtLog.objects.create(
                object_id=instance.id,
                app_name=content_type.app_label,
                model_name=content_type.model,
                action=action,
                object_instance=serializers.serialize('json', [instance]),
                user=user,
                ip=self.ip_address,
            )

    def _update_post_save_info(
            self,
            user,
            session,
            sender,
            instance,
            **kwargs
    ):
        if sender in [LogEntry, Session]:
            return
        if kwargs['created']:
            self._save_to_log(instance, ExtLog.ACTION_TYPE_CREATE, user)
        else:
            self._save_to_log(instance, ExtLog.ACTION_TYPE_UPDATE, user)

    def _update_post_delete_info(
            self,
            user,
            session,
            sender,
            instance,
            **kwargs
    ):
        if sender in [LogEntry, Session]:
            return
        self._save_to_log(instance, ExtLog.ACTION_TYPE_DELETE, user)
