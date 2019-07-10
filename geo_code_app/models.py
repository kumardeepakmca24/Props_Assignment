# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class GeoFileUpload(models.Model):
    '''Model class to save upload file details in database
    '''
    pk_id = models.AutoField(primary_key=True, db_column="pk_id")
    file_name = models.CharField(max_length=100)
    new_file_name = models.CharField(max_length=100, null=True, blank=True)
    file_path = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{0} - {1}'.format(self.file_name, self.new_file_name)

    def __repr__(self):
        return '<GeoFileUpload: {0} - {1}>'.format(
            self.file_name, self.new_file_name)
