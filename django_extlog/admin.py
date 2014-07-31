#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: AxiaCore S.A.S. http://axiacore.com
from django.contrib import admin
from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html

from django_extlog.models import ExtLog
from django_extensions.db.fields.json import JSONField


class JSONReadonlyTextArea(forms.Textarea):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        html = u''
        if value:
            for key, item in value[0]['fields'].items():
                html += u'''
                    <strong>{0}</strong>: {1} <br />
                    '''.format(key, force_text(item))
        return format_html(html)


class ExtLogAdmin(admin.ModelAdmin):

    list_filter = [
        'user',
        'action',
        'created_at',
    ]

    date_hierarchy = 'created_at'

    list_display = [
        'created_at',
        'action',
        'get_model_name',
        'object_id',
        'user',
        'ip',
    ]

    search_fields = [
        'object_instance',
        'ip',
    ]

    formfield_overrides = {
        JSONField: {'widget': JSONReadonlyTextArea},
    }

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super(ExtLogAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        if 'object_instance' in readonly_fields:
            readonly_fields.remove('object_instance')
        return readonly_fields

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'object_instance':
            kwargs['widget'] = JSONReadonlyTextArea()
        return super(ExtLogAdmin, self).formfield_for_dbfield(
            db_field,
            **kwargs
        )

admin.site.register(ExtLog, ExtLogAdmin)
