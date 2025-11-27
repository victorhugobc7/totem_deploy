from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Pet, PetImagem
import json

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
    
    # Porte (0-25 pontos)
    porte_compatibilidade = {
        'pequeno': {'pequeno': 25, 'medio': 15, 'grande': 5},
        'medio': {'pequeno': 15, 'medio': 25, 'grande': 15},
        'grande': {'pequeno': 5, 'medio': 15, 'grande': 25}
    }
    
    preferencia_porte = preferencias.get('porte')
    if preferencia_porte and preferencia_porte != 'sem_preferencia':
        pontuacao += porte_compatibilidade.get(preferencia_porte, {}).get(pet.porte, 0)
    else:
        pontuacao += 20  # Pontuação média se não houver preferência
    
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
    # Get available pets for carousel
    pets = Pet.objects.filter(disponivel=True)[:6]  # Limit to 6 pets for carousel
    
    return render(request, 'comecar.html', {
        'pets': pets
    })

def pergunta_dupla(request, step=1):
    """Perguntas com duas opções"""
    perguntas = {
        1: {
            'titulo': 'Você prefere um cachorro ou um gato?',
            'opcoes': [
                {'valor': 'cachorro', 'texto': 'Cachorro', 'icone': 'fas fa-dog fa-5x'},
                {'valor': 'gato', 'texto': 'Gato', 'icone': 'fas fa-cat fa-5x'}
            ],
            'proxima': '/pergunta/dupla/2/'
        },
        2: {
            'titulo': 'Você prefere macho ou fêmea?',
            'opcoes': [
                {'valor': 'macho', 'texto': 'Macho', 'icone': 'fas fa-mars fa-5x'},
                {'valor': 'femea', 'texto': 'Fêmea', 'icone': 'fas fa-venus fa-5x'}
            ],
            'proxima': '/pergunta/dupla/3/'
        },
        3: {
            'titulo': 'Qual faixa etária você prefere?',
            'opcoes': [
                {'valor': 'filhote', 'texto': 'Filhote (0-2 anos)', 'icone': 'fas fa-dog fa-5x'},
                {'valor': 'adulto', 'texto': 'Adulto (3-7 anos)', 'icone': 'fas fa-paw fa-5x'}
            ],
            'proxima': '/pergunta/tripla/4/'
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
    
    # Buscar pets disponíveis
    pets_disponiveis = Pet.objects.filter(disponivel=True)
    
    # Calcular compatibilidade
    pets_compatíveis = []
    for pet in pets_disponiveis:
        compatibilidade = calcular_compatibilidade(pet, preferencias)
        if compatibilidade >= 50:  # Mostrar apenas pets com 50%+ compatibilidade
            # Check if pet has images in database, if not, try to find in static folder
            if not pet.imagens.exists():
                static_image_path = f"images/info-pets/Imagens/{pet.nome}.png"
            else:
                static_image_path = None
                
            pets_compatíveis.append({
                'pet': pet,
                'compatibilidade': compatibilidade,
                'static_image_path': static_image_path
            })
    
    # Ordenar por compatibilidade
    pets_compatíveis.sort(key=lambda x: x['compatibilidade'], reverse=True)
    
    return render(request, 'pet_lista.html', {
        'pets_compatíveis': pets_compatíveis,
        'preferencias': preferencias
    })

def pet_detalhes(request, pet_id):
    """Mostra detalhes de um pet específico"""
    pet = get_object_or_404(Pet, id=pet_id)
    imagens = pet.imagens.all()
    
    # Check if pet has images in database, if not, try to find in static folder
    if not imagens:
        # Try to find image in static folder based on pet name
        static_image_path = f"images/info-pets/Imagens/{pet.nome}.png"
    else:
        static_image_path = None
    
    return render(request, 'pet_detalhes.html', {
        'pet': pet,
        'imagens': imagens,
        'static_image_path': static_image_path
    })

def cadastrar_pet(request):
    """Formulário para cadastrar novo pet"""
    if request.method == 'POST':
        try:
            pet = Pet.objects.create(
                nome=request.POST.get('nome'),
                tipo=request.POST.get('tipo'),
                raca=request.POST.get('raca'),
                idade=int(request.POST.get('idade')),
                porte=request.POST.get('porte'),
                personalidade=request.POST.get('personalidade'),
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
            
            messages.success(request, 'Pet cadastrado com sucesso!')
            return redirect('pet_detalhes', pet_id=pet.id)
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar pet: {str(e)}')
    
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
def core_cadastrar_pet(request):
    """Formulário para cadastrar novo pet com autenticação"""
    if request.method == 'POST':
        try:
            pet = Pet.objects.create(
                nome=request.POST.get('nome'),
                tipo=request.POST.get('tipo'),
                raca=request.POST.get('raca'),
                idade=int(request.POST.get('idade')),
                porte=request.POST.get('porte'),
                personalidade=request.POST.get('personalidade'),
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
            
            messages.success(request, 'Pet cadastrado com sucesso!')
            return redirect('core_dashboard')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar pet: {str(e)}')
    
    return render(request, 'core/cadastrar_pet.html', {})