# Generated by Django 4.0.5 on 2022-06-22 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saving_plans_apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, null=None)),
            ],
        ),
        migrations.AddField(
            model_name='plans',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='promotions',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='promotions',
            name='promotionCount',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='CustomerGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(null=None)),
                ('tenure', models.IntegerField(null=None)),
                ('startDat', models.DateTimeField(null=None)),
                ('depositAmount', models.FloatField(default=0, null=None)),
                ('benefitPercentage', models.FloatField(null=None)),
                ('planID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saving_plans_apps.plans')),
                ('promotionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saving_plans_apps.promotions')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saving_plans_apps.user')),
            ],
        ),
    ]
