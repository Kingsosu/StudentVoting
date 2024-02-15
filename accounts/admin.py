from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account

# Register the Account model
class AccountAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'is_student', 'is_candidate', 'is_staff', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'password', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)

