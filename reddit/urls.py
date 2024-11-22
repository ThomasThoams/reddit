# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('posts/', include('posts.urls')),
    path('communities/', include('communities.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
