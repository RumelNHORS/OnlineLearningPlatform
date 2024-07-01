from django import forms
from django.contrib.auth.models import User
from .models import Course, Lesson, Enrollment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['creator', 'slug', 'title', 'description', 'course_image']
        help_texts = {
            'title': 'Example: Python, Django, ReactJs etc.',
            'description': 'Enter a brief description of the course',
            'course_image': 'You can upload an image of the course or leave it empty'
        }
        labels = {
            'title': 'Course Title'
        }
        widgets = {
            'creator': forms.HiddenInput(),
            'slug': forms.HiddenInput()
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson 
        fields = ['slug', 'title', 'course', 'content', 'position']
        help_texts = {
            'title': 'Enter the lesson title',
            'course': 'Select the course to which this lesson belongs',
            'content': 'Enter the main content or material for this lesson. You can include text, images, videos, or any other relevant resources.',
            'position': 'Enter the lesson position or sequence number'
            
        }
        widgets = {
            'slug': forms.HiddenInput()
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['progress']

        help_texts = {
            # 'student': 'Select the student who is enrolling in the course.',
            # 'course': 'Select the course in which the student wants to enroll.',
            'progress': 'Enter the progress of the student in the course as a percentage (0-100).',
        }

