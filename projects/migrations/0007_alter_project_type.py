# Generated by Django 3.2.5 on 2021-07-28 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20210728_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('front-end', 'front-end'), ('back-end', 'back-end'), ('IOS', 'IOS'), ('Android', 'Android')], max_length=20),
        ),
    ]