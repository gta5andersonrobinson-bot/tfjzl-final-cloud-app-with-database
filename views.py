from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Submission

def submit(request, course_id):
    # submit exam logic
    return redirect('show_exam_result', course_id=course_id, submission_id=1)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    total_score = 0
    possible_score = 0
    
    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(submission.choices.all()):
            total_score += question.grade
            
    context = {
        'course': course,
        'total_score': total_score,
        'possible_score': possible_score
    }
    return render(request, 'exam_result.html', context)
