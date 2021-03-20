# Generated by Django 3.0.5 on 2020-05-23 11:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='img_steg_enc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_img', models.CharField(blank=True, max_length=255)),
                ('cover_img', models.CharField(blank=True, max_length=255)),
                ('pin_img', models.IntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(6)])),
                ('enc_img_steg', models.CharField(blank=True, max_length=255)),
                ('user_id_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=255)),
                ('image_path', models.ImageField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('encoded_img', models.CharField(blank=True, max_length=255)),
                ('pin', models.IntegerField(default=None, null=True, validators=[django.core.validators.MaxValueValidator(6)])),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]