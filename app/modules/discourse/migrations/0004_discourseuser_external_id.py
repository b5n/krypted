# Generated by Django 2.0.3 on 2018-07-24 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0003_auto_20180525_0523'),
    ]

    operations = [
        migrations.AddField(
            model_name='discourseuser',
            name='external_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
