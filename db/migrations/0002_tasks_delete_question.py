# Generated by Django 4.0.4 on 2022-04-20 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=200)),
                ('accounts', models.CharField(max_length=5000)),
            ],
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
