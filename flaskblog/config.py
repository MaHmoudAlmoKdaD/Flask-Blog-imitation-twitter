import os 
class Config:
    # this secret key : it will protect against modifying cookies 
    # and croos-site request forgery(تزوير) attacks and think like that
    # note(to set secret key go to py amd write the commend 
    # import secrets
    # secrets.token_hex(16) --this tal=ke int and
    #  return String value[we can don't pass anything]--)
    SECRET_KEY = '15d8d036dd7d909cdf26d05ccbbbad6f'#os.environ.get('SECRET_KEY') #

    # write this line to avoid the warrning during import the db from Cmd.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # /// (three slash means relativa path from the current file)
    # //// (four slash means absolute path)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # how our app send mail so we are need gonna need a mail server port
    # whether to use TLS(Transport Layer Security) and also a username and password for that server.
    # DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mahmoud.almokdad.technology.hang@gmail.com'#os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = 'hanger015794861794795$'#os.environ.get('EMAIL_PASS')
