from django.shortcuts import render
# Create your views here.
import json
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse

def swagger_ui(request):
    with open('docs/templates/docs/swagger.json') as f:
        data = json.load(f)
    renderer = JSONRenderer()
    json_data = renderer.render(data)
    return HttpResponse(json_data, content_type='application/json')