# Generated by Django 4.2.5 on 2023-12-08 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportalapp', '0008_alter_job_job_type_alter_job_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='experience',
            field=models.CharField(max_length=200),
        ),
    ]
