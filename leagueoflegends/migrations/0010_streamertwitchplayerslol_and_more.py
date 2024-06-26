# Generated by Django 5.0.1 on 2024-05-15 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagueoflegends', '0009_delete_loluser'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamerTwitchPlayersLol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('puuid', models.CharField(max_length=1000)),
                ('channelId', models.CharField(max_length=500)),
                ('region', models.CharField(default='BR', max_length=100)),
                ('rank', models.CharField(default='I', max_length=400)),
                ('tier', models.CharField(default='Unranked', max_length=100)),
                ('pdl', models.IntegerField(default=0)),
                ('thumbUrl', models.CharField(default='', max_length=1400)),
                ('started_at', models.DateTimeField(default=None, null=True)),
                ('isOnline', models.BooleanField(default=False)),
                ('isPlaying', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='playersonline',
            name='famousTwitchPlayersLol',
        ),
        migrations.DeleteModel(
            name='FamousTwitchPlayersLol',
        ),
        migrations.DeleteModel(
            name='PlayersOnline',
        ),
    ]
