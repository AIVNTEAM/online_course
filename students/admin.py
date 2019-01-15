from django.contrib import admin
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.admin import UserAdmin as UA2
from courses.models import User as CUser
from courses.models import Student, Teacher

# Register your models here.

class UserAdmin(admin.ModelAdmin):
	#cac fields su dung cho form add / edit
	fields = ['username', 'first_name', 'last_name', 'email', 'is_teacher', 'is_student', 'is_active']
	list_display = ('username', 'first_name', 'last_name', 'email', 'is_teacher', 'is_student', 'is_active')
	list_filter = ('is_active', 'date_joined', 'is_teacher', 'is_student')
	ordering = ['first_name', 'last_name', 'email', 'is_active', 'is_teacher', 'is_student']
	search_fields = ('user', 'email')
	list_editable = ['is_active', ]
admin.site.register(CUser, UserAdmin)

# below lines should be added
# admin.site.unregister(User)
admin.site.register(AuthUser, UA2)