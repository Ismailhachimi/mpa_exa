from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from accounts.api import UserViewSet
from events.api import EventViewSet

from rest_framework.documentation import include_docs_urls

admin.autodiscover()
admin.site.site_header = 'Toteneo Administration'

router = DefaultRouter()
router.register(r'api/users', UserViewSet)
router.register(r'api/events', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/docs/', include_docs_urls(title='Toteneo API Doc')),
    path('api/auth/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls')),

    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
