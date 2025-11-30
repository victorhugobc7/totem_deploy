# Generated manually
from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_petimagem_ordem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='idade',
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(30)
                ],
                verbose_name='Idade (anos)'
            ),
        ),
        migrations.AlterField(
            model_name='pet',
            name='personalidade',
            field=models.TextField(blank=True, null=True, verbose_name='Personalidade'),
        ),
        migrations.AlterModelOptions(
            name='pet',
            options={'ordering': ['nome'], 'verbose_name': 'Bichinho', 'verbose_name_plural': 'Bichinhos'},
        ),
    ]
