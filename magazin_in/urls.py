
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from magazin_in import settings
from store import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
