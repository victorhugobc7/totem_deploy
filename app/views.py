from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Pet, PetImagem
import json

def test_view(request):
    """Simple test view to verify deployment"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test - MaryCats Totem</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; background: #b11c6c; color: white; }
            h1 { font-size: 48px; }
            .success { color: #fdd12c; }
        </style>
    </head>
    <body>
        <h1>🎉 <span class="success">Success!</span> 🎉</h1>
        <h2>MaryCats Totem is LIVE on Railway!</h2>
        <p>Django server is running correctly.</p>
        <p>Domain: cuxrie.xyz</p>
        <hr>
        <p><a href="/comecar/" style="color: #fdd12c;">Go to Main App</a></p>
    </body>
    </html>
    """
    return HttpResponse(html)

def calcular_compatibilidade(pet, preferencias):
    """Calcula a compatibilidade entre um pet e as preferências do usuário"""
    pontuacao = 0
    
    # Tipo de pet (0-40 pontos)
    tipo_preferido = preferencias.get('tipo')
    if tipo_preferido and tipo_preferido != 'sem_preferencia':
        if pet.tipo == tipo_preferido:
            pontuacao += 40
    else:
        pontuacao += 20
    
    # Sexo (0-25 pontos)
    sexo_preferido = preferencias.get('sexo')
    if sexo_preferido and sexo_preferido != 'sem_preferencia':
        if pet.sexo == sexo_preferido:
            pontuacao += 25
    else:
        pontuacao += 12  # Pontuação média se não houver preferência
    
    # Idade (0-20 pontos)
    idade_preferida = preferencias.get('idade')
    if idade_preferida and idade_preferida != 'sem_preferencia':
        if pet.idade_categoria == idade_preferida:
            pontuacao += 20
    else:
        pontuacao += 10  # Pontuação média se não houver preferência
    
    # Personalidade (0-15 pontos)
    personalidade_preferida = preferencias.get('personalidade', [])
    if personalidade_preferida and 'sem_preferencia' not in personalidade_preferida:
        for palavra in personalidade_preferida:
            if palavra.lower() in pet.personalidade.lower():
                pontuacao += 5
    else:
        pontuacao += 7  # Pontuação média se não houver preferência
    
    return min(pontuacao, 100)

# Views principais
def tela_base(request):
    return render(request, 'base.html', {})

def header(request):
    return render(request, 'header.html', {})

def footer(request):
    return render(request, 'footer.html', {})

def tela_comecar(request):
    """Tela inicial com botão para começar o fluxo"""
    # Get available pets for carousel with their images
    pets = Pet.objects.filter(disponivel=True).prefetch_related('imagens')[:6]  # Limit to 6 pets for carousel
    
    return render(request, 'comecar.html', {
        'pets': pets
    })

def pergunta_dupla(request, step=1):
    """Perguntas com duas opções"""
    
    # Get the pet type preference from session for dynamic title
    preferencias = request.session.get('preferencias', {})
    tipo_pet = preferencias.get('tipo', 'gato')
    
    # Dynamic title based on pet type
    if tipo_pet == 'cachorro':
        titulo_idade = 'Que idade de cachorrinho você prefere?'
    else:
        titulo_idade = 'Que idade de gatinho você prefere?'
    
    perguntas = {
        1: {
            'titulo': 'Escolha seu novo melhor amigo.',
            'opcoes': [
                {'valor': 'cachorro', 'texto': 'Cachorro', 'icone': 'fas fa-dog fa-5x'},
                {'valor': 'gato', 'texto': 'Gato', 'icone': 'fas fa-cat fa-5x'}
            ],
            'proxima': '/pergunta/dupla/2/'
        },
        2: {
            'titulo': 'Você tem preferência de gênero do bichinho?',
            'opcoes': [
                {'valor': 'macho', 'texto': 'Macho', 'icone': 'fas fa-mars fa-5x'},
                {'valor': 'femea', 'texto': 'Fêmea', 'icone': 'fas fa-venus fa-5x'}
            ],
            'proxima': '/pergunta/dupla/3/'
        },
        3: {
            'titulo': titulo_idade,
            'opcoes': [
                {'valor': 'filhote', 'texto': 'Filhote', 'icone': 'fas fa-dog fa-5x'},
                {'valor': 'adulto', 'texto': 'Adulto', 'icone': 'fas fa-paw fa-5x'}
            ],
            'proxima': '/resultados/'
        }
    }
    
    pergunta = perguntas.get(step)
    if not pergunta:
        return redirect('tela_comecar')
    
    return render(request, 'pergunta_dupla.html', {
        'pergunta': pergunta,
        'step': step
    })

