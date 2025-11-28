# Generated migration for adding static_image_path field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_pet_sexo'),
    ]

    operations = [
        migrations.AddField(
            model_name='petimagem',
            name='static_image_path',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Caminho da Imagem Estática'),
        ),
    ]
