from django.contrib import admin
from .models import Product, Variation, ReviewRating
from django.utils.text import slugify

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    actions = ['duplicate_product']

    def duplicate_product(self, request, queryset):
        for obj in queryset:
            obj.pk = None  # This tells Django to create a new object
            obj.product_name = f"{obj.product_name} (Copy)"  # Optional: modify name
            # Generate a unique slug
            base_slug = slugify(obj.product_name)
            unique_slug = f"{base_slug}"
            obj.slug = unique_slug # Clear slug so it can be auto-generated if using slugify
            obj.save()
        self.message_user(request, "Selected products were duplicated successfully.")
    
    duplicate_product.short_description = "Duplicate selected products"


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
