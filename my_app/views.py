from django.shortcuts import HttpResponse, render, redirect
import json,os
from django.db.models import Max
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
import random
from collections import Counter


from django.http import JsonResponse
from django.db import connection
from django.shortcuts import render

from django.shortcuts import render
import hashlib

#include table
from my_app.models import Students, Enrolled, Class, Classroom, Teacher, Category, Payment, Time, Account
from my_app.models import Semester

# Create your views here.
def homepage(request):
    class_list = Class.objects.raw('''SELECT DISTINCT cid,time,years_old,subject,category,day,available,start
                                        FROM Class JOIN Time ON Class.time=Time.start
                                        WHERE available=1
                                        ORDER BY time''')

    classroom=[1,2,3,4,5,6]
    Days=['一','二','三','四','五','六','日']

    time = Time.objects.raw('SELECT DISTINCT * FROM Time WHERE semid_id=(SELECT MAX(semid) FROM Semester) ORDER BY start')
    return render(request, 'homepage.html',{'class':class_list,'Days':Days,'time':time,'classroom':classroom})


def student_list(request):
    student_list = Students.objects.raw('''SELECT *,
                                            CASE 
                                                WHEN EXISTS (SELECT eid,period,COUNT(amount) AS paid_period,
                                                          CASE WHEN (COUNT(amount)>=period) THEN 1
                                                          ELSE 0
                                                          END AS pay_or_not
                                                        FROM Enrolled
                                                        LEFT OUTER JOIN Payment ON Enrolled.eid=Payment.eid_id 
                                                        WHERE Enrolled.sid_id=s.sid
                                                        GROUP BY Enrolled.eid,Enrolled.period
                                                        HAVING COUNT(Payment.amount) < Enrolled.period
                                                        ) THEN 0
                                                ELSE 1
                                        END AS fully_paid
                                        FROM Students s ORDER BY years_old''')

    tingkat_ada_convert = ['xxx','國小一','國小二','國小三','國小四','國小五','國小六','國一','國二','國三','高一','高二','高三']
    tingkat_tiada_convert = ['xxx','兒美小','兒美中','兒美大','留學','社會人士','其他']

    return render(request, 'student_list.html',{'student_list':student_list,'tingkat':tingkat_ada_convert,'tingkat_tiada':tingkat_tiada_convert})

def student_detail(request,sid):
    student_detail = Students.objects.raw('''SELECT * FROM Students WHERE sid=%s''',[sid])
    class_taken= Class.objects.raw('''SELECT year,eid,cid,day,time,remark,period,subject,category,Enrolled.cid_id,
                                        CASE
                                            WHEN (SELECT COUNT(amount) AS payment FROM Payment WHERE sid_id=%s AND Payment.eid_id=Enrolled.eid) > 0 THEN (SELECT COUNT(amount) FROM Payment WHERE Payment.eid_id=Enrolled.eid)
                                            ELSE 0
                                        END AS payment
                                        FROM Enrolled
                                        JOIN Class ON Class.cid = Enrolled.cid_id
                                        WHERE Enrolled.sid_id = %s
                                        ''',(sid,sid))

    tingkat_ada_convert = ['xxx', '國小一', '國小二', '國小三', '國小四', '國小五', '國小六', '國一', '國二', '國三',
                           '高一', '高二', '高三']
    tingkat_tiada_convert = ['xxx', '兒美小', '兒美中', '兒美大', '留學', '社會人士', '其他']

    return render(request, 'student_detail.html',{'student_detail': student_detail[0],'tingkat':tingkat_ada_convert,'tingkat_tiada':tingkat_tiada_convert,'class_taken':class_taken})

def class_list(request,available):

    class_list = Teacher.objects.raw('''SELECT Class.*, Teacher.*,Semester.*, COALESCE(enrolled_counts.tuple_count, 0) AS student_count,Class.quota - COALESCE(enrolled_counts.tuple_count, 0) AS remain
                                        FROM Class LEFT JOIN Teacher ON Class.tid_id = Teacher.tid
                                        LEFT JOIN (SELECT cid_id, COUNT(*) AS tuple_count FROM Enrolled GROUP BY cid_id
                                        ) AS enrolled_counts ON enrolled_counts.cid_id = Class.cid 
                                        JOIN Semester ON Semester.semid=Class.year 
                                        WHERE available=%s
                                        ORDER BY year DESC,
                                                CASE day
                                                    WHEN '一' THEN 1
                                                    WHEN '二' THEN 2
                                                    WHEN '三' THEN 3
                                                    WHEN '四' THEN 4
                                                    WHEN '五' THEN 5
                                                    WHEN '六' THEN 6
                                                    ELSE 7
                                                END,time
                                        ;''',[available])

    semester = Semester.objects.raw('SELECT * FROM Semester ORDER BY semid DESC')

    return render(request, 'class_list_table.html', {'class_list': class_list, 'available':available,'semester':semester})

