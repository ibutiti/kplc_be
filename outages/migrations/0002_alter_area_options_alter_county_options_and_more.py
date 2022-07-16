# Generated by Django 4.0.5 on 2022-07-15 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("outages", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="area",
            options={"ordering": ("name",)},
        ),
        migrations.AlterModelOptions(
            name="county",
            options={"ordering": ("name",), "verbose_name_plural": "Counties"},
        ),
        migrations.AlterModelOptions(
            name="neighbourhood",
            options={"ordering": ("name",)},
        ),
        migrations.AlterModelOptions(
            name="outage",
            options={"ordering": ("start_time",)},
        ),
        migrations.AlterField(
            model_name="neighbourhood",
            name="name",
            field=models.CharField(max_length=64),
        ),
    ]
