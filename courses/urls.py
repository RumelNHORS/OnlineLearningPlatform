from django.urls import path
from django.contrib.auth.decorators import login_required

from courses.views import HomeView, AboutView, CourseDetailView, LessonDetailView, create_course, create_lesson, course_list, course_edit, course_delete, LessonListView, lesson_edit, lesson_delete, enroll_course, enrolled_courses

# from courses import views


app_name = 'courses'


urlpatterns = [
    # Home page view
    path('', HomeView.as_view(), name='home'),
    # About page view
    path('about/', AboutView.as_view(), name='about'),
    # View to create a course
    path('create/course/', create_course, name='create_course'),
     # View to create a lesson
    path('create/lesson/', create_lesson, name='create_lesson'),
    # View to list all courses
    path('all_course_list/', course_list, name='all_courses'),
    # View to list all lessons
    path('lessons/', LessonListView.as_view(), name='lesson_list'),
    # View to edit a course, login required
    path('courses/<slug:slug>/edit/', login_required(course_edit), name='course_edit'),
    # View to delete a course, login required
    path('courses/<slug:slug>/delete/', login_required(course_delete), name='course_delete'),
    # Detailed view of a course, login required
    path('courses/<slug:slug>/', login_required(CourseDetailView.as_view()), name='course_detail'),
    # Detailed view of a lesson, login required
    path('courses/<slug:course_slug>/<slug:lesson_slug>/', login_required(LessonDetailView.as_view()), name='lesson_detail'),
    # View to edit a lesson
    path('courses/<slug:course_slug>/<slug:lesson_slug>/edit/', lesson_edit, name='lesson_edit'),
    # View to delete a lesson
    path('courses/<slug:course_slug>/<slug:lesson_slug>/delete/', lesson_delete, name='lesson_delete'),
    # View to enroll in a course
    path('enroll_course/<slug:course_slug>/', enroll_course, name='enroll_course'),
    # path('course/<slug:course_slug>/', course_detail, name='course_detail'),
    # View to list enrolled courses
    path('my-courses/', enrolled_courses, name='enrolled_courses'),


]
