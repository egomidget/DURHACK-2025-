from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import Questionaire, Person, Answers, Question
from core.forms import DynamicQuestionnaireForm
import uuid
import qrcode
import base64
from io import BytesIO
import os

from django.shortcuts import render
from durhack import ResponseProcessing 

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
            return redirect('thank_you')
    else:
        form = DynamicQuestionnaireForm(questions=questions)

    return render(request, "core/questionaire.html", {
        "questionnaire": questionnaire,
        "form": form
    })



def qr_redirect(request):
    return redirect('/questionnaire/1/')


def qr(request):
    return render(request, 'core/qr.html')


def homePage(request):
    try:
        qr_url = "http://127.0.0.1:8000/questionnaire/1/"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        print("✅ QR generated successfully")

        # ✅ Use Django's render function instead of manual open
        return render(request, "core/index.html", {"qr_image": qr_image})

    except Exception as e:
        print("❌ Error generating QR:", e)
        return HttpResponse("<h1>Error generating QR code</h1>")
    

