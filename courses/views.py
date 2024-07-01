import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, View, ListView, UpdateView, DeleteView
from courses.models import Course, Lesson, Enrollment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CourseForm, LessonForm, EnrollmentForm
from django.urls import reverse_lazy


class HomeView(TemplateView):
    """
    View for rendering the home page.
    - Displays all categories of courses.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Course.objects.all()
        context['categories'] = categories
        return context


class AboutView(TemplateView):
    # View for rendering the about page.
    template_name = 'about.html'


class CourseDetailView(DetailView):
    """
    View for displaying details of a specific course.
    - Retrieves the course and its associated lessons.
    """
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['lessons'] = course.lessons.all()
        return context


class LessonDetailView(View, LoginRequiredMixin):
    """
    View for displaying details of a specific lesson within a course.
    - Retrieves the lesson based on course and lesson slugs.
    """
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug, course=course)
        context = {'lesson': lesson}
        return render(request, "courses/lesson_detail.html", context)
    

class LessonListView(ListView):
    """
    View for listing all courses with their associated lessons.
    - Retrieves all courses and prefetches related lessons for efficient querying.
    """
    model = Course
    template_name = 'courses/lesson_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.prefetch_related('lessons').all()


@login_required
def create_course(request):
    """
    View for creating a new course.
    - Only accessible to users with teacher accounts.
    - Handles form submission for creating a new course.
    """
    if not request.user.profile.is_teacher:
        messages.error(request, 'Only teacher accounts can access this URL!')
        return redirect('courses:home')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.creator = request.user
            course.save()
            messages.success(request, 'Your course has been created.')
            return redirect('/courses/' + course.slug) 
    else:
        form = CourseForm(initial={'creator': request.user.id, 'slug': secrets.token_hex(nbytes=16)})
    
    context = {
        'form': form
    }
    return render(request, 'courses/create_course.html', context)


@login_required
def create_lesson(request):
    """
    View for creating a new lesson.
    - Only accessible to users with teacher accounts.
    - Handles form submission for creating a new lesson.
    """
    if not request.user.profile.is_teacher:
        messages.error(request, 'Only teacher accounts can access this URL!')
        return redirect('courses:home')
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.save()
            messages.success(request, 'Your lesson has been created.')
            return redirect('/courses/' + str(lesson.course.slug))
    else:
        form = LessonForm(initial={'slug': secrets.token_hex(nbytes=16)})
    
    context = {
        'form': form
    }
    return render(request, 'courses/create_lesson.html', context)


def course_list(request):
    """
    View for listing all courses.
    - Retrieves and displays all courses.
    """
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'courses/course_list.html', context)


@login_required
def course_edit(request, slug):
    """
    View for editing an existing course.
    - Only accessible to users with teacher accounts.
    - Handles form submission for editing a course.
    """
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('courses:course_detail', slug=course.slug)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_edit.html', {'form': form})


@login_required
def course_delete(request, slug):
    """
    View for deleting an existing course.
    - Only accessible to users with teacher accounts.
    - Deletes the specified course.
    """
    course = get_object_or_404(Course, slug=slug)
    course.delete()
    messages.success(request, 'Course deleted successfully.')
    return redirect('courses:all_courses')


@login_required
def lesson_edit(request, course_slug, lesson_slug):
    """
    View for editing an existing lesson within a course.
    - Only accessible to users with teacher accounts.
    - Handles form submission for editing a lesson.
    """
    lesson = get_object_or_404(Lesson, course__slug=course_slug, slug=lesson_slug)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lesson updated successfully.')
            return redirect('courses:course_detail', slug=course_slug)
    else:
        form = LessonForm(instance=lesson)
    
    return render(request, 'courses/lesson_edit.html', {'form': form, 'course_slug': course_slug, 'lesson_slug': lesson_slug})


@login_required
def lesson_delete(request, course_slug, lesson_slug):
    lesson = get_object_or_404(Lesson, course__slug=course_slug, slug=lesson_slug)
    
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, 'Lesson deleted successfully.')
        return redirect('courses:course_detail', slug=course_slug)
    
    return redirect('courses:lesson_detail', course_slug=course_slug, lesson_slug=lesson_slug)




@login_required
def enroll_course(request, course_slug):
    """
    View for deleting an existing lesson within a course.
    - Only accessible to users with teacher accounts.
    - Deletes the specified lesson.
    """
    course = get_object_or_404(Course, slug=course_slug)
    student = request.user

    # Check if the student is already enrolled
    enrollment_exists = Enrollment.objects.filter(student=student, course=course).exists()
    if enrollment_exists:
        messages.warning(request, f'You are already enrolled in "{course.title}" go to MY COURSES.')
        # return redirect('course_detail', course_slug=course.slug)
        return render(request, 'courses/enroll_course_detail.html')
        # return render(request, 'courses/lesson_list.html')

    if request.method == 'POST':
        print("POST request received")
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.course = course
            enrollment.save()
            messages.success(request, f'You have successfully enrolled in "{course.title}"go to MY COURSES.')
            # return redirect('course_detail', course_slug=course.slug)
            return render(request, 'courses/enroll_course_detail.html')
            # return render(request, 'courses/lesson_list.html')
        
        else:
            print("Form is not valid")
            print(form.errors)
            messages.error(request, 'Invalid form submission.')
    else:
        form = EnrollmentForm()

    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'courses/enroll_course.html', context)

# @login_required
# def course_detail(request, course_slug):
#     """
#     View for displaying detailed information about a course.
#     - Retrieves the course details.
#     - Checks if the logged-in user is enrolled in the course.
#     """
#     course = get_object_or_404(Course, slug=course_slug)
#     student = request.user
#     is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()

#     context = {
#         'course': course,
#         'is_enrolled': is_enrolled,
#     }
#     return render(request, 'courses/course_detail.html', context)
    

@login_required
def enrolled_courses(request):
    """
    View for displaying all courses in which the current user is enrolled.
    - Retrieves and displays all enrollments of the current user.
    """
    student = request.user
    enrollments = Enrollment.objects.filter(student=student)

    course_progress = {}  
    for enrollment in enrollments:
        # Assuming Enrollment model has a 'progress' field
        course_progress[enrollment.course.title] = enrollment.progress
        print('course_progress:', course_progress)

    context = {
        'enrollments': enrollments,
        'course_progress': course_progress,
    }
    return render(request, 'courses/enroll_course_detail.html', context)

