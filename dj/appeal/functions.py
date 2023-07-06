from .const import *

def imns_query_to_select(queryset):
    rez_list = []
    for i_elem in queryset:
        buf_typle = (i_elem.id, i_elem.shot_name)
        rez_list.append(buf_typle)
    return rez_list

def imns_query_to_select_number(queryset):
    rez_list = []
    for i_elem in queryset:
        buf_typle = (i_elem.number, i_elem.number)
        rez_list.append(buf_typle)
    return rez_list

def get_access(id):
    rez = id
    for i in access_dict:
        if i[0] == id:
            rez = i[1]
            return rez
        
        
def dep_query_to_select(queryset):
    rez_list = []
    for i_elem in queryset:
        buf_typle = (i_elem.name, i_elem.name)
        rez_list.append(buf_typle)
    return rez_list
