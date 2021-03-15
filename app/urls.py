from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from app import settings

schema_view = get_swagger_view(title="Store API")
statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
statics += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doc', schema_view),
    path('api/', include(('store.urls', 'store'), namespace='store'))
] + statics

