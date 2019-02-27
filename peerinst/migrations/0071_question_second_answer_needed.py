# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-27 16:02
from __future__ import unicode_literals

from django.db import migrations, models


def add_second_choice_needed_false_to_rationale_only(apps, _):
    Question = apps.get_model("peerinst", "Question")

    for question in Question.objects.filter(type="RO"):
        question.second_answer_needed = True
        question.save()


class Migration(migrations.Migration):

    dependencies = [("peerinst", "0070_answer_datetime_fix")]

    operations = [
        migrations.AddField(
            model_name="question",
            name="second_answer_needed",
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.RunPython(add_second_choice_needed_false_to_rationale_only),
    ]
