# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_pet_idade_personalidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='raca',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Raça'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='porte',
            field=models.CharField(blank=True, choices=[('pequeno', 'Pequeno'), ('medio', 'Médio'), ('grande', 'Grande')], max_length=20, null=True, verbose_name='Porte'),
        ),
    ]
