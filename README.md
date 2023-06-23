# Flask Homework Assignment

In class we build up a trivial Flask application and demonstrated XSS, CSRF
and SQL injection attacks against it.

This repo contains the code from the class code-along, which did patch those
three vulnerabilities, but still has a host of other security problems for
you to fix up.

Look through the code for the word "Homework" in comments and complete the
assigned tasks. Most of them involve validations and moving secrets to the
environment. However, there are many more opportunities in this code for
you to apply other security principles. Identify as many as you can and make
this application as secure as you can.

Find a good linter that knows about security, and find a classmate so you
can do mutual code reviews.

## Setup

1. Fork this repo
2. Clone your fork
3. Create a virtualenv: `python3 -m venv env`
4. Enter the environment: `source env/bin/activate` (will be different on Windows)
5. Install the requirements: `pip install -r requirements.txt`
6. Run the app: `FLASK_ENV=development flask run`

Have fun!