def pergunta_tripla(request, step=2):
    """Perguntas com três opções"""
    perguntas = {
        4: {
            'titulo': 'Qual porte você prefere?',
            'opcoes': [
                {'valor': 'pequeno', 'texto': 'Pequeno', 'icone': 'fas fa-cat fa-5x'},
                {'valor': 'medio', 'texto': 'Médio', 'icone': 'fas fa-dog fa-5x'},
                {'valor': 'grande', 'texto': 'Grande', 'icone': 'fas fa-dragon fa-5x'}
            ],
            'proxima': '/resultados/'
        }
    }
    
    # Porte question disabled: always redirect to resultados
    return redirect('resultados')

def salvar_preferencia(request):
    """Salva as preferências do usuário na sessão"""
    if request.method == 'POST':
        data = json.loads(request.body)
        chave = data.get('chave')
        valor = data.get('valor')
        
        if 'preferencias' not in request.session:
            request.session['preferencias'] = {}
        
        request.session['preferencias'][chave] = valor
        request.session.modified = True
        
        return JsonResponse({'status': 'sucesso'})
    return JsonResponse({'status': 'erro'}, status=400)

def resultados(request):
    """Mostra pets compatíveis com as preferências"""
    preferencias = request.session.get('preferencias', {})
    
    # Buscar pets disponíveis com prefetch de imagens
    pets_disponiveis = Pet.objects.filter(disponivel=True).prefetch_related('imagens')
    
    # Apply strict filters first
    tipo_preferido = preferencias.get('tipo')
    if tipo_preferido and tipo_preferido != 'sem_preferencia':
        pets_disponiveis = pets_disponiveis.filter(tipo=tipo_preferido)
    
    sexo_preferido = preferencias.get('sexo')
    if sexo_preferido and sexo_preferido != 'sem_preferencia':
        pets_disponiveis = pets_disponiveis.filter(sexo=sexo_preferido)
    
    idade_preferida = preferencias.get('idade')
    if idade_preferida and idade_preferida != 'sem_preferencia':
        if idade_preferida == 'filhote':
            pets_disponiveis = pets_disponiveis.filter(idade__lte=2)
        elif idade_preferida == 'adulto':
            pets_disponiveis = pets_disponiveis.filter(idade__gte=3, idade__lte=7)
        elif idade_preferida == 'idoso':
            pets_disponiveis = pets_disponiveis.filter(idade__gte=8)
    
    # Build results list
    pets_compatíveis = []
    for pet in pets_disponiveis:
        # Check if pet has any images
        primeira_imagem = pet.imagens.first()
        if primeira_imagem and primeira_imagem.static_image_path:
            static_image_path = primeira_imagem.static_image_path
        elif not primeira_imagem:
            static_image_path = f"images/info-pets/Imagens/{pet.nome}.png"
        else:
            static_image_path = None
            
        pets_compatíveis.append({
            'pet': pet,
            'compatibilidade': 100,
            'static_image_path': static_image_path
        })
    
    return render(request, 'pet_lista.html', {
        'pets_compatíveis': pets_compatíveis,
        'preferencias': preferencias
    })

