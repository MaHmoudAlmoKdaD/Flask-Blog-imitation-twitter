import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import  mail

# convert the picture to code(hexadecimal) and save it
def save_picture(form_picture):
    # ستضع وظيفة الصورة الامنة لحفظ المتخدمين الذين تم تحميل الصورة اليهم
    # لا نريد الاحتفاظ باسم الصورة لانه قد يتصادم مع اسم صورة اخرى موجودة بالفعل
    # سنختار اسم للصورة عشوائيا مع شي مثل 
    # random hex(token_hex from secrets) /import secrets
    random_hex = secrets.token_hex(8)
    # والان نريد التاكد اننا نحفظ هذا الملف بنفس الطريقة
    # مع الامتداد الخاص به سواء كان PNG او JPG
    # وللحصول على امتداد الملف الذي حمله المستخدم سنستورد 
    # import os (operating system)
    # -------------------------------
    # والام يمكننا استخدام وظيفة تحويل المسار , مسار نظام التشغيل للحصول على الامتداد
    # حيث هذ الوظيفة تعيد قيمتين اسم الملف بدون الامتداد والامتداد نفسه
    # للحصول على الاثنين سنقول
    # note: متغير يمكننا وضع اندرسكور بدل اسم المتغير
    # we can replace file_name by _
    # we pass in splitext(اسم الملف)
    file_name, file_extention = os.path.splitext(form_picture.filename)
    # الان سنجمع بين الرقم العشوائي وامتادا الملف-الصورة-
    picture_file_name = random_hex + file_extention
    # الان نحتاج للوصول للمسار الكامل حتى يعرف بايثون مكان حفظها
    # وسنستخدم الدالة التي تعطينا المسار على طول الطريق الى موقعنا اذا كنا نريد حفظ الصورة في صورنا الشخصية داخل المجلد
    # نحن نضم الى ذلك جذر نقطة التطبيق app.root_path
    # الذي سيعطينا المسار الكامل وصولا لدليل الحزمة الخاص بنا
    # 'static/profile_pics وسنضم الى ذلك مجلدنا الذي فية صور الملف الشخصي
    # ثم نضم اسم ملف الصورة الشخصي 
    # os يساعد بتسلسل ذلك بشكل صحيح في مسار واحد طويل
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_file_name)
    # سنقوم بتغيير حجم الصورة قبل حفظها
    output_size = (125, 125)
    # سنفتح الصورة التي مررناها الى ال function
    i = Image.open(form_picture)
    # تغيير حجم الصورة
    i.thumbnail(output_size)  
    # thumbnail : ظفر الابهام
    # thumbnails : صور مصغرة
    
    # والان نحفظ الصورة في المسار الذي انشاناه 
    i.save(picture_path)

    return picture_file_name


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='mahmoud.almokdad.technology.hang@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

