from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_synes import views  # Add this import to fix the error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_synes.urls')),  # Inclui as rotas do app
    path('debug_cloudinary/', views.debug_cloudinary_urls, name='debug_cloudinary'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)