from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Habit, HabitRecord


def create_habit(habit_text="Hábito de prueba", days_offset=0):
    """
    Crea y retorna un hábito con el texto dado.

    days_offset permite ajustar la fecha de creación relativa a ahora,
    similar a create_question en el tutorial oficial.
    """
    pub_date = timezone.now() + timedelta(days=days_offset)
    return Habit.objects.create(
        habit_text=habit_text,
        description="Descripción de prueba",
        pub_date=pub_date,
    )


class HabitModelTests(TestCase):
    def test_total_records_returns_zero_if_no_records(self):
        """total_records() debe devolver 0 cuando no hay registros."""
        habit = create_habit("Hábito sin registros")
        self.assertEqual(habit.total_records(), 0)

    def test_total_records_counts_all_associated_records(self):
        """total_records() debe contar correctamente los HabitRecord."""
        habit = create_habit("Hábito con registros")
        HabitRecord.objects.create(habit=habit, notes="Primer registro", progress=80)
        HabitRecord.objects.create(habit=habit, notes="Segundo registro", progress=100)
        self.assertEqual(habit.total_records(), 2)


class HabitIndexViewTests(TestCase):
    def test_no_habits(self):
        """Si no hay hábitos, index muestra mensaje y lista vacía."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay hábitos registrados todavía")
        self.assertQuerySetEqual(response.context["latest_habit_list"], [])

    def test_one_habit_is_displayed(self):
        """Si hay un hábito, debe aparecer en la vista index."""
        habit = create_habit("Beber agua")
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_habit_list"],
            [habit],
        )
        self.assertContains(response, "Beber agua")

    def test_multiple_habits_are_displayed_ordered_by_pub_date_desc(self):
        """La vista index debe ordenar descendentemente por pub_date."""
        old_habit = create_habit("Hábito antiguo", days_offset=-2)
        new_habit = create_habit("Hábito reciente", days_offset=0)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_habit_list"],
            [new_habit, old_habit],
        )


class HabitDetailViewTests(TestCase):
    def test_detail_view_non_existing_habit_returns_404(self):
        """Si el hábito no existe, detail debe devolver 404."""
        url = reverse("polls:detail", args=(9999,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_existing_habit(self):
        """Detail debe mostrar información del hábito existente."""
        habit = create_habit("Leer 15 minutos")
        url = reverse("polls:detail", args=(habit.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Leer 15 minutos")
        self.assertEqual(response.context["habit"], habit)
