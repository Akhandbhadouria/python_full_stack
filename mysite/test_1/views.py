from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required

# Create your views here.

from test_1.models import Student
def home(request):
    content={
     'stud':Student.objects.all()
}
    return render(request,'home.html',content)


@login_required
def st_details(request,pk):
    sd=get_object_or_404(Student,pk=pk)
   
    return render(request,'st_detail.html',{'sd':sd})