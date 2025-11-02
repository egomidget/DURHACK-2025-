# File: core/compatibility.py
#
# This file provides functions for analyzing the compatibility between two users
# based on their questionnaire answers.
#
# You can import this file into your views.py or other scripts like this:
# from .compatibility import get_compatibility_insights
#
# Then you can call the function with your data:
# insights = get_compatibility_insights(id1, id2, peoples_answers_dict)

# Define constants for the answer scale.
# This makes it easy to change if your scale ever changes from 1-10.
MIN_ANSWER_SCALE = 1
MAX_ANSWER_SCALE = 10
# Calculate the maximum possible difference between two answers.
# For a 1-10 scale, the max difference is 10 - 1 = 9.
MAX_DIFFERENCE = MAX_ANSWER_SCALE - MIN_ANSWER_SCALE

def get_compatibility_insights(session_id1, session_id2, peoples_answers):
    """
    Analyzes the answers for two users and finds the top 3 things they
    have most in common and the 1 thing they have least in common.

    Args:
        session_id1 (str): The session ID of the first person.
        session_id2 (str): The session ID of the second person.
        peoples_answers (dict): The dictionary of all user answers,
                                formatted like:
                                {
                                    'session_id_A': [q1, q2, q3...],
                                    'session_id_B': [q1, q2, q3...]
                                }

    Returns:
        list: A 2D list (list of lists) containing the insights.
              Format:
              [
                  [common_q_num_1, perc_diff_1],
                  [common_q_num_2, perc_diff_2],
                  [common_q_num_3, perc_diff_3],
                  [least_common_q_num, perc_diff_4]
              ]
              Returns None if an error occurs (e.g., user not found).
    """

    # --- 1. Data Retrieval ---
    # Get the answer lists for both users from the main dictionary.
    # We use .get() which safely returns None if the key doesn't exist,
    # preventing a crash.
    answers1 = peoples_answers.get(str(session_id1))
    answers2 = peoples_answers.get(str(session_id2))

    # --- 2. Error Handling ---
    # Check if we successfully found answer lists for both users.
    if not answers1 or not answers2:
        print(f"Error: Could not find answer list for {session_id1} or {session_id2}")
        return None  # Return None to indicate an error

    # Check if the answer lists have the same number of questions.
    if len(answers1) != len(answers2):
        print("Error: User answer lists have different lengths. Cannot compare.")
        return None  # Return None as we can't compare them

    # --- 3. Calculate Differences ---
    # This list will store tuples of (question_number, percentage_difference)
    question_differences = []

    # Iterate over each answer in the lists.
    # We use enumerate to get both the index (i) and the value.
    for i in range(len(answers1)):
        # Get the answer from each person for the current question
        ans1 = answers1[i]
        ans2 = answers2[i]

        # Calculate the absolute difference (e.g., |1 - 5| = 4)
        abs_diff = abs(ans1 - ans2)

        # Calculate the percentage difference.
        # (absolute_difference / maximum_possible_difference) * 100
        # If MAX_DIFFERENCE is 0 (e.g., scale is 1-1), handle division by zero.
        if MAX_DIFFERENCE == 0:
            perc_diff = 0.0 if abs_diff == 0 else 100.0
        else:
            perc_diff = (abs_diff / MAX_DIFFERENCE) * 100

        # Get the human-readable question number (index 0 is Question 1)
        question_num = i + 1

        # Store the result
        question_differences.append((question_num, perc_diff))

    # At this point, question_differences looks like:
    # [(1, 11.1), (2, 0.0), (3, 100.0), ...]

    # --- 4. Sort to Find Insights ---
    # Sort the list based on the percentage difference (the second item in each tuple).
    # `key=lambda item: item[1]` tells sorted() to use the percentage (index 1)
    # for sorting. This sorts in ascending order (lowest difference first).
    sorted_differences = sorted(question_differences, key=lambda item: item[1])

    # The "most in common" are the ones with the lowest percentage difference,
    # so they are at the beginning of the sorted list.
    # We use min(3, len(sorted_differences)) in case there are fewer than 3 questions.
    top_3_common = sorted_differences[:min(3, len(sorted_differences))]

    # The "least in common" is the one with the highest percentage difference,
    # so it is at the very end of the sorted list.
    # We use a slice `[-1:]` to get it as a list, even if it's the only item.
    if sorted_differences:
        top_1_least_common = sorted_differences[-1:]
    else:
        top_1_least_common = [] # Handle case of zero questions

    # --- 5. Format and Return Output ---
    # We will build the 2D array as requested.
    insights_report = []

    # Add the top 3 common questions
    # Convert tuple (q_num, diff) to list [q_num, rounded_diff]
    for q_num, diff in top_3_common:
        insights_report.append([q_num, round(diff, 2)])

    # Add the top 1 least common question
    # Note: If there are fewer than 4 questions, this might be a repeat
    # of one of the "top 3 common" ones. This is expected.
    for q_num, diff in top_1_least_common:
        insights_report.append([q_num, round(diff, 2)])

    # Return the final list
    return insights_report

# --- Example Usage (Test Block) ---
# This special block only runs if you execute this file directly
# (e.g., `python core/compatibility.py`)
# It's a great way to test your function without running the whole server.
if __name__ == "__main__":
    
    # 1. Create a mock `PeoplesAnswers` dictionary for testing.
    # This is the same format your ResponseProcessing.py creates.
    mock_data = {
        "alice_session_123": [1, 10, 5,  8, 3, 9, 7],
        "bob_session_456":   [2, 10, 1,  7, 4, 2, 6], # Similar to Alice
        "charlie_session_789": [9,  2, 5, 10, 1, 9, 8], # Different from Alice
    }

    print("--- Test 1: Alice and Bob (Similar) ---")
    # 2. Call the function to get insights for Alice and Bob
    insights_ab = get_compatibility_insights("alice_session_123", "bob_session_456", mock_data)

    # 3. Print the results
    if insights_ab:
        print("Compatibility Report: [Question #, % Difference]")
        for insight in insights_ab:
            print(insight)
    
    # Expected Output for Alice vs Bob (scale 1-10, max_diff=9):
    # Q1: |1-2|=1 -> 11.1%
    # Q2: |10-10|=0 -> 0.0%
    # Q3: |5-1|=4 -> 44.4%
    # Q4: |8-7|=1 -> 11.1%
    # Q5: |3-4|=1 -> 11.1%
    # Q6: |9-2|=7 -> 77.8%
    # Q7: |7-6|=1 -> 11.1%
    #
    # Sorted Diffs: (Q2, 0.0), (Q1, 11.1), (Q4, 11.1), (Q5, 11.1), (Q7, 11.1), (Q3, 44.4), (Q6, 77.8)
    # Top 3 Common: [2, 0.0], [1, 11.11], [4, 11.11] (or any of the 11.11s)
    # Top 1 Least: [6, 77.78]
    # Result: [[2, 0.0], [1, 11.11], [4, 11.11], [6, 77.78]] (order of 11.11s may vary)


    print("\n--- Test 2: Alice and Charlie (Different) ---")
    insights_ac = get_compatibility_insights("alice_session_123", "charlie_session_789", mock_data)
    
    if insights_ac:
        print("Compatibility Report: [Question #, % Difference]")
        for insight in insights_ac:
            print(insight)

    print("\n--- Test 3: Missing User ---")
    insights_missing = get_compatibility_insights("alice_session_123", "dave_session_000", mock_data)
    
    if not insights_missing:
        print("Report: None (Correctly handled missing user)")
