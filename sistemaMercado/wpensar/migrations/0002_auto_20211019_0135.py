# Generated by Django 3.2.8 on 2021-10-19 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wpensar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='produtocompra',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
