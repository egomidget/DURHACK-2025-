
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from core.models import Questionaire, Person, Answers, Question
import uuid
from core.forms import DynamicQuestionnaireForm

####
from django.shortcuts import render, redirect
from django.http import HttpResponse
import qrcode
from io import BytesIO
####


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


from django.shortcuts import redirect

def qr_redirect(request):
    return redirect('/questionnaire/1/')

from django.shortcuts import render

def qr(request):
    return render(request, 'core/qr.html')

#####
import qrcode
import base64
from io import BytesIO
from django.shortcuts import render

def homePage(request):
    print("✅ homePage() function was called")  # <-- add this line

    qr_url = "http://127.0.0.1:8000/questionnaire/1/"
    qr = qrcode.make(qr_url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    print("✅ QR code successfully generated and sent to template!")  # <-- add this line too

    return render(request, "core/index.html", {"qr_image": qr_image})
