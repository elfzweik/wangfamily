# -*- coding:utf-8 -*-
from __future__ import unicode_literals
 
from django.contrib.contenttypes.models import ContentType
 
def run():
    failed_list = []
 
    def do(table):
        if table is not None:
            try:
                table_objects = table.objects.all()
                for i in table_objects:
                    i.save(using='slave')
            except:
                failed_list.append(table)
 
    ContentType.objects.using('slave').all().delete()
 
    for i in ContentType.objects.all():
        do(i.model_class())
 
    while failed_list:
        table = failed_list.pop(0)
        do(table)