from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Arena
from .forms import ArenaForm

def register(request):
    # Handle GET request - show registration form
    if request.method == 'GET':
        return render(request, 'app_synes/register.html')
    
    # Handle POST request
    if request.method == 'POST':
        # Check if request is AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:
                return JsonResponse({'success': False, 'message': 'As senhas não coincidem.'})

            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Nome de usuário já existe.'})

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'E-mail já está registrado.'})

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            return JsonResponse({'success': True, 'message': 'Cadastro realizado com sucesso!'})
        
        # Handle non-AJAX POST request
        return render(request, 'app_synes/register.html')

    # Handle other methods
    return HttpResponseNotAllowed(['GET', 'POST'])

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

def map_view(request):
    arenas = Arena.objects.all().order_by('nome')
    neighborhoods = Arena.objects.values_list('bairro', flat=True).distinct().order_by('bairro')
    return render(request, 'app_synes/map.html', {'arenas': arenas, 'neighborhoods': neighborhoods})

@login_required
def cadastrar_arena(request):
    if request.method == 'POST':
        form = ArenaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ArenaForm()
    return render(request, 'app_synes/cadastrar_arena.html', {'form': form})