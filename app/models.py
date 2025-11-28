from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Pet(models.Model):
    TIPO_CHOICES = [
        ('cachorro', 'Cachorro'),
        ('gato', 'Gato'),
    ]
    
    PORTE_CHOICES = [
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande'),
    ]
    
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('femea', 'Fêmea'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name='Nome do Pet')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, default='macho', verbose_name='Sexo')
    raca = models.CharField(max_length=100, verbose_name='Raça')
    idade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        verbose_name='Idade (anos)'
    )
    porte = models.CharField(max_length=20, choices=PORTE_CHOICES, verbose_name='Porte')
    personalidade = models.TextField(verbose_name='Personalidade')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    disponivel = models.BooleanField(default=True, verbose_name='Disponível para Adoção')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
    
    def __str__(self):
        return f"{self.nome} - {self.raca}"
    
    @property
    def idade_categoria(self):
        if self.idade <= 2:
            return 'filhote'
        elif self.idade <= 7:
            return 'adulto'
        else:
            return 'idoso'

class PetImagem(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='pets/', verbose_name='Imagem', blank=True, null=True)
    static_image_path = models.CharField(max_length=255, blank=True, null=True, verbose_name='Caminho da Imagem Estática')
    ordem = models.IntegerField(default=1, verbose_name='Ordem')
    principal = models.BooleanField(default=False, verbose_name='Imagem Principal')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['ordem', '-principal', 'uploaded_at']
        verbose_name = 'Imagem do Pet'
        verbose_name_plural = 'Imagens do Pet'
    
    def __str__(self):
        return f"Imagem de {self.pet.nome}"