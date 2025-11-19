from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # 👉 Cuando entren a la raíz "/", los mandamos al index de hábitos
    path("", RedirectView.as_view(pattern_name="polls:index", permanent=False)),

    # Rutas de la app de hábitos
    path("polls/", include("polls.urls")),

    # Admin de Django
    path("admin/", admin.site.urls),
]
