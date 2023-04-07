# Libraries
from dotenv import load_dotenv
import openai
from twilio.rest import Client
import phonenumbers
import os
from os.path import dirname, join
from sys import argv

# Function to generate an excuse and text it to a recipient. If no parameters are given, either by being passed in or given via the Command Line, it will prompt the user for input
# If you want to send a text by passing in parameters, just pass in the first 4. If you want to add a person, set the first 4 to '' and only put actual values for the last 2
def generate_excuse(user = "", recipient = "", problem = "", excuse = "", new_recipient = "", new_recipient_phone_number = "", send_text = False):
    ENV_NAME = "personal_info"  # CHANGE THIS TO YOUR ENVIRONMENT NAME (.env file)

    # If no parameters are given
    if not user or recipient or problem or excuse:
        # If command line arguments are given, use them
        if len(argv) == 5 or len(argv) == 6:
            # Load command line arguments
            user = argv[1]
            recipient = argv[2]
            problem = argv[3]
            excuse = argv[4]
            if len(argv) == 6 and (argv[5].lower() == "-s" or argv[5].lower() == "--send"):
                send_text = True

        # If no arguments are given, ask for user input
        elif len(argv) == 1:
            user = input("Enter who is sending the text: ")
            recipient = input("Enter who you want to text: ")
            problem = input("Enter the fake problem you are having: ")
            excuse = input("Enter the excuse you want to use: ")
            send_text_question = input("Do you want to send the text? (y/n): ")
            if send_text_question.lower() == "y" or send_text_question.lower() == "yes":
                send_text = True

        # If the -a or --add flag is given with correct parameters, or if correct parameters passed in, add a new user to the .env file
        elif (new_recipient and new_recipient_phone_number) or (len(argv) == 4 and (argv[1].lower() == "-a" or argv[1].lower() == "--add") and phonenumbers.is_valid_number(phonenumbers.parse(argv[3]))):
            lines = []
            if new_recipient == '' or new_recipient_phone_number == '':
                new_recipient = argv[2]
                new_recipient_phone_number = argv[3]
            # Add a new user to the .env file
            with open(f"{ENV_NAME}.env", "r") as file:
                lines = file.readlines()
            if f"{new_recipient.upper()}_PHONE_NUMBER = \"{new_recipient_phone_number}\"\n" in lines:
                    print(f"Error: Recipient \'{new_recipient}\' already exists in .env file!")
                    exit()
            index = lines.index("# Phone Numbers to text\n")
            lines.insert(index + 1, f"{new_recipient.upper()}_PHONE_NUMBER = \"{new_recipient_phone_number}\"\n")
            with open(f"{ENV_NAME}.env", "w") as file:
                file.writelines(lines)
                print(f"Added recipient \'{new_recipient}\' with phone number \'{new_recipient_phone_number}\' to .env file!")
            exit()

        # Else, give info on how to use the program
        else:
            print("\nUsage: python3 text_excuse_generator.py [sender] [recipient] [problem] [excuse] [--send_flag]")
            print("\tsender: The person who is sending the text")
            print("\trecipient: The person you want to text (can be saved person or a phone number)")
            print("\tproblem: The \"problem\" you are having")
            print("\texcuse: The excuse you want to use")
            print("\t--send_flag: If you want to send the text, add -s or --send. If you don't want to send the text, don't add this flag\n")
            print("Or just run the program with no arguments to be prompted for input")
            print("Put any parameters longer than a single word in quotes, e.g. \"I'm sick\"\n")
            print("To add a new recipient to the .env file, run python3 text_excuse_generator.py [-a/--add] [recipient] [PHONE_NUMBER]\n\te.g. python3 text_excuse_generator.py -a \"John Doe\" \"+1 555 555 5555\"\n")
            print("The prompt sent to ChatGPT is: \"Write a text message to {recipient} explaining that you {problem} because {excuse}.\"\n")
            exit()

    # Load environment variables
    ENV_PATH = join(dirname(__file__), f"{ENV_NAME}.env")
    load_dotenv(ENV_PATH)

    to_phone_number = ""
    # Check if recipient is a phone number or a saved person
    if (recipient[0] == '+' and recipient[1:].isnumeric()) and phonenumbers.is_valid_number(phonenumbers.parse(recipient)):
        to_phone_number = recipient
    elif send_text:
        to_phone_number = os.getenv(f"{recipient.upper()}_PHONE_NUMBER")
        if to_phone_number == None:
            print(f"\nError: No phone number found for recipient \'{recipient}\' in .env file!")
            if len(argv) != 1:  # If not in user input mode
                exit()

            ADD_RECIPIENT_QUESTION = input("Do you want to add this recipient to the .env file? (y/n): ")
            if not ADD_RECIPIENT_QUESTION.lower() == "y" or not ADD_RECIPIENT_QUESTION.lower() == "yes":
                exit()

            new_recipient_phone_number = input("Enter the phone number of the recipient: ")
            if not phonenumbers.is_valid_number(phonenumbers.parse(new_recipient_phone_number)):
                print("Error: Invalid phone number!")
                exit()

            lines = []
            with open(f"{ENV_NAME}.env", "r") as file:
                lines = file.readlines()
            index = lines.index("# Phone Numbers to text\n")
            lines.insert(index + 1, f"{recipient.upper()}_PHONE_NUMBER = \"{new_recipient_phone_number}\"\n")
            with open(f"{ENV_NAME}.env", "w") as file:
                file.writelines(lines)
                print(f"Added recipient \'{recipient}\' with phone number \'{new_recipient_phone_number}\' to .env file!")

    CHATGPT_CONTEXT = f"Write a text message to {recipient} explaining that you {problem} because {excuse}. Also start the message by stating this is {user}"
    print("\nCreating message...\n")

    # OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    AI_QUERY = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": CHATGPT_CONTEXT}]
    )

    AI_RESPONSE = AI_QUERY.choices[0].message.content
    print(f"Chat GPT's Response:\n{AI_RESPONSE}\n")

    if not send_text:
        return AI_RESPONSE
        
    # If the -s or --send flag is given, send the text
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # Twilio API
    # Sends the text
    print("Sending text...\n")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to = to_phone_number,
        from_ = TWILIO_PHONE_NUMBER,
        body = AI_RESPONSE
    )
    print("Text sent!\n")
    return AI_RESPONSE


if __name__ == "__main__":
    generate_excuse()