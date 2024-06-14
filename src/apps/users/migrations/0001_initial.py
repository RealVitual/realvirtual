# Generated by Django 5.0 on 2024-03-11 21:47

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('conf', '0001_initial'),
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('prefix', models.CharField(blank=True, choices=[('mr', 'Sr.'), ('ms', 'Sra.')], max_length=120, null=True, verbose_name='Prefijo')),
                ('names', models.CharField(blank=True, max_length=100, null=True, verbose_name='names')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='first name')),
                ('first_surname', models.CharField(blank=True, max_length=100, null=True, verbose_name='first surname')),
                ('last_surname', models.CharField(blank=True, max_length=100, null=True, verbose_name='last surname')),
                ('email', models.EmailField(error_messages={'unique': 'El email ya se encuentra registrado.'}, max_length=254, null=True, unique=True, verbose_name='email address')),
                ('has_email_confirmed', models.BooleanField(default=False, help_text='Designates whether this user should be treated as email confirmed. Unselect this instead of uncofirmed email.', verbose_name='email confirmed?')),
                ('uuid_hash', models.CharField(blank=True, default='', help_text='Random UUID hash to remember password.', max_length=36, verbose_name='UUID')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_tester', models.BooleanField(default=False, help_text='Designates whether this user should be treated as tester account. Select this when need test experience.', verbose_name='tester account')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='phone')),
                ('mobile', models.CharField(blank=True, max_length=50, null=True, verbose_name='mobile')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Hombre'), ('female', 'Mujer')], max_length=30, null=True, verbose_name='gender')),
                ('document', models.CharField(blank=True, max_length=120, null=True, verbose_name='document')),
                ('date_birth', models.DateField(blank=True, null=True, verbose_name='date birth')),
                ('facebook_id', models.CharField(blank=True, max_length=255, null=True)),
                ('google_id', models.CharField(blank=True, max_length=255, null=True)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True, verbose_name='Profesion ')),
                ('company', models.CharField(blank=True, max_length=255, null=True, verbose_name='Empresa / II.EE.')),
                ('company_position', models.CharField(blank=True, max_length=255, null=True, verbose_name='Cargo / Carrera')),
                ('is_worker', models.BooleanField(default=False, verbose_name='Colaborador')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_img', verbose_name='Imagen Perfil')),
                ('credential_img', models.ImageField(blank=True, null=True, upload_to='credentials', verbose_name='credential')),
                ('being_used', models.BooleanField(default=False, verbose_name='Siendo usado')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='direccion')),
                ('has_shared', models.BooleanField(default=False, verbose_name='Ha compartido')),
                ('generated_credential', models.BooleanField(default=False, verbose_name='Ha generado credencial')),
                ('received_welcome_email', models.BooleanField(default=False, verbose_name='Recibió correo')),
                ('avoid_credential', models.BooleanField(default=False, verbose_name='Avoid credential')),
                ('certificate', models.FileField(blank=True, null=True, upload_to='certificates', verbose_name='certificado')),
                ('age_range', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='age_range_users', to='conf.agerange')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='country_users', to='conf.country')),
                ('document_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_set', to='conf.documenttype')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='%(class)s_set', related_query_name='%(class)s', to='auth.group', verbose_name='groups')),
                ('speciality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='specialities_users', to='conf.speciality')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='%(class)s_set', related_query_name='%(class)s', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['-modified'],
            },
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Administrator',
                'verbose_name_plural': 'Administrators',
                'ordering': ['-modified'],
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
                'ordering': ['-created'],
            },
        ),
    ]
