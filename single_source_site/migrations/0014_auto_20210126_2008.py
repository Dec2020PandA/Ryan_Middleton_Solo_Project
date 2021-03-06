# Generated by Django 2.2 on 2021-01-27 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('single_source_site', '0013_auto_20210122_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='single_source_site.Category'),
        ),
    ]
