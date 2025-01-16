import os
import json
import uuid
from Document_Categorization.code.index_fetch import index_fetch
from rich import print
import os
import json

def save_feedback_to_json(feedback_data, feedback_file="feedback.json", summary_file="feedback_summary.json", threshold=1):
    """
    Save feedback data to a JSON file and generate a summary after reaching the threshold.
    """
    # Load existing feedback if the file exists
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r', encoding='utf-8') as f:
            existing_feedback = json.load(f)
    else:
        existing_feedback = []

    # Add new feedback data
    existing_feedback.append(feedback_data)

    # Save updated feedback to the JSON file
    with open(feedback_file, 'w', encoding='utf-8') as f:
        json.dump(existing_feedback, f, indent=4)
    print(f"Feedback saved to {feedback_file}")

def RLHF_operator(uuid_path, file_path, is_rlhf=True, feedback: str = None, feedback_file="feedback.json"):
    """
    Match the file path with the provided UUID JSON file and fetch only the final_data.
    """
    # Load data from the UUID file
    with open(uuid_path, 'r', encoding='utf-8') as f:
        uuid_data = json.load(f)


    # print(uuid_data)
    # input("-----> Press Enter to continue <-----")
    # Initialize variable to store final_data
    final_data = {}

    # Match the file path
    for record in uuid_data:
        # print(record)
        # input("-----")
        if record['file'] == file_path:
            # Fetch only final_data from matched record
            final_data = record.get('final_data', {})
            document_type = record.get('document_type', '')

            # Debugging logs
            # print("final_data:", final_data)
            # print("document_type:", document_type)
            # print("feedback:", feedback)

            # input("-----> Press Enter to continue <-----")

            # Ensure final_data is a dictionary
            if not isinstance(final_data, dict):
                raise ValueError(f"Expected final_data to be a dictionary, got {type(final_data)}")

            # Process the data
            update_data = index_fetch(document_type, final_data, is_rlhf=is_rlhf, feedback_intent=feedback)

            # Debugging logs
            print("update_data:", update_data)

            # Prepare feedback data
            feedback_data = {
                "file": file_path,
                "feedback": feedback,
                "updated_data": update_data,
                "updated": update_data != final_data
            }

            # Save feedback to JSON
            save_feedback_to_json(feedback_data, feedback_file)

            return update_data


# # # Example Usage
# uuid_path = r"C:\Users\Rushikesh\Desktop\Hridayam\output\5ee5c5fe-a3a5-43f7-8205-adbe9e61686f.json"
# file_path = r"C:\Users\Rushikesh\Desktop\Hridayam\document_category\test_2.png"
# feedback = "due date for it 23 Jan 2023 in payment_due_date key"
# RLHF_operator(uuid_path, file_path, feedback=feedback)