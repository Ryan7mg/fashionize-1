# Generated by Django 4.2 on 2024-03-15 03:18

from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('outfits', '0003_remove_outfit_bottoms_remove_outfit_shoes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='outfit',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
