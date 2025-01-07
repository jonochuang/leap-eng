import json
import base64
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

print('File name :    ', os.path.basename(__file__))
print('Directory Name:     ', os.path.dirname(__file__))

# Function to send an email
def send_email(to, subject, message_text):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    # Load Gmail API credentials
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    # Create the email body
    message = {
        'raw': base64.urlsafe_b64encode(
            f"To: {to}\nSubject: {subject}\n\n{message_text}".encode("utf-8")
        ).decode("utf-8")
    }
    
    # Send the email
    try:
        result = service.users().messages().send(userId="me", body=message).execute()
        print(f"Email sent successfully to {to}: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to process the JSON file and trigger email
def process_json(file_path, trigger_status):
    try:
        # Load JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract fields
        status = data.get('status')
        message = data.get('message')
        recipient = data.get('recipient')
        
        # Check the status and send the email if the condition is met
        if status == trigger_status:
            if not message or not recipient:
                print("Invalid JSON data: 'message' or 'recipient' missing.")
                return 
            send_email(to=recipient, subject="Automated Email", message_text=message)
        else:
            print(f"Status '{status}' does not match the trigger status '{trigger_status}'.")
    except FileNotFoundError:
        print(f"JSON file not found: {file_path}")
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Specify the path to your JSON file
    json_file_path = os.path.dirname(__file__) + '/medium.json'
    
    # Specify the status that triggers the email
    trigger_status = "send_email"
    
    # Process the JSON and send the email if the status matches
    process_json(json_file_path, trigger_status)
