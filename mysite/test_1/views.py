from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import StudentForm
from .models import Student

def home(request):
    content = {
        'stud': Student.objects.all()
    }
    return render(request, 'home.html', content)

@login_required
def st_details(request, pk):
    sd = get_object_or_404(Student, pk=pk)
    return render(request, 'st_detail.html', {'sd': sd})

@login_required
def data_input(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm()
    return render(request, 'insert.html', {'form': form})
    