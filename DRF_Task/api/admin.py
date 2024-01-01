from api.models import Book, CustomUser, Favourite
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("id", "name", "email", "is_author", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        ("User credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_author", "is_admin", "is_active")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "is_author",
                    "password",
                    "password2",
                ),
            },
        ),
    ]
    search_fields = ("email",)
    ordering = ("email", "id")
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)

admin.site.register(Favourite)


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "description",
        "cover_img",
        "author",
        "in_stock",
    ]


# admin.site.register(CustomUser)
