from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateNewList
from .models import VisitorGroup, IntervallDate, ChurchDayVisitorGroup
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta, date
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model


@login_required
def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():

            name = form.cleaned_data["name"]
            group_size = form.cleaned_data["group_size"]

            gl = VisitorGroup(name=name,group_size=group_size)
            gl.save()

        return HttpResponseRedirect("/groups/%i" %gl.id)

    else:
        form = CreateNewList()

    return render(response, "groups/create.html", {"form": form})


@login_required
def groups(response):
    groups = VisitorGroup.objects.all()
    group_list = []
    visitor_list = []
    for group in groups:
        group_list.append({
            "id": group.id,
            "name": group.name,
            "size": group.group_size,
            "user_list" : group.visitor_set.all(),
            "member_count": len(group.visitor_set.all()),
        })
        for visitor in group.visitor_set.all():
            visitor_list.append({
                "visitor_author": visitor.author,
                "family_number": visitor.family_number,
                "visitor_groupname": visitor.visitorgroup
            })

    return render(response, 'groups/groups.html', {"group_list": group_list,
                                                   "visitor_list": visitor_list,
                                                   "title": "Gruppen"})


@login_required
def list(response, id):
    ls = VisitorGroup.objects.get(id=id)
    i = 0

    for name in ls.visitor_set.all():
        print(name.id)
        print(name)


    if response.method == "POST":
        if 'delete' in response.POST:
            id_delete = response.POST.get("delete")

            deleted_member_name = str(ls.visitor_set.get(id=id_delete))
            ls.visitor_set.filter(id=id_delete).delete()
            messages.error(response, deleted_member_name + ' wurde aus der Gruppe entfernt.')

            length_of_vg = len(ChurchDayVisitorGroup.objects.all())
            while i < length_of_vg:
                vg = ChurchDayVisitorGroup.objects.all()[i]
                if id_delete in vg.visitor_list:
                    del vg.visitor_list[id_delete]
                    ChurchDayVisitorGroup.objects.filter(id=vg.id).update(visitor_list=vg.visitor_list)
                i += 1


        elif response.POST.get("newName"):
            txt = response.POST.get("new")
            global tmp_name1
            tmp_name1 = txt

            if len(txt) >= 2 and txt.find(" ") != -1:
                    if not ls.visitor_set.filter(text=txt):
                        x=0
                        visitor_group_list = VisitorGroup.objects.all()
                        for name in visitor_group_list:
                            vg_name = VisitorGroup.objects.get(name=name)
                            visitor_list = vg_name.visitor_set.filter(text=txt)
                            visitor_list = str(visitor_list)

                            if visitor_list.find(txt) != -1:
                                vg_name = VisitorGroup.objects.get(name=name)
                                global tmp_vg_name
                                tmp_vg_name = str(vg_name)
                                messages.info(response, ' ', extra_tags='safe2')
                                x = 1

                        if x == 0:
                            ls.visitor_set.create(text=txt, author=response.user, address=response.user.profile.address,
                                                  number=response.user.profile.number ,
                                                  family_number=response.user.profile.family_number)
                            messages.success(response, txt + ' wurde zur Gruppe hinzugefügt.')

                            #add name to all church_events
                            for test in ChurchDayVisitorGroup.objects.all():
                                if id == test.visitorgroup_id:
                                    dict = ChurchDayVisitorGroup.objects.filter(id=test.id)[0].visitor_list
                                    visitor_id = ls.visitor_set.get(text=txt).id

                                    #check if user is already mentioned in calender groups
                                    str_dict = str(dict)
                                    res = str_dict.count(str(txt))

                                    if res == 0:
                                        dict.update({str(visitor_id): [[str(txt), str(response.user),str(response.user.profile.address),
                                                                        str(response.user.profile.number),str(response.user.profile.family_number)]]})
                                        ChurchDayVisitorGroup.objects.filter(id=test.id).update(visitor_list=dict)
                                    else:
                                        messages.info(response, txt + ' ist schon am '+ str(test.date)+' eingetragen und wurde übernommen. Sollte es nicht dein Name sein,'
                                                                ' dann gib vor dem jeweiligen Gottesdienst dem Personal diesbezüglich Bescheid. '+
                                                                txt+' wurde bei den sonstigen Gottesdienstterminen eingetragen.')
                    else:
                        messages.info(response, ' ', extra_tags='safe1')

            elif len(txt)<2:
                messages.info(response,'Der Name ist zu kurz.')

            else:
                messages.info(response, 'Bitte Vor- und Nachnamen eingeben.')

        elif response.POST.get("equalname"):
            equal_name = response.POST.get("equalname")
            equal_name = equal_name.replace("_", " ")

            tmp_counter = 1
            for name in ls.visitor_set.all():
                if str(equal_name) in str(name):
                    tmp_counter += 1

            equal_name = equal_name + " (" + str(tmp_counter) + ")"
            ls.visitor_set.create(text=equal_name, author=response.user, address=response.user.profile.address,
                                  number=response.user.profile.number,
                                  family_number=response.user.profile.family_number)
            messages.success(response, equal_name + ' wurde zur Gruppe 1 hinzugefügt.')

            dict = ChurchDayVisitorGroup.objects.filter(visitorgroup_id=id)[0].visitor_list
            visitor = ls.visitor_set.get(text=equal_name)
            dict.update({str(visitor.id): [[str(equal_name), str(response.user), str(response.user.profile.address),
                                            str(response.user.profile.number),
                                            str(response.user.profile.family_number)]]})
            ChurchDayVisitorGroup.objects.filter(visitorgroup_id=id).update(visitor_list=dict)

    visitor_group_list = VisitorGroup.objects.get(id=id)
    ls_allow = visitor_group_list.allow_group_login

    length_grouplist = len(ls.visitor_set.all())


    try:tmp_name1
    except NameError:tmp_name1 = -1
    try:tmp_vg_name
    except NameError:tmp_vg_name = -1

    context = {
        'ls': ls,
        'lg': length_grouplist,
        'title': ls.name,
        'id': id,
        'new_member_name':tmp_name1,
        'other_group_name':tmp_vg_name,
        'ls_allow':ls_allow
    }

    return render(response, 'groups/list.html', context)


