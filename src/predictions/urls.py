from django.conf.urls import url

from .views import (
		SearchTwitterView, 
		)


urlpatterns = [
    url(r'^$', SearchTwitterView.as_view(), name='content'),
]