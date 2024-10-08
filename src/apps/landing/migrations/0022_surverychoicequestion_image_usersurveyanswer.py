# Generated by Django 5.0 on 2024-08-11 04:13

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0019_header_show_more_events'),
        ('landing', '0021_surveryquestion_surverychoicequestion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='surverychoicequestion',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='test_realvirtual/icons/', verbose_name='Imagen icon'),
        ),
        migrations.CreateModel(
            name='UserSurveyAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('choice_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_choice_survey_questions', to='landing.surverychoicequestion')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_survey_answers', to='companies.company')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_survey_questions', to='landing.surveryquestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_survey_answers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Respuesta de Encuesta',
                'verbose_name_plural': 'Respuestas de Encuesta',
                'ordering': ['-modified'],
            },
        ),
    ]
