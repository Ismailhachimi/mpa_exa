from django.contrib import admin

from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "joined_at", "user_groups")

    def user_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    class Meta:
        model = User


admin.site.register(User, UserAdmin)
