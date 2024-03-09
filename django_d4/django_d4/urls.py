"""
URL configuration for django_d4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from simpleapp.views import multiply, ProductsList
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from rest_framework import routers
from simpleapp import views


router = routers.DefaultRouter()
router.register(r'product', views.ProductViewset)
router.register(r'category', views.CategoryViewset)
# router.register(r'subscriptions', views.SubscriptionsViewset)


urlpatterns = [
    # path(r'^', include('polls.urls')), admin/
    path('', ProductsList.as_view(), name='product_list'),
    path('admin/', admin.site.urls),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    path('pages/', include('django.contrib.flatpages.urls')),
    # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
    # подключались к главному приложению с префиксом products/.
    path('products/', include('simpleapp.urls')),
    path('multiply/', multiply),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('accounts.urls')),  # Добавил
    path('accounts/', include('allauth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
# urlpatterns += i18n_patterns(
#     path('', include('basic.urls'))
# )
