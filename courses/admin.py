from django.contrib import admin
from .models import Subject, Course, Module, Booking

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug']
	prepopulated_fields = {'slug': ('title',)}

class ModuleInline(admin.StackedInline):
	model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	#chi can dua thuoc tinh chua khoa ngoai - doi tuong se hien thi
	# khi doi tuong do co ham __str__ roi: vd o day thuoc tinh owner
	# tro den User -> hien thi ten thay vi id
	list_display = ['title', 'subject', 'created', 'is_active', 'owner']
	list_filter = ['created', 'subject', 'is_active']
	search_fields = ['title', 'overview']
	prepopulated_fields = {'slug': ('title',)}
	inlines = [ModuleInline]
	list_editable = ['is_active', ]
	ordering = ['is_active', 'created']
	
	#ham nay nham cap nhat model khi save
	def save_model(self, request, obj, form, change):
		obj.approved = request.user
		super().save_model(request, obj, form, change)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	#chi can dua thuoc tinh chua khoa ngoai - doi tuong se hien thi
	# khi doi tuong do co ham __str__ roi: vd o day thuoc tinh owner
	# tro den User -> hien thi ten thay vi id	
	list_display = ['course', 'student', 'created', 'is_active', 'payment_status', 'message']
	list_filter = ['created', 'payment_status', 'is_active']
	search_fields = ['student', ]
	list_editable = ['is_active', 'message', 'payment_status']
	ordering = ['is_active', 'created']
	