def pet_detalhes(request, pet_id):
    """Mostra detalhes de um pet específico"""
    pet = get_object_or_404(Pet, id=pet_id)
    imagens = list(pet.imagens.all())  # Convert to list to avoid multiple DB queries
    
    # Check if images have static_image_path set
    primeira_imagem = imagens[0] if imagens else None
    if primeira_imagem and primeira_imagem.static_image_path:
        static_image_path = primeira_imagem.static_image_path
    else:
        static_image_path = None
    
    # Check if user is authenticated in core
    is_authenticated = request.session.get('authenticated', False)
    
    return render(request, 'pet_detalhes.html', {
        'pet': pet,
        'imagens': imagens,
        'static_image_path': static_image_path,
        'primeira_imagem': primeira_imagem,
        'is_authenticated': is_authenticated
    })

def cadastrar_pet(request):
    """Formulário para cadastrar novo bichinho"""
    if request.method == 'POST':
        try:
            # Handle optional fields
            idade_str = request.POST.get('idade', '').strip()
            idade = int(idade_str) if idade_str else None
            
            personalidade = request.POST.get('personalidade', '').strip() or None
            raca = request.POST.get('raca', '').strip() or None
            porte = request.POST.get('porte', '').strip() or None
            
            pet = Pet.objects.create(
                nome=request.POST.get('nome'),
                tipo=request.POST.get('tipo'),
                sexo=request.POST.get('sexo', 'macho'),
                raca=raca,
                idade=idade,
                porte=porte,
                personalidade=personalidade,
                descricao=request.POST.get('descricao', ''),
                disponivel=True
            )
            
            # Salvar imagens
            if request.FILES.get('imagem'):
                PetImagem.objects.create(
                    pet=pet,
                    imagem=request.FILES.get('imagem'),
                    principal=True
                )
            
            messages.success(request, 'Bichinho cadastrado com sucesso!')
            return redirect('pet_detalhes', pet_id=pet.id)
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar bichinho: {str(e)}')
    
    return render(request, 'cadastrar_pet.html', {})

