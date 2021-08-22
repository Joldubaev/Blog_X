"""
WSGI config for idea_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idea_api.settings')

application = get_wsgi_application()
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Idea-X API",
      default_version='v1',
      description="Swagger UI - это небольшая коллекция скриптов для создания интерактивной документации для API веб-приложений с REST протоколом. ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('api/account/', include('account.urls')),
    path('api/v1/docs', schema_view.with_ui()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)