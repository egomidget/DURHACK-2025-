from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import Questionaire, Person, Answers, Question, Match
from core.forms import DynamicQuestionnaireForm
import uuid
import qrcode
import base64
from io import BytesIO
import os

from django.shortcuts import render
from durhack.ResponseProcessing import *

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
            person.name=form.cleaned_data.get('name')
            person.save()
            for question in questions:
                field_name = f"question_{question.id}"
                answer_text = form.cleaned_data.get(field_name)
                if answer_text:
                    a, _ = Answers.objects.get_or_create(
                        question=question,
                        # response=answer_text,
                        person=person
                    )
                    a.response = answer_text
                    a.save()

            print(process_answers())
            return HttpResponse("<h1>Thank you, please wait while we process the results</h1>")
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

def process_matches(matches_data):
    for session_a, session_b, score in matches_data:
        try:
            person_a = Person.objects.get(session_id=session_a)
            person_b = Person.objects.get(session_id=session_b)

            # Avoid duplicate (A↔B and B↔A)
            if not Match.objects.filter(
                person_a=person_a,
                person_b=person_b
            ).exists() and not Match.objects.filter(
                person_a=person_b,
                person_b=person_a
            ).exists():

                Match.objects.create(
                    person_a=person_a,
                    person_b=person_b,
                    score=score
                )

            return HttpResponse("Matches Made")

        except Person.DoesNotExist:
            # In case one of the people wasn't found (shouldn’t happen normally)
            continue


def see_match(request):
    session_id = request.session.get('session_id')

    person = Person.objects.get(session_id=session_id)

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
    

