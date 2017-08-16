from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.


class SalaryInline(admin.StackedInline):
    model = Salary
    can_delete = False


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'join_time', 'category', 'country', 'city', 'street', 'update_time')
    inlines = (SalaryInline,)

admin.site.register(Company, CompanyAdmin)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserExtendInline(admin.StackedInline):
    model = UserExtend
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserExtendInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class SalaryAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_extend', 'company', 'title', 'monthly_pay', 'update_time')

admin.site.register(Salary, SalaryAdmin)


class UserExtendAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = (SalaryInline,)

admin.site.register(UserExtend, UserExtendAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('salary', 'user_extend', 'message', 'created_time')

admin.site.register(Comment, CommentAdmin)
