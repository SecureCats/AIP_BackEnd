from django.contrib import admin
from .models import PublicKey
from Crypto.Util import number
import random

# Register your models here.
@admin.register(PublicKey)
class PublicKeyAdmin(admin.ModelAdmin):

    actions = ['init_pubkey']
    
    def init_pubkey(self, request, queryset):
        for obj in queryset:
            if obj.n == '':
                p = number.getStrongPrime(2048)
                q = number.getStrongPrime(2048)
                n = p*q
                randlis = [random.randrange(0, 1<<1024) for _ in range(4)]
                rand2lis = list(map(lambda x: pow(x, 2, n) ,randlis))
                h = rand2lis[3]
                r = random.randrange(100)
                g = pow(h, r, n)
                obj.p = str(p)
                obj.n = str(n)
                obj.a = str(rand2lis[0])
                obj.b = str(rand2lis[1])
                obj.c = str(rand2lis[2])
                obj.h = str(rand2lis[3])
                obj.g = str(g)
                obj.save()

    