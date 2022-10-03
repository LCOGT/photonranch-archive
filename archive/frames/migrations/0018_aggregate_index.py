# Generated by Django 3.2.15 on 2022-09-27 17:25

from django.db import migrations
from django.db.models.indexes import Index
from django.db.models.expressions import F


class Migration(migrations.Migration):

    dependencies = [
        ('frames', '0017_alter_frame_index_together'),
    ]

    operations = [
        migrations.AddIndex(
          "Frame",
          Index(
            F("observation_date").desc(nulls_last=True),
            F("public_date").desc(nulls_last=True),
            F("proposal_id"),
            F("configuration_type"),
            F("site_id"),
            F("telescope_id"),
            F("instrument_id"),
            F("primary_optical_element"),
            name="frames_frame_aggregate"
          )
        )
    ]
