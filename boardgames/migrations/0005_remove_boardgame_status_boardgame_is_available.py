# Generated by Django 4.2 on 2023-04-21 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardgames', '0004_alter_boardgame_options_boardgame_date_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardgame',
            name='status',
        ),
        migrations.AddField(
            model_name='boardgame',
            name='is_available',
            field=models.BooleanField(choices=[(True, 'Available'), (False, 'Borrowed')], default=True),
        ),
    ]
