# Generated by Django 4.2.3 on 2023-07-11 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_directors_alter_director_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='year',
            field=models.IntegerField(default=2004, verbose_name='Год выпуска'),
            preserve_default=False,
        ),
    ]
