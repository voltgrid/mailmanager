# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatchAll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ['domain', 'user'],
                'verbose_name_plural': 'Catch All',
            },
        ),
        migrations.CreateModel(
            name='EmailAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(help_text=b'Alias (local part)', max_length=64)),
            ],
            options={
                'ordering': ['alias'],
                'verbose_name_plural': 'Email Alias',
            },
        ),
        migrations.CreateModel(
            name='EmailDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.ForeignKey(to='account.Domain')),
            ],
            options={
                'ordering': ['domain'],
                'verbose_name_plural': 'Domains',
            },
        ),
        migrations.CreateModel(
            name='EmailForward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('destination', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='EmailUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Local part of email address', max_length=64)),
                ('password', models.CharField(help_text=b'Hashed Password', max_length=256)),
                ('domain', models.ForeignKey(to='mail.EmailDomain')),
            ],
            options={
                'ordering': ['name', 'domain'],
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.AddField(
            model_name='emailforward',
            name='user',
            field=models.ForeignKey(to='mail.EmailUser'),
        ),
        migrations.AddField(
            model_name='emailalias',
            name='user',
            field=models.ForeignKey(to='mail.EmailUser'),
        ),
        migrations.AddField(
            model_name='catchall',
            name='domain',
            field=models.ForeignKey(to='mail.EmailDomain'),
        ),
        migrations.AddField(
            model_name='catchall',
            name='user',
            field=models.ForeignKey(to='mail.EmailUser'),
        ),
        migrations.AlterUniqueTogether(
            name='emailuser',
            unique_together=set([('domain', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='emailforward',
            unique_together=set([('user', 'destination')]),
        ),
        migrations.AlterUniqueTogether(
            name='emailalias',
            unique_together=set([('user', 'alias')]),
        ),
        migrations.AlterUniqueTogether(
            name='catchall',
            unique_together=set([('domain', 'user')]),
        ),
    ]
