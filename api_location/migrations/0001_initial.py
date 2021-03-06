# Generated by Django 3.0.6 on 2020-05-18 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LocationModel',
            fields=[
                ('seq', models.BigIntegerField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=12)),
                ('user_nm', models.CharField(max_length=20)),
                ('user_mobile_no', models.CharField(max_length=20)),
                ('lat', models.CharField(max_length=20)),
                ('lng', models.CharField(max_length=20)),
                ('collect_dt', models.DateTimeField()),
                ('save_dt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tb_location_info',
                'ordering': ['-seq'],
                'managed': False,
            },
        ),
    ]
