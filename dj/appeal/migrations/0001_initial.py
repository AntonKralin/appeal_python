# Generated by Django 4.2.3 on 2023-07-06 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255, verbose_name='name')),
            ],
            options={
                'db_table': 'departments',
            },
        ),
        migrations.CreateModel(
            name='Imns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(help_text='address', max_length=255, verbose_name='address')),
                ('mail', models.CharField(help_text='email', max_length=255, verbose_name='email')),
                ('name', models.CharField(help_text='name', max_length=255, verbose_name='name')),
                ('number', models.IntegerField(help_text='code number', verbose_name='code number')),
                ('post', models.CharField(help_text='post', max_length=255, verbose_name='post')),
                ('shot_name', models.CharField(help_text='shot_name', max_length=255, verbose_name='shot_name')),
                ('unp', models.CharField(help_text='unp', max_length=255, verbose_name='unp')),
            ],
            options={
                'db_table': 'imns',
            },
        ),
        migrations.CreateModel(
            name='Appeals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='date', verbose_name='date')),
                ('done', models.TextField(help_text='done', verbose_name='done')),
                ('result', models.CharField(help_text='result', max_length=255, verbose_name='result')),
                ('type', models.CharField(help_text='type', max_length=255, verbose_name='type')),
                ('unit', models.CharField(help_text='unit', max_length=255, verbose_name='unit')),
                ('what', models.TextField(help_text='what', verbose_name='what')),
                ('who', models.CharField(help_text='who', max_length=255, verbose_name='who')),
                ('message', models.CharField(help_text='message', max_length=255, verbose_name='message')),
                ('imns', models.CharField(help_text='imns', max_length=255, verbose_name='imns')),
                ('id_imns', models.ForeignKey(db_column='id_imns', help_text='id_imns', on_delete=django.db.models.deletion.DO_NOTHING, to='appeal.imns')),
            ],
            options={
                'db_table': 'appeals',
            },
        ),
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.IntegerField(help_text='1-obl, 2-raion', verbose_name='1-obl, 2-raion')),
                ('login', models.CharField(help_text='login', max_length=255, verbose_name='login')),
                ('password', models.CharField(help_text='password', max_length=255, verbose_name='password')),
                ('id_imns', models.ForeignKey(db_column='id_imns', help_text='imns', on_delete=django.db.models.deletion.CASCADE, to='appeal.imns')),
            ],
            options={
                'db_table': 'admins',
            },
        ),
    ]