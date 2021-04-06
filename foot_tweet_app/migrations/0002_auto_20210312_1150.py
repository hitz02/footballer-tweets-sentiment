# Generated by Django 3.1.7 on 2021-03-12 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foot_tweet_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweets',
            name='player_name',
            field=models.CharField(default='NA', max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tweets',
            name='screen_name',
            field=models.CharField(default='NA', max_length=150),
        ),
    ]
