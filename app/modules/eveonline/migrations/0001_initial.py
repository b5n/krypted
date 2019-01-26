# Generated by Django 2.1.5 on 2019-01-26 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EveCharacter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_id', models.IntegerField()),
                ('character_name', models.CharField(max_length=255)),
                ('character_portrait', models.URLField(blank=True, max_length=255, null=True)),
                ('character_alt_type', models.CharField(blank=True, choices=[('super_alt', 'Super Alt'), ('rorqual_alt', 'Rorqual Alt'), ('cap_alt', 'Capital Alt'), ('subcap_pve_alt', 'Subcap PvE Alt'), ('subcap_pvp_alt', 'Subcap PvP Alt'), ('industry_alt', 'Industry Alt'), ('useless_alt', 'Useless Alt')], max_length=255, null=True)),
            ],
            options={
                'permissions': (('audit_eve_character', 'Can audit an EVE character.'),),
            },
        ),
        migrations.CreateModel(
            name='EveCorporation',
            fields=[
                ('corporation_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=512)),
                ('ticker', models.CharField(max_length=5)),
                ('member_count', models.IntegerField()),
                ('alliance_id', models.IntegerField(null=True)),
                ('tax_rate', models.FloatField()),
                ('ceo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eveonline.EveCharacter')),
            ],
        ),
        migrations.CreateModel(
            name='EveToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(blank=True, null=True)),
                ('refresh_token', models.TextField(blank=True, null=True)),
                ('expires_in', models.IntegerField(default=0)),
                ('expiry', models.DateTimeField(auto_now_add=True)),
                ('scopes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='evecharacter',
            name='corporation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eveonline.EveCorporation'),
        ),
        migrations.AddField(
            model_name='evecharacter',
            name='main',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='eveonline.EveCharacter'),
        ),
        migrations.AddField(
            model_name='evecharacter',
            name='token',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='eveonline.EveToken'),
        ),
        migrations.AddField(
            model_name='evecharacter',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
