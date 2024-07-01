from django.contrib import admin
from courses.models import Course, Lesson, Enrollment

# Register your models here.

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Enrollment)

