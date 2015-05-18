from django.conf.urls.defaults import *

urlpatterns = patterns('myapp.views',
    url(
        regex=r'^$',
        view='my_view',
        name='my_view',
    ),
)
