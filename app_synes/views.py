import traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Arena, Jogo
from .forms import ArenaForm, EditProfileForm, CustomPasswordChangeForm, JogoForm
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, timezone, date
from django.utils import timezone
from django.db.models import Q
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
import json
import re
from django.views.decorators.http import require_POST
from zoneinfo import ZoneInfo

def check_username(request):
    username = request.GET.get('username')
    User = get_user_model()
    
    if User.objects.filter(username__iexact=username).exists():
        return JsonResponse({
            'exists': True,
            'message': 'Nome de usuário já em uso'
        })
    return JsonResponse({'exists': False})

def check_email(request):
    email = request.GET.get('email')
    if email and CustomUser.objects.filter(email__iexact=email).exists():
        return JsonResponse({
            'exists': True,
            'message': 'E-mail já está registrado.'
        })
    return JsonResponse({'exists': False})

# Expressão regular para validar o formato do e-mail
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

def cadastrar_usuario(request):
    if request.method == 'GET':
        return render(request, 'app_synes/cadastrar_usuario.html')
    
    if request.method == 'POST':
        # Tratamento para requisição AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            levar_bola = request.POST.get("levar_bola", False)

            # Validação de formato de e-mail
            if not re.match(EMAIL_REGEX, email):
                return JsonResponse({'success': False, 'message': 'Digite um e-mail válido.'})
            
            # Verifica se o e-mail já está registrado (ignora case)
            if CustomUser.objects.filter(email__iexact=email).exists():
                return JsonResponse({'success': False, 'message': 'E-mail já está registrado.'})
            
            if password != confirm_password:
                return JsonResponse({'success': False, 'message': 'As senhas não coincidem.'})
            
            # Verifica se o nome de usuário já existe
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Nome de usuário já existe.'})
            
            # Cria o novo usuário
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                levar_bola=levar_bola
            )
            
            return JsonResponse({'success': True, 'message': 'Cadastro realizado com sucesso!'})
        
        return render(request, 'app_synes/cadastrar_usuario.html')
    
    return HttpResponseNotAllowed(['GET', 'POST'])

