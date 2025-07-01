from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Habilete
from .serializers import JsonHabileteSerializer



@csrf_exempt
def json_habiletes_list(request):
    """
    List habiletes
    """
    if request.method == 'GET':
        habiletes = Habilete.objects.all()
        serializer = JsonHabileteSerializer(habiletes, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
