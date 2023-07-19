from django.urls import path
from . import views

app_name = 'appeal'

urlpatterns = [
    path('', views.index, name='free'),
    path('index', views.index, name='index'),
    path('main', views.main, name='main'),
    path('imns/<int:id>', views.imns, name='edit_imns'),
    path('imns', views.imns, name='imns'),
    path('save_imns', views.save_imns, name='save_imns'),
    path('delete_imns/<int:id>', views.delete_imns, name='delete_imns'),
    path('departments/<int:id>', views.departments, name='edit_departments'),
    path('departments', views.departments, name='departments'),
    path('save_departments', views.save_departments, name='save_departments'),
    path('delete_departments/<int:id>', views.delete_departments, name='delete_departments'),
    path('users/<int:id>', views.users, name='edit_user'),
    path('users', views.users, name='users'),
    path('save_user', views.save_user, name='save_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('appeal/<int:id>', views.appeal, name='edit_appeal'),
    path('appeal', views.appeal, name='appeal'),
    path('save_appeal', views.save_appeal, name='save_appeal'),
    path('report', views.report, name='report'),
    path('viewreport', views.view_report, name='view_report'),
    path('clear_session', views.clear_session, name='clear_session'),
]