# Generated by Django 2.0.2 on 2018-03-19 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eveonline', '0002_auto_20180319_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evecharacter',
            name='corporation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eveonline.EveCorporation'),
        ),
    ]