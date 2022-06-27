# Generated by Django 4.0.5 on 2022-06-26 20:19

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], help_text='Gender of the customer, it can be (for now), male (m) or female (f).', max_length=4, null=True, verbose_name='Gender')),
                ('customer_type', models.CharField(blank=True, choices=[('patient', 'Patient'), ('familiar', 'Familiar')], help_text='Type of the customer, it can be a patient or a familiar.', max_length=10, null=True, verbose_name='Customer type')),
                ('birthdate', models.DateField(blank=True, help_text='Birthday of teh customer.', null=True, verbose_name='Birthday')),
                ('current_neighbourhood', models.CharField(blank=True, help_text='Current neighbourhood of the customer, it can change if in the future the customer moves to another.', max_length=128, null=True, verbose_name='Current neighbourhood')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ClinicHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('scholarship', models.BooleanField(blank=True, help_text='Field indicating whether the customer is suffering from scholarship.', null=True, verbose_name='Scholarship')),
                ('hypertension', models.BooleanField(blank=True, help_text='Field that shows if the customer has an active hypertension.', null=True, verbose_name='Hypertension')),
                ('diabetes', models.BooleanField(blank=True, help_text='Field indicating whether the customer is suffering from diabetes.', null=True, verbose_name='Diabetes')),
                ('alcoholism', models.BooleanField(blank=True, help_text='Field indicating whether the customer is suffering from alcoholism.', null=True, verbose_name='Alcoholism')),
                ('handicap', models.BooleanField(blank=True, help_text='Field indicating whether the customer is suffering from handicap.', null=True, verbose_name='Handicap')),
                ('user', models.ForeignKey(help_text='User associated to the clinic history', on_delete=django.db.models.deletion.CASCADE, related_name='clinic_history', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Clinic history',
                'verbose_name_plural': 'Clinic histories',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('scheduled', models.DateTimeField(blank=True, help_text='Date when the appointment was scheduled.', null=True, verbose_name='Scheduled')),
                ('day', models.DateField(blank=True, help_text='Day when the appointment will take place.', null=True, verbose_name='Day')),
                ('sms_received', models.DateTimeField(blank=True, help_text='The moment when the user receives the sms.', null=True, verbose_name='Sms received')),
                ('attended', models.BooleanField(blank=True, help_text='Field that show if the user attended the appointment.', null=True, verbose_name='Attendance')),
                ('user', models.ForeignKey(help_text='Clinic history of the user.', on_delete=django.db.models.deletion.PROTECT, related_name='user_clinic_history', to=settings.AUTH_USER_MODEL, verbose_name='Clinic history')),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointments',
            },
        ),
    ]