# Imported Libraries
from dotenv import load_dotenv
import openai   # I would just import the necessary functions, but api_key is too generic of a name, so I'm gonna keep the OpenAI namespace
import twilio.rest
from phonenumbers import is_valid_number, parse

# Python Libraries
from os import getenv
from os.path import dirname, join, isfile
from sys import argv

# Constants
ENV_NAME = "personal_info"  # CHANGE THIS TO YOUR ENVIRONMENT NAME (.env file)
ENV_PATH = join(dirname(__file__), f"{ENV_NAME}.env")


# Set up .env file
def setup_env(TWILIO_ACCOUNT_SID: str, TWILIO_AUTH_TOKEN: str, TWILIO_PHONE_NUMBER: str, OPENAI_API_KEY: str) -> bool:
    # Check if .env file exists and not empty
    if isfile(f"{ENV_NAME}.env"):
        print(f"Error: \'{ENV_NAME}.env\' file already set up!")
        return False
    
    if not is_valid_number(parse(TWILIO_PHONE_NUMBER)):
        print("Error: Invalid phone number!")
        return False

    # Set up the .env file
    lines = ["# Twilio API\n", f"TWILIO_ACCOUNT_SID = {TWILIO_ACCOUNT_SID}\n", f"TWILIO_AUTH_TOKEN = {TWILIO_AUTH_TOKEN}\n", f"TWILIO_PHONE_NUMBER = {TWILIO_PHONE_NUMBER}\n", "\n", "# OpenAI API\n", f"OPENAI_API_KEY = {OPENAI_API_KEY}\n", "\n", "# Phone Numbers to text\n"]

    # Write to the .env file
    with open(f"{ENV_NAME}.env", "w") as file:
        file.writelines(lines)

    print(f"Set up \'{ENV_NAME}.env\' file!")
    return True


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
    if not isfile(ENV_PATH):
        print(f"Error: \'{ENV_NAME}.env\' file not set up! Use the -e or --setup_env flag to set up the .env file")
        return
    
    # Load the .env file
    load_dotenv(ENV_PATH)

    print("Sending text...")
    # Twilio API
    twilio_client = twilio.rest.Client(getenv("TWILIO_ACCOUNT_SID"), getenv("TWILIO_AUTH_TOKEN"))  # Login to Twilio
    twilio_client.messages.create(
        to = TO_PHONE_NUMBER,
        from_ = getenv("TWILIO_PHONE_NUMBER"),
        body = MESSAGE
    )
    
    print("Text sent!")
    return


# Generate an excuse and text it to a recipient. If no parameters are given, either by being passed in or given via the Command Line, it will prompt the user for input
def generate_excuse(user: str = "", recipient: str = "", problem: str = "", excuse: str = "", send_text: bool = False) -> str:
    if not user or recipient or problem or excuse:  # If no parameters are given
        if len(argv) == 4 or len(argv) == 5 or len(argv) == 6:        # If command line arguments are given, use them
            if len(argv) == 4 and (argv[1].lower() == "-a" or argv[1].lower() == "--add"):  # If the -a or --add flag is given with correct parameters, and correct # of parameters are passed in
                add_recipient(argv[2], argv[3])
                return
            elif (len(argv) == 6 and (argv[1].lower() == "-e" or argv[1].lower() == "--setup_env")):   # If the -e or --setup_env flag is given with correct parameters, and correct # of parameters are passed in
                setup_env(argv[2], argv[3], argv[4], argv[5])
                return
            
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
            if not isfile(ENV_PATH):  # If the .env file is not set up, ask the user if they want to set it up
                set_up_env_question = input(f"Error: \'{ENV_NAME}.env\' file not set up!\nDo you want to set it up now? (y/n): ")
                if not set_up_env_question.lower() == "y" or not set_up_env_question.lower() == "yes":
                    return
                
                TWILIO_ACCOUNT_SID = input("Enter your Twilio Account SID: ")
                TWILIO_AUTH_TOKEN = input("Enter your Twilio Auth Token: ")
                TWILIO_PHONE_NUMBER = input("Enter your Twilio Phone Number: ")
                OPENAI_API_KEY = input("Enter your OpenAI API Key: ")
                setup_env(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, OPENAI_API_KEY)
            
            user = input("Enter who is sending the text: ")
            recipient = input("Enter who you want to text: ")
            problem = input("Enter the fake problem you are having: ")
            excuse = input("Enter the excuse you want to use: ")

            send_text_question = input("Do you want to send the text? (y/n): ")
            if send_text_question.lower() == "y" or send_text_question.lower() == "yes":
                send_text = True

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
            print("To setup the .env file, run python3 text_excuse_generator.py [-e/--setup_env] [TWILIO_ACCOUNT_SID] [TWILIO_AUTH_TOKEN] [TWILIO_PHONE_NUMBER] [OPENAI_API_KEY]\n\te.g. python3 text_excuse_generator.py -e \"AC1234567890abcdef1234567890abcdef\" \"1234567890abcdef1234567890abcdef\" \"+15555555555\" \"1234567890abcdef1234567890abcdef\"\n")
            print("The prompt sent to ChatGPT is: \"Write a text message to [recipient] explaining that you [problem] because [excuse].\"\n")
            return

    # If the .env file is not set up, or is empty, return   
    if not isfile(ENV_PATH):
        print(f"Error: \'{ENV_NAME}.env\' file not set up! Use the -e or --setup_env flag to set up the .env file")
        return
    
    # Load the .env file
    load_dotenv(ENV_PATH)

    to_phone_number = ""
    if (recipient[0] == '+' and recipient[1:].isnumeric()) and is_valid_number(parse(recipient)):   # Check if recipient is a phone number
        to_phone_number = recipient
    elif send_text:
        RECIPIENT_FORMATTED = recipient.replace(" ", "_")
        to_phone_number = getenv(f"{RECIPIENT_FORMATTED.upper()}_PHONE_NUMBER")
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