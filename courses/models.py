from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Course(models.Model):
    """
    Model representing a course.

    Attributes:
        creator (ForeignKey): Reference to the User who created the course.
        slug (SlugField): URL-friendly identifier for the course.
        title (CharField): Title of the course.
        description (TextField): Description of the course.
        created_at (DateTimeField): Date and time when the course was created.
        course_image (ImageField): Image associated with the course.
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now=True)
    course_image = models.ImageField(upload_to='course_images', default='default.jpg')

    def __str__(self):
        # String representation of the course, shown as its title.
        return self.title

    def get_absolute_url(self):
        # Returns the absolute URL to view the course detail.
        return reverse("courses:course_detail", kwargs={"slug": self.slug})


class Lesson(models.Model):
    """
    Model representing a lesson within a course.

    Attributes:
        slug (SlugField): URL-friendly identifier for the lesson.
        title (CharField): Title of the lesson.
        content (TextField): Content of the lesson.
        course (ForeignKey): Reference to the Course that the lesson belongs to.
        position (PositiveIntegerField): Order of the lesson within the course.
    """
    slug = models.SlugField()
    title = models.CharField(max_length=250)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    position = models.PositiveIntegerField()

    def __str__(self):
        # String representation of the lesson, shown as its title.
        return self.title

    def get_absolute_url(self):
        # Returns the absolute URL to view the lesson detail.
        return reverse("courses:lesson_detail", kwargs={"course_slug": self.course.slug, 'lesson_slug': self.slug})
    

class Enrollment(models.Model):
    """
    Model representing a student's enrollment in a course.

    Attributes:
        slug (SlugField): URL-friendly identifier for the enrollment.
        student (ForeignKey): Reference to the User who is enrolled.
        course (ForeignKey): Reference to the Course that the user is enrolled in.
        progress (IntegerField): Tracks the user's progress in the course as a percentage.
    """
    slug = models.SlugField()
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # To track progress as a percentage
    progress = models.IntegerField(default=0)

    class Meta:
        # Meta class to specify unique constraint on student and course together.
        unique_together = ('student', 'course')

    def __str__(self):
        # String representation of the enrollment, showing the student's username and the course title.
        return f"{self.student.username} enrolled in {self.course.title}"

    