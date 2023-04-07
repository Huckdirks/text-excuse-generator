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
def generate_excuse(USER = "", RECIPIENT = "", PROBLEM = "", EXCUSE = "", NEW_RECIPIENT = "", NEW_RECIPIENT_PHONE_NUMBER = ""):
    ENV_NAME = "personal_info"  # CHANGE THIS TO YOUR ENVIRONMENT NAME (.env file)

    # If no parameters are given
    if not USER or RECIPIENT or PROBLEM or EXCUSE:
        # If no arguments are given, ask for user input
        if len(argv) == 1:
            USER = input("Enter who is sending the text: ")
            RECIPIENT = input("Enter who you want to text: ")
            PROBLEM = input("Enter the fake problem you are having: ")
            EXCUSE = input("Enter the excuse you want to use: ")

        # If the -a or --add flag is given with correct parameters, or if correct parameters passed in, add a new user to the .env file
        elif (NEW_RECIPIENT and NEW_RECIPIENT_PHONE_NUMBER) or (len(argv) == 4 and (argv[1] == "-a" or argv[1] == "--add") and phonenumbers.is_valid_number(phonenumbers.parse(argv[3]))):
            lines = []
            if NEW_RECIPIENT == '' or NEW_RECIPIENT_PHONE_NUMBER == '':
                NEW_RECIPIENT = argv[2]
                NEW_RECIPIENT_PHONE_NUMBER = argv[3]
            # Add a new user to the .env file
            with open(f"{ENV_NAME}.env", "r") as file:
                lines = file.readlines()
            if f"{NEW_RECIPIENT.upper()}_PHONE_NUMBER = \"{NEW_RECIPIENT_PHONE_NUMBER}\"\n" in lines:
                    print(f"Error: Recipient \'{NEW_RECIPIENT}\' already exists in .env file!")
                    exit()
            index = lines.index("# Phone Numbers to text\n")
            lines.insert(index + 1, f"{NEW_RECIPIENT.upper()}_PHONE_NUMBER = \"{NEW_RECIPIENT_PHONE_NUMBER}\"\n")
            with open(f"{ENV_NAME}.env", "w") as file:
                file.writelines(lines)
                print(f"Added recipient \'{NEW_RECIPIENT}\' with phone number \'{NEW_RECIPIENT_PHONE_NUMBER}\' to .env file!")
            exit()
        
        # If command line arguments are given, use them
        elif len(argv) == 5:
            # Load command line arguments
            USER = argv[1]
            RECIPIENT = argv[2]
            PROBLEM = argv[3]
            EXCUSE = argv[4]

        # Else, give info on how to use the program
        else:
            print("\nUsage: python3 text_excuse_generator.py [sender] [recipient] [problem] [excuse]")
            print("\tsender: The person who is sending the text")
            print("\trecipient: The person you want to text (can be saved person or a phone number)")
            print("\tproblem: The \"problem\" you are having")
            print("\texcuse: The excuse you want to use")
            print("Or just run the program with no arguments to be prompted for input")
            print("Put any parameters longer than a single word in quotes, e.g. \"I'm sick\"\n")
            print("To add a new recipient to the .env file, run the program with the -a or --add flag then {RECIPIENT} then {PHONE_NUMBER}, e.g. python3 text_excuse_generator.py -a \"John Doe\" \"+1 555 555 5555\"\n")
            print("The prompt sent to ChatGPT is: \"Write a text message to {RECIPIENT} explaining that you {PROBLEM} because {EXCUSE}.\"\n")
            exit()

    # Load environment variables
    ENV_PATH = join(dirname(__file__), f"{ENV_NAME}.env")
    load_dotenv(ENV_PATH)

    TO_PHONE_NUMBER = ""
    # Check if recipient is a phone number or a saved person
    if (RECIPIENT[0] == '+' and RECIPIENT[1:].isnumeric()) and phonenumbers.is_valid_number(phonenumbers.parse(RECIPIENT)):
        TO_PHONE_NUMBER = RECIPIENT
    else:
        TO_PHONE_NUMBER = os.getenv(f"{RECIPIENT.upper()}_PHONE_NUMBER")
        if TO_PHONE_NUMBER == None:
            print(f"Error: No phone number found for user \'{RECIPIENT}\' in .env file!")
            exit()

    CHATGPT_CONTEXT = f"Write a text message to {RECIPIENT} explaining that you {PROBLEM} because {EXCUSE}. Also start the message by stating this is {USER}"
    print("\nCreating text message...\n")

    # OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    AI_QUERY = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": CHATGPT_CONTEXT}]
    )

    AI_RESPONSE = AI_QUERY.choices[0].message.content
    print(f"Chat GPT's Response:\n{AI_RESPONSE}\n")

    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # Twilio API
    # Sends the text
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to = TO_PHONE_NUMBER,
        from_ = TWILIO_PHONE_NUMBER,
        body = AI_RESPONSE
    )


if __name__ == "__main__":
    generate_excuse()