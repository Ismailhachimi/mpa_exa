from django.contrib import admin
from events.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ("client", "expert", "start", "end",)

    class Meta:
        model = Event


admin.site.register(Event, EventAdmin)
