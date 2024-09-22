from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Listing


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_buyer','is_seller', 'is_superuser', 'is_staff']  # Add any fields you want to display in the admin list view


from django.contrib import admin
from .models import Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'seller')
    list_filter = ('is_published', 'list_date')
    search_fields = ('title', 'description', 'address', 'city', 'state', 'zip_code', 'price')
    # Exclude or remove 'category_name' if it is not in the model
    # fields = ['title', 'description', 'address', 'city', 'state', 'zip_code', 'price', 'bedrooms', 'bathrooms', 'square_feet', 'year_built', 'photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6', 'is_published']

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                'title', 'description', 'address', 'city', 'state', 'zip_code', 'price', 'bedrooms',
                'bathrooms', 'square_feet', 'year_built', 'photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4',
                'photo_5', 'photo_6', 'is_published')
            }),
            ('Seller', {
                'fields': ('seller',),
            }),
        )
        return fieldsets

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'seller':
            user = get_user_model()
            if request.user.is_superuser:
                kwargs['queryset'] = user.objects.filter(is_seller=True)
            else:
                kwargs['queryset'] = user.objects.filter(id=request.user.id, is_seller=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at')
    search_fields = ('name', 'email')

admin.site.register(Listing, ListingAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
