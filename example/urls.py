import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    ('^admin/', include(admin.site.urls)),
    (r'^myapp/', include('myapp.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(
            regex=r'^media/(?P<path>.*)$',
            view='django.views.static.serve',
            kwargs={'document_root': os.path.join(os.path.dirname(__file__),
                    "media")},
        )
    )
