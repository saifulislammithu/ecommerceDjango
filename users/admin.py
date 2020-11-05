
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from users.models import NewUser

class UserAdmin(BaseUserAdmin):
    fieldsets=(
        (None,{'fields':('username','email','first_name','last_name',)}),
    ('Permission',{'fields':('is_staff','is_active')}),
    ('Personal',{'fields':('about',)}),
    
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'first_name', 'password1', 'password2'),
        }),
    )


admin.site.register(NewUser, UserAdmin)
# admin.site.unregister(Group)