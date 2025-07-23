from django.contrib import admin
from .models import Category, Product, ProductImage, Discount, Comment


admin.site.register(Comment)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "description")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title", )}


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "description", "price", "stock_status", "quantity", "category")
    search_fields = ("title", "slug", "price", "category")
    prepopulated_fields = {"slug": ("title", )}
    fields = ["id", "title", "slug", "description", "price", "quantity", "stock_status", "category", "discount", "author", "created", "updated"]
    readonly_fields = ["id", "author", "created", "updated"]
    list_filter = ["created", "updated", "stock_status", "category"]
    inlines = [ProductImageAdmin]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "percent", "deadline")
