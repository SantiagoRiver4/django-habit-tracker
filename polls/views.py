from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Habit, HabitRecord, Calificacion
from .forms import HabitForm, HabitRecordForm, CalificacionForm


def index(request):
    """Lista los hábitos más recientes."""
    latest_habit_list = Habit.objects.order_by("-pub_date")
    context = {"latest_habit_list": latest_habit_list}
    return render(request, "polls/index.html", context)


def detail(request, habit_id):
    """Muestra el detalle de un hábito y sus registros."""
    habit = get_object_or_404(Habit, pk=habit_id)
    records = habit.habitrecord_set.order_by("-record_date")
    return render(request, "polls/detail.html", {"habit": habit, "records": records})


def results(request, habit_id):
    """Vista de resultados/progreso de un hábito concreto."""
    habit = get_object_or_404(Habit, pk=habit_id)
    total_registros = habit.habitrecord_set.count()
    ultimo_registro = habit.habitrecord_set.order_by("-record_date").first()
    context = {
        "habit": habit,
        "total_registros": total_registros,
        "ultimo_registro": ultimo_registro,
    }
    return render(request, "polls/results.html", context)


def add_habit(request):
    """Crea un nuevo hábito."""
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("polls:index")
    else:
        form = HabitForm()
    return render(request, "polls/add_habit.html", {"form": form})


def edit_habit(request, habit_id):
    """Edita un hábito existente usando el mismo HabitForm."""
    habit = get_object_or_404(Habit, pk=habit_id)

    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            # Después de editar, lo redirigimos al detalle del hábito
            return redirect("polls:detail", habit_id=habit.id)
    else:
        form = HabitForm(instance=habit)

    context = {
        "form": form,
        "habit": habit,
    }
    return render(request, "polls/edit_habit.html", context)


def delete_habit(request, habit_id):
    """Elimina un hábito existente (con confirmación previa)."""
    habit = get_object_or_404(Habit, pk=habit_id)

    if request.method == "POST":
        # Esto también borra los HabitRecord asociados por el on_delete=models.CASCADE
        habit.delete()
        return redirect("polls:index")

    # GET -> mostrar pantalla de confirmación
    return render(request, "polls/delete_habit.html", {"habit": habit})


def add_record(request, habit_id):
    """Crea un nuevo registro para un hábito concreto."""
    habit = get_object_or_404(Habit, pk=habit_id)
    if request.method == "POST":
        form = HabitRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.habit = habit
            # Si el modelo ya tiene auto_now_add en record_date, esta línea
            # es opcional, pero la dejamos por claridad.
            if not getattr(record, "record_date", None):
                record.record_date = timezone.now()
            record.save()
            return redirect("polls:detail", habit_id=habit.id)
    else:
        form = HabitRecordForm()

    context = {
        "form": form,
        "habit": habit,
    }
    return render(request, "polls/add_record.html", context)


def calificar(request):
    """Permite que un usuario deje una calificación y comentario sobre la app."""
    if request.method == "POST":
        form = CalificacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("polls:ver_calificaciones")
    else:
        form = CalificacionForm()
    return render(request, "polls/calificar.html", {"form": form})


def ver_calificaciones(request):
    """Lista todas las calificaciones registradas."""
    calificaciones = Calificacion.objects.all()
    return render(request, "polls/ver_calificaciones.html", {"calificaciones": calificaciones})
