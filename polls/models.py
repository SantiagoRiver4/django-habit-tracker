from django.db import models


class Habit(models.Model):
    habit_text = models.CharField(max_length=200, verbose_name="Nombre del hábito")
    description = models.TextField(blank=True, verbose_name="Descripción")
    pub_date = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de modificación", auto_now=True)

    def __str__(self):
        return self.habit_text

    def total_records(self):
        return self.habitrecord_set.count()


class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    record_date = models.DateTimeField("Fecha y hora del registro", auto_now_add=True)
    notes = models.CharField("Notas", max_length=255, blank=True)
    progress = models.IntegerField("Progreso (0-100)", default=100)

    def __str__(self):
        return f"{self.habit.habit_text} - {self.record_date.strftime('%Y-%m-%d')}"


class Calificacion(models.Model):
    nombre_usuario = models.CharField("Nombre de usuario", max_length=100)
    calificacion = models.IntegerField(
        "Calificación",
        choices=[(i, f"{i} estrella{'s' if i > 1 else ''}") for i in range(1, 6)]
    )
    # 🔽 comentario opcional
    comentario = models.TextField("Comentario", blank=True, null=True)
    created_at = models.DateTimeField("Fecha", auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre_usuario} - {self.calificacion} ⭐"
