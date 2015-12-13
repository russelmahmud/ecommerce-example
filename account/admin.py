# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
#
# from my_user_profile_app.models import Employee
#
# # Define an inline admin descriptor for Employee model
# # which acts a bit like a singleton
# class EmployeeInline(admin.StackedInline):
#     model = Employee
#     can_delete = False
#     verbose_name_plural = 'employee'
#
# # Define a new User admin
# class UserAdmin(UserAdmin):
#     inlines = (EmployeeInline, )
#
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)