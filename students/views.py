from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from braces.views import LoginRequiredMixin
from .forms import CourseEnrollForm, ModuleQuestionForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from courses.models import User, Course, Booking, Question, Module, Student


# Create your views here.
class StudentRegistrationView(CreateView):
	template_name = 'students/student/registration.html'
	# 	form_class: The form for creating objects, which has to be a ModelForm. We
	# use Django's UserCreationForm as registration form to create User objects
	form_class = UserCreationForm
	success_url = reverse_lazy('student_course_list')

	def form_valid(self, form):
		result = super(StudentRegistrationView, self).form_valid(form)
		cd = form.cleaned_data
		user = authenticate(username = cd['username'],
			password = cd['password1'])
		login(self.request, user)
		return result

#inherits from the LoginRequiredMixin so that only logged in users can
# access the view
class StudentEnrollView(LoginRequiredMixin, FormView):
	course = None	#storing the given Course object
	form_class = CourseEnrollForm

	def form_valid(self, form):
		self.course = form.cleaned_data['course'] #lay course tu form
		useradmin = get_object_or_404(User, pk=1) #mac dinh useradmin se quan ly tat ca nguoi dang ky moi
		student = self.request.user.student
		#add the current user to the students enrolled in the course.
		# self.course.students.add(self.request.user)
		#them vao bookings table
		Booking.objects.create(course=self.course, student=student, user=useradmin)
		return super(StudentEnrollView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('student_course_detail', args=[self.course.id])

class StudentCourseListView(LoginRequiredMixin, ListView):
	model = Course
	template_name = 'students/course/list.html'
	#doi tuong goi ra layout mac dinh la object_list

	def get_queryset(self):
		qs = super(StudentCourseListView, self).get_queryset()
		return qs.filter(students__in=[self.request.user.student])

#Vua cho SV xem chi tiet tung module
#vua cho SV dat cau hoi - co su dung form luu vo DB -> CreateView
class StudentCourseDetailView(CreateView, DetailView):
	#cho phan DetailView
	model = Course
	template_name = 'students/course/detail.html'
	#cho phan CreateView
	form_class = ModuleQuestionForm
	success_url = reverse_lazy('student_course_list')
	
	def get_queryset(self):
		qs = super(StudentCourseDetailView, self).get_queryset()
		return qs.filter(students__in=[self.request.user.student])

	# override the get_context_data() method to set a course module 
	# in the context if the module_id URL parameter is given. 
	# Otherwise, we set the first  module of the course. This way, 
	# students will be able to navigate through modules inside a course.
	def get_context_data(self, **kwargs):
		context = super(StudentCourseDetailView, self).get_context_data(**kwargs)
		
		#get course object
		course = self.get_object()
		if 'module_id' in self.kwargs:
			#get current module
			context['module'] = course.modules.get(
				id=self.kwargs['module_id'])
			# context['dscauhoi'] = Question.objects.get()
		else:
			#get first module
			context['module'] = course.modules.all()[0]

		# lay danh sach cac cau hoi thuoc module
		# context['dscauhoi'] = Question.objects.get(lesson=context['module'])
		#them form StudentQuestion vao detail de hoc vien dat cau hoi
		# context['form'] = StudentQuestion()
		# context['form'] = self.get_form()
		#test thu noi dung de dua ra template
		# context['cauhoi'] = "BUI CONG THANH HOI TRA LOI"
		return context

	# def post(self, request, *args, **kwargs):
	# 	if self.form.is_valid():
	# 		model_instance = self.form.save(commit=False)
	# 		#muon luu gi khac thi thiet lap tai day
	# 		# model_instance.timestamp = timezone.now()
	# 		model_instance.save()
	#doi voi phan form - truoc khi luu du lieu can them thong tin
	def form_valid(self, form):
		model_instance = form.save(commit=False)
		
		#lay bai hoc dua vao id bai hoc tren duong dan
		# model_instance.lesson = Module.objects.get(pk=1)
		if 'module_id' in self.kwargs:
			model_instance.lesson = Module.objects.get(pk=self.kwargs['module_id'])
		else:
			model_instance.lesson = Module.objects.all()[0]
		model_instance.student = self.request.user.student

		model_instance.save()

		return super(StudentCourseDetailView, self).form_valid(form)

		# return FormView.post(self, request, *args, **kwargs)

# class StudentQuestion(FormView):
	# template_name='students\student\testform.html'
	# def get_queryset()
	# model = Question
	# form_class = ModuleQuestionForm
	# success_url = reverse_lazy('student_course_list')  #test only
