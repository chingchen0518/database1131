from django.db import models

# Create your models here.

class Classroom(models.Model):
    crid = models.AutoField(primary_key=True,default='0')
    quota = models.IntegerField(default=0)
    classroom_name = models.CharField(default="-", null=True, max_length=10)
    class Meta:
        db_table = 'classroom'

class Teacher(models.Model):
    tid = models.AutoField(primary_key=True,default=0)
    teacher_name = models.CharField(default="-", null=True, max_length=10)
    phone = models.CharField(default="-", null=True, max_length=10)
    line = models.CharField(default="-", null=True, max_length=20)

    class Meta:
        db_table = 'teacher'

class Class(models.Model):
    cid = models.AutoField(primary_key=True)
    category = models.CharField(default="-", null=True, max_length=20)
    subject = models.CharField(default="-", null=True, max_length=20)
    time = models.TimeField(null=True, blank=True)
    day = models.CharField(default="一", null=False, max_length=1)
    year = models.IntegerField(default=0)
    years_old = models.CharField(default="-", null=True, max_length=10)
    quota = models.IntegerField(default=0)
    crid = models.ForeignKey(Classroom, on_delete=models.CASCADE, to_field='crid', auto_created=False, unique=False,default='0')
    tid = models.ForeignKey(Teacher, to_field='tid',  on_delete=models.CASCADE, auto_created=False, default=0)
    periods = models.IntegerField(default=1)
    available = models.IntegerField(default=1)

    class Meta:
        db_table = 'class'
#
class Students(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(default="-", null=False, max_length=20)
    parent_name = models.CharField(default="-", null=False, max_length=20)
    hp = models.CharField(default="-", null=False, max_length=10)
    parent_hp = models.CharField(default="-", null=False, max_length=10)
    years_old = models.IntegerField(default=0)
    school = models.CharField(default="-", null=False, max_length=20)
    birthday = models.DateField(null=True,blank=True)
    remarks=models.TextField(default="-", null=True, max_length=1000)
    address = models.CharField(default="-", null=True, max_length=100)

    class Meta:
        db_table = 'students'

class Enrolled(models.Model):
    eid = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Students, on_delete=models.CASCADE, to_field='sid', auto_created=False, unique=False, default=0)
    cid = models.ForeignKey(Class, on_delete=models.CASCADE, to_field='cid', auto_created=False, unique=False,default=0)
    remark=models.TextField(default="-", null=True, max_length=1000)
    period = models.IntegerField(default=1)
    class Meta:
        db_table = 'enrolled'

class Category(models.Model):
    catid=models.AutoField(primary_key=True)
    category=models.CharField(default="-", null=True, max_length=1000)
    class Meta:
        db_table = 'category'

class Payment(models.Model):
    eid=models.ForeignKey(Enrolled, on_delete=models.CASCADE, to_field='eid', auto_created=False, unique=False, default=0)
    sid=models.ForeignKey(Students, on_delete=models.CASCADE, to_field='sid', auto_created=False, unique=False, default=0)
    cid=models.ForeignKey(Class, on_delete=models.CASCADE, to_field='cid', auto_created=False, unique=False, default=0)
    amount=models.IntegerField(default=0)
    date=models.DateField(null=True,blank=True)
    class Meta:
        db_table = 'payment'

class Semester(models.Model):
    semid=models.IntegerField(default=1111,primary_key=True)
    sem=models.IntegerField(default=1)
    real_year=models.IntegerField(default=111)
    semtext=models.CharField(default="-", null=True, max_length=100)
    class Meta:
        db_table = 'semester'

class Time(models.Model):
    tid=models.AutoField(primary_key=True)
    semid=models.ForeignKey(Semester, on_delete=models.CASCADE, to_field='semid', auto_created=False, unique=False, default=0)
    start=models.TimeField(null=True,blank=True)
    end=models.TimeField(null=True,blank=True)
    sequence=models.IntegerField(default=1)
    class Meta:
        db_table = 'time'

class Account(models.Model):
    aid=models.AutoField(primary_key=True)
    username=models.CharField(default="-", null=True, max_length=100)
    password=models.CharField(default="-", null=True, max_length=100)
    permission=models.IntegerField(default=0)
    class Meta:
        db_table = 'account'