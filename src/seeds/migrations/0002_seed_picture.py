# Generated by Django 2.0.2 on 2018-08-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seeds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seed',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='pics/'),
        ),
    ]