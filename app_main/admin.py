from django.contrib import admin
from .models import Role, User, BigCategory, Category, Doc
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Ko‘rinadigan ustunlar
    list_display = ("id", "full_name", "phone", "role", "create_at", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("full_name", "phone")
    readonly_fields = ("create_at",)

    # User ko‘rinishidagi maydonlar
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Shaxsiy ma'lumotlar", {"fields": ("full_name", "role")}),
        ("Ruxsatlar", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Sanalar", {"fields": ("create_at",)}),
    )

    # Yangi user qo‘shish formasi
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "full_name", "role", "password1", "password2"),
        }),
    )

    ordering = ("id",)

@admin.register(BigCategory)
class BigCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "big_category", "ichki_raqam", "tartib_raqami")
    list_filter = ("big_category",)
    search_fields = ("ichki_raqam", "izoh")
    ordering = ("tartib_raqami",)


@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category")
    list_filter = ("category",)
    search_fields = ("title",)
