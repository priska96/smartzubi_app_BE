import json
import sys

def calculate_test_score(json_file_path):
    try:
        # Load the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Initialize total score
        total_score = 0

        # Iterate through the questions
        for question in data.get("questions", []):
            question_points = 0
            for answer in question.get("answers", []):
                if answer.get("correct"):
                    question_points += answer.get("points", 0)

            print(f"The points for question {question.get('title')} are: {question_points}")
            total_score += question_points

        print(f"The total score for the test is: {total_score}")
        return total_score

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_test_score.py <path_to_json_file>")
    else:
        json_file_path = sys.argv[1]
        calculate_test_score(json_file_path)
