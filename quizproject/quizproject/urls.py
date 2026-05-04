from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Custom admin URLs must come BEFORE django.contrib.admin to take precedence
    path('admin/quiz/', include('quizapp.admin_urls')),
    path('admin/', admin.site.urls),
    path('', include('quizapp.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

