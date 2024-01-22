# Generated by Django 4.2.5 on 2023-12-08 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobportalapp', '0009_alter_job_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='apply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(upload_to='media')),
                ('applydate', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Declined', 'Declined'), ('Pending', 'Pending')], max_length=20)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportalapp.jobseeker')),
                ('jobapply_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportalapp.job')),
            ],
        ),
    ]