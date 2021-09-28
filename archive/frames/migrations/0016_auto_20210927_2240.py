# Generated by Django 2.0.13 on 2021-09-27 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frames', '0015_auto_20210927_0642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='frame',
            options={'ordering': ['-observation_date']},
        ),
        migrations.RemoveField(
            model_name='frame',
            name='BLKUID',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='DATE_OBS',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='DAY_OBS',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='EXPTIME',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='FILTER',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='INSTRUME',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='L1PUBDAT',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='OBJECT',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='OBSTYPE',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='PROPID',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='REQNUM',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='RLEVEL',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='SITEID',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='TELID',
        ),
    ]
