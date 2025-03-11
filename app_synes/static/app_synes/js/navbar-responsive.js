document.addEventListener('DOMContentLoaded', function() {
    // Elementos
    const searchToggleBtn = document.querySelector('.search-toggle-btn');
    const mobileSearchContainer = document.querySelector('.mobile-search-container');
    const searchCloseBtn = document.querySelector('.search-close-btn');
    const mobileSearchBar = document.getElementById('MobileSearchBar');
    const mobileSearchResults = document.querySelector('.mobile-search-results');
    
    // Função para abrir a barra de pesquisa mobile
    if (searchToggleBtn) {
        searchToggleBtn.addEventListener('click', function() {
            mobileSearchContainer.classList.add('active');
            // Foca no campo de pesquisa automaticamente
            setTimeout(() => {
                mobileSearchBar.focus();
            }, 300);
        });
    }
    
    // Função para fechar a barra de pesquisa mobile
    if (searchCloseBtn) {
        searchCloseBtn.addEventListener('click', function() {
            mobileSearchContainer.classList.remove('active');
            mobileSearchResults.classList.remove('show');
        });
    }
    
    // Fecha a barra de pesquisa mobile ao clicar fora dela
    document.addEventListener('click', function(event) {
        if (mobileSearchContainer && mobileSearchContainer.classList.contains('active')) {
            const isClickInside = mobileSearchContainer.contains(event.target) || 
                                  (searchToggleBtn && searchToggleBtn.contains(event.target));
            
            if (!isClickInside) {
                mobileSearchContainer.classList.remove('active');
                mobileSearchResults.classList.remove('show');
            }
        }
    });

    // Função para exibir resultados de pesquisa
    function displayMobileSearchResults(data) {
        mobileSearchResults.innerHTML = '';
        if (data.arenas.length || data.jogos.length) {
            data.arenas.forEach(arena => {
                const item = document.createElement('div');
                item.classList.add('search-results-item');
                item.innerHTML = `
                    <div><span class="label-quadra">Quadra:</span> ${arena.nome}</div>
                    <div>${arena.endereco}</div>
                `;
                mobileSearchResults.appendChild(item);
            });
            data.jogos.forEach(jogo => {
                const item = document.createElement('div');
                item.classList.add('search-results-item');
                item.innerHTML = `
                    <div><span class="label-jogo">Racha:</span> ${jogo.titulo}</div>
                    <div>${jogo.arena} - ${jogo.data} às ${jogo.horario}</div>
                    <div class="description">${jogo.descricao || 'Sem descrição'}</div>
                `;
                mobileSearchResults.appendChild(item);
            });
            mobileSearchResults.classList.add('show');
        } else {
            mobileSearchResults.innerHTML = '<div class="no-results-message">Nenhum resultado encontrado</div>';
            mobileSearchResults.classList.add('show');
        }
    }

    // Função para buscar resultados
    mobileSearchBar.addEventListener('input', function() {
        const query = mobileSearchBar.value.trim();
        if (query.length >= 2) {
            fetch(`/search/?q=${query}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                displayMobileSearchResults(data);
            })
            .catch(error => console.error('Erro na busca:', error));
        } else {
            mobileSearchResults.classList.remove('show');
        }
    });

    // Função para verificar e ajustar o layout conforme o tamanho da tela
    function checkScreenSize() {
        const navbarCollapse = document.getElementById('navbarContent');
        
        if (window.innerWidth <= 991.98) {
            // Em telas menores, garantir que o menu está colapsado inicialmente
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
            }
        }
    }
    
    // Verificar o tamanho da tela ao carregar
    checkScreenSize();
    
    // Verificar o tamanho da tela ao redimensionar
    window.addEventListener('resize', checkScreenSize);
    
    // Melhorias para o dropdown de perfil
    const profileButton = document.getElementById('profileDropdown');
    if (profileButton) {
        // Inicializar o dropdown via Bootstrap JS para garantir comportamento correto
        const profileDropdown = new bootstrap.Dropdown(profileButton, {
            popperConfig: {
                placement: 'bottom-end',
                modifiers: [
                    {
                        name: 'offset',
                        options: {
                            offset: [0, 8],
                        },
                    },
                ],
            }
        });
        
        // Adicionar animações suaves
        const dropdownMenu = profileButton.nextElementSibling;
        if (dropdownMenu) {
            dropdownMenu.addEventListener('show.bs.dropdown', function () {
                this.classList.add('animate__animated', 'animate__fadeIn');
                this.style.animationDuration = '0.3s';
            });
        }
    }
});
