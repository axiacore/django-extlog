#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: AxiaCore S.A.S. http://axiacore.com
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django_extensions.db.fields.json import JSONField


class ExtLog(models.Model):
    ACTION_TYPE_CREATE = 1
    ACTION_TYPE_UPDATE = 2
    ACTION_TYPE_DELETE = 3
    ACTION_TYPE_CHOICES = (
        (ACTION_TYPE_CREATE, u'created'),
        (ACTION_TYPE_UPDATE, u'updated'),
        (ACTION_TYPE_DELETE, u'deleted'),
    )

    object_id = models.PositiveIntegerField(
        verbose_name=u'object ID',
        blank=True,
        null=True,
    )

    app_name = models.CharField(
        verbose_name=u'application name',
        max_length=30,
    )

    model_name = models.CharField(
        verbose_name=u'model name',
        max_length=30,
    )

    action = models.PositiveSmallIntegerField(
        verbose_name=u'action',
        choices=ACTION_TYPE_CHOICES,
    )

    object_instance = JSONField(
        default=[],
        verbose_name=u'object values after the action',
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=u'user who made the action'
    )

    ip = models.IPAddressField(
        verbose_name=u'IP',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        verbose_name=u'date and time when the changes were made',
        default=timezone.now,
    )

    def get_model_name(self):
        content_type = ContentType.objects.get(
            app_label=self.app_name,
            model=self.model_name,
        )
        return content_type.model_class()._meta.verbose_name.title()
    get_model_name.short_description = u'Model verbose name'

    class Meta:
        verbose_name = 'Ext Log'
        verbose_name_plural = 'Ext Log'
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'{0}.{1}'.format(self.app_name, self.model_name)
