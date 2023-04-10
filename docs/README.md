# Text Excuse Generator

## Table of Contents

- [Introduction](#introduction)
- [Uses](#uses)
    - [Running from Command Line](#running-from-command-line)
    - [Running with Command Line Arguments](#running-with-command-line-arguments)
        - [Sending a Text Message](#sending-a-text-message)
        - [Setting Up .env File](#setting-up-env-file)
        - [Saving a New Recipient](#saving-a-new-recipient)
    - [Importing as a Module](#importing-as-a-module)
        - [Installing with pip](#installing-with-pip)
        - [`generate_excuse()`](#generate_excuse-takes-in)
        - [`setup_env()`](#setup_env-takes-in)
        - [`add_recipient()`](#add_recipient-takes-in)
        - [`send_twilio_text()`](#send_twilio_text-takes-in)
- [Running](#running)
    - [Dependencies](#dependencies)
    - [Setting Up .env File](#setting-up-env-file-1)
    - [Running](#running-1)
- [Quality Assurance](#quality-assurance)
- [Suggestions](#suggestions)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Recently, I came across a reddit post on [r/ProgrammerHumor](https://www.reddit.com/r/ProgrammerHumor/) that had a comment that referenced [this repository](https://github.com/NARKOZ/hacker-scripts#readme). While not only being a pretty funny story and set of scripts, it also got me thinking about creating a script of my own to create excuses and text them to whoever I want/need to. Unlike the scripts that I took inspiration from: [hangover.py](https://github.com/NARKOZ/hacker-scripts/blob/master/python3/hangover.py) & [smack_my_bitch_up.py](https://github.com/NARKOZ/hacker-scripts/blob/master/python3/smack_my_bitch_up.py), that just picked excuses from a predetermined list, I decided to generate the excuses using [OpenAI's GPT-3.5-turbo](https://openai.com/blog/openai-api/) API, and I used [Twilio's API](https://www.twilio.com/docs/sms/quickstart/python) to send text messages. The program prompts the user (or can be passed in as arguments) for: the sender of the text, the recipient of the text, the 'problem', an excuse for the problem, and the option to send the generated message as a text. It also has a system to save phone numbers to names, so you can just type in a name instead of a phone number. Since the program uses OpenAI's [GPT-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5) model, it can generate a pretty good excuse to anyone for virtually anything! The program can be run normally, with command line arguments, or imported as a module into another python file. Since it can have command line arguments passed in to operate it, it can be used in other programs, such as a Bash script, or used in a cron job.

## Uses

There are three main ways to interact with the program: by running it normally, by running it with command line arguments, or by importing it into another python file.

Note: `[recipient]` can be a name or a case sensitive phone number: e.g. `Huck` or `+15555555555`. You must also set up your .env file (more details in [Dependencies](#setting-up-env-file)).

### Running from Command Line

I'd recommend just downloading [excuse_generator.py](../text_excuse_generator/excuse_generator.py) and running it from the command line. You can run it by typing:
```bash
python3 text_excuse_generator.py
```
If you just want the [excuse_generator.py](../text_excuse_generator/excuse_generator.py) file for a project, please also include the [LICENSE](../LICENSE) file in the same directory as [excuse_generator.py](../text_excuse_generator/excuse_generator.py).

When you run the program normally, it will ask you for the sender, recipient, problem, and excuse, and if you want to send the text message. It will then generate a text message, and send it to the recipient if chosen. If you input a name into recipient that isn't saved to the system yet when sending a text, it will ask you if you want to save it to the system. If you choose to save it, it will ask you for the phone number, and then save it to the system. You can also just use a phone number for the recipient field, and it will send the text to that number.

### Running with Command Line Arguments

You can also run the program with command line arguments. If you want to send the text message, you can add `--send` or `-s` as the last argument. All command line arguments longer than a single word need to be in parentheses. I'd recommend just downloading [excuse_generator.py](../text_excuse_generator/excuse_generator.py) and running it from the command line. If you just want the [excuse_generator.py](../text_excuse_generator/excuse_generator.py) file for a project, please also include the [LICENSE](../LICENSE) file in the same directory as [excuse_generator.py](../text_excuse_generator/excuse_generator.py).

#### **Sending a Text Message**

If you want to send a text with command line arguments, run:
```bash
python3 text_excuse_generator.py [sender] [recipient] [problem] [excuse] [--send_text_flag]
```
e.g.
```bash
python3 text_excuse_generator.py Me "Your mom" "I'm late to 😈" "Too many wizards around" -s
```
Omit the `[--send_text_flag]` if you don't want to send the text message.

#### **Setting Up .env File**
If you want to set up the .env file, run:
```bash
python3 text_excuse_generator.py [-e/--setup_env] [TWILIO_ACCOUNT_SID] [TWILIO_AUTH_TOKEN] [TWILIO_PHONE_NUMBER] [OPENAI_API_KEY]
```
e.g.
```bash
python3 text_excuse_generator.py -e "AC1234567890" "1234567890" "+15555555555" "sk-1234567890"
```

#### **Saving a New Recipient**

If you want to save a new recipient to the system, run:
```bash
python3 text_excuse_generator.py [-a/--add] [name] [phone_number]
```
e.g.
```bash
python3 text_excuse_generator.py -a "Your mom" +15555555555
```

### Importing as a Module

You can also import the program as a module into another python file. The `text_excuse_generator` module has  four functions: `generate_excuse()`, `setup_env()`, `add_recipient()`, & `send_twilio_text()`.

#### Installing with pip

Simply run:
```bash
pip install text-excuse-generator
```
To import the module into your python file, put this at the top of your file:
```python
from text_excuse_generator.excuse_generator import *
```
Or you can import the individual functions.

#### `generate_excuse()` takes in:
```python
generate_excuse(USER: str, RECIPIENT: str, PROBLEM: str, EXCUSE: str, SEND_TEXT: bool) -> str
```
`generate_excuse()` returns a string of the text message that was generated.

If you want to generate a text message, call the function like this:

```python
generate_excuse("user", "recipient", "problem", "excuse", True)
```
e.g.
```python
generate_excuse(user = "me", recipient = "your mom", problem = "I'm late to 😈", excuse = "Too many wizards around", send_text = True)
```
Make sure to put the fields before the variables when calling the function. Omit the `[--send_text_flag]` if you don't want to send the text message.

#### `setup_env()` takes in:
```python
setup_env(TWILIO_ACCOUNT_SID: str, TWILIO_AUTH_TOKEN: str, TWILIO_PHONE_NUMBER: str, OPENAI_API_KEY: str) -> bool
```
If you want to set up your .env file, call `setup_env()` like this:
```python
setup_env("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_PHONE_NUMBER", "OPENAI_API_KEY")
```
e.g.
```python
setup_env("AC1234567890abcdef1234567890abcdef", "1234567890abcdef1234567890abcdef", "+15555555555", "sk-1234567890")
```
`setup_env()` returns True if the .env file was successfully set up, and False if it wasn't (Invalid phone number).

#### `add_recipient()` takes in:
```python
add_recipient(NAME: str, PHONE_NUMBER: str) -> bool
```
If you want to save a new recipient to the system, call `add_recipient()` like this:
```python
add_recipient("new_recipient_name", "new_recipient_phone_number")
```
e.g.
```python
add_recipient("Your Mom", "+15555555555")
```
`add_recipient()` returns True if the recipient was successfully added to the system, and False if it wasn't (Invalid phone number or phone number is already in the system).

#### `send_twilio_text()` takes in:
```python
send_twilio_text(RECIPIENT_PHONE_NUMBER: str, MESSAGE: str) -> None
```
If you want to send a text message, call `send_twilio_text()` like this:
```python
send_twilio_text("recipient_phone_number", "message")
```
e.g.
```python
send_twilio_text("+15555555555", "Beep boop beep bop")
```

## Running

### Dependencies

#### Accounts

You'll need to create a [Twilio](https://www.twilio.com/try-twilio) account to get a phone number. You can either use the free trial phone number, or pay $1/month for a real phone number, but you'll need to verify any phone numbers you want to text with the trial account.

You'll also need to create an [OpenAI account](https://platform.openai.com/signup) to get an [API key](https://platform.openai.com/account/api-keys). You'll also need to give payment information to OpenAI to use the API, but with the GPT-3.5-Turbo model it's **extremely cheap**: $0.002/1000 tokens: at one word, punctuation, special character, or space per token. As of right now, I've sent ~30 requests to the OpenAI API, and I've only spent $0.02 so far!

Once you get these two accounts set up, you'll need to find out this information from Twilio:
- Account SID
- Auth Token
- Twilio Phone Number

And this information from OpenAI:
- OpenAI API Key

And then [set up the `.env` file](#setting-up-env-file-1) with this information.
#### Install

##### For Command Line Use

Double click [`dependencies`](../dependencies), or run `bash `[`dependencies`](../dependencies) or `./`[`dependencies`](../dependencies) in the root directory or to install the python dependencies. You must have [pip](https://pip.pypa.io/en/stable/installation/) installed to download the new dependencies. Also, you'll need to install [python](https://www.python.org/downloads/) yourself if you haven't already.

##### For Importing as a Module

If you just run:
```bash
pip install text-excuse-generator
```
The dependencies will be installed automatically, along with the rest of the module!

**[List of Dependencies](DEPENDENCIES.md)**

### Setting Up .env File

Either run the program without any arguments to manually input the information for the .env file, run with [command line arguments](#setting-up-env-file) to automatically input the information for the .env file, or pass in the correct parameters to the [`setup_env()`](#setup_env-takes-in) function in the `text_excuse_generator` module.

### Running

**YOU HAVE TO INSTALL THE DEPENDENCIES & SETUP THE `.env` FILE BEFORE TRYING TO RUN THE PROGRAM!!!**

Run `python3 text_excuse_generator.py` or `python3 text_excuse_generator.py [sender] [recipient] [problem] [excuse] [--send_text_flag]` in the command line in the source directory.

More detailed instructions are in the [Uses](#uses) section.

## Quality Assurance
All variable, function, class, module, & file names are written in [snake_case](https://en.wikipedia.org/wiki/Snake_case) to make sure everything is consistent, and all `const` variables are written in ALL-CAPS. The code is also quite commented and the variable names are quite verbose, so it should be easy enough to understand what's going on.

If there are any other/better ways to check for quality assurance, please let me know in the [suggestions](https://github.com/Huckdirks/Excuse_Text_Generator/discussions/new?category=suggestions)!

## Suggestions

If you have any suggestions about anything, please create a [new discussion in suggestions](https://github.com/Huckdirks/Excuse_Text_Generator/discussions/new?category=suggestions).

## Contributing

Contributions are always welcomed! Look at [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## License

The project is available under the [MIT](https://opensource.org/licenses/MIT) license.