def check_invalid_username(username):
    pattern = re.compile(r'^[a-zA-Z](?!.*__)[a-zA-Z0-9]*(_[a-zA-Z0-9]+)*$')
    return not pattern.match(username)

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
            if check_invalid_username(user.username):
                login(request, user)  # Log the user in to allow username update
                return JsonResponse({
                    'success': False,
                    'needs_update': True,
                    'message': 'Seu nome de usuário precisa ser atualizado.'
                })
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Usuário ou senha inválidos.'})
    return render(request, 'app_synes/logar.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    """
    View para a página inicial.
    """
    return render(request, "app_synes/index.html")

def mapa_view(request):
    arenas = Arena.objects.all().order_by('nome')
    neighborhoods = Arena.objects.values_list('bairro', flat=True).distinct().order_by('bairro')
    return render(request, 'app_synes/mapa.html', {'arenas': arenas, 'neighborhoods': neighborhoods})

@login_required
def cadastrar_quadra(request):
    if request.method == 'POST':
        form = ArenaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mapa')
    else:
        form = ArenaForm()
    return render(request, 'app_synes/cadastrar_quadra.html', {'form': form})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user)  # Add request.FILES
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        
        if 'username' in request.POST or 'email' in request.POST or 'foto_perfil' in request.FILES:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Perfil atualizado com sucesso.')
            else:
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, error, extra_tags='danger')
        
        if 'old_password' in request.POST or 'new_password1' in request.POST or 'new_password2' in request.POST:
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Important!
                messages.success(request, 'Senha alterada com sucesso.')
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        if field == 'old_password' and 'incorrect' in error.lower():
                            messages.error(request, 'A senha atual está incorreta.', extra_tags='danger')
                        elif 'The two password fields didn’t match.' in error:
                            messages.error(request, 'Os dois campos de senha não coincidem.', extra_tags='danger')
                        else:
                            messages.error(request, error, extra_tags='danger')
        
        return redirect('editar_perfil')
    else:
        profile_form = EditProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'app_synes/editar_perfil.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })

@login_required
def confirmar_exclusao_usuario(request):
    return render(request, 'app_synes/confirmar_exclusao_usuario.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        messages.success(request, 'Sua conta foi desativada com sucesso.')
        return redirect('index')
    return redirect('confirmar_exclusao_usuario')

def criar_jogo(request):
    if request.method == 'POST':
        form = JogoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nome_da_view_de_sucesso')
    else:
        form = JogoForm()
    return render(request, 'app_synes/criar_jogo.html', {'form': form})

@login_required
def cadastrar_racha(request):
    # Get the arena_id from URL parameters
    arena_id = request.GET.get('arena_id')
    
    if request.method == 'POST':
        form = JogoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                jogo = form.save(commit=False)
                jogo.usuario = request.user
                jogo.criador_jogo = request.user
                jogo.bolas = int(request.POST.get('bolas', 0))
                jogo.save()
                jogo.participantes.add(request.user)
                messages.success(request, 'Racha criado com sucesso!')
                return redirect('detalhes_jogo', jogo.id)
            except Exception as e:
                print(f"Erro ao salvar jogo: {e}")
                messages.error(request, f'Erro ao salvar o racha: {str(e)}')
        else:
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                messages.error(request, f'Erro no campo {field}: {", ".join(errors)}')
    else:
        initial_data = {}
        if arena_id:
            try:
                arena = Arena.objects.get(id=arena_id)
                initial_data = {'arena': arena}
                form = JogoForm(initial=initial_data)
            except Arena.DoesNotExist:
                form = JogoForm()
        else:
            form = JogoForm()
    
    return render(request, 'app_synes/cadastrar_racha.html', {'form': form})

@login_required
def listar_jogos(request):
    # Obtém o timezone de Brasília
    tz_brasil = ZoneInfo("America/Sao_Paulo")
    agora = timezone.now().astimezone(tz_brasil)

    # Obtém os jogos e converte para lista para poder ordenar
    jogos_criados = list(Jogo.objects.filter(criador_jogo=request.user))
    jogos_confirmados = list(Jogo.objects.filter(participantes=request.user).exclude(criador_jogo=request.user))

    # Função auxiliar para ordenação
    def get_datetime_jogo(jogo):
        data = jogo.data
        horario = datetime.strptime(jogo.horario, '%H:%M').time()
        return timezone.make_aware(
            datetime.combine(data, horario),
            timezone=tz_brasil
        )

    # Ordena os jogos por data e horário
    jogos_criados.sort(key=lambda x: get_datetime_jogo(x))
    jogos_confirmados.sort(key=lambda x: get_datetime_jogo(x))

    # Remove jogos que já passaram
    jogos_criados = [j for j in jogos_criados if get_datetime_jogo(j) >= agora]
    jogos_confirmados = [j for j in jogos_confirmados if get_datetime_jogo(j) >= agora]

    context = {
        'jogos_criados': jogos_criados,
        'jogos_confirmados': jogos_confirmados,
        'timestamp': timezone.now().timestamp(),
    }
    return render(request, 'app_synes/listar_jogos.html', context)

def listar_todos_jogos(request):
    hoje = date.today()

    # Excluir jogos expirados
    Jogo.objects.filter(data__lt=hoje).delete()

    # Recuperar todos os jogos restantes
    jogos = Jogo.objects.all()

    return render(request, 'app_synes/listar_todos_jogos.html', {'jogos': jogos})

def search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '').strip()
        if len(query) >= 2:
            arenas = Arena.objects.filter(
                Q(nome__icontains=query) |
                Q(bairro__icontains=query)
            )[:5]

            arena_ids = [arena.id for arena in arenas]

            jogos = Jogo.objects.filter(
                Q(titulo__icontains=query) |
                Q(descricao__icontains=query) |
                Q(arena_id__in=arena_ids)
            ).select_related('arena')[:5]

            results = {
                'arenas': [
                    {
                        'id': arena.id,
                        'nome': arena.nome,
                        'endereco': f"{arena.bairro}, {arena.cidade}",
                        'tipo': 'quadra'
                    } for arena in arenas
                ],
                'jogos': [
                    {
                        'id': jogo.id,
                        'titulo': jogo.titulo,
                        'arena': jogo.arena.nome,
                        'data': jogo.data.strftime('%d/%m/%Y'),
                        'horario': str(jogo.horario),
                        'descricao': str(jogo.descricao),  # Convert to string explicitly
                        'tipo': 'jogo'
                    } for jogo in jogos
                ]
            }
            return JsonResponse(results)
        
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def editar_jogo(request, id):
    jogo = get_object_or_404(Jogo, id=id)
    jogos = Jogo.objects.all()
    if request.method == 'POST':
        form = JogoForm(request.POST, instance=jogo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogo atualizado com sucesso!')
            return redirect('listar_jogos')
            
        else:
            messages.error(request, 'Erro ao atualizar jogo.')
    else:
        form = JogoForm(instance=jogo)
    return render(request, 'app_synes/editar_jogo.html', {'form': form, 'jogo': jogo})

@login_required
def excluir_jogo(request, id):
    jogo = get_object_or_404(Jogo, id=id)
    if request.method == 'POST':
        jogo.delete()
        messages.success(request, 'Jogo excluído com sucesso!')
        return redirect('listar_jogos')
    return render(request, 'app_synes/excluir_jogo.html', {'jogo': jogo})

@login_required
def confirmar_presenca(request, id):
    jogo = get_object_or_404(Jogo, id=id)
    user = request.user

    if user in jogo.participantes.all():
        return JsonResponse({'status': 'error', 'message': 'Você já confirmou presença.'})

    jogo.participantes.add(user)
    return JsonResponse({'status': 'success',
                          'message': 'Presença confirmada!',
                          'texto_cancelar_presenca':'Cancelar presença',
                          'acao_cancelar_presenca':'cancelar-presenca'})


@login_required
def excluir_presenca(request, id):
    jogo = get_object_or_404(Jogo, id=id)
    user = request.user

    if user not in jogo.participantes.all():
        return JsonResponse({'status': 'error', 'message': 'Você não confirmou presença neste evento.'})

    jogo.participantes.remove(user)
    return JsonResponse({'status': 'success',
                          'message': 'Presença removida com sucesso!',
                          'texto_confirmar_presenca':'Confirmar presença',
                          'acao_confirmar_presenca':'confirmar-presenca'})
    

@login_required
def levar_bola(request, jogo_id):
    jogo = get_object_or_404(Jogo, id=jogo_id)

    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao == 'adicionar':
            jogo.bolas += 1
            request.user.leva_bola = True  # Marcamos que esse usuário está levando a bola
            messages.success(request, "Você confirmou que levará uma bola!")
        elif acao == 'remover' and request.user.leva_bola:
            jogo.bolas -= 1
            request.user.leva_bola = False  # Desmarca que o usuário está levando a bola
            messages.success(request, "Você cancelou sua bolinha.")

        jogo.save()
        request.user.save()

    return redirect('listar_todos_jogos')

def update_username(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_username = data.get('username')
        
        if not re.match(r'^[a-zA-Z](?!.*__)[a-zA-Z0-9]*(_[a-zA-Z0-9]+)*$', new_username):
            return JsonResponse({
                'success': False,
                'message': 'Nome de usuário inválido'
            })
            
        try:
            request.user.username = new_username
            request.user.save()
            return JsonResponse({
                'success': True,
                'message': 'Nome de usuário atualizado com sucesso'
            })
        except:
            return JsonResponse({
                'success': False,
                'message': 'Erro ao atualizar nome de usuário'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def teste(request):
    return render(request, 'app_synes/detalhes_quadra.html')  # Especifique o caminho completo

def todos(request):
    # Obtém o timezone de Brasília
    tz_brasil = ZoneInfo("America/Sao_Paulo")
    agora = timezone.now().astimezone(tz_brasil)

    # Obtém todas as quadras
    quadras = Arena.objects.all()

    # Obtém os jogos e converte para lista para ordenar
    jogos = list(Jogo.objects.all())

    # Função auxiliar para ordenação
    def get_datetime_jogo(jogo):
        data = jogo.data
        horario = datetime.strptime(jogo.horario, '%H:%M').time()
        return timezone.make_aware(
            datetime.combine(data, horario),
            timezone=tz_brasil
        )

    # Ordena os jogos por data e horário
    jogos.sort(key=lambda x: get_datetime_jogo(x))

    # Remove jogos que já passaram
    jogos = [j for j in jogos if get_datetime_jogo(j) >= agora]

    return render(request, 'app_synes/todos.html', {
        'quadras': quadras,
        'jogos': jogos,
        'timestamp': timezone.now().timestamp(),
    })

def detalhes_quadra(request, id):
    # Obtém o timezone de Brasília
    tz_brasil = ZoneInfo("America/Sao_Paulo")
    agora = timezone.now().astimezone(tz_brasil)

    # Busca a quadra específica ou retorna 404 se não encontrar
    quadra = get_object_or_404(Arena, id=id)
    
    # Busca todos os jogos relacionados a esta quadra e converte para lista
    jogos_quadra = list(Jogo.objects.filter(arena=quadra))

    # Função auxiliar para ordenação
    def get_datetime_jogo(jogo):
        data = jogo.data
        horario = datetime.strptime(jogo.horario, '%H:%M').time()
        return timezone.make_aware(
            datetime.combine(data, horario),
            timezone=tz_brasil
        )

    # Ordena os jogos por data e horário
    jogos_quadra.sort(key=lambda x: get_datetime_jogo(x))

    # Remove jogos que já passaram
    jogos_quadra = [j for j in jogos_quadra if get_datetime_jogo(j) >= agora]
    
    context = {
        'quadra': quadra,
        'jogos_quadra': jogos_quadra,
    }
    return render(request, 'app_synes/detalhes_quadra.html', context)

def detalhes_jogo(request, id):
    jogo = get_object_or_404(Jogo, id=id)
    participantes = jogo.participantes.all()
    tem_bolas = jogo.participantes.filter(levar_bola=True).exists()
    
    context = {
        'jogo': jogo,
        'jogadores': participantes,
        'tem_bolas': tem_bolas
    }
    return render(request, 'app_synes/detalhes_racha.html', context)

@login_required
def detalhes_racha_user(request, id):
    jogo = get_object_or_404(Jogo, id=id)
    participantes = jogo.participantes.all()
    
    context = {
        'jogo': jogo,
        'jogadores': participantes
    }
    return render(request, 'app_synes/detalhes_racha_user.html', context)

def test_jogo(request):
    return render(request, 'app_synes/detalhes_racha_user.html')

@require_POST
def toggle_presenca(request):
    try:
        data = json.loads(request.body)
        jogo_id = data.get('jogo_id')
        confirmar = data.get('confirmar')
        
        jogo = get_object_or_404(Jogo, id=jogo_id)
        
        if confirmar:
            # Adiciona o usuário aos participantes
            jogo.participantes.add(request.user)
            mensagem = "Presença confirmada com sucesso!"
        else:
            # Remove o usuário dos participantes
            jogo.participantes.remove(request.user)
            # Se o usuário estava levando bola, decrementa o contador
            if request.user.levar_bola:
                jogo.bolas = max(0, jogo.bolas - 1)
                request.user.levar_bola = False
                request.user.save()
            jogo.save()
            mensagem = "Presença cancelada com sucesso!"
        
        return JsonResponse({'success': True, 'message': mensagem})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@require_POST
def toggle_levar_bola(request):
    try:
        data = json.loads(request.body)
        jogo_id = data.get('jogo_id')
        levar_bola = data.get('levar_bola')
        
        jogo = get_object_or_404(Jogo, id=jogo_id)
        user = request.user
        
        if user in jogo.participantes.all():
            user.levar_bola = levar_bola
            user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Você precisa confirmar presença primeiro'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

def buscar(request):
    query = request.GET.get('q', '')
    
    quadras = Arena.objects.filter(
        Q(nome__icontains=query) |
        Q(bairro__icontains=query) |
        Q(cidade__icontains=query)
    )
    
    jogos = Jogo.objects.filter(
        Q(titulo__icontains=query) |
        Q(arena__nome__icontains=query) |
        Q(arena__bairro__icontains=query)
    )
    
    context = {
        'query': query,  # Esta é a linha importante
        'quadras': quadras,
        'jogos': jogos,
    }
    
    return render(request, 'app_synes/buscar.html', context)

