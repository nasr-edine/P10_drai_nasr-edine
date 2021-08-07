# Generated by Django 3.2.5 on 2021-07-26 19:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0014_auto_20210726_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='issue_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='issues.issue'),
        ),
    ]
