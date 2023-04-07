# Libraries
from dotenv import load_dotenv
import openai
from twilio.rest import Client
import os
from os.path import dirname, join
import sys

def main():
    USER = ""
    RECIPIENT = ""
    PROBLEM = ""
    EXCUSE = ""

    # If no command line arguments are given, ask for user input
    if len(sys.argv) == 1:
        USER = input("Enter who is sending the text: ")
        RECIPIENT = input("Enter who you want to text: ")
        PROBLEM = input("Enter the fake problem you are having: ")
        EXCUSE = input("Enter the excuse you want to use: ")

    # If command line arguments are given, use them
    elif len(sys.argv) == 5:
        # Load command line arguments
        USER = sys.argv[1]
        RECIPIENT = sys.argv[2]
        PROBLEM = sys.argv[3]
        EXCUSE = sys.argv[4]

    # Else, give info on how to use the program
    else:
        print("Usage: python text_excuse_generator.py [sender] [recipient] [problem] [excuse]")
        print("Use underscores for spaces in any of the fields. Also, don't use any special characters.")
        print("\tsender: The person who is sending the text")
        print("\trecipient: The person you want to text")
        print("\tproblem: The fake problem you are having")
        print("\texcuse: The excuse you want to use")
        exit()

    # Load environment variables
    DOTENV_PATH = join(dirname(dirname(__file__)), "personal_info.env")
    load_dotenv(DOTENV_PATH)

    AI_CONTEXT = f"Write a text message to {RECIPIENT} explaining that you can't {PROBLEM} because {EXCUSE}. Also start the message by stating this is {USER}"
    print("\nCreating text message...\n")

    # OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    AI_QUERY = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "Turn all _'s into spaces in user input."},
            {"role": "user", "content": AI_CONTEXT}
        ]
    )
    AI_RESPONSE = AI_QUERY.choices[0].message.content
    print(f"Chat GPT's Response:\n{AI_RESPONSE}\n")

    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    TO_PHONE_NUMBER = "+12087207857"

    # Twilio API
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to = TO_PHONE_NUMBER,
        from_ = TWILIO_PHONE_NUMBER,
        body = AI_RESPONSE
    )



if __name__ == "__main__":
    main()