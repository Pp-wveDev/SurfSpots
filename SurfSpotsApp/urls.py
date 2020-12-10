"""SurfSpotsApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Configuring drf_yasg
schema_view = get_schema_view(
   openapi.Info(
      title="Graffiti Web",
      default_version='v1',
      description="Looking for a spot with awesome waves? You are at the right spot!",
      terms_of_service="https://www.grafittiApp.com/policies/terms/",
      contact=openapi.Contact(email="contact@graffitiApp.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Apps
    path('', include('SurfSpotsAPI.urls')),
    path('', include('SurfSpotsWeb.urls')),
    
    # OpenAPI
    path('api/', schema_view.with_ui('swagger',
                                 cache_timeout=0), name="schema-swagger-ui"),
]
