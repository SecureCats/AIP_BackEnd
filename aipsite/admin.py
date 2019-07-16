from django.contrib import admin
from django import forms
from .models import PublicKey, AipUser, TeachingClass
from Crypto.Util import number
from django.contrib.auth.admin import UserAdmin, UserChangeForm
import random

# Register your models here.
class PublicKeyForm(forms.ModelForm):
    class Meta:
        model = PublicKey
        fields = ['teaching_class', 'semester']

@admin.register(PublicKey)
class PublicKeyAdmin(admin.ModelAdmin):

    actions = ['init_pubkey', 'renew_pubkey']
    fieldsets = (
        (None, {
            "fields": (
                'teaching_class', 'semester'
            ),
        }),
        ('KeyDetails',{
            'fields':(
                'a', 'b', 'c', 'g', 'n', 'h', 'p'
            ),
            'classes':('collapse', 'wide')
        })
    )
    list_display=('__str__', 'teaching_class', 'semester')
    form = PublicKeyForm
    
    
    def init_pubkey(self, request, queryset):
        for obj in queryset:
            if obj.n == '':
                obj.init_key()
                obj.save()

    def renew_pubkey(self, requst, queryset):
        for obj in queryset:
            ret = obj.renew()
            if ret:
                ret.save()

class AipUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = AipUser

@admin.register(AipUser)
class AipUserAdmin(UserAdmin):
    form = AipUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('AipInfo', {'fields': ('teaching_class', 'is_signed')}),
        ('Permissions',
        {'fields': ('is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class PubkeyInline(admin.StackedInline):
    model = PublicKey
    fields = ['semester']
    readonly_fields = ['semester']
    extra = 0

class AIPUserInline(admin.StackedInline):
    model = AipUser
    fields = ['is_signed', 'username']
    extra = 0
    

@admin.register(TeachingClass)
class TeachingClassAdmin(admin.ModelAdmin):
    list_display = ('classno', 'school')
    inlines = [PubkeyInline, AIPUserInline]
