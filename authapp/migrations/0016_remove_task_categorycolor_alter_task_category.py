# Generated by Django 4.2.11 on 2024-06-11 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0015_alter_task_categorycolor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='categoryColor',
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.category'),
        ),
    ]