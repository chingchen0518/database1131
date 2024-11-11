"""
URL configuration for tuition_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
import my_app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',my_app.views.homepage, name='homepage'),

    #學生相關
    path('student_list', my_app.views.student_list, name='student_list'),
    path('student_detail/<int:sid>', my_app.views.student_detail, name='student_detail'),

    #課程相關
    path('class_list/<int:available>', my_app.views.class_list, name='class_list'),
    path('class_detail/<int:cid>', my_app.views.class_detail, name='class_detail'),

    path('add_class', my_app.views.add_class, name='add_class'),
    path('add_class_action', my_app.views.add_class_action, name='add_class_action'),
    path('edit_class/<int:cid>', my_app.views.edit_class, name='edit_class'),
    path('edit_class_action/<int:cid>', my_app.views.edit_class_action, name='edit_class_action'),
    path('delete_class_action/<int:cid>', my_app.views.delete_class_action, name='delete_class_action'),
    path('end_class_action/<int:cid>', my_app.views.end_class_action, name='end_class_action'),
    path('recover_class_action/<int:cid>', my_app.views.recover_class_action, name='recover_class_action'),

    path('copy_class/<int:cid>', my_app.views.copy_class, name='copy_class'),
    path('copy_class_action', my_app.views.copy_class_action, name='copy_class_action'),

    path('add_teacher', my_app.views.add_teacher, name='add_teacher'),
    path('add_teacher_action', my_app.views.add_teacher_action, name='add_teacher_action'),
    path('delete_teacher_action/<int:tid>', my_app.views.delete_teacher_action, name='delete_teacher_action'),


    path('add_category', my_app.views.add_category, name='add_category'),
    path('add_category_action', my_app.views.add_category_action, name='add_category_action'),
    path('delete_category_action/<int:catid>', my_app.views.delete_category_action, name='delete_category_action'),


    path('add_enroll/<int:cid>', my_app.views.add_enroll, name='add_enroll'),
    path('add_enroll_action/<int:cid>', my_app.views.add_enroll_action, name='add_enroll_action'),
    path('delete_enrolled_student/<int:sid>/<int:cid>', my_app.views.delete_enrolled_student, name='delete_enrolled_student'),
    path('delete_enrolled_student_from_class_detail/<int:cid>', my_app.views.delete_enrolled_student_from_class_detail,
         name='delete_enrolled_student_from_class_detail'),


    path('edit_student_status/<int:sid>/<int:cid>', my_app.views.edit_student_status,
         name='edit_student_status'),
    path('edit_student_status_action/<int:sid>/<int:cid>', my_app.views.edit_student_status_action,
         name='edit_student_status_action'),

    path('upload_payment/<int:eid>', my_app.views.upload_payment, name='upload_payment'),
    path('upload_payment_action/<int:eid>/<int:cid>/<int:sid>', my_app.views.upload_payment_action, name='upload_payment_action'),

    path('add_student', my_app.views.add_student, name='add_student'),
    path('add_student_action', my_app.views.add_student_action, name='add_student_action'),
    path('edit_student/<int:sid>', my_app.views.edit_student, name='edit_student'),
    path('edit_student_action/<int:sid>', my_app.views.edit_student_action, name='edit_student_action'),
    path('delete_student_action/<int:sid>', my_app.views.delete_student_action, name='delete_student_action'),

    path('add_time', my_app.views.add_time, name='add_time'),
    path('add_time_action/<int:years>', my_app.views.add_time_action, name='add_time_action'),
    path('delete_time_action/<int:tid>', my_app.views.delete_time_action, name='delete_time_action'),


    path('sem_convert', my_app.views.sem_convert, name='sem_convert'),
    path('sem_convert_action', my_app.views.sem_convert_action, name='sem_convert_action'),

    path('login_page', my_app.views.login_page, name='login_page'),
    path('login_page_action', my_app.views.login_page_action, name='login_page_action'),
    path('logout_action', my_app.views.logout_action, name='logout_action'),
    path('add_account/<int:repeat>', my_app.views.add_account, name='add_account'),
    path('add_account_action', my_app.views.add_account_action, name='add_account_action'),

    #統計資訊
    path('statics', my_app.views.statics, name='statics'),

]
