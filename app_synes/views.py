from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Arena
from .forms import ArenaForm

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "app_synes/register.html")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já existe.")
            return render(request, "app_synes/register.html")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "E-mail já está registrado.")
            return render(request, "app_synes/register.html")

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True,  # Ativo por padrão
            )
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect("login")  # Substitua pela URL de login

        except Exception as e:
            messages.error(request, f"Erro ao cadastrar usuário: {e}")
            return render(request, "app_synes/register.html")

    return render(request, "app_synes/register.html")

def login_view(request):
    if request.method == 'POST':
        login_input = request.POST['login']
        password = request.POST['password']
        
        # Check if login_input is an email or username
        if '@' in login_input:
            try:
                user = CustomUser.objects.get(email=login_input)
                username = user.username
            except CustomUser.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid email or password'})
        else:
            username = login_input
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login efetuado com sucesso!'})
        else:
            return JsonResponse({'success': False, 'message': 'Usuário/E-mail ou senha inválidos.'})
    
    return render(request, 'app_synes/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    """
    View para a página inicial.
    """
    return render(request, "app_synes/index.html")

def map(request):
    """
    View para a página do mapa.
    """
    return render(request, "app_synes/map.html")

@login_required
def cadastrar_arena(request):
    if request.method == 'POST':
        form = ArenaForm(request.POST)
        if form.is_valid():
            arena = form.save(commit=False)
            arena.usuario = request.user
            arena.save()
            return redirect('map')  # Redireciona de volta para o mapa
    else:
        # Recupera latitude e longitude dos parâmetros GET
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lng')
        
        # Inicializa o formulário com as coordenadas
        form = ArenaForm(initial={
            'latitude': latitude,
            'longitude': longitude
        })
    
    return render(request, 'app_synes/cadastrar_arena.html', {'form': form})

def map(request):
    arenas = Arena.objects.filter(status=True)
    return render(request, 'app_synes/map.html', {'arenas': arenas})