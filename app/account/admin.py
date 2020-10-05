from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy

from app.account.models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("uuid", "password",)}),
        (
            gettext_lazy("Personal info"),
            {"fields": ("email", "first_name", "last_name")},
        ),
        (
            gettext_lazy("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            gettext_lazy("Important dates"),
            {"fields": ("last_login", "date_joined", "updated")},
        ),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    readonly_fields = ("uuid", "updated")
