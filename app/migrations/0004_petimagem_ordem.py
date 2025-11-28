# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_petimagem_static_image_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='petimagem',
            name='ordem',
            field=models.IntegerField(default=1, verbose_name='Ordem'),
        ),
        migrations.AlterModelOptions(
            name='petimagem',
            options={'ordering': ['ordem', '-principal', 'uploaded_at'], 'verbose_name': 'Imagem do Pet', 'verbose_name_plural': 'Imagens do Pet'},
        ),
    ]
