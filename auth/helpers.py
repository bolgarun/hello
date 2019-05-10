from auth.exceptions import ValidationError
import hashlib
import binascii
import os
from iso3166 import countries
from sendgrid import SendGridAPIClient
from application.config import Config


sg = SendGridAPIClient(Config.API_KEY_SENDGRID)


def validate_nickname(nickname):
    if nickname.islower():
        return nickname
    raise ValidationError("Enter valid nickname")


def validate_email(email):
    if "@" in email:
        return email
    raise ValidationError("Enter valid email")


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('utf-8')
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000
        )
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('utf-8')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        provided_password.encode('utf-8'),
        salt.encode('utf-8'), 100000
        )
    pwdhash = binascii.hexlify(pwdhash).decode('utf-8')
    return pwdhash == stored_password


def validate_password(password):
    letter = False
    number = False
    up = False
    low = False
    for x in password:
        if x.isalpha():
            letter = True
        if x.isdigit():
            number = True
        if x.isupper():
            up = True
        if x.islower():
            low = True

    if letter is True and number is True and up is True and low is True:
        return password
    raise ValidationError("Enter valid password")


def check_if_letter(word):
    if word.isalpha():
        return word
    raise ValidationError("Enter valid first_name or last_name")


def validate_age(age):
    if age.isdigit():
        return age
    raise ValidationError("Enter valid age")


def validate_gender(gender):
    if gender == 'male' or gender == 'female':
        return gender
    raise ValidationError("Enter valid gender")


def validate_country(word):
    country = countries.get(word)
    return country[0]
