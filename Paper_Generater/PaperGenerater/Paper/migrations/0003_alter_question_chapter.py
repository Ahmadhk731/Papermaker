# Generated by Django 5.0.6 on 2024-11-30 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Paper', '0002_rename_subject_question_chapter_chapter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='Paper.chapter'),
        ),
    ]