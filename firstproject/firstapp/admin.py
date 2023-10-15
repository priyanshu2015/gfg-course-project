from django.contrib import admin
from .models import Account
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


User = get_user_model()

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ('amount', 'currency', 'extra')
    list_filter = ('currency',)
    search_fields = ('amount',)
    # fields = ('amount', 'currency')
    fieldsets = (
        (None, {'fields': ("amount",)}),
        ('Extra Info', {'fields': ("currency", "user")})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('amount', 'currency')
        }
        )
    )

    def extra(self, obj):
        return obj.id
    

class AccountInline(admin.TabularInline):
    model = Account
    

class CustomerUserAdmin(UserAdmin):
    inlines = [
        AccountInline
    ]


admin.site.register(Account, AccountAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomerUserAdmin)
