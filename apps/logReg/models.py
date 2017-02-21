from __future__ import unicode_literals

from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
PASSWORD_REGEX = re.compile(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,})', re.MULTILINE)
name_regex = re.compile(r'[a-zA-Z]+', re.MULTILINE)

# Create your models here.
class Umanager(models.Manager):
    def reg(self, first, last, email, password, confirm):
        if not name_regex.match(first):
            return False
        elif not name_regex.match(last):
            return False
        elif not EMAIL_REGEX.match(email):
            return False
        elif not PASSWORD_REGEX.match(password):
            return False
        elif not password == confirm:
            return False
        else:
            password = password.encode()
            pwhash = bcrypt.hashpw(password, bcrypt.gensalt())
            return super(Umanager, self).create(first=first, last=last, email=email, pw_hash=pwhash)
    def log(self, email, password):
        password = password.encode()
        if len(User.objects.filter(email=email)) > 0:
            print "matching email was found"
            pwhash = User.objects.filter(email=email)[0].pw_hash
            print pwhash
            pwhash = pwhash.encode()
            if bcrypt.hashpw(password, pwhash) == pwhash:
                print "password matched"
                return User.objects.filter(email=email)[0].id
            else:
                return False
        else:
            return False
class User(models.Model):
    first = models.CharField(max_length=45)
    last = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = Umanager()