def class_detail(request,cid):
    class_detail = Teacher.objects.raw('''SELECT Class.*, Teacher.*,Classroom.classroom_name, COALESCE(enrolled_counts.tuple_count, 0) AS student_count,Class.quota - COALESCE(enrolled_counts.tuple_count, 0) AS remain
                                            FROM Class LEFT JOIN Teacher ON Class.tid_id = Teacher.tid
                                            LEFT JOIN (SELECT cid_id, COUNT(*) AS tuple_count FROM Enrolled GROUP BY cid_id
                                            ) AS enrolled_counts ON enrolled_counts.cid_id = Class.cid JOIN Classroom ON Classroom.crid=Class.crid_id WHERE Class.cid=%s''',[cid])

    students = Students.objects.raw('SELECT * FROM Students,Enrolled WHERE Enrolled.sid_id=Students.sid AND Enrolled.cid_id=%s',[cid])
    return render(request, 'class_detail.html',{'class_detail': class_detail[0],'students':students})

def add_category(request):
    if 'login' in request.session and request.session['login'] == 1:
        if 'permission' in request.session and request.session['permission'] == 1:
            category = Category.objects.raw('SELECT * FROM Category')

            return render(request, 'add_category.html',{'category':category})
        else:
            return render(request, 'no_access.html')
    else:
        return render(request, 'no_access.html')

def add_category_action(request):
    category = request.POST['category']

    try:
        latest_id = Category.objects.latest('catid')
        latest_id = latest_id.catid
        latest_id = latest_id + 1
    except ObjectDoesNotExist:
        latest_id=0

    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Category VALUES (%s, %s)', (latest_id, category))

    add_category=f'/add_category'
    return redirect(add_category)  # back to homepage

def delete_category_action(request,catid):
    Category.objects.filter(catid=catid).delete()

    add_category=f'/add_category'
    return redirect(add_category)  # back to homepage

def add_class(request):
    category = Category.objects.raw('SELECT * FROM Category')
    teacher = Teacher.objects.raw('SELECT tid,teacher_name FROM Teacher')
    classroom = Classroom.objects.raw('SELECT * FROM Classroom')

    time = Time.objects.raw('SELECT * FROM Time WHERE semid_id=(SELECT MAX(semid) FROM Semester) ORDER BY start')
    year = Semester.objects.raw('SELECT * FROM Semester WHERE semid=(SELECT MAX(semid) FROM Semester)')

    if 'login' in request.session and request.session['login'] == 1:
        if 'permission' in request.session and request.session['permission'] == 1:
            return render(request, 'add_class.html',
                          {'categories': category, 'teachers': teacher, 'classrooms': classroom, 'time': time,
                           'years': year[0]})
        else:
            return render(request, 'no_access.html')
    else:
        return render(request, 'no_access.html')


def add_class_action(request):
    category = request.POST['category']
    subject = request.POST['subject']
    time= request.POST['time']
    year = request.POST['year']
    quota = request.POST['quota']
    classroom = request.POST['classroom']
    teacher= request.POST['teacher']
    day = request.POST['day']
    years_old = request.POST['age']
    class_period = request.POST['class_period']
    try:
        latest_id = Class.objects.latest('cid')
        latest_id = latest_id.cid
        cid = latest_id + 1
    except ObjectDoesNotExist:
        cid = 0


    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Class (cid,category,subject,time,year,quota,crid_id,tid_id,day,years_old,periods,available) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)', (cid,category,subject,time,year,quota,classroom,teacher,day,years_old,class_period,1))

    return redirect('/class_list/1')#back to homepage

