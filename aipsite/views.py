from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from . import models
from django.shortcuts import get_object_or_404

# Create your views here.
def pubkey_query(request, classno):
    pubkey = get_object_or_404(models.PublicKey, classno=classno)
    return JsonResponse({
        'n': pubkey.n,
        'a': pubkey.a,
        'b': pubkey.b,
        'c': pubkey.c,
        'g': pubkey.g,
        'h': pubkey.h
    })
