# Generated by Django 4.2.11 on 2024-06-04 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0012_contact_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(default='#ffffff', max_length=7)),
            ],
        ),
    ]
