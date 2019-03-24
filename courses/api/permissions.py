from rest_framework.permissions import BasePermission
from ..models import Booking

# custom permissions: tao cac quyen trong file nay
class IsEnrolled(BasePermission):
	# has_permission(): View-level permission check
	# has_object_permission(): Instance-level permission check
	def has_object_permission(self, request, view, obj):
		#neu trong Booking co' course tuong ung voi student id thi co quyen
		#obj day la doi tuong cua class Course
		#kiem tra xong trong Booking co: course = obj va student = student trong request ko?
		return Booking.objects.filter(course=obj, student=request.user.student).exists()