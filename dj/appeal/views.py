from django.shortcuts import render
from django.http import HttpRequest, HttpResponsePermanentRedirect, HttpResponseNotFound, HttpResponse
from django.conf import settings
from .models import Admins, Imns, Departments, Appeals
from .forms import ImnsForm, DepartmentsForm, UserForm, AppealForm, ReportForm
from . import const as const
from .functions import *
import csv
import os


# Create your views here.
def index(request:HttpRequest):
    if request.method == "POST":
        login = request.POST.get("login", None)
        password = request.POST.get("password", None)
        if not login or not password:
            context = {"message": "Введите правильный логин/пароль"}
            return render(request, 'appeal/index.html', context=context)
        #admin = Admins.objects.get(login=login)
        admin = Admins.objects.filter(login=login).first()
        if not admin:
            context = {"message": "Введите правильный логин/пароль"}
            return render(request, 'appeal/index.html', context=context)
        if admin.password != password:
            context = {"message": "Введите правильный логин/пароль"}
            return render(request, 'appeal/index.html', context=context)
        request.session['admin'] = admin.id
        return HttpResponsePermanentRedirect('/main')
    return render(request, 'appeal/index.html')

def main(request:HttpRequest):
    id_admin = request.session.get('admin', None)
    if not id_admin:
        return HttpResponseNotFound('пожалуйста зарегистрируйтесь')
    admin = Admins.objects.get(id=id_admin)
    
    
    appeal_list = []
    if admin.access != 1:
        appeal_list = Appeals.objects.filter(id_imns=admin.id_imns)
    else:
        appeal_list = Appeals.objects.all()
    
    table_list = []
    for i_appeal in appeal_list:
        i_appeal.message = str(i_appeal.date) + " / " + i_appeal.message
        table_list.append(i_appeal)
    
    context = {'table_list': table_list,
               'access': admin.access}
    
    return render(request, 'appeal/main.html', context=context)

def imns(request:HttpRequest, id:int=None):
    id_admin = request.session.get('admin', None)
    if not id_admin:
        return HttpResponseNotFound('пожалуйста зарегистрируйтесь')
    admin = Admins.objects.get(id=id_admin)

    imns_list = []
    if admin.access != 1:
        imns_list.append(admin.id_imns)
    else:
        imns_list = Imns.objects.all()
        
    imns_form = ImnsForm()
    if id:
        imns = Imns.objects.get(id=id)
        imns_form.fields['id'].initial = imns.id
        imns_form.fields['number'].initial = imns.number
        imns_form.fields['name'].initial = imns.name
        imns_form.fields['shot_name'].initial = imns.shot_name
        imns_form.fields['mail'].initial = imns.mail
        imns_form.fields['post'].initial = imns.post
        imns_form.fields['address'].initial = imns.address
        imns_form.fields['unp'].initial = imns.unp
    
    context = {'imns_form': imns_form, 'imns_list': imns_list,
               'access': admin.access}
    return render(request, 'appeal/imns.html', context=context)

def save_imns(request:HttpRequest):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        number = request.POST.get('number')
        name = request.POST.get('name')
        shot_name = request.POST.get('shot_name')
        address = request.POST.get('address', '')
        unp = request.POST.get('unp', '')
        post = request.POST.get('post', '')
        mail = request.POST.get('mail', '')
    
    imns = Imns()
    if id != '':
        imns = Imns.objects.get(id=id)

    imns.number = number
    imns.name = name
    imns.shot_name = shot_name
    imns.address = address
    imns.unp = unp
    imns.post = post
    imns.mail = mail
    imns.save()
    
    return HttpResponsePermanentRedirect('/imns')

def delete_imns(request:HttpRequest, id:int=None):
    id_admin = request.session.get('admin', None)
    if id and id_admin:
       imns = Imns.objects.get(id=id)
       imns.delete()
    return HttpResponsePermanentRedirect('/imns') 

