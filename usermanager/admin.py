from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from usermanager.forms import MallocUserCreateForm, MallocChangeForm
from usermanager.models import MallocBaseUser

admin.site.unregister(Group)


# class MallocUserAdmin(UserAdmin):
#     add_form = MallocUserCreateForm
#     form = MallocChangeForm
#     model = MallocBaseUser
#     list_display = ('login', 'is_staff', 'is_activate')
#     list_filter = ('login',)
#     fieldsets = (
#         (None, {'fields': ('login', 'email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)


admin.site.register(MallocBaseUser)