# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-10 03:25


from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("peerinst", "0076_auto_20190402_1456")]

    operations = [
        migrations.AlterModelOptions(
            name="questionflagreason",
            options={"verbose_name": "Question flag reason"},
        ),
        migrations.AddField(
            model_name="questionflag",
            name="datetime_created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="questionflag",
            name="datetime_last_modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="questionflag",
            name="flag",
            field=models.BooleanField(default=True),
        ),
    ]
