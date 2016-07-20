"""cerbereapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, url, include
from django.contrib import admin
from . import views

urlpatterns = [
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout'),
    # ex: /
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    # Registration
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^account/', views.account, name='account'),
    # Dashboard
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    # Document Models
    url(r'^documentmodels/', views.documentmodels_list, name='documentmodels_list'),
    url(r'^documentmodel/(\d+)', views.documentmodel_details, name='documentmodel_details'),
    url(r'^documentmodel/trash/(\d+)', views.documentmodel_trash, name='documentmodel_trash'),
    # Employees
    url(r'^employees/', views.employees_list, name='employees_list'),
    url(r'^employee/(\d+)', views.employee_details, name='employee_details'),
    url(r'^employee/trash/(\d+)', views.employee_trash, name='employee_trash'),
    # Profiles
    url(r'^profiles/', views.profiles_list, name='profiles_list'),
    url(r'^profile/(\d+)', views.profile_details, name='profile_details'),
    url(r'^profile/trash/(\d+)', views.profile_trash, name='profile_trash'),
    # Admin
    url(r'^admin/', admin.site.urls),
]
