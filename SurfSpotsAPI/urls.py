from django.conf.urls import url,include

from .views.UserViews import *
from .views.SpotViews import *
from .views.ReviewViews import *

urlpatterns = [
    url(r'^users/$', UserBasic.as_view()),
    url(r'^spots/$', SpotBasic.as_view()),
    url(r'^users/(?P<pk>[a-zA-Z0-9-]+)/$', UserDetail.as_view()),
    url(r'^users/username/(?P<username>[a-zA-Z0-9-]+)/$', UserByName.as_view()),
    url(r'^reviews/forSpot/(?P<spk>[a-zA-Z0-9-]+)/$', ReviewBasic.as_view()),
]
