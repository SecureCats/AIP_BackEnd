from django.urls import path, include
from . import views

urlpatterns = [
    path('api/', include([
        path('v1/', include([
            path('pubkey/<str:semester>/<str:classno>', views.pubkey_query),
            path('sign', views.sign),
            path('info',views.userinfo)
        ]))
    ])),
    path('', views.frontend),
    path('home', views.frontend),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('', views.index, name='index'),
]
