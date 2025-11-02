# ResponseProcessing.py
# This script processes the questionnaire responses from the database.
# It assumes this script is run within the context of the Django project
# (e.g., via 'python manage.py shell' and then importing this file).

# Import the necessary models from the 'core' application
from core.models import Person, Answers, Question
from utils import *#i wanna import my utils -sarah

# Initialize the main list that will hold all individual person's answer lists
PeoplesAnswers = []

# Retrieve all Person objects from the database
all_people = Person.objects.all()

# Iterate over each person found in the database
for person in all_people:
    
    # Create a new list to store this specific person's data
    person_list = []

    # Retrieve all answers for the current person.
    # We use order_by('question__order') to ensure the answers
    # are in the same order as the questions were presented.
    persons_answers = Answers.objects.filter(person=person).order_by('question__order')

    # Iterate over the ordered answers and append the response value
    for answer in persons_answers:
        person_list.append(answer.response)

    # As requested, append the person's name as the second-to-last element
    person_list.append(person.name)

    # Append the person's session_id as the last element
    person_list.append(person.session_id)

    # Add the fully populated list for this person to the main list
    PeoplesAnswers.append(person_list)

# The script finishes here.
# The 'PeoplesAnswers' list is now populated in memory and can be
# accessed by whichever script or shell session imported this file.
# No output is printed, as requested.



#sarahs part now yay (hashtag no ai hastag authentic hash critical thinking)
#gameplan
pairedIndexes = input_vectors_output_pairs(PeoplesAnswers) #use the array and my function from utils to get the pair return
#[(0,3),(2,5),..] is the format of above
#pair return can be processed then

#todo next
#display a page or even an alert idc that says {ur partner name} is your match by {number}%.
#note, ur partner name accessed from paired indexes,number needs to multiplu by 100 and round