def departments(request:HttpRequest, id:int=None):
    id_admin = request.session.get('admin', None)
    if not id_admin:
        return HttpResponseNotFound('пожалуйста зарегистрируйтесь')
    admin = Admins.objects.get(id=id_admin)
    
    departments_form = DepartmentsForm()
    if id:
        department = Departments.objects.get(id=id)
        departments_form.fields['id'].initial = department.id
        departments_form.fields['name'].initial = department.name
    
    departments_list = Departments.objects.all()
    
    context = {"departments_form": departments_form,
               "access": admin.access,
               "departments_list": departments_list}
    return render(request, 'appeal/departments.html', context=context)

def save_departments(request:HttpRequest):
    if request.method == "POST":
        id = request.POST.get('id', '')
        name = request.POST.get('name')
    
    department = Departments()
    if id != '':
        department = Departments.objects.get(id=id)
    department.name = name
    department.save()
        
    return HttpResponsePermanentRedirect('/departments')

def delete_departments(request:HttpRequest, id:int=None):
    id_admin = request.session.get('admin', None)
    if id and id_admin:
        department = Departments.objects.get(id=id)
        department.delete()
    
    return HttpResponsePermanentRedirect('/departments')

def users(request:HttpRequest, id:int=None):
    id_admin = request.session.get('admin', None)
    if not id_admin:
        return HttpResponseNotFound('Пожалуйста зарегистрируйтесь')
    admin = Admins.objects.get(id=id_admin)
    
    user_form = UserForm()
    
    if id:
        user = Admins.objects.get(id=id)
        user_form.fields['id'].initial = user.id
        user_form.fields['login'].initial = user.login
        user_form.initial['access'] = user.access
        user_form.initial['imns'] = user.id_imns.id
    
    users_list = []
    if admin.access != 1:
        admin.access = get_access(admin.access)
        users_list.append(admin)
        imns_list = Imns.objects.filter(id=admin.id_imns.id)
        user_form.fields['access'].choices = [(2, 'район')]
        user_form.fields['imns'].choices = imns_query_to_select(imns_list)
    else:
        imns_list = Imns.objects.all()
        user_form.fields['access'].choices = const.access_dict
        user_form.fields['imns'].choices = imns_query_to_select(imns_list)
        users_list_buf = Admins.objects.all()
        for i_user in users_list_buf:
            i_user.access = get_access(i_user.access)
            users_list.append(i_user)
    
    context = {"user_form": user_form,
               "users_list": users_list,
               "access": admin.access}
    
    return render(request, 'appeal/users.html', context=context)

def save_user(request:HttpRequest):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        login = request.POST.get('login')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        access = request.POST.get('access')
        id_imns = request.POST.get('imns')
        
        if password1 != password2:
            return HttpResponseNotFound('Ошибка заполнения формы')
        
        user = Admins()
        if id != '':
            user = Admins.objects.get(id=id)
        user.login = login
        user.password = password1
        user.access = access
        user.id_imns = Imns.objects.get(id=id_imns)
        user.save()
    
    return HttpResponsePermanentRedirect('/users')

def delete_user(request:HttpRequest, id:int=None):
    id_admin = request.session.get('admin', None)
    if id_admin and id:
        user = Admins.objects.get(id=id)
        user.delete()
    return HttpResponsePermanentRedirect('/users')

def appeal(request:HttpRequest, id:int=None):
    id_admin = request.session.get('admin', None)
    if not id_admin:
        return HttpResponseNotFound("Пожалуйста зарегистрируйтесь")
    admin = Admins.objects.get(id=id_admin)
    
    appeal_form = AppealForm()
    departments_list = Departments.objects.all()
    dep_select = dep_query_to_select(departments_list)
    appeal_form.fields['unit'].choices = dep_select
    imns_select = []
    if admin.access != 1:
        imns_select = [(admin.id_imns.number, admin.id_imns.number)]
    else:
        imns_select = imns_query_to_select_number(Imns.objects.all())
    appeal_form.fields['imns'].choices = imns_select
    
    if id:
        appeal = Appeals.objects.get(id=id)
        appeal_form.fields['id'].initial = appeal.id
        appeal_form.fields['date'].initial = appeal.date
        appeal_form.fields['done'].initial = appeal.done
        appeal_form.initial['result'] = appeal.result
        appeal_form.initial['type'] = appeal.type
        appeal_form.initial['unit'] = appeal.unit
        appeal_form.fields['what'].initial = appeal.what
        appeal_form.fields['who'].initial = appeal.who
        appeal_form.fields['message'].initial = appeal.message
        appeal_form.initial['imns'] = appeal.imns.split(' ')
    
    context = {'appeal_form': appeal_form,
               'access': admin.access}
    
    return render(request, 'appeal/appeal.html', context=context)

