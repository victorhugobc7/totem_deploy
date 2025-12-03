from django.db import migrations, models


def convert_idade_to_choice(apps, schema_editor):
    """Converte valores numéricos de idade para 'filhote' ou 'adulto'"""
    Pet = apps.get_model('app', 'Pet')
    for pet in Pet.objects.all():
        if pet.idade is not None:
            try:
                idade_num = int(pet.idade)
                if idade_num <= 2:
                    pet.idade = 'filhote'
                else:
                    pet.idade = 'adulto'
                pet.save()
            except (ValueError, TypeError):
                # Se já for string ou inválido, deixa como está
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_pet_raca_porte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='idade',
            field=models.CharField(
                blank=True,
                choices=[('filhote', 'Filhote'), ('adulto', 'Adulto')],
                max_length=20,
                null=True,
                verbose_name='Idade'
            ),
        ),
        migrations.RunPython(convert_idade_to_choice, migrations.RunPython.noop),
    ]
