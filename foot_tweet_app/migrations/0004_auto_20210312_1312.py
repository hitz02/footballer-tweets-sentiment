# Generated by Django 3.1.7 on 2021-03-12 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foot_tweet_app', '0003_sentiment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sentiment',
            old_name='tweet',
            new_name='cleaned_tweet',
        ),
    ]
