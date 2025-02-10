<div align="center">

# Synes - cadêURacha 🏀

</div>


<div align="center">

###### Palavras-Chave: Basquete • Projeto Integrado I • Sistemas e Mídias Digitais • cadêURacha

</div>

## Sumário:
- [Sobre](#sobre)
- [Equipe](#equipe)
- [Instalação](#instalacao)
- [Requisitos Funcionais](#requisitos-funcionais)
- [Relatório e Apresentação](#relatório-e-apresentação)

---

<a id="sobre"></a>
## 🎥 Sobre:

Estamos fazendo um projeto que busca suprir as necessidades dos **atletas** e **entusiastas de basquete** no que tange ao **mapeamento e organização da utilização de arenas públicas**.  

Esperamos melhorar a **logística** e **organização de jogos independentes**.  

Para isso, optamos por utilizar a linguagem **Python** com o framework **Django** para o *Back-End* e **HTML**, **CSS** e **Bootstrap** como ferramentas para o *Front-End*.

---

<a id="equipe"></a>
  
## 🙋 Nossa Equipe:


<div align="center">
<br>

| Nome                                | Função             |
|-------------------------------------|--------------------|
| Carla Suenne Barbosa da Silva       | Back-End           |
| Jerbesson Silva da Costa            | Full Stack         |
| Lorenna Aguiar Nunes                | Front-End          |
| Maria Luíza de Meneses Albuquerque  | Designer           |
| Renan Carlos da Silva Nunes         | Designer e Líder   |
| Samya Soares Pereira                | Front-End          |

</div>

<br>

---

<a id="instalacao"></a>
## 🚀 Instalação

### Pré-requisitos

#### Instalações via Navegador:
1. **Python 3.8+**: 
   - Baixe do [site oficial do Python](https://www.python.org/downloads/)
   - Durante a instalação, marque a opção "Add Python to PATH"

2. **Git**: 
   - Baixe do [site oficial do Git](https://git-scm.com/downloads)

3. **Visual Studio Code** (ou outro editor de código):
   - Baixe do [site oficial do VS Code](https://code.visualstudio.com/download)


#### Configuração do Projeto:

1. **Clone o repositório:**
```sh
git clone https://github.com/Syne-s/CadeURacha.git
```

2. **Acessar o diretório local:**
```sh
cd CadeURacha
```

3. **Abrir o diretório no Editor de Código (VS Code):**
```sh
code .
```

#### Instalações via Terminal:
Após instalar o Python e acessar o diretório clonado, abra o terminal no VS Code (ou outro editor de código) e execute:

1. **Instalar pip**:
```sh
python -m pip install --upgrade pip
```

2. **Instalar virtualenv**:
```sh
python -m pip install virtualenv
```

3. **Criar ambiente virtual**:
```sh
python -m venv venv
```

4. **Ativar ambiente virtual**:
```sh
venv/Scripts/activate
```

5. **Instalar dependências do projeto**:
```sh
pip install -r requirements.txt
```

#### Configurações finais para execução local:
Após instalar todas as dependências:

1. **Configurar arquivos estáticos**:
```sh
python manage.py collectstatic
```

2. **Executar migrações**:
```sh
python manage.py migrate
```

3. **Rodar o servidor local**:
```sh
python manage.py runserver
```

4. **Acessar o servidor local**:
   - CTRL + Clique no link fornecido pelo Terminal
   - O endereço padrão é: http://127.0.0.1:8000/

---

  
<a id="requisitos-funcionais"></a>
## 📑 Requisitos Funcionais: 





<br>

<div align="center">


| **ID** | **Requisito Funcional**                                  | **Status**     | 
|--------|-----------------------------------------------------------|----------------|
| RF001  | Cadastrar Usuário                                         | ✅ Concluído    |
| RF002  | Autenticar Usuário                                         | ✅ Concluído    |
| RF003  | Editar Dados do Usuário                                    | ✅ Concluído    |
| RF004  | Alterar Foto de Perfil                                     | ✅ Concluído    |
| RF005  | Exibir Foto de Perfil                                      | ✅ Concluído    |
| RF006  | Excluir Conta                                              | ✅ Concluído    |
| RF007  | Sair do Sistema                                            | ✅ Concluído    |
| RF008  | Filtrar Quadras por Bairro                                 | ✅ Concluído    |
| RF009  | Capturar Localização Atual do Usuário                      | ✅ Concluído    |
| RF010  | Filtrar Quadras por Raio de Busca                          | ✅ Concluído    |
| RF011  | Buscar Quadras                                             | ✅ Concluído    |
| RF012  | Editar Quadra                                              | ⏳ Em andamento |
| RF013  | Visualizar Detalhes de Quadras                             | ⏳ Em andamento |
| RF014  | Cadastrar Jogo                                             | ✅ Concluído    |
| RF015  | Editar Jogo                                                | ⏳ Em andamento |
| RF016  | Excluir Jogo                                               | ⏳ Em andamento |
| RF017  | Verificar Disponibilidade de Quadra                        | ✅ Concluído    |
| RF018  | Confirmar Participação em Jogo (Racha)                     | ✅ Concluído    |
| RF019  | Cancelar Presença em Jogo                                  | ✅ Concluído    |
| RF020  | Visualizar Lista de Participantes de um Jogo               | ✅ Concluído    |
| RF021  | Visualizar Detalhes de Jogos                               | ⏳ Em andamento |
| RF022  | Levar Bola                                                 | ✅ Concluído    |
| RF023  | Visualizar Mapa                                            | ✅ Concluído    |
| RF024  | Visualizar Quadras no Mapa                                 | ✅ Concluído    |

---
<a id="requisitos-desejaveis"></a>
## 📑 Requisitos Desejáveis: 

<br>

<div align="center">
| **ID** | **Requisito Desejável**                                  | **Status**     |
|--------|-----------------------------------------------------------|----------------|
| RD001  | Notificação para jogadores sobre a criação de novos jogos | 🛑 Não iniciado |
| RD002  | Funcionalidade de chat entre usuários                     | 🛑 Não iniciado |
| RD003  | Sistema de níveis para classificar e recompensar usuários | 🛑 Não iniciado |
| RD004  | Recomendação de jogos para iniciantes                     | 🛑 Não iniciado |
| RD005  | Permitir o cadastro de quadras apenas para administradores | 🛑 Não iniciado |
| RD006  | Visualizar Tela de Alerta de Confirmação de Exclusão      | 🛑 Não iniciado |
| RD007  | Visualizar Tela de Feedback de Cadastro e Edição          | 🛑 Não iniciado |
| RD008  | Avaliar Quadra                                            | 🛑 Não iniciado |


</div>

<br>

---

<a id="relatório-e-apresentação"></a>
## 📝 Relatórios e Apresentação:

### Arquivos e Documentos Importantes:
- [Documento Oficial de Requisitos Funcionais e Não Funcionais](https://docs.google.com/document/d/1Ld6v-xZWNANKwsz1KVL2QF71mMjOWA8E/edit?usp=sharing&ouid=116392937404212256733&rtpof=true&sd=true)
- [Relatório Detalhado - Propostas Alternativas | Atualização de Requisitos](https://docs.google.com/document/d/1KjsB0fQIU5rVq6Xi0fGJ0Ob9SQvN61hODizhosGPWV0/edit?usp=sharing)
