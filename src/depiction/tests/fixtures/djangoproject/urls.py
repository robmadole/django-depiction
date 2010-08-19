from django.conf.urls.defaults import *

from depiction.tests.fixtures.djangoproject import views

urlpatterns = patterns('',
    # Example:
    # (r'^djangoproject/', include('djangoproject.foo.urls')),
    (r'^test/middleware$', views.dummy_view),
)