def save_appeal(request:HttpRequest):
    id_admin = request.session.get('admin')
    admin = Admins.objects.get(id=id_admin)
    if request.method == "POST":
        id = request.POST.get('id', '')
        date = request.POST.get('date')
        done = request.POST.get('done')
        result = request.POST.get('result')
        types = request.POST.get('type')
        unit = request.POST.get('unit')
        what = request.POST.get('what')
        who = request.POST.get('who')
        message = request.POST.get('message')
        imns = request.POST.getlist('imns')
        
        appeal = Appeals()
        if id != '':
            appeal = Appeals.objects.get(id=id)
            
        appeal.date = date
        appeal.done = done
        appeal.result = result
        appeal.type = types
        appeal.unit = unit
        appeal.what = what
        appeal.who = who
        appeal.message = message
        appeal.id_imns = admin.id_imns
        appeal.imns = " ".join(imns)
        appeal.save()
    return HttpResponsePermanentRedirect('/main')

def report(request:HttpRequest):
    id_admin = request.session.get('admin', None)

    if id_admin:
        admin = Admins.objects.get(id=id_admin)
        
        report_form = ReportForm()
        
        context = {'access': admin.access,
                   'report_form': report_form}
        
        return render(request, 'appeal/reports.html', context=context)
        
    return HttpResponseNotFound('Пожалуйста зарегистрируйтесь')

def view_report(request:HttpRequest):
    if request.method == 'POST':
        id_admin = request.session.get('admin', None)
        date_from = request.POST.get('date_from', None)
        date_to = request.POST.get('date_to', None)
        
        if date_from and date_to and id_admin:
            admin = Admins.objects.get(id=id_admin)
            
            appeal_list = []
            if admin.access != 1:
                if 'report_mail' in request.POST or 'excel_report_mail' in request.POST:
                    appeal_list = Appeals.objects.filter(date__range=[date_from, date_to], type__contains='Письм', id_imns=admin.id_imns)
                if 'report_appeal' in request.POST or 'excel_report_appeal' in request.POST:
                    appeal_list = Appeals.objects.filter(date__range=[date_from, date_to], id_imns=admin.id_imns).exclude(type__contains='Письм')
            else:
                if 'report_mail' in request.POST or 'excel_report_mail' in request.POST:
                    appeal_list = Appeals.objects.filter(date__range=[date_from, date_to], type__contains='Письм')
                if 'report_appeal' in request.POST or 'excel_report_appeal' in request.POST:
                    appeal_list = Appeals.objects.filter(date__range=[date_from, date_to]).exclude(type__contains='Письм')
            
            table_list = []
            excel_list = []
            for i_appeal in appeal_list:
                i_appeal.message = str(i_appeal.date) + " / " + i_appeal.message
                table_list.append(i_appeal)
                list_buf = [i_appeal.id, i_appeal.message, i_appeal.who, i_appeal.what, i_appeal.result, 
                            i_appeal.done, i_appeal.type, i_appeal.unit, i_appeal.imns]
                excel_list.append(list_buf)
                
            if 'excel_report_appeal' in request.POST or 'excel_report_mail' in request.POST:
                header = ['№ п/п', 'Дата и номер письма МНС', 'Наименование плательщика', 'Суть жалобы', 'Результат расмотрения жалобы',
                          'Что сделано', 'Вид документа', 'Управление, самостоятельный отдел', 'ИМНС']
                with open(admin.login + '.csv', 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(excel_list)
                    
                file_path = os.path.join(settings.MEDIA_ROOT, admin.login + '.csv')
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as fh:
                        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                        return response
            
            context = {'access': admin.access,
                       'table_list': table_list}
            return render(request, 'appeal/main.html', context=context)
            
    return HttpResponseNotFound('request error')

def clear_session(request:HttpRequest):
    request.session.clear()
    request.session.modified = True
    return HttpResponsePermanentRedirect('/index')