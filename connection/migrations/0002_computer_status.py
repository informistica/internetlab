# Generated by Django 5.1.3 on 2024-11-29 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='status',
            field=models.CharField(choices=[('blocked', 'Bloccato'), ('unblocked', 'Sbloccato')], default='unblocked', max_length=10),
        ),
    ]
