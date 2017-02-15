from django.http import HttpRequest
from django.shortcuts import render, redirect

from course_management_app.forms import CourseForm, LectureForm
from course_management_app.models import Course, Lecture
from accounts.decorators import teacher_required


def index(request: HttpRequest):
    courses = []
    for course in Course.objects.all():
        course.duration = (course.end_date - course.start_date)

        courses.append(course)

    return render(request, 'index.html', {'courses': courses})


# Create your views here.
@teacher_required(redirect_url='/')
def new_course(request: HttpRequest):
    if request.method == 'POST':
        form = CourseForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'new_course.html', {'form': form})

        course = form.save()
        return redirect(f'/course/{course.id}')
    return render(request, 'new_course.html', {'form': CourseForm()})


@teacher_required(redirect_url='/')
def new_lecture(request: HttpRequest):
    if request.method == 'POST':
        form = LectureForm(data=request.POST)

        if not form.is_valid():
            print(form.errors)
            return render(request, 'new_lecture.html', {'form': form})

        lecture = form.save()
        return redirect(f'/lecture/{lecture.id}')

    return render(request, 'new_lecture.html', {'form': LectureForm()})


@teacher_required(redirect_url='/')
def edit_lecture(request: HttpRequest, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)

    if lecture is None:
        return redirect('/')

    if request.method == 'POST':
        form = LectureForm(data=request.POST, instance=lecture)

        if not form.is_valid():
            return render(request, 'edit_lecture.html', {'form': form, 'lecture': lecture})

        form.save()
        return redirect(lecture)

    return render(request, 'edit_lecture.html', {'form': LectureForm(instance=lecture), 'lecture': lecture})


def view_lecture(request: HttpRequest, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)

    if lecture is None:
        return redirect('/')

    return render(request, 'lecture.html', {'lecture': lecture})


def view_course(request: HttpRequest, course_name):
    course = Course.objects.filter(name=course_name).first()

    if course is None:
        return redirect('/')

    return render(request, 'course.html', {'course': course})


@teacher_required(redirect_url='/')
def edit_course(request: HttpRequest, course_name):
    course = Course.objects.filter(name=course_name).first()

    if course is None:
        return redirect('/')

    if request.method == 'POST':
        form = CourseForm(data=request.POST, instance=course)

        if not form.is_valid():
            return render(request, 'edit_course.html', {'form': form, 'course': course})

        form.save()
        return redirect(course)

    return render(request, 'edit_course.html', {'form': CourseForm(instance=course), 'course': course})


def redirect_404(request: HttpRequest):
    """ Handler for all URLs that are not mapped """
    return redirect('/')
