from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/users/', include('apps.users.urls')),
    path('api/', include('apps.cities.urls')),
]

urlpatterns += (
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
)

if settings.DEBUG:
    from debug_toolbar import urls
    from django.conf.urls.static import static

    urlpatterns += (
        path(route="__debug__/", view=include(arg=urls)),
    )
    urlpatterns += tuple(static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns += tuple(static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
