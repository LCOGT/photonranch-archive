# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-25 17:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frames', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='version',
            options={'ordering': ['-created']},
        ),
        migrations.RenameField(
            model_name='version',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.AddField(
            model_name='frame',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 1, 25, 17, 35, 8, 391282)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='frame',
            name='INSTRUME',
            field=models.CharField(default='', help_text='Instrument used. FITS header: INSTRUME', max_length=10),
        ),
        migrations.AlterField(
            model_name='frame',
            name='L1PUBDAT',
            field=models.DateTimeField(db_index=True, help_text='The date the frame becomes public. FITS header: L1PUBDAT', null=True),
        ),
        migrations.AlterField(
            model_name='frame',
            name='PROPID',
            field=models.CharField(default='', help_text='Textual proposal id. FITS header: PROPID', max_length=200),
        ),
        migrations.AlterField(
            model_name='frame',
            name='RLEVEL',
            field=models.SmallIntegerField(default=0, help_text='Reduction level of the frame'),
        ),
    ]
