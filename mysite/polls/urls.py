from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'info/.*', views.display_info, name='information'),
        url(r'suggest/.*', views.index, name='search'),    
]
