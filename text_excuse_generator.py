# Libraries
from dotenv import load_dotenv
import openai
from twilio.rest import Client
import os
from os.path import dirname, join
from sys import argv

def main():
    USER = ""
    RECIPIENT = ""
    PROBLEM = ""
    EXCUSE = ""
    ENV_NAME = "personal_info"  # CHANGE THIS TO YOUR ENVIRONMENT NAME (.env file)

    # If no command line arguments are given, ask for user input
    if len(argv) == 1:
        USER = input("Enter who is sending the text: ")
        RECIPIENT = input("Enter who you want to text: ")
        PROBLEM = input("Enter the fake problem you are having: ")
        EXCUSE = input("Enter the excuse you want to use: ")

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
        print("\trecipient: The person you want to text")
        print("\tproblem: The \"problem\" you are having")
        print("\texcuse: The excuse you want to use")
        print("Or just run the program with no arguments to be prompted for input")
        print("Put any parameters longer than a single word in quotes, e.g. \"I'm sick\"\n")
        print("The prompt sent to ChatGPT is: \"Write a text message to {RECIPIENT} explaining that you {PROBLEM} because {EXCUSE}.\"\n")
        exit()

    # Load environment variables
    ENV_PATH = join(dirname(__file__), f"{ENV_NAME}.env")
    load_dotenv(ENV_PATH)

    TO_PHONE_NUMBER = os.getenv(f"{RECIPIENT.upper()}_PHONE_NUMBER")
    if TO_PHONE_NUMBER == None:
        print(f"Error: No phone number found for user \'{USER}\' in .env file!")
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
    main()