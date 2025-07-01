from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {"activite": "famille2025"}
    return render(request, "glo/index.html", context)

@login_required
def debug(request):
    context = {}
    return render(request, "glo/debug.html", context)

@login_required
def test(request):
    context = {}
    return render(request, "glo/test.html", context)