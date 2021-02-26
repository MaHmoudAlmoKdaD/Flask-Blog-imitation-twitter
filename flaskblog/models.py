from datetime import datetime
# when we say from flaskblog we say from(__init__)
# so we don't need to specifiy flaskblog.__init__ import bd
from flaskblog import db, login_manager

from flask import current_app
# we can generate a a secure time-sensitive token to ensure that only a specific 
# user who has access to the user's email can reset that password, to do that 
# we will be using the package itsdangerous .

# we can do that:
# s = serializer(secet_key, expired_by_second)
# token = s.dumps({'user_id': 1}).decode('utf-8') // dump : تفريغ | with s for string
# token
# s.loads(token)

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# -we need to inherit this class(UserMixin)  
# - توقع ان يكون نوذج المستخدم الخاص بك سمات واسليب معينة 
# تتوقع ان تكون تسمى
#  athunicated والتي ستعيد true 
#  اذا قدمو اوراق اعتماد صالحة 
#  يسمى اخر activate 
#  واخر يسمى anonymous
#  واخر دالة تسمى  get ID
# نستطيع اضافة هؤلاء بواسطة انفسنا لكن جميعها مشتركو بواسطة امتداد(extentios) 
# يزودنا بواسطة كلاس بسيط يسمى يمكننا وراثته  UserMixin
# ونضيف جميع الميثود والخصائص لاجل عملنا
# -it's going to expect for to be exact one is called is authenticated
# which will return true if they have provided vaild credentials
# another is called is actiavte another is called nonymous and  the last method called get ID 
from flask_login import UserMixin 

# this is for reloading the user from the user ID stored in the session(database)
@login_manager.user_loader
def user_load(user_id):
    return User.query.get(int(user_id))
    

# inerite the UserMixim in class User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    # our post attribute has a relationship to the post model and the 'Post' reference to Post model(class)
    # backref: is similar to adding another column to the Post model
    # what the backref allows us to do is when we have a post we can simply
    # use this attribute to get  the user who creates the post . 
    # lazy: just define when SQLAlchemy loads the data from the database
    # so True means that SQLAlchemy will load the data as necessary in one go
    # so this is convenient(ملائم) because with this relationship we will be able to simply use 
    # this post attribute to  get all of the posts created by individual user .
    # notice: that this is a relationship and not a column so if we were to actually 
    # look at our actual database stracture in some kind of SQL client 
    # would't see this post column here this is actually just running an additional
    # query in the background that will get all of the posts this user has created .
    # 'Post' references to class Post
    posts = db.relationship('Post', backref = 'author', lazy = True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    # dunder method or magic method: this specifically is how our object is printed 
    # whenever we print it out, so this and  __str__ method as well 
    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.image_file}'')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    # 'user.id': here we mean the table user cuz the class User is convert to table in database
    # so user references to table user in database .
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.content}')"
