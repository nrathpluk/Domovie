from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.urls import api_urlpatterns as auth_api_urls

urlpatterns = [
    path('django-admin/', admin.site.urls),

    # API routes
    path('api/auth/', include((auth_api_urls, 'api_auth'))),
    path('api/', include('movies.api_urls')),
    path('api/', include('store.urls')),

    # Django template routes
    path('', include('movies.urls')),
    path('', include('accounts.urls')),
    path('admin-panel/', include('movies.admin_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
