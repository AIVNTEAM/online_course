from django import forms
from courses.models import Course, Question

#form for students to enroll in courses
#form nay chi chua 1 truong ẩn luu thong tin course 
# The course field is
# for the course in which the user gets enrolled
class CourseEnrollForm(forms.Form):
	course = forms.ModelChoiceField(queryset=Course.objects.all(),
		widget=forms.HiddenInput)

class ModuleQuestionForm(forms.ModelForm):
	# question = forms.TextField(required=True)
	# title = models.CharField(max_length=100)
	# text = models.CharField(max_length=255)
	# notes = models.CharField(max_length=255)
	class Meta:
		model = Question
		fields = ['question', 'status', ]
