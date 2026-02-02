from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import QuestionPaper, Question, Result

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')
    return render(request, 'test_app/home.html')

def student_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'test_app/signup.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'test_app/login.html', {'form': form})

@login_required
def student_dashboard(request):
    papers = QuestionPaper.objects.all().order_by('-created_at')
    return render(request, 'test_app/dashboard.html', {'papers': papers})

@login_required
def take_test(request, paper_id):
    paper = get_object_or_404(QuestionPaper, id=paper_id)
    questions = paper.questions.all()
    if not questions:
        return render(request, 'test_app/test.html', {'error': 'No questions available in this paper.'})
    return render(request, 'test_app/test.html', {'paper': paper, 'questions': questions})

@login_required
def submit_test(request, paper_id):
    if request.method == 'POST':
        paper = get_object_or_404(QuestionPaper, id=paper_id)
        questions = paper.questions.all()
        score = 0
        total = 0
        for q in questions:
            total += q.marks
            selected_option = request.POST.get(f'question_{q.id}')
            if selected_option == q.answer:
                score += q.marks
        
        Result.objects.create(student=request.user, paper=paper, marks=score, total_marks=total)
        return render(request, 'test_app/result_detail.html', {'paper': paper, 'score': score, 'total': total})
    return redirect('student_dashboard')

@login_required
def view_results(request):
    results = Result.objects.filter(student=request.user).order_by('-date')
    return render(request, 'test_app/results_list.html', {'results': results})

def logout_view(request):
    logout(request)
    return redirect('home')

# Admin Portal Views

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                return render(request, 'test_app/admin_login.html', {'form': form, 'error': 'Only admins can access this portal.'})
    else:
        form = AuthenticationForm()
    return render(request, 'test_app/admin_login.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    total_students = User.objects.filter(is_staff=False).count()
    papers = QuestionPaper.objects.all().order_by('-created_at')
    return render(request, 'test_app/admin_dashboard.html', {
        'total_students': total_students,
        'papers': papers
    })

@login_required
def create_paper(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        QuestionPaper.objects.create(title=title, description=description)
        return redirect('admin_dashboard')
    return render(request, 'test_app/create_paper.html')

@login_required
def view_paper_admin(request, paper_id):
    if not request.user.is_staff:
        return redirect('home')
    paper = get_object_or_404(QuestionPaper, id=paper_id)
    questions = paper.questions.all()
    return render(request, 'test_app/view_paper_admin.html', {
        'paper': paper,
        'questions': questions
    })

@login_required
def add_question(request, paper_id):
    if not request.user.is_staff:
        return redirect('home')
    paper = get_object_or_404(QuestionPaper, id=paper_id)
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        answer = request.POST.get('answer')
        marks = request.POST.get('marks')
        
        Question.objects.create(
            paper=paper,
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            answer=answer,
            marks=int(marks) if marks else 0
        )
        return redirect('view_paper_admin', paper_id=paper.id)
    return render(request, 'test_app/add_question.html', {'paper': paper})

@login_required
def admin_view_results(request):
    if not request.user.is_staff:
        return redirect('home')
    results = Result.objects.all().order_by('-date')
    return render(request, 'test_app/admin_results.html', {'results': results})
