from django.conf.urls import url
from . import views
from django.urls import path,include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('', views.default_map, name="default"),
    path('result/<int:pk>/', views.show_result, name='list'),
    path('map/<int:pk>/', views.show_map, name='map'),
    path('api/', include('distanceapi.urls')),
    path('docs/',include_docs_urls(title='SBXAPI')),
    path('schema', get_schema_view(
        title='SBXAPI',
        description='API for SBX API',
        version='1.0.0'),
        name='openapi-schema'),
]
