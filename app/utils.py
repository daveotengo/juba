import random
import string

from flask import render_template
from flask_mail import Message

from app import mail


def gen_pass():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    all = lower + upper + num + symbols
    temp = random.sample(all, 16)
    password = "".join(temp)
    return password;

characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
#you may change length to actual value
# temp = random.sample(all,16)
# password = "".join(temp)

#@staticmethod
def generate_random_password():
    ## length of password from the user
    length = int(input("Enter password length: "))

    ## shuffling the characters
    random.shuffle(characters)

    ## picking random characters from the list
    password = []
    for i in range(length):
        password.append(random.choice(characters))

    ## shuffling the resultant password
    random.shuffle(password)

    ## converting the list to string
    ## printing the list
    print("".join(password))


def send_email(user):
    token = user.get_reset_token()
    msg = Message()
    msg.subject = "Login System: Password Reset Request"
    msg.sender = 'username@gmail.com'
    msg.recipients = [user.email]
    print("printing user before rendering")
    print(user)
    msg.html = render_template('email_template.html', user = user, token = token)

    mail.send(msg)