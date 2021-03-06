from django.db import migrations, models
import django.utils.timezone
import imagekit.models.fields
import members.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True,
                                                  help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                                                  verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profile_image', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='profile_image')),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('birthday', models.CharField(blank=True, max_length=100)),
                ('username', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='이메일')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('facebook_id', models.CharField(blank=True, max_length=200)),
                ('is_facebook_user', models.BooleanField(default=False)),
                ('kakao_id', models.CharField(blank=True, max_length=200)),
                ('is_kakao_user', models.BooleanField(default=False)),
                ('is_host', models.BooleanField(default=False)),
                ('activate', models.BooleanField(default=False)),
                ('gender', models.CharField(choices=[('N', 'Nothing'), ('F', 'Female'), ('M', 'Male')], default='N',
                                            max_length=1)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True,
                                                  help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                                  related_name='user_set', related_query_name='user', to='auth.Group',
                                                  verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', members.models.UserManager()),
            ],
        ),
    ]
