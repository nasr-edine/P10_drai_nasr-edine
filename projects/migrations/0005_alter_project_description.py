# Generated by Django 3.2.5 on 2021-07-28 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_project_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
