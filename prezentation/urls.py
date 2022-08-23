"""prezentation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# функция для возврата картинки
from upload_app.views import home_page, database, database_in


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', home_page, name='homepage'),
    # path('database/', DatabaseCreate.as_view()),
    path('database/', database, name='database'),
    path('database_in/<int:database_id>', database_in, name='dbin'),
    path('upload/', include('upload_app.urls')),
    path('accounts/login', LoginView.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),
    path('accounts/', include('accounts.urls')),
    path('templates/', include('db_templates.urls')),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)