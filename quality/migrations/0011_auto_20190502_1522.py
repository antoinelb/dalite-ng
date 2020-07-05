# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-02 15:22


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("quality", "0010_auto_20190430_1401")]

    operations = [
        migrations.AddField(
            model_name="likelihoodcriterion",
            name="for_quality_use_types",
            field=models.ManyToManyField(to="quality.QualityUseType"),
        ),
        migrations.AddField(
            model_name="mincharscriterion",
            name="for_quality_use_types",
            field=models.ManyToManyField(to="quality.QualityUseType"),
        ),
        migrations.AddField(
            model_name="minwordscriterion",
            name="for_quality_use_types",
            field=models.ManyToManyField(to="quality.QualityUseType"),
        ),
        migrations.AddField(
            model_name="negwordscriterion",
            name="for_quality_use_types",
            field=models.ManyToManyField(to="quality.QualityUseType"),
        ),
        migrations.AddField(
            model_name="rightanswercriterion",
            name="for_quality_use_types",
            field=models.ManyToManyField(to="quality.QualityUseType"),
        ),
        migrations.AddField(
            model_name="selectedanswercriterion",
            name="for_quality_use_types",
            field=models.ManyToManyField(to="quality.QualityUseType"),
        ),
    ]