@login_required
def calender(response):

    #get start_date and end_date from model IntervallDate
    start_date = str(IntervallDate.objects.all()[0].start_date)
    start_date = start_date.replace("-"," ")
    numbers = [int(word) for word in start_date.split() if word.isdigit()]
    start_date = date(numbers[0], numbers[1], numbers[2])
    end_date = str(IntervallDate.objects.all()[0].end_date)
    end_date = end_date.replace("-"," ")
    numbers = [int(word) for word in end_date.split() if word.isdigit()]
    end_date = date(numbers[0], numbers[1], numbers[2])

    i = 0
    y = 0
    church_day_count = 0
    group_list = VisitorGroup.objects.all()
    churchday_list = []
    church_day_visitor_list = []

    for single_date in daterange(start_date, end_date):
        if single_date.weekday() == 2 or single_date.weekday() == 6:

            #if get_size_of_services() != len(group_list):
            #    print("Listenanzahl hat sich geändert!!!!")
            #    ChurchDayVisitorGroup.objects.all().delete()

            if len(group_list) != 0:
                set_size_of_services(len(group_list))
                group_name = group_list[i]

                i += 1
                churchday_list.append({
                    "date": single_date.strftime("%Y-%m-%d"),
                    "year": single_date.strftime("%Y"),
                    "month": single_date.strftime("%m"),
                    "day": single_date.strftime("%d"),
                    "weekday": single_date.weekday(),
                    "group": group_name,
                })

                church_day_count += 1
                if i == len(group_list):
                    i = 0

                for group in group_list:
                    if str(group_name) == group.name:
                        if not ChurchDayVisitorGroup.objects.filter(date=single_date.strftime("%Y-%m-%d")):
                            vg_name = VisitorGroup.objects.get(id=group.id)
                            visitor_list = vg_name.visitor_set.all()
                            visitor_counter = 1
                            json_obj = {}

                            for name in visitor_list:
                                User = get_user_model()
                                user = User.objects.get(username=str(name.author))


                                visitor = vg_name.visitor_set.get(text=name)
                                json_obj.update({str(visitor.id): [[str(name), str(name.author), str(user.profile.address),
                                            str(user.profile.number),
                                            str(user.profile.family_number)]]})
                                visitor_counter += 1

                            vg = ChurchDayVisitorGroup(name=group.name, group_size=group.group_size,
                                                       date=single_date.strftime("%Y-%m-%d"),
                                                       visitor_list=json_obj,
                                                       visitorgroup_id=group.id,)
                            vg.save()
                        vg_id = ChurchDayVisitorGroup.objects.all()[y].id
                        dict_visitor = ChurchDayVisitorGroup.objects.filter(id=vg_id)[0].visitor_list
                        church_day_visitor_list.append({
                            "id": vg_id,
                            "dict_visitor": dict_visitor
                        })

                #get id and size of ChurchDayVisitorGroup and store it in churchday_list
                vg_id = ChurchDayVisitorGroup.objects.all()[y].id
                vg_size = ChurchDayVisitorGroup.objects.all()[y].group_size
                dict_id = {'id':vg_id, 'group_size':vg_size, 'visitor_size':len(dict_visitor)}
                churchday_list[y].update(dict_id)
                y += 1


    # new tmp list for paginator
    pagintor_churchday_list = churchday_list
    tmp_pag_list = []
    for day in pagintor_churchday_list:

        if get_date_size(day["date"]) == 1:
            tmp_pag_list.append(day)


    paginator = Paginator(tmp_pag_list, per_page=5)
    page_number = response.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)


    return render(response, 'groups/calendar.html', {"church_day_visitor_list":church_day_visitor_list, "churchday_list":page_obj.object_list, "paginator":paginator})


