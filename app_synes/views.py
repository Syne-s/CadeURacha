from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import CustomUser  # Importe o modelo CustomUser

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
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': "Login realizado com sucesso!"})
            else:
                return JsonResponse({'success': False, 'message': "E-mail ou senha inválidos."})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': "E-mail ou senha inválidos."})

    return render(request, "app_synes/login.html")

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