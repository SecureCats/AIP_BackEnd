from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse, \
    HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from . import models
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import json
from .utils import cl_sign
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.


def pubkey_query(request, semester, classno):
    pubkey = get_object_or_404(
        models.PublicKey,
        teaching_class__classno=classno,
        semester=semester
    )
    return JsonResponse({
        'n': pubkey.n,
        'a': pubkey.a,
        'b': pubkey.b,
        'c': pubkey.c,
        'g': pubkey.g,
        'h': pubkey.h
    })

# @login_required
# def index(request):
#     return HttpResponse('hello, world')


def frontend(request):
    return render(request, 'login/index.html')


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def userinfo(request):
    me = models.AipUser.objects.get(username=request.user)
    return JsonResponse({
        'username': me.username,
    })


@require_POST
@login_required
def sign(request):
    if request.user.is_signed:
        return HttpResponseForbidden('You have got the signiture')
    recv_json = json.loads(request.body)
    teaching_class = request.user.teaching_class
    if not teaching_class:
        return HttpResponseForbidden('You have not joined a class')
    pubkey = teaching_class.publickey_set.get(semester=models.get_semester())
    if not pubkey:
        return HttpResponseForbidden('Prof commmitment has not start yet')
    param_list = ('x', 'C', 'z1', 'z2', 'y')
    try:
        params = {i: recv_json[i] for i in param_list}
    except:
        return HttpResponseBadRequest()
    ret = cl_sign(pubkey, **params)
    if not ret:
        return HttpResponseBadRequest('you are fooling me')
    request.user.is_signed = True
    request.user.save()
    return JsonResponse({
        'r_': str(ret[0]),
        'e': str(ret[1]),
        'v': str(ret[2])
    })
