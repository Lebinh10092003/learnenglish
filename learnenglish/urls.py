from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('chat_ai/', include('chat_ai.urls')),
    #path('grammar/', include('grammar.urls')),
    path('vocabulary/', include('vocabulary.urls')),
    path('user/', include('user.urls')),
    #path('review/', include('review.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

