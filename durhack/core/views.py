
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from core.models import Questionaire, Person, Answers, Question
import uuid
from core.forms import DynamicQuestionnaireForm


# Create your views here.
def homePage(request):
    return render(request,'core/index.html')

def questionnaire(request, questionaire_id):
    questionnaire = get_object_or_404(Questionaire, id=questionaire_id)
    questions = questionnaire.questions.order_by('order')

    session_id = request.session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['session_id'] = session_id
    person, _ = Person.objects.get_or_create(session_id=session_id)

    if request.method == "POST":
        form = DynamicQuestionnaireForm(request.POST, questions=questions)
        if form.is_valid():
            for question in questions:
                field_name = f"question_{question.id}"
                answer_text = form.cleaned_data.get(field_name)
                if answer_text:
                    Answers.objects.create(
                        question=question,
                        response=answer_text,
                        person=person
                    )

            # calling function for loading peoples submissions

            return redirect('thank_you')
    else:
        form = DynamicQuestionnaireForm(questions=questions)

    return render(request, "core/questionaire.html", {
        "questionnaire": questionnaire,
        "form": form
    })
