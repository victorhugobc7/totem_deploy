# Generated migration for PetImagem model updates

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_pet_sexo'),
    ]

    operations = [
        migrations.AddField(
            model_name='petimagem',
            name='ordem',
            field=models.IntegerField(default=1, verbose_name='Ordem'),
        ),
        migrations.AddField(
            model_name='petimagem',
            name='static_image_path',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Caminho da Imagem Estática'),
        ),
        migrations.AlterField(
            model_name='petimagem',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='pets/', verbose_name='Imagem'),
        ),
        migrations.AlterModelOptions(
            name='petimagem',
            options={'ordering': ['ordem', '-principal', 'uploaded_at'], 'verbose_name': 'Imagem do Pet', 'verbose_name_plural': 'Imagens do Pet'},
        ),
    ]
