# Generated by Django 3.2.9 on 2021-12-02 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IMS_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_obj_marks', models.FloatField(default=0)),
                ('subject_pract_marks', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMS_app.students')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IMS_app.subjects')),
            ],
        ),
        migrations.RemoveField(
            model_name='notificationstudent',
            name='student_id',
        ),
        migrations.DeleteModel(
            name='NotificationStaffs',
        ),
        migrations.DeleteModel(
            name='NotificationStudent',
        ),
    ]