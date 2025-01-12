<div align="center">

# Synes - CadêURacha 🏀

</div>


<div align="center">

###### Palavras-Chave: Basquete • Projeto Integrado I • Sistemas e Mídias Digitais • CadêURacha

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

<div align="center">


<br>

| Código | Descrição                              | Status |
|--------|----------------------------------------|:------:|
| RF001  | Cadastrar Usuário                      |   ✓    |
| RF002  | Autenticar Usuário                     |   ✓    |
| RF003  | Cadastrar Jogo                         |   ✓    |
| RF004  | Filtrar Bairro                         |   ✓    |
| RF005  | Buscar Rachas                          |   ✓    |
| RF006  | Editar Dados do Usuário                |   ✓    |
| RF007  | Editar Jogo                            |   ✓    |
| RF008  | Cancelar Presença em Jogo              |   ✕    |
| RF009  | Verificar Disponibilidade de Quadra    |   ✕    |
| RF010  | Avaliar Quadra                         |   ✕    |
| RF011  | Confirmar Participação em Jogo (Racha) |   ✕    |
| RF012  | Notificar Novo Jogo                    |   ✕    |
| RF013  | Sair do Sistema                        |   ✓    |
| RF014  | Excluir Conta                          |   ✓    |
| RF015  | Excluir Jogo                           |   ✓    |
| RF016  | Recomendar Jogos para Iniciantes       |   ✕    |


</div>

<br>

---

<a id="relatório-e-apresentação"></a>
## 📝 Relatórios e Apresentação:

### Arquivos e Documentos Importantes:
- [Documento Oficial de Requisitos Funcionais e Não Funcionais](https://docs.google.com/document/d/1Ld6v-xZWNANKwsz1KVL2QF71mMjOWA8E/edit?usp=sharing&ouid=116392937404212256733&rtpof=true&sd=true)
- [Relatório Detalhado - Propostas Alternativas | Atualização de Requisitos](https://docs.google.com/document/d/1KjsB0fQIU5rVq6Xi0fGJ0Ob9SQvN61hODizhosGPWV0/edit?usp=sharing)
