# Generated by Django 5.1.7 on 2025-03-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('STORED', '보관'), ('PUBLISHED', '발행')], default='STORED', max_length=15),
        ),
    ]