def core_login(request):
    """Simple login view for core admin"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Simple authentication with hardcoded credentials
        if username == 'admin' and password == '1234':
            # Create a fake user session
            request.session['authenticated'] = True
            request.session['core_user'] = 'admin'
            return redirect('core_dashboard')
        else:
            messages.error(request, 'Credenciais inválidas')
    
    return render(request, 'core/login.html')

def core_logout(request):
    """Logout from core admin"""
    request.session.pop('authenticated', None)
    request.session.pop('core_user', None)
    messages.success(request, 'Logout realizado com sucesso')
    return redirect('core_login')

def core_auth_required(view_func):
    """Decorator for core authentication"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('authenticated'):
            return redirect('core_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@core_auth_required
def core_dashboard(request):
    """Core admin dashboard"""
    # Get statistics
    total_pets = Pet.objects.count()
    pets_disponiveis = Pet.objects.filter(disponivel=True).count()
    total_cachorros = Pet.objects.filter(tipo='cachorro').count()
    total_gatos = Pet.objects.filter(tipo='gato').count()
    
    context = {
        'total_pets': total_pets,
        'pets_disponiveis': pets_disponiveis,
        'total_cachorros': total_cachorros,
        'total_gatos': total_gatos,
    }
    
    return render(request, 'core/dashboard.html', context)

@core_auth_required
def core_lista_pets(request):
    """Lista de bichinhos para o admin core"""
    q = request.GET.get('q', '').strip()
    filtro_disponivel = request.GET.get('disponivel')
    
    pets = Pet.objects.all().prefetch_related('imagens')
    
    if q:
        pets = pets.filter(nome__icontains=q)
    
    if filtro_disponivel in ['true', 'false']:
        pets = pets.filter(disponivel=(filtro_disponivel == 'true'))
    
    pets = pets.order_by('nome')
    
    return render(request, 'core/lista_pets.html', {
        'pets': pets,
        'q': q,
        'filtro_disponivel': filtro_disponivel,
        'hide_nav_logo': True
    })

@core_auth_required
def core_cadastrar_pet(request):
    """Formulário para cadastrar novo bichinho com autenticação"""
    if request.method == 'POST':
        try:
            # Handle optional fields
            idade_str = request.POST.get('idade', '').strip()
            idade = int(idade_str) if idade_str else None
            
            personalidade = request.POST.get('personalidade', '').strip() or None
            raca = request.POST.get('raca', '').strip() or None
            porte = request.POST.get('porte', '').strip() or None
            
            pet = Pet.objects.create(
                nome=request.POST.get('nome'),
                tipo=request.POST.get('tipo'),
                sexo=request.POST.get('sexo', 'macho'),
                raca=raca,
                idade=idade,
                porte=porte,
                personalidade=personalidade,
                descricao=request.POST.get('descricao', ''),
                disponivel=True
            )
            
            # Salvar imagens
            if request.FILES.get('imagem'):
                PetImagem.objects.create(
                    pet=pet,
                    imagem=request.FILES.get('imagem'),
                    principal=True
                )
            
            messages.success(request, 'Bichinho cadastrado com sucesso!')
            return redirect('core_dashboard')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar bichinho: {str(e)}')
    
    return render(request, 'core/cadastrar_pet.html', {})

def painel_pets(request):
    """Admin panel to manage all pets with filtering"""
    q = request.GET.get('q', '').strip()
    filtro_disponivel = request.GET.get('disponivel')
    
    pets = Pet.objects.all()
    
    if q:
        pets = pets.filter(nome__icontains=q)
    
    if filtro_disponivel in ['true', 'false']:
        pets = pets.filter(disponivel=(filtro_disponivel == 'true'))
    
    pets = pets.order_by('nome')
    
    return render(request, 'painel_pets.html', {
        'pets': pets,
        'q': q,
        'filtro_disponivel': filtro_disponivel
    })

def editar_pet(request, pet_id):
    """Edit existing bichinho"""
    pet = get_object_or_404(Pet, id=pet_id)
    is_authenticated = request.session.get('authenticated', False)
    
    if request.method == 'POST':
        try:
            # Handle optional idade field
            idade_str = request.POST.get('idade', '').strip()
            idade = int(idade_str) if idade_str else None
            
            # Handle optional fields
            personalidade = request.POST.get('personalidade', '').strip() or None
            raca = request.POST.get('raca', '').strip() or None
            porte = request.POST.get('porte', '').strip() or None
            
            pet.nome = request.POST.get('nome')
            pet.tipo = request.POST.get('tipo')
            pet.sexo = request.POST.get('sexo', pet.sexo)
            pet.raca = raca
            pet.idade = idade
            pet.porte = porte
            pet.personalidade = personalidade
            pet.descricao = request.POST.get('descricao', '')
            pet.save()
            
            if request.FILES.get('imagem'):
                PetImagem.objects.create(
                    pet=pet,
                    imagem=request.FILES.get('imagem'),
                    principal=False
                )
            
            messages.success(request, 'Bichinho atualizado com sucesso!')
            # Redirect to core list if authenticated, otherwise to painel_pets
            if is_authenticated:
                return redirect('core_lista_pets')
            return redirect('painel_pets')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar bichinho: {str(e)}')
    
    return render(request, 'editar_pet.html', {
        'pet': pet,
        'is_authenticated': is_authenticated
    })

def excluir_pet(request, pet_id):
    """Delete a bichinho"""
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        nome = pet.nome
        pet.delete()
        messages.success(request, f'Bichinho {nome} excluído com sucesso!')
    return redirect('painel_pets')

@csrf_exempt
def alternar_disponibilidade_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.disponivel = not pet.disponivel
        pet.save()
        messages.success(request, f"Disponibilidade de {pet.nome} alterada para {'Disponível' if pet.disponivel else 'Indisponível'}.")
    return redirect('painel_pets')