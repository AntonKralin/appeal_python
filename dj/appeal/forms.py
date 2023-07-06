from django.core.exceptions import ValidationError
from django import forms
from .const import results, types
import datetime
from .models import Imns


class ImnsForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False, initial="")
    number = forms.IntegerField(label='Код организации')
    name = forms.CharField(label='Полное название организации')
    shot_name = forms.CharField(label='Короткое название организации')
    address = forms.CharField(label='Адресс', required=False)
    mail = forms.CharField(label='Электронная почта', required=False)
    post = forms.CharField(label='Почта', required=False)
    unp = forms.CharField(label='УНП', required=False)
    

class DepartmentsForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput, required=False, initial="")
    name = forms.CharField(label="Название")
    

class UserForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False, initial="")
    login = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())
    access = forms.ChoiceField(choices=[], required=True, label="")
    imns = forms.ChoiceField(choices=[], required=True, label="")

class AppealForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False, initial='')
    date = forms.DateField(label='Дата рассмотрения жалобы, письма', initial=datetime.date.today, widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))  
    done = forms.CharField(label='Что сделано / Результат проделанной работы, направленной на устранение нарушений, отраженных в письме, предписании, ином документе',
                           widget=forms.Textarea(attrs={"rows":"3"}))
    result = forms.ChoiceField(choices=results, label='Результат')
    type = forms.ChoiceField(choices=types, label='Тип')      
    unit = forms.ChoiceField(choices=[], label='Подразделение')
    what = forms.CharField(label='Суть жалобы / Суть нарушений в письме, предписании, ином документе',
                           widget=forms.Textarea(attrs={"rows":'3'}))
    who = forms.CharField(label='Наименование плательщика',  widget=forms.TextInput(attrs={'size':'36'}))
    message = forms.CharField(label='Номер письма, предписания, иного документа')
    imns = forms.MultipleChoiceField(choices=[])
    
    
class ReportForm(forms.Form):
    date_from = forms.DateField(label='С', initial=datetime.date.today, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    date_to = forms.DateField(label='По', initial=datetime.date.today, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
