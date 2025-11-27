from django.core.management.base import BaseCommand
from app.models import Pet

class Command(BaseCommand):
    help = 'Popula o banco de dados com os 9 gatos do MaryCats'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a recriação dos pets mesmo se já existirem',
        )

    def handle(self, *args, **options):
        # Se --force foi passado, limpar pets existentes
        if options.get('force'):
            Pet.objects.all().delete()
            self.stdout.write(self.style.WARNING('Pets existentes removidos.'))
        elif Pet.objects.exists():
            # Se já existem pets e não foi passado --force, apenas avisar e continuar
            count = Pet.objects.count()
            self.stdout.write(self.style.SUCCESS(f'✓ {count} pets já existem no banco de dados.'))
            return
        
        pets_data = [
            {
                'nome': 'Gamora',
                'tipo': 'gato',
                'sexo': 'femea',
                'raca': 'SRD',
                'idade': 1,
                'porte': 'pequeno',
                'personalidade': 'Brincalhona e carinhosa',
                'descricao': 'Gamora é uma gatinha cheia de energia que adora brincar.',
                'disponivel': True
            },
            {
                'nome': 'Luke',
                'tipo': 'gato',
                'sexo': 'macho',
                'raca': 'SRD',
                'idade': 2,
                'porte': 'medio',
                'personalidade': 'Calmo e tranquilo',
                'descricao': 'Luke é um gato sereno que gosta de carinho.',
                'disponivel': True
            },
            {
                'nome': 'Davi',
                'tipo': 'gato',
                'sexo': 'macho',
                'raca': 'SRD',
                'idade': 1,
                'porte': 'pequeno',
                'personalidade': 'Curioso e ativo',
                'descricao': 'Davi está sempre explorando novos lugares.',
                'disponivel': True
            },
            {
                'nome': 'Dora',
                'tipo': 'gato',
                'sexo': 'femea',
                'raca': 'SRD',
                'idade': 3,
                'porte': 'pequeno',
                'personalidade': 'Amorosa e quieta',
                'descricao': 'Dora é uma gatinha doce que gosta de colo.',
                'disponivel': True
            },
            {
                'nome': 'Buck',
                'tipo': 'gato',
                'sexo': 'macho',
                'raca': 'SRD',
                'idade': 4,
                'porte': 'medio',
                'personalidade': 'Independente mas carinhoso',
                'descricao': 'Buck gosta de sua independência mas também de carinho.',
                'disponivel': True
            },
            {
                'nome': 'Lady',
                'tipo': 'gato',
                'sexo': 'femea',
                'raca': 'SRD',
                'idade': 5,
                'porte': 'pequeno',
                'personalidade': 'Elegante e tranquila',
                'descricao': 'Lady é refinada e gosta de ambientes calmos.',
                'disponivel': True
            },
            {
                'nome': 'Michelangelo',
                'tipo': 'gato',
                'sexo': 'macho',
                'raca': 'SRD',
                'idade': 1,
                'porte': 'pequeno',
                'personalidade': 'Artista e brincalhão',
                'descricao': 'Michelangelo é criativo e adora brincar.',
                'disponivel': True
            },
            {
                'nome': 'Verônica',
                'tipo': 'gato',
                'sexo': 'femea',
                'raca': 'SRD',
                'idade': 6,
                'porte': 'medio',
                'personalidade': 'Madura e sábia',
                'descricao': 'Verônica é uma gata experiente e tranquila.',
                'disponivel': True
            },
            {
                'nome': 'Mavie',
                'tipo': 'gato',
                'sexo': 'femea',
                'raca': 'SRD',
                'idade': 7,
                'porte': 'medio',
                'personalidade': 'Sociável e amigável',
                'descricao': 'Mavie adora companhia e fazer novos amigos.',
                'disponivel': True
            }
        ]
        
        for pet_data in pets_data:
            pet = Pet.objects.create(**pet_data)
            self.stdout.write(self.style.SUCCESS(f'✓ Pet criado: {pet.nome}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n{len(pets_data)} pets cadastrados com sucesso!'))
