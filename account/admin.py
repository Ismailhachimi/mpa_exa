from django.contrib import admin
from account.models import User


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User

    list_display = ("email", "joined_at", )

admin.site.register(User, UserAdmin)
