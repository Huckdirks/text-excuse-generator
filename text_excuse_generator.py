# Imported Libraries
from dotenv import load_dotenv
import openai   # I would just import the necessary functions, but api_key is too generic of a name, so I'm gonna keep the OpenAI namespace
import twilio.rest
from phonenumbers import is_valid_number, parse

# Python Libraries
from os import getenv
from os.path import dirname, join
from sys import argv

# Constants
ENV_NAME = "personal_info"  # CHANGE THIS TO YOUR ENVIRONMENT NAME (.env file)
ENV_PATH = join(dirname(__file__), f"{ENV_NAME}.env")

# Load the .env file
load_dotenv(ENV_PATH)


# Save a phone number to the .env file
def add_recipient(RECIPIENT: str, PHONE_NUMBER: str) -> bool:
    if not is_valid_number(parse(PHONE_NUMBER)):
        print("Error: Invalid phone number!")
        return False
    
    # Replace spaces with underscores for formatting
    NEW_RECIPIENT = RECIPIENT.replace(" ", "_")
    lines = []
    
    # Add a new user to the .env file
    with open(f"{ENV_NAME}.env", "r") as file:
        lines = file.readlines()

    if f"{NEW_RECIPIENT.upper()}_PHONE_NUMBER" in lines:
        print(f"Error: Recipient \'{NEW_RECIPIENT}\' already exists in .env file! Manually edit the .env file if you want to change the phone number.")
        return False
    
    index = lines.index("# Phone Numbers to text\n")
    lines.insert(index + 1, f"{NEW_RECIPIENT.upper()}_PHONE_NUMBER = \"{PHONE_NUMBER}\"\n")

    with open("personal_info.env", "w") as file:
        file.writelines(lines)
        print(f"Added recipient \'{NEW_RECIPIENT}\' with phone number \'{PHONE_NUMBER}\' to .env file!")

    return True


# If the -s or --send flag is given, send the text
def send_twilio_text(TO_PHONE_NUMBER: str, MESSAGE: str) -> None:
    TWILIO_ACCOUNT_SID = getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = getenv("TWILIO_PHONE_NUMBER")

    # Twilio API
    # Sends the text
    print("Sending text...")
    twilio_client = twilio.rest.Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)  # Login to Twilio
    twilio_client.messages.create(
        to = TO_PHONE_NUMBER,
        from_ = TWILIO_PHONE_NUMBER,
        body = MESSAGE
    )
    print("Text sent!")


# Generate an excuse and text it to a recipient. If no parameters are given, either by being passed in or given via the Command Line, it will prompt the user for input
def generate_excuse(user: str = "", recipient: str = "", problem: str = "", excuse: str = "", send_text: bool = False) -> str:
    if not user or recipient or problem or excuse:  # If no parameters are given
        if len(argv) == 5 or len(argv) == 6:        # If command line arguments are given, use them
            # Load command line arguments
            user = argv[1]
            recipient = argv[2]
            problem = argv[3]
            excuse = argv[4]
            if len(argv) == 6 and (argv[5].lower() == "-s" or argv[5].lower() == "--send"):
                send_text = True
            elif len(argv) == 6:
                print("\nError: Invalid flag given! Use -s or --send to send the text")
                return

        elif len(argv) == 1:    # If no arguments are given, ask for user input
            user = input("Enter who is sending the text: ")
            recipient = input("Enter who you want to text: ")
            problem = input("Enter the fake problem you are having: ")
            excuse = input("Enter the excuse you want to use: ")

            send_text_question = input("Do you want to send the text? (y/n): ")
            if send_text_question.lower() == "y" or send_text_question.lower() == "yes":
                send_text = True

        elif (len(argv) == 4 and (argv[1].lower() == "-a" or argv[1].lower() == "--add")):    # If the -a or --add flag is given with correct parameters, and correct # of parameters are passed in
            add_recipient(argv[2], argv[3])
            return

        else:   # Give info on how to use the program
            print("\nUsage: python3 text_excuse_generator.py [sender] [recipient] [problem] [excuse] [--send_flag]")
            print("\tsender: The person who is sending the text")
            print("\trecipient: The person you want to text (can be saved person or a phone number)")
            print("\tproblem: The \"problem\" you are having")
            print("\texcuse: The excuse you want to use")
            print("\t--send_flag: If you want to send the text, add -s or --send. If you don't want to send the text, omit this flag\n")
            print("Or just run the program with no arguments to be prompted for input")
            print("Put any parameters longer than a single word in quotes, e.g. \"I'm sick\"\n")
            print("To add a new recipient to the .env file, run python3 text_excuse_generator.py [-a/--add] [recipient] [PHONE_NUMBER]\n\te.g. python3 text_excuse_generator.py -a \"John Doe\" \"+15555555555\"\n")
            print("The prompt sent to ChatGPT is: \"Write a text message to [recipient] explaining that you [problem] because [excuse].\"\n")
            return

    to_phone_number = ""
    if (recipient[0] == '+' and recipient[1:].isnumeric()) and is_valid_number(parse(recipient)):   # Check if recipient is a phone number
        to_phone_number = recipient
    elif send_text:
        recipient_formatted = recipient.replace(" ", "_")
        to_phone_number = getenv(f"{recipient_formatted.upper()}_PHONE_NUMBER")
        if to_phone_number == None: # If the recipient is not in the .env file
            print(f"\nError: No phone number found for recipient \'{recipient}\' in .env file!")
            if len(argv) != 1:  # If not in user input mode, exit, else ask if they want to add the recipient
                return
            
            # Ask if they want to add the recipient
            ADD_RECIPIENT_QUESTION = input("Do you want to add this recipient to the .env file? (y/n): ")
            if not ADD_RECIPIENT_QUESTION.lower() == "y" or not ADD_RECIPIENT_QUESTION.lower() == "yes":
                return
            
            to_phone_number = input("Enter the phone number of the recipient: ")
            if not add_recipient(recipient, to_phone_number):   # If the recipient could not be added
                return

    # Create the message (AI Time!)
    CHATGPT_CONTEXT = f"Write a text message to {recipient} explaining that you {problem} because {excuse}. Also start the message by stating this is {user}, and end the message by telling the recipient to text my actual phone number back if you really need me."
    print("\nCreating message...\n")

    # OpenAI API
    openai.api_key = getenv("OPENAI_API_KEY")
    AI_QUERY = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": CHATGPT_CONTEXT}]
    )

    AI_RESPONSE = AI_QUERY.choices[0].message.content
    print(f"Chat GPT's Response:\n{AI_RESPONSE}\n")

    if send_text:   # If the -s or --send flag is given, send the text
        send_twilio_text(to_phone_number, AI_RESPONSE)

    return AI_RESPONSE


if __name__ == "__main__":
    generate_excuse()