def edit_class(request,cid):
    class_detail = Class.objects.raw('SELECT * FROM Class WHERE cid=%s',[cid])
    category = Category.objects.raw('SELECT * FROM Category')
    teacher = Teacher.objects.raw('SELECT * FROM Teacher')
    classroom = Classroom.objects.raw('SELECT * FROM Classroom')

    class_year = Class.objects.raw('SELECT * FROM Class WHERE cid=%s',[cid])[0].year

    time = Time.objects.raw('SELECT * FROM Time WHERE semid_id=%s ORDER BY start',[class_year])

    year = Semester.objects.raw('SELECT * FROM Semester WHERE semid=%s',[class_year])

    return render(request, 'edit_class.html',{'class_detail':class_detail[0],'categories':category,'teachers':teacher,'classrooms':classroom,'time':time,'years':year[0]})

def edit_class_action(request,cid):
    category = request.POST['category']
    subject = request.POST['subject']
    time= request.POST['time']
    year = request.POST['year']
    quota = request.POST['quota']
    classroom = request.POST['classroom']
    teacher= request.POST['teacher']
    day = request.POST['day']
    years_old = request.POST['age']
    class_period = request.POST['class_period']

    with connection.cursor() as cursor:
        cursor.execute('UPDATE Class SET category=%s, subject=%s, time=%s, year=%s, quota=%s, crid_id=%s, tid_id=%s, day=%s, years_old=%s,periods=%s WHERE cid=%s', (category,subject,time,year,quota,classroom,teacher,day,years_old,class_period,cid,))

    class_detail = f'/class_detail/{cid}'

    return redirect(class_detail)#back to homepage

def delete_class_action(request,cid):
    Class.objects.filter(cid=cid).delete()

    return redirect('/class_list/1')#back to homepage

def end_class_action(request,cid):
    with connection.cursor() as cursor:
        cursor.execute('UPDATE Class SET available=0 WHERE cid=%s',[cid])

    return redirect('/class_list/1')#back to homepage

def recover_class_action(request,cid):
    with connection.cursor() as cursor:
        cursor.execute('UPDATE Class SET available=1 WHERE cid=%s',[cid])
    return redirect('/class_list/0')  # back to homepage

def copy_class(request,cid):
    class_detail = Class.objects.raw('SELECT * FROM Class WHERE cid=%s', [cid])
    category = Category.objects.raw('SELECT * FROM Category')
    teacher = Teacher.objects.raw('SELECT * FROM Teacher')
    classroom = Classroom.objects.raw('SELECT * FROM Classroom')

    time = Time.objects.raw('SELECT * FROM Time WHERE semid_id=(SELECT MAX(semid) FROM Semester) ORDER BY sequence')
    year = Semester.objects.raw('SELECT * FROM Semester ORDER BY semid DESC')

    return render(request, 'copy_class.html',
                  {'class_detail': class_detail[0], 'categories': category, 'teachers': teacher,
                   'classrooms': classroom, 'time': time, 'years': year[0]})

def copy_class_action(request):
    category = request.POST['category']
    subject = request.POST['subject']
    time = request.POST['time']
    year = request.POST['year']
    quota = request.POST['quota']
    classroom = request.POST['classroom']
    teacher = request.POST['teacher']
    day = request.POST['day']
    years_old = request.POST['age']
    class_period = request.POST['class_period']

    try:
        latest_id = Class.objects.latest('cid')
        latest_id = latest_id.cid
        cid = latest_id + 1
    except ObjectDoesNotExist:
        cid = 0


    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Class VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)', (cid,category,subject,time,year,quota,classroom,teacher,day,years_old,class_period,1))

    class_detail = f'/class_detail/{cid}'

    return redirect(class_detail)  # back to homepaged


def add_teacher(request):
    if 'login' in request.session and request.session['login'] == 1:
        if 'permission' in request.session and request.session['permission'] == 1:
            teacher = Teacher.objects.raw('SELECT * FROM Teacher')

            return render(request, 'add_teacher.html',{'teacher':teacher})
        else:
            return render(request, 'no_access.html')
    else:
        return render(request, 'no_access.html')

def add_teacher_action(request):
    name = request.POST['name']
    phone = request.POST['phone']
    line = request.POST['line']
    try:
        latest_id = Teacher.objects.latest('tid')
        latest_id = latest_id.tid
        latest_id = latest_id + 1
    except ObjectDoesNotExist:
        latest_id = 0

    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Teacher VALUES (%s, %s, %s, %s)', (latest_id,name,line,phone))

    add_teacher=f'/add_teacher'
    return redirect(add_teacher)#back to homepage

def delete_teacher_action(request,tid):

    Teacher.objects.filter(tid=tid).delete()

    add_teacher=f'/add_teacher'
    return redirect(add_teacher)#back to homepage


def add_enroll(request,cid):
    student_list = Students.objects.raw('''SELECT sid,name FROM Students EXCEPT
                                        SELECT DISTINCT sid,name FROM Students,Enrolled 
                                        WHERE Students.sid = Enrolled.sid_id and Enrolled.cid_id=%s''',[cid])
    student_enrolled = Students.objects.raw('''SELECT DISTINCT sid,name FROM Students,Enrolled 
                                            WHERE Students.sid = Enrolled.sid_id and Enrolled.cid_id=%s''', [cid])

    return render(request, 'add_enroll.html',{'student_list':student_list,'student_enrolled':student_enrolled,'cid':cid})

def add_enroll_action(request,cid):
    new_students = request.POST.getlist('student')

    period=Class.objects.raw('SELECT * FROM Class WHERE cid=%s',[cid])
    period=period[0].periods

    for student_id in new_students:
        try:
            latest_id = Enrolled.objects.latest('eid')
            latest_id = latest_id.eid
            latest_id = latest_id + 1
        except ObjectDoesNotExist:
            latest_id = 0
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO Enrolled (eid,cid_id,sid_id,remark,period) VALUES (%s, %s, %s, %s,%s)', (latest_id,cid,student_id,"-",period))



    class_detail=f'/class_detail/{cid}'

    return redirect(class_detail)#back to homepage

def delete_enrolled_student(request,sid,cid):

    Enrolled.objects.filter(sid_id=sid, cid_id=cid).delete()

    class_detail=f'/class_detail/{cid}'
    return redirect(class_detail)#back to previous page

def delete_enrolled_student_from_class_detail(request,cid):
    student_to_delete = request.POST.getlist('enrolled_student')


    for i in student_to_delete:
        Enrolled.objects.filter(sid_id=i, cid_id=cid).delete()

    class_detail = f'/class_detail/{cid}'
    return redirect(class_detail)  # back to previous page


def edit_student_status(request,sid,cid):

    remark = Enrolled.objects.raw('SELECT * FROM Enrolled WHERE sid_id=%s AND cid_id=%s',[sid,cid])

    return render(request, 'edit_student_status.html',{'remark':remark[0]})

def edit_student_status_action(request,sid,cid):
    remark = request.POST['remark']

    with connection.cursor() as cursor:
        cursor.execute('UPDATE Enrolled SET remark=%s WHERE cid_id=%s AND sid_id=%s', (remark, cid, sid))

    class_detail = f'/class_detail/{cid}'
    return redirect(class_detail)  # back to homepage

def upload_payment(request,eid):
    students=Class.objects.raw('''SELECT name,cid,category,subject,eid,sid
                                    FROM Students,Enrolled,Class 
                                    Where Students.sid=Enrolled.sid_id 
                                    AND Enrolled.cid_id=Class.cid 
                                    AND Enrolled.eid=%s
                                  ''',[eid])
    return render(request, 'upload_payment.html',{'student':students[0]})

def get_file_extension(uploaded_file):
    filename, file_extension = os.path.splitext(uploaded_file.name)
    return file_extension.lower()

def upload_payment_action(request,eid,sid,cid):
    amount=request.POST['amount'];
    date=request.POST['date'];


    if request.method == 'POST' and request.FILES['receipt']:
        file = request.FILES['receipt']
        file_extension=get_file_extension(file)

        # 看這堂課有幾個payment
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(amount) AS num FROM Payment WHERE Payment.eid_id=%s',[eid])
            latest_payment = cursor.fetchall()
            latest_payment = latest_payment[0][0]+1

        # 看學生名字
        students = Students.objects.raw('SELECT sid,name FROM Students WHERE sid=%s',[sid])
        student_name = students[0].name

        # 看課程名字
        class_detail = Class.objects.filter(cid=cid).values('cid', 'subject', 'year')
        semester=class_detail[0]['year']
        class_name = class_detail[0]['subject']

        # 設置文件上傳的目錄
        upload_dir = 'my_app/static/img/receipt/'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        # 構造新的文件路徑，將文件名更改為 "xxx"

        new_file_path = f'{upload_dir}{student_name}_{class_name}({semester})_{latest_payment}{file_extension}'
        # 寫入文件到指定目錄
        with open(new_file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO Payment (eid_id,date,amount) VALUES  (%s,%s,%s)', (eid,date,amount))

    previous_page = f'/student_detail/{sid}'
    return redirect(previous_page)#back to homepage

def add_student(request):
    if 'login' in request.session and request.session['login'] == 1:
        if 'permission' in request.session and request.session['permission'] == 1:

            return render(request, 'add_student.html')
        else:
            return render(request, 'no_access.html')
    else:
        return render(request, 'no_access.html')

def add_student_action(request):
    name=request.POST['name']
    hp=request.POST['hp']
    parent_name=request.POST['parent_name']
    parent_hp=request.POST['parent_hp']
    years_old=request.POST['years_old']
    school=request.POST['school']
    birthday=request.POST['birthday']
    address=request.POST['address']
    remarks=request.POST['remarks']

    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Students (name,hp,parent_name,parent_hp, years_old,school,birthday,address,remarks) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (name,hp,parent_name,parent_hp, years_old,school,birthday,address,remarks))

    student_list_page='/student_list'
    return  redirect(student_list_page)#back to homepage

def edit_student(request,sid):
    if 'login' in request.session and request.session['login'] == 1:
        if 'permission' in request.session and request.session['permission'] == 1:
            Student = Students.objects.raw('Select * FROM Students WHERE sid=%s',[sid])

            return render(request, 'edit_student.html',{'student':Student[0]})
        else:
            return render(request, 'no_access.html')
    else:
        return render(request, 'no_access.html')

def edit_student_action(request,sid):
    name=request.POST['name']
    hp=request.POST['hp']
    parent_name=request.POST['parent_name']
    parent_hp=request.POST['parent_hp']
    years_old=request.POST['years_old']
    school=request.POST['school']
    birthday=request.POST['birthday']
    address=request.POST['address']
    remarks=request.POST['remarks']

    with connection.cursor() as cursor:
        cursor.execute('UPDATE Students SET name=%s,hp=%s,parent_name=%s,parent_hp=%s,years_old=%s,school=%s,birthday=%s,address=%s,remarks=%s WHERE sid=%s',(name, hp, parent_name, parent_hp, years_old, school, birthday, address, remarks,sid))

    student_detail=f'/student_detail/{sid}'
    return redirect(student_detail)#back to homepage

def delete_student_action(request,sid):

    Students.objects.filter(sid=sid).delete()

    student_list = f'/student_list'
    return redirect(student_list)  # back to homepage

def add_time(request):
    if 'login' in request.session and request.session['login'] == 1:
        if 'permission' in request.session and request.session['permission'] == 1:
            years=Semester.objects.raw('SELECT * FROM Semester ORDER BY semid DESC')
            time = Time.objects.raw('SELECT * FROM Time WHERE semid_id=(SELECT MAX(semid) FROM Semester) ORDER BY start')

            return render(request, 'add_time.html',{'years':years[0],'time':time})
        else:
            return render(request, 'no_access.html')
    else:
        return render(request, 'no_access.html')

def add_time_action(request,years):

    start  = request.POST['start']
    duration = float(request.POST['duration'])
    start_str = datetime.strptime(start , '%H:%M')

    # timedelta(hours=1, minutes=30)
    if(duration % 1 == 0.5):
        hour = duration-0.5
        end_str = start_str + timedelta(hours=hour,minutes=30)
    else:
        end_str = start_str + timedelta(hours=duration)

    end = end_str.strftime('%H:%M')

    next_sequence = 1


    latest_timeid = Time.objects.raw('SELECT * FROM Time ORDER BY time_id DESC')[0]
    next_timeid = latest_timeid.time_id+1

    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Time (time_id, start, sequence, semid_id, "end") VALUES (%s, %s, %s, %s, %s)',(next_timeid,start,next_sequence,years,end))

    add_time=f'/add_time'
    return redirect(add_time)#back to homepage

