# Generated by Django 5.1.1 on 2025-04-20 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YellowDealsAPP', '0008_storeowner_note_storeowner_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='admin_tel',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
