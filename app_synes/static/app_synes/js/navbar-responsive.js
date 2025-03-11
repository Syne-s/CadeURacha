document.addEventListener('DOMContentLoaded', function() {
    // Elementos
    const searchToggleBtn = document.querySelector('.search-toggle-btn');
    const mobileSearchContainer = document.querySelector('.mobile-search-container');
    const searchCloseBtn = document.querySelector('.search-close-btn');
    const mobileSearchBar = document.getElementById('MobileSearchBar');
    
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
        });
    }
    
    // Fecha a barra de pesquisa mobile ao clicar fora dela
    document.addEventListener('click', function(event) {
        if (mobileSearchContainer && mobileSearchContainer.classList.contains('active')) {
            const isClickInside = mobileSearchContainer.contains(event.target) || 
                                 (searchToggleBtn && searchToggleBtn.contains(event.target));
            
            if (!isClickInside) {
                mobileSearchContainer.classList.remove('active');
            }
        }
    });
    
    // Função para verificar e ajustar o layout conforme o tamanho da tela
    function checkScreenSize() {
        const navbarCollapse = document.getElementById('navbarContent');
        const navbarToggler = document.querySelector('.navbar-toggler');
        
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
});
