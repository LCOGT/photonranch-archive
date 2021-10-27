# Generated by Django 2.0.13 on 2021-09-27 06:42

from django.db import migrations
from django.db.utils import ProgrammingError


def forward(apps, schema_editor):
    # Fill in the configuration_type_links from the existing configuration_types in each instrument_type
    Frame = apps.get_model('frames', 'Frame')
    for frame in Frame.objects.using(schema_editor.connection.alias):
        frame.observation_date = frame.DATE_OBS
        frame.observation_day = frame.DAY_OBS
        frame.proposal_id = frame.PROPID
        frame.instrument_id = frame.INSTRUME
        frame.target_name = frame.OBJECT
        frame.reduction_level = frame.RLEVEL
        frame.site_id = frame.SITEID
        frame.telescope_id = frame.TELID
        frame.exposure_time = frame.EXPTIME
        frame.primary_filter = frame.FILTER
        frame.public_date = frame.L1PUBDAT
        frame.configuration_type = frame.OBSTYPE
        frame.observation_id = frame.BLKUID
        frame.request_id = frame.REQNUM
        frame.save()


class Migration(migrations.Migration):

    dependencies = [
        ('frames', '0014_auto_20210927_0639'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]
