from django.contrib import admin
from .models import Category, Product, Order, OrderItem, ProductImage, Brand, ColorOption
@admin.register(ColorOption)
class ColorOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'price', 'category', 'created_at', 'featured_in_hero', 'color_names')
    list_editable = ('featured_in_hero',)
    inlines = [ProductImageInline]
    filter_horizontal = ('colors',)

    def color_names(self, obj):
        return ", ".join([color.name for color in obj.colors.all()])
    color_names.short_description = "Culori disponibile"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shipping_address', 'created_at', 'paid')
    inlines = [OrderItemInline]
