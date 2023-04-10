from setuptools import setup, find_packages
from os.path import dirname, join

# Get the long description from the README file
README_PATH = join(dirname(__file__), "docs/README.md")

with open(README_PATH, "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name = "text_excuse_generator",
    version = "1.0.0",
    author = "Huck Dirksmeier",
    author_email = "Huckdirks@gmail.com",
    description = "Uses Open AI's GPT-3.5 model to create an excuse from given parameters & text it",
    long_description = LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    packages = find_packages(),
    install_requires = ["python-dotenv", "twilio", "openai", "phonenumbers"],
    keywords = ["text excuse generator", "openai", "twilio", "text message", "GPT-3.5"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.8"
)