# Generated by Django 5.0.6 on 2024-05-30 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_company_company_id_alter_company_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='company_id',
        ),
    ]
