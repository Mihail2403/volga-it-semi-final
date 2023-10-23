from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework import renderers
from .views import swagger_ui

urlpatterns = [
    path('docs/', TemplateView.as_view(
        template_name='docs/swagger.html',
        extra_context={'schema_url':'openapi-schema-json'}
    ), name='swagger-ui'),
    path('openapi.json', swagger_ui, name='openapi-schema-json')
]
