"""edplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path

from documentation.swagger import swagger_schema_view

urlpatterns = [
    # Auth & Admin
    path("admin/", admin.site.urls),
    path(
        "api/user_manager/",
        include(("core_modules.user_manager.urls", "user_manager"), namespace="user_manager"),
    ),
    path(
        "api/testing/",
        include(("core_modules.testing.urls", "testing"), namespace="testing"),
    ),
    # Documentation urls
    path(
        "documentation/swagger/",
        swagger_schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "documentation/redoc/",
        swagger_schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("", swagger_schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