@login_required
def datevisitorlist(response,id):

    vg = ChurchDayVisitorGroup.objects.get(id=id)

    global equal_addr,equal_numb

    if response.method == "POST":
        if 'delete' in response.POST:
            vg = ChurchDayVisitorGroup.objects.get(id=id)
            id_delete = response.POST.get('delete')
            deleted_list = vg.visitor_list.get(str(id_delete))
            deleted_member_name = deleted_list[0][0]
            messages.error(response, deleted_member_name + ' wurde aus der Gruppe entfernt.')
            del vg.visitor_list[id_delete]

        elif response.POST.get("equalname"):
            current_groupname = ChurchDayVisitorGroup.objects.filter(id=id)[0].name
            equal_name = response.POST.get("equalname")
            equal_name = str(equal_name.replace("_", " "))
            dict = ChurchDayVisitorGroup.objects.filter(id=id)[0].visitor_list
            count = str(dict).count(equal_name)

            ls = VisitorGroup.objects.get(name=current_groupname)
            group_list = ls.visitor_set.all()


            for member in group_list:
                if str(equal_name) == str(member):
                    new_id = str(member.id)
                    print(new_id)
                    break
                else:
                    # get highest number of extern id's and count from highest number
                    extern_id_list = []
                    for key in dict:
                        if 'extern' in str(key):
                            tmp_id = str(key)
                            x = tmp_id.replace('extern (', '')
                            x = x.replace(')', '')
                            extern_id_list.append(x)

                    if not extern_id_list:
                        extern_id_list.append(-1)
                    id_index = int(max(extern_id_list)) + 1
                    print(id_index)

                    new_id = 'extern ' + '(' + str(id_index) + ')' + str(response.user.id)

            if len(group_list) == 0:
                new_id = 'extern ' + str(member.id)


            # if input for address and number is empty, take data from logged in user
            if str(equal_addr) == "" and str(equal_numb) == "" or not response.user.is_superuser:
                dict.update({new_id: [[equal_name +" ("+str(count)+")", str(response.user), str(response.user.profile.address),
                                            str(response.user.profile.number),
                                            str(response.user.profile.family_number)]]})
                vg.visitor_list = dict
                ChurchDayVisitorGroup.objects.filter(id=id).update(visitor_list=dict)
                messages.success(response, equal_name + ' wurde zur Liste hinzugefügt.')

            else:
                dict.update({new_id: [[equal_name + " (" + str(count) + ")", str(response.user), str(equal_addr), str(equal_numb),
                                       str(response.user.profile.family_number)]]})
                vg.visitor_list = dict
                ChurchDayVisitorGroup.objects.filter(id=id).update(visitor_list=dict)
                messages.success(response, equal_name + ' wurde zur Liste hinzugefügt.')


        elif response.POST.get("newName"):
            txt = response.POST.get("new")
            address = response.POST.get("address")
            number = response.POST.get("number")

            global tmp_name2
            tmp_name2 = txt
            dict = ChurchDayVisitorGroup.objects.filter(id=id)[0].visitor_list
            dict_str = str(dict)

            if len(txt) >= 2 and dict_str.find(txt) == -1 and txt.find(" ") != -1:
                current_groupname = ChurchDayVisitorGroup.objects.filter(id=id)[0].name
                ls = VisitorGroup.objects.get(name=current_groupname)
                group_list = ls.visitor_set.all()


                for member in group_list:
                    if str(txt) == str(member):
                        new_id = str(member.id)
                        break
                    else:
                        #get highest number of extern id's and count from highest number
                        extern_id_list = []
                        for key in dict:
                            if 'extern' in str(key):
                                tmp_id = str(key)
                                x = tmp_id.replace('extern (','')
                                x = x.replace(')','')
                                extern_id_list.append(x)

                        if not extern_id_list:
                            extern_id_list.append(-1)
                        id_index = int(max(extern_id_list))+1
                        print(id_index)

                        new_id = 'extern ' +'('+str(id_index)+')'

                if len(group_list) == 0:
                    new_id = 'extern ' + str(member.id)


                #if input for address and number is empty, take data from logged in user
                if str(address) == "" and str(number) == "" or not response.user.is_superuser:
                    dict.update({new_id: [[txt, str(response.user), str(response.user.profile.address),
                                            str(response.user.profile.number),
                                            str(response.user.profile.family_number)]]})
                    vg.visitor_list = dict
                    ChurchDayVisitorGroup.objects.filter(id=id).update(visitor_list=dict)
                    messages.success(response, txt + ' wurde zur Liste hinzugefügt.')

                else:
                    dict.update({new_id: [[txt, str(response.user), str(address), str(number), str(response.user.profile.family_number)]]})
                    vg.visitor_list = dict
                    ChurchDayVisitorGroup.objects.filter(id=id).update(visitor_list=dict)
                    messages.success(response, txt + ' wurde zur Liste hinzugefügt.')

            elif len(txt)<2:
                messages.info(response,'Der Name ist zu kurz oder Name eingeben.')

            elif dict_str.find(txt) != -1:
                #messages.info(response, txt + ' ist schon in dieser Gruppe eingetragen.')
                messages.info(response, ' ', extra_tags='safe1')
                equal_addr = response.POST.get("address")
                equal_numb = response.POST.get("number")

            else:
                messages.info(response, 'Bitte Vor- und Nachnamen eingeben.')

    ChurchDayVisitorGroup.objects.filter(id=id).update(visitor_list=vg.visitor_list)

    reverse_visitor_list = reverse_dict(vg.visitor_list)

    try:tmp_name2
    except NameError:tmp_name2 = -1

    day = vg.date.strftime("%d")
    month = vg.date.strftime("%m")
    year = vg.date.strftime("%y")
    date = vg.date.strftime("%Y-%m-%d")

    return render(response, 'groups/datevisitorlist.html', {"visitor_list": vg.visitor_list,
                                                            "group_size": vg.group_size,
                                                            "group_date": date,
                                                            "group_date_year":year,
                                                            "group_date_month": month,
                                                            "group_date_day": day,
                                                            "new_member_name":tmp_name2,
                                                            "reverse_visitor_list":reverse_visitor_list})

def reverse_dict(my_dict):

    list_keys = []
    for k in my_dict.keys():
        list_keys.append(k)
    rev_dict = {}
    for i in reversed(list_keys):
        rev_dict[i] = my_dict[i]
    return rev_dict


def set_size_of_services(size):
    global sos
    sos = size


def get_size_of_services():
    global sos
    try: sos
    except NameError: sos=-1
    return sos


def get_date_size(y):

    date_for_weekday = y.replace("-"," ")
    numbers = [int(word) for word in date_for_weekday.split() if word.isdigit()]
    date_for_weekday = date(numbers[0], numbers[1], numbers[2])

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    dt = now.strptime(dt_string,"%Y-%m-%d %H:%M:%S")

    ExpectedDate1 = str(y)
    if date_for_weekday.weekday() == 2:
        ExpectedTime2 = "21:00"
    if date_for_weekday.weekday() == 6:
        ExpectedTime2 = "11:00"
    space = " "
    ExpectedDate = ExpectedDate1 + space + ExpectedTime2
    ExpectedDate = datetime.strptime(ExpectedDate, "%Y-%m-%d %H:%M")

    if dt > ExpectedDate:
        return 0
    else:
        return 1


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


