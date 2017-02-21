import bcrypt
password= 'helloworld'
password = password.encode()
password2= 'helloworld'
password2 = password.encode()
pwhash = bcrypt.hashpw(password, bcrypt.gensalt())
if bcrypt.hashpw(password2, pwhash) == pwhash:
    print 'glory to god'