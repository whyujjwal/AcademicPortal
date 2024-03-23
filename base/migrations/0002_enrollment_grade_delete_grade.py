# Generated by Django 5.0.3 on 2024-03-23 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='grade',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'), ('C', 'C'), ('C-', 'C-'), ('D', 'D'), ('E', 'E'), ('NC', 'No Credit')], max_length=2, null=True),
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
    ]
