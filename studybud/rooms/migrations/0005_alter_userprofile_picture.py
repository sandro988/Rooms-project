# Generated by Django 4.0.3 on 2022-04-06 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]