from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add_habit, name="add_habit"),

    path("<int:habit_id>/edit/", views.edit_habit, name="edit_habit"),
    path("<int:habit_id>/delete/", views.delete_habit, name="delete_habit"),

    path("<int:habit_id>/", views.detail, name="detail"),
    path("<int:habit_id>/results/", views.results, name="results"),
    path("<int:habit_id>/add/", views.add_record, name="add_record"),

    # Calificaciones
    path("calificar/", views.calificar, name="calificar"),
    path("ver_calificaciones/", views.ver_calificaciones, name="ver_calificaciones"),
]
