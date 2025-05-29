from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Activite
from .serializers import JsonActiviteSerializer

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def json_activite_list(request):
    """
    List activites
    """
    if request.method == 'GET':
        activites = Activite.objects.all()
        serializer = JsonActiviteSerializer(activites, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def json_activite_detail(request, slug):
    """
    Retrieve an activite
    """
    try:
        act = Activite.objects.get(slug=slug)
    except Activite.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = JsonActiviteSerializer(act,  context={'request': request})
        return JsonResponse(serializer.data)

        