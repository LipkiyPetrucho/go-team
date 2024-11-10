from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView

from user.views import home_view

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        "accounts/register/",
        CreateView.as_view(
            template_name="registration/register.html",
            form_class=UserCreationForm,
            success_url="/",
        ),
        name="register",
    ),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("api/", include("user.api.urls")),  # подключение маршрутов API
    path("", home_view, name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
