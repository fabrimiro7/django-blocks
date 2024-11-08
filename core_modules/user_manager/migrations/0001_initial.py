# Generated by Django 3.2.20 on 2024-09-27 14:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=40, null=True, validators=[django.core.validators.MinLengthValidator(4)])),
                ('email', models.CharField(db_index=True, max_length=70, unique=True, validators=[django.core.validators.MinLengthValidator(4)])),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('permission', models.PositiveSmallIntegerField(choices=[(100, 'SuperAdmin'), (50, 'Admin'), (1, 'Utente')], default=1, verbose_name='Livello permessi utente')),
                ('user_type', models.CharField(choices=[('Persona Fisica', 'Persona Fisica'), ('Azienda', 'Azienda'), ('NoProfit', 'Ente No Profit')], default='Persona Fisica', max_length=30)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Cognome')),
                ('fiscal_code', models.CharField(blank=True, max_length=16, null=True, verbose_name='Codice Fiscale')),
                ('phone', models.CharField(blank=True, max_length=12, null=True, verbose_name='Telefono')),
                ('mobile', models.CharField(blank=True, max_length=12, null=True, verbose_name='Cellulare')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utente',
                'verbose_name_plural': 'Utenti',
                'ordering': ('last_name',),
            },
        ),
    ]
