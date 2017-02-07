from django.http import HttpRequest
from django.shortcuts import render, redirect

from course_management_app.forms import CourseForm


# Create your views here.
def new_course(request: HttpRequest):
    if request.method == 'POST':
        print(request.POST)
        form = CourseForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'new_course.html', {'form': form})

        course = form.save()

        return redirect(f'/course/{course.name}')
    return render(request, 'new_course.html', {'form': CourseForm()})