def delete_time_action(request,tid):

    Time.objects.filter(time_id=tid).delete()

    add_time=f'/add_time'
    return redirect(add_time)#back to homepage
def sem_convert(request):
    if 'login' in request.session and request.session['login'] == 1:
        if 'permission' in request.session and request.session['permission'] == 1:
            years = Semester.objects.raw('SELECT * FROM Semester ORDER BY semid DESC')

            new_year = 0
            if years[0].sem == 4:
                new_year = years[0].semid + 7
            return render(request, 'sem_convert.html', {'years': years[0]})
            # return render(request, 'no_access.html')

        else:
            return render(request, 'no_access.html')
    else:
        return render(request, 'no_access.html')


def sem_convert_action(request):
    semid  = request.POST['next_sem']
    sem = int(semid) % 10
    real_year = int(semid) // 10

    text=['上','寒','下','暑']
    semText = f'{real_year}{text[sem-1]}'

    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Semester (semid, real_year, sem, semText) VALUES (%s, %s, %s, %s)',(semid, real_year, sem, semText))


    if sem == 4:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE Students SET years_old=years_old+1 WHERE years_old between 7 AND 17')

    sem_convert = f'/sem_convert'
    return redirect(sem_convert)#back to homepage

def login_page(request):
    # data="lee123456"
    # a=hashlib.md5(data.encode()).hexdigest()
    #
    # with connection.cursor() as cursor:
    #     cursor.execute('INSERT INTO Account (aid, username, password, permission) VALUES (%s, %s, %s, %s)',(2,'ching2chen',a,1))

    return render(request, 'login_page.html')

def login_page_action(request):
    username = request.POST['username']
    password = request.POST['password']

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    account_data = Account.objects.raw('SELECT * FROM Account WHERE username=%s AND password=%s',[username,hashed_password])

    if account_data:
        request.session['username']=username
        request.session['login'] = 1
        request.session['permission'] = account_data[0].permission

        if 'login' in request.session and request.session['login'] == 1:
            student_list = f'/student_list'
            return redirect(student_list)
        else:
            return redirect('/login_page')


    else:
        return redirect('/login_page')

def logout_action(request):
    request.session.flush()
    return redirect('/')

def add_account(request,repeat):

    if 'login' in request.session and request.session['login'] == 1:
        # return render(request, 'no_access.html')
        return render(request, 'add_account.html',{'repeat':repeat})
    else:
        return render(request, 'no_access.html')


def add_account_action(request):
    username = request.POST['username']
    password = request.POST['password']
    permission = request.POST['permission']

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    # account=Account.objects.raw('SELECT * FROM Account WHERE username=%s',[username])
    account = Account.objects.filter(username=username).exists()

    if account:
        add_account = f'/add_account/1'
        return redirect(add_account)
    else:
        try:
            latest_id = Account.objects.latest('aid')
            latest_id = latest_id.aid
            latest_id = latest_id + 1
        except ObjectDoesNotExist:
            latest_id = 0

        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO Account (aid,username, password, permission) VALUES (%s, %s, %s, %s)',(latest_id,username,hashed_password,permission))

        add_account = f'/add_account/2'
        return redirect(add_account)

def statics(request):
    # 查詢所有學生的年齡

    age_mapping = {
        51: "兒美小",
        52: "兒美中",
        53: "兒美大",
        7: "國小一",
        8: "國小二",
        9: "國小三",
        10: "國小四",
        11: "國小五",
        12: "國小六",
        13: "國一",
        14: "國二",
        15: "國三",
        16: "高一",
        17: "高二",
        18: "高三",
        54: "留學",
        55: "社會人士",
        56: "其他"
    }
    # 提取所有學生的年齡
    students = Students.objects.values_list('years_old', flat=True)

    # 統計每個年齡的學生數量
    age_count = {label: 0 for label in age_mapping.values()}

    for age in students:
        if age in age_mapping:
            age_count[age_mapping[age]] += 1

    context = {
        'age_count': age_count
    }

    # labels = ['XX6', 'XX7', 'XX8', 'XX9', 'XX10', 'XX11', 'XX12', 'XX13', 'XX14', 'XX15', 'XX16', 'XX17', 'XX18']
    # data = ['1','2','3']
    #
    # context = {
    #     'labels': labels,
    #     'data': data,
    # }

    return render(request, 'statics.html', {'data': context})

