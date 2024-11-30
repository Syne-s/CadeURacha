from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Verifica se as senhas coincidem
        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "app_synes/register.html")  # Caminho correto para o template

        # Verifica se o e-mail já existe
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está em uso.")
            return render(request, "app_synes/register.html")  # Caminho correto para o template

        try:
            # Cria o usuário com is_active=True por padrão
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
            return render(request, "app_synes/register.html")  # Caminho correto para o template

    return render(request, "app_synes/register.html")  # Caminho correto para o template
