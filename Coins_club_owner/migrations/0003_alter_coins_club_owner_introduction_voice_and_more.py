# Generated by Django 4.0.1 on 2023-06-14 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Coins_club_owner', '0002_coins_club_owner_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coins_club_owner',
            name='Introduction_voice',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='coins_club_owner',
            name='profile_picture',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
