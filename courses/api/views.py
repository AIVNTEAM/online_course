from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import detail_route
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models import Subject, Course, Booking, User, Student
from .serializers import SubjectSerializer, CourseSerializer, CourseWithContentSerializer
from .permissions import IsEnrolled

class SubjectListView(generics.ListAPIView):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer

# custome view for custom Request and 
# Response objects and handling APIException
class CourseEnrollView(APIView):
	
	# su dung kieu Authentication la BasicAuthentication
	# co 3 kieu Authentication la: BasicAuthentication, TokenAuthentication, SessionAuthentication
	authentication_classes = (BasicAuthentication,)
	
	# de gioi han truy cap co nhieu loai: AllowAny, IsAuthenticated, DjangoModelPermissions...
	# o day su dung IsAuthenticated co nghia la xac thuc moi dc truy cap
	permission_classes = (IsAuthenticated,)
	
	def post(self, request, pk, format=None):
		#lay doi tuong course
		course = get_object_or_404(Course, pk=pk)
		#lay doi tuong student
		student = request.user.student
		#lay doi tuong admin (mac dinh do admin quan ly thong tin dang ki)
		useradmin = get_object_or_404(User, pk=1)

		#them vao thong tin dang ky - Booking
		Booking.objects.create(course=course, student=student, user=useradmin)
		# course.students.add(request.user.student)
		return Response({'enrolled':True})

# ReadOnlyModelViewSet, which provides the read-only actions list()
# and retrieve() to both list objects or retrieve a single object
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

	# detail_route decorator of the framework to specify that this is
	# can action to be performed on a single object.
	@detail_route(methods=['post'], 
		authentication_classes=[BasicAuthentication],
		permission_classes=[IsAuthenticated])
	# Adding additional actions to view sets
	def enroll(self, request, *args, **kwargs):
		#lay doi tuong course
		# course = get_object_or_404(Course, pk=pk)
		# self.get_object() to retrieve the Course object
		course = self.get_object()
		#lay doi tuong student
		student = request.user.student
		#lay doi tuong admin (mac dinh do admin quan ly thong tin dang ki)
		useradmin = get_object_or_404(User, pk=1)

		#them vao thong tin dang ky - Booking
		Booking.objects.create(course=course, student=student, user=useradmin)
		# course.students.add(request.user.student)
		return Response({'enrolled':True})

	# detail_route decorator to specify that this action is performed on a single object
	# only the GET method is allowed for this action make sure that only users enrolled in the course are able
	# to access its contents
	# use the existing retrieve() action to return the course object
	@detail_route(methods=['get'],
						serializer_class=CourseWithContentSerializer,
						authentication_classes=[BasicAuthentication],
						permission_classes=[IsAuthenticated, IsEnrolled]
					)
	def contents(self, request, *args, **kwargs):
		#retrieve() method to get a single object
		return self.retrieve(request, *args, **kwargs)  