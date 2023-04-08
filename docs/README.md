# Text Excuse Generator

## Table of Contents

- [Introduction](#introduction)
- [Uses](#uses)
    - [Running from Command Line](#running-from-command-line)
    - [Running with Command Line Arguments](#running-with-command-line-arguments)
    - [Importing as a Module](#importing-as-a-module)
- [Running](#running)
    - [Dependencies](#dependencies)
    - [Setting Up .env File](#setting-up-env-file)
    - [Running](#running-1)
- [Quality Assurance](#quality-assurance)
- [Suggestions](#suggestions)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Recently, I came across a reddit post on [r/ProgrammerHumor](https://www.reddit.com/r/ProgrammerHumor/) that had a comment that referenced [this repository](https://github.com/NARKOZ/hacker-scripts#readme). While not only being a pretty funny story and set of scripts, it also got me thinking about creating a script of my own to create excuses and text them to whoever I want/need to. Unlike the scripts that I took inspiration from: [hangover.py](https://github.com/NARKOZ/hacker-scripts/blob/master/python3/hangover.py) & [smack_my_bitch_up.py](https://github.com/NARKOZ/hacker-scripts/blob/master/python3/smack_my_bitch_up.py), that just picked excuses from a predetermined list, I decided to generate the excuses using [OpenAI's GPT-3.5-turbo](https://openai.com/blog/openai-api/) API, and I used [Twilio's API](https://www.twilio.com/docs/sms/quickstart/python) to send text messages. The program prompts the user (or can be passed in as arguments) for: the sender of the text, the recipient of the text, the 'problem', an excuse for the problem, and the option to send the generated message as a text. It also has a system to save phone numbers to names, so you can just type in a name instead of a phone number. Since the program uses OpenAI's [GPT-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5) model, it can generate a pretty good excuse to anyone for virtually anything! The program can be run normally, with command line arguments, or imported as a module into another python file. Since it can have command line arguments passed in to operate it, it can be used in other programs, such as a BASH script, or used in a cron job.

## Uses

There are three main ways to interact with the program: by running it normally, by running it with command line arguments, or by importing it into another python file.

Note: Recipient can be a name or a case sensitive phone number: e.g. `Huck` or `+15555555555`. You must also set up your .env file (more details in [Dependencies](#setting-up-env-file)).

### Running from Command Line

When you run the program normally, it will ask you for the sender, recipient, problem, and excuse, and if you want to send the text message. It will then generate a text message, and send it to the recipient if chosen. If you input a name into recipient that isn't saved to the system yet when sending a text, it will ask you if you want to save it to the system. If you choose to save it, it will ask you for the phone number, and then save it to the system. You can also just use a phone number for the recipient field, and it will send the text to that number.

### Running with Command Line Arguments

You can also run the program with command line arguments. If you want to send the text message, you can add `--send` or `-s` as the last argument. All command line arguments longer than a single word need to be in parentheses.

`python3 text_excuse_generator.py [sender] [recipient] [problem] [excuse] [--send_flag]`

e.g. `python3 text_excuse_generator.py Me "Your mom" "I'm late to 😈" "Too many wizards around" -s`


If you want to save a new recipient to the system, run:

`python3 text_excuse_generator.py --add [name] [phone_number]`

e.g. `python3 text_excuse_generator.py -a "Your mom" +15555555555`

### Importing as a Module

You can also import the program as a module into another python file. The `text_excuse_generator` module has only one function: `generate_excuse()`. It takes in:

```python
generate_excuse(user: str, recipient: str, problem: str, excuse: str, send_text: bool, new_recipient_name: str, new_recipient_phone_number: str)
```

It returns a string of the text message that was generated. If you want to keep a field blank you must pass in an empty string `''`. 

If you want to generate a text message, call the function like this:

```python
generate_excuse("user", "recipient", "problem", "excuse", True)
```
Omit the `send_text` parameter if you don't want to send the text message.

If you want to save a new recipient to the system, call the function like this:
```python
generate_excuse('', '', '', '', False, "new_recipient_name", "new_recipient_phone_number")
```

## Running

### Dependencies

#### Accounts

You'll need to create a [Twilio](https://www.twilio.com/try-twilio) account to get a phone number. You can either use the free trial phone number, or pay $1/month for a real phone number, but you'll need to verify any phone numbers you want to text with the trial account. Once you get a phone number, you'll have to save the Account SID, Auth Token, and phone number in a `.env` file in the root directory. You can use the `personal_info.txt` file as a template.

You'll also need to create an [OpenAI account](https://platform.openai.com/signup) to get an [API key](https://platform.openai.com/account/api-keys). You'll also need to give payment information to OpenAI to use the API, but with the GPT-3.5-Turbo model it's **extremely cheap**: $0.002/1000 tokens, at one word, punctuation, special character, or space per token.

#### Install

Double click `dependencies`, or run `bash dependencies` or `./dependencies` in the root directory or to install the python dependencies. You must have [pip](https://pip.pypa.io/en/stable/installation/) installed to download the new dependencies. Also, you'll need to install [python](https://www.python.org/downloads/) yourself if you haven't already.

**[List of Dependencies](DEPENDENCIES.md)**

### Setting Up .env File

In the root directory, you'll need to rename [`personal_info.txt`](https://github.com/Huckdirks/Excuse_Text_Generator/blob/main/personal_info.txt) to `personal_info.env` and put your information from your Twilio & OpenAI accounts. You can manually put phone numbers in there if you want, or you could add it via the program.

### Running

**YOU HAVE TO INSTALL THE DEPENDENCIES & CONFIGURE YOUR .env FILE BEFORE TRYING TO RUN THE PROGRAM!!!**

Run `python3 text_excuse_generator.py` or `python3 text_excuse_generator.py [sender] [recipient] [problem] [excuse]` in the command line in the root directory.

e.g. `python3 text_excuse_generator.py Me "Your mom" "I'm late to 😈" "Too many wizards around"`

## Quality Assurance
All variable, function, class, module, & file names are written in [snake_case](https://en.wikipedia.org/wiki/Snake_case) to make sure everything is consistent, and all `const` variables are written in ALL-CAPS. The code is also quite commented and the variable names are quite verbose, so it should be easy enough to understand what's going on.

If there are any other/better ways to check for quality assurance, please let me know in the [suggestions](https://github.com/Huckdirks/Excuse_Text_Generator/discussions/new?category=suggestions)!

## Suggestions

If you have any suggestions about anything, please create a [new discussion in suggestions](https://github.com/Huckdirks/Excuse_Text_Generator/discussions/new?category=suggestions).

## Contributing

Contributions are always welcomed! Look at [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## License

The project is available under the [MIT](https://opensource.org/licenses/MIT) license.
