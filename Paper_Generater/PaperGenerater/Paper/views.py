# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import GradeSelectionForm, SubjectSelectionForm, ChapterSelectionForm
from .models import *
from xhtml2pdf import pisa

def select_grade(request):
    if request.method == "POST":
        form = GradeSelectionForm(request.POST)
        if form.is_valid():
            # Store the selected grade in the session
            selected_grade = form.cleaned_data['grade']
            request.session['selected_grade'] = selected_grade.id
            return redirect('select_subject')  # Step 2: Subject selection
    else:
        form = GradeSelectionForm()

    return render(request, 'paper/select_grade.html', {'form': form})

def select_subject(request):
    if 'selected_grade' not in request.session:
        return redirect('select_grade')  # Ensure the user has selected a grade first

    selected_grade = Grade.objects.get(id=request.session['selected_grade'])

    if request.method == "POST":
        form = SubjectSelectionForm(request.POST, grade=selected_grade)
        if form.is_valid():
            # Store the selected subject in the session
            selected_subject = form.cleaned_data['subject']
            request.session['selected_subject'] = selected_subject.id
            return redirect('select_chapter')  # Step 3: Generate the paper
    else:
        form = SubjectSelectionForm(grade=selected_grade)

    return render(request, 'paper/select_subject.html', {'form': form, 'grade': selected_grade})

def select_chapter(request):
    if 'selected_subject' not in request.session:
        return redirect('select_subject')  # Ensure the user has selected a grade first

    selected_subject = Subject.objects.get(id=request.session['selected_subject'])

    if request.method == "POST":
        form = ChapterSelectionForm(request.POST, subject=selected_subject)
        if form.is_valid():
            # Store the selected subject in the session
            selected_chapter = form.cleaned_data['chapter']
            request.session['selected_chapter'] = selected_chapter.id
            return redirect('generate_paper')  # Step 3: Generate the paper
    else:
        form = ChapterSelectionForm(subject=selected_subject)

    return render(request, 'paper/select_chapter.html', {'form': form, 'subject': selected_subject})

from django.utils import timezone

def generate_paper(request):
    if 'selected_chapter' not in request.session:
        return redirect('select_chapter')
    
    selected_chapter = Chapter.objects.get(id=request.session['selected_chapter'])
    
    # Get only 10 short questions and 5 long questions for the selected chapter
    shortquestions = shortQuestion.objects.filter(chapter=selected_chapter)[:10]
    longquestions = LongQuestion.objects.filter(chapter=selected_chapter)[:5]
    mcqs = MCQ.objects.filter(chapter=selected_chapter)[:15]

    current_date = timezone.now()

    if request.GET.get('download_pdf'):
        # Render the HTML content to a string
        html_content = render(request, 'paper/generate_paper.html', {
            'chapter': selected_chapter,
            'shortquestions': shortquestions,
            'longquestions': longquestions,
            'mcqs': mcqs,
            'current_date': current_date
        }).content.decode('utf-8')

        # PDF generation code
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{selected_chapter.name}_questions.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors while generating your PDF', status=500)

        return response

    return render(request, 'paper/generate_paper.html', {
        'chapter': selected_chapter,
        'shortquestions': shortquestions,
        'longquestions': longquestions,
        'mcqs': mcqs,
        'current_date': current_date
    })