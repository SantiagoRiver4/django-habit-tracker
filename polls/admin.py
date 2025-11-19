from django.contrib import admin
from .models import Habit, HabitRecord, Calificacion


# 🔧 Personalización global del sitio de administración
admin.site.site_header = "Panel de Administración - Seguimiento de Hábitos"
admin.site.site_title = "Admin Hábitos"
admin.site.index_title = "Gestión de hábitos y registros"


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("habit_text", "description", "pub_date", "updated_at", "total_records")
    search_fields = ("habit_text",)
    list_filter = ("pub_date", "updated_at")
    date_hierarchy = "updated_at"
    ordering = ("-updated_at",)
    readonly_fields = ("pub_date", "updated_at")


@admin.register(HabitRecord)
class HabitRecordAdmin(admin.ModelAdmin):
    list_display = ("habit", "record_date", "progress", "notes")
    list_filter = ("habit", "record_date", "progress")
    search_fields = ("habit__habit_text", "notes")
    date_hierarchy = "record_date"
    ordering = ("-record_date",)


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ("nombre_usuario", "calificacion", "comentario_resumido", "created_at")
    list_filter = ("calificacion", "created_at")
    search_fields = ("nombre_usuario", "comentario")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def comentario_resumido(self, obj):
        if not obj.comentario:
            return ""
        return obj.comentario if len(obj.comentario) <= 40 else obj.comentario[:37] + "..."

    comentario_resumido.short_description = "Comentario"
