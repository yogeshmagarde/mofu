# Generated by Django 4.0.1 on 2023-06-05 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audio_Jockey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio_jockey',
            name='Is_Approved',
            field=models.BooleanField(default=False),
        ),
    ]
