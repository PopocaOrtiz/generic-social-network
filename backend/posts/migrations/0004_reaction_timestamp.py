# Generated by Django 4.2.7 on 2023-11-30 00:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment_created_at_alter_comment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reaction',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
