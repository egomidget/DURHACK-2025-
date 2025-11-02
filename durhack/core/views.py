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
from durhack.ResponseProcessing import process_answers
from core.models import Person 
from django.urls import reverse
from django.shortcuts import redirect, render

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

        return render(request, "core/index.html", {"qr_image": qr_image})

    except Exception as e:
        print("❌ Error generating QR:", e)
        return HttpResponse("<h1>Error generating QR code</h1>")
    
def show_matches(request):
    paired_ids = process_answers()
    matches = []
    for id1, id2, score in paired_ids:
        try:
            person1 = Person.objects.get(session_id=id1)
            person2 = Person.objects.get(session_id=id2)
            matches.append({
                'person1_name': person1.name,
                'person2_name': person2.name,
                'score': round(score * 100, 2)
            })
        except Person.DoesNotExist:
            continue
    return render(request, 'core/matches.html', {'matches': matches})


def loading_view(request):
    """
    Displays the loading screen before showing match results.
    """
    return render(request, 'core/loading.html')

def go_to_matches(request):
    """
    Redirects to the matches page after the loading screen.
    """
    return redirect('show_matches')
