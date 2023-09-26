# Generated by Django 2.2.13 on 2023-08-29 14:39

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import docsearch.models
import docsearch.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docsearch', '0014_flatdrawing_building_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='range',
            field=docsearch.models.InclusiveIntegerRangeField(blank=True, help_text='Specify the lower and upper bounds for the range of values represented by this field. If this field only has one value, set it as both the lower and upper bounds.', max_length=255, null=True, validators=[docsearch.validators.validate_int_range]),
        ),
        migrations.AlterField(
            model_name='book',
            name='section',
            field=docsearch.models.InclusiveIntegerRangeField(blank=True, help_text='Specify the lower and upper bounds for the range of values represented by this field. If this field only has one value, set it as both the lower and upper bounds.', max_length=255, null=True, validators=[docsearch.validators.validate_int_range]),
        ),
        migrations.AlterField(
            model_name='book',
            name='source_file',
            field=models.FileField(upload_to='BOOKS', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='controlmonumentmap',
            name='part_of_section',
            field=models.CharField(blank=True, choices=[('E1/2', 'E1/2'), ('W1/2', 'W1/2')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='controlmonumentmap',
            name='range',
            field=models.PositiveIntegerField(null=True, validators=[docsearch.validators.validate_int_btwn]),
        ),
        migrations.AlterField(
            model_name='controlmonumentmap',
            name='section',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(null=True), help_text='Set multiple values for this field by separating them with commas. E.g. to save the values 1, 2, and 3, record them as 1,2,3.', size=None, validators=[docsearch.validators.validate_int_array]),
        ),
        migrations.AlterField(
            model_name='controlmonumentmap',
            name='source_file',
            field=models.FileField(upload_to='CONTROL_MONUMENT_MAPS', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='deeptunnel',
            name='source_file',
            field=models.FileField(upload_to='DEEP_PARCEL_SURPLUS', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='dossier',
            name='document_number',
            field=models.CharField(max_length=3, validators=[docsearch.validators.validate_positive_int]),
        ),
        migrations.AlterField(
            model_name='dossier',
            name='file_number',
            field=models.CharField(max_length=255, validators=[docsearch.validators.validate_positive_int]),
        ),
        migrations.AlterField(
            model_name='dossier',
            name='source_file',
            field=models.FileField(upload_to='DOSSIER_FILES', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='easement',
            name='easement_number',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[docsearch.validators.validate_positive_int]),
        ),
        migrations.AlterField(
            model_name='easement',
            name='source_file',
            field=models.FileField(upload_to='EASEMENTS', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='flatdrawing',
            name='area',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[docsearch.validators.validate_int_btwn]),
        ),
        migrations.AlterField(
            model_name='flatdrawing',
            name='cad_file',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(['dwg', 'dxf', 'dgn', 'stl'])], verbose_name='CAD file'),
        ),
        migrations.AlterField(
            model_name='flatdrawing',
            name='cross_ref_area',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[docsearch.validators.validate_int_btwn]),
        ),
        migrations.AlterField(
            model_name='flatdrawing',
            name='cross_ref_section',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[docsearch.validators.validate_int_btwn]),
        ),
        migrations.AlterField(
            model_name='flatdrawing',
            name='date',
            field=models.CharField(blank=True, help_text='Enter the date as "YYYY-MM-DD"', max_length=255, null=True, validators=[docsearch.validators.validate_date]),
        ),
        migrations.AlterField(
            model_name='flatdrawing',
            name='number_of_sheets',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[docsearch.validators.validate_positive_int]),
        ),
        migrations.AlterField(
            model_name='flatdrawing',
            name='source_file',
            field=models.FileField(upload_to='FLAT_DRAWINGS', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='indexcard',
            name='source_file',
            field=models.FileField(upload_to='INDEX_CARDS', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='license',
            name='diameter',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[docsearch.validators.validate_positive_int]),
        ),
        migrations.AlterField(
            model_name='license',
            name='end_date',
            field=models.CharField(blank=True, help_text='Enter the date as "YYYY-MM-DD"', max_length=255, null=True, validators=[docsearch.validators.validate_date]),
        ),
        migrations.AlterField(
            model_name='license',
            name='license_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='license',
            name='range',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(null=True), default=list, help_text='Set multiple values for this field by separating them with commas. E.g. to save the values 1, 2, and 3, record them as 1,2,3.', size=None, validators=[docsearch.validators.validate_int_array]),
        ),
        migrations.AlterField(
            model_name='license',
            name='section',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(null=True), default=list, help_text='Set multiple values for this field by separating them with commas. E.g. to save the values 1, 2, and 3, record them as 1,2,3.', size=None, validators=[docsearch.validators.validate_int_array]),
        ),
        migrations.AlterField(
            model_name='license',
            name='source_file',
            field=models.FileField(upload_to='LICENSES', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='license',
            name='status',
            field=models.CharField(blank=True, choices=[('TBD', 'TBD'), ('active', 'Active'), ('cancelled', 'Cancelled'), ('continuous', 'Continuous'), ('expired', 'Expired'), ('indefinite', 'Indefinite'), ('perpetual', 'Perpetual')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='license',
            name='type',
            field=models.CharField(blank=True, choices=[('combined_sewer', 'Combined Sewer'), ('electric', 'Electric'), ('gas', 'Gas'), ('pipeline', 'Pipeline'), ('sanitary_sewer', 'Sanitary Sewer'), ('storm sewer', 'Storm Sewer'), ('telecom', 'Telecom'), ('water main', 'Water Main'), ('other', 'Other')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='area',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[docsearch.validators.validate_int_btwn]),
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='cabinet_number',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[docsearch.validators.validate_int_btwn]),
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='section',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[docsearch.validators.validate_int_btwn]),
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='source_file',
            field=models.FileField(upload_to='PROJECT_FILES', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='rightofway',
            name='source_file',
            field=models.FileField(upload_to='RIGHT_OF_WAY', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='surplusparcel',
            name='source_file',
            field=models.FileField(upload_to='DEEP_PARCEL_SURPLUS', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='survey',
            name='cross_ref_area',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[docsearch.validators.validate_int_btwn]),
        ),
        migrations.AlterField(
            model_name='survey',
            name='cross_ref_section',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[docsearch.validators.validate_int_btwn]),
        ),
        migrations.AlterField(
            model_name='survey',
            name='date',
            field=models.CharField(blank=True, help_text='Enter the date as "YYYY-MM-DD"', max_length=255, null=True, validators=[docsearch.validators.validate_date]),
        ),
        migrations.AlterField(
            model_name='survey',
            name='number_of_sheets',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[docsearch.validators.validate_positive_int]),
        ),
        migrations.AlterField(
            model_name='survey',
            name='range',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), help_text='Set multiple values for this field by separating them with commas. E.g. to save the values 1, 2, and 3, record them as 1,2,3.', size=None, validators=[docsearch.validators.validate_int_array]),
        ),
        migrations.AlterField(
            model_name='survey',
            name='section',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), help_text='Set multiple values for this field by separating them with commas. E.g. to save the values 1, 2, and 3, record them as 1,2,3.', size=None, validators=[docsearch.validators.validate_int_array]),
        ),
        migrations.AlterField(
            model_name='survey',
            name='source_file',
            field=models.FileField(upload_to='SURVEYS', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='title',
            name='control_number',
            field=models.CharField(max_length=255, validators=[docsearch.validators.validate_positive_int]),
        ),
        migrations.AlterField(
            model_name='title',
            name='source_file',
            field=models.FileField(upload_to='TITLES', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.CreateModel(
            name='NotificationSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
