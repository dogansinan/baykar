
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from baykarapp.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('baykarapp.urls'))



]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
