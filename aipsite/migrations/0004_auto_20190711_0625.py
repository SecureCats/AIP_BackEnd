# Generated by Django 2.2.3 on 2019-07-11 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aipsite', '0003_auto_20190711_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aipuser',
            name='classno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aipsite.PublicKey'),
        ),
    ]