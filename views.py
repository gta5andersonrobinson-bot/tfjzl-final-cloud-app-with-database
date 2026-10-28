from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Submission, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('question_'):
                choice_id = int(value)
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
    submission.save()
    return redirect('show_exam_result', course_id=course_id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    selected_ids = [choice.id for choice in submission.choices.all()]
    total_score = 0
    possible_score = 0
    
    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    grade = (total_score / possible_score) * 100 if possible_score > 0 else 0
    
    context = {
        'course': course,
        'total_score': total_score,
        'possible_score': possible_score,
        'grade': grade,
        'selected_ids': selected_ids
    }
    return render(request, 'course_details_bootstrap.html', context)
