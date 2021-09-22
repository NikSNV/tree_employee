from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import *

from faker import Factory
from faker.providers import person, job, date_time
from random import randint


def show_tree(request):
    rows = Employee.objects.filter(boss=None)
    print(f'BOSS - {rows}')
    empl = []
    for row in rows:
        tmpdict = {}
        # print(f"Проверка ФИО {row.pk}")
        tmpdict['fio'] = row.fio
        tmpdict['post'] = row.post
        tmpdict['salary'] = row.salary
        tmpdict['date_create'] = row.date_create
        tmpdict['subordinates'] = []
        subordinates = Employee.objects.filter(boss=row)
        if len(subordinates) != 0:
            for s in subordinates:
                tmps = {}
                tmps['fio'] = s.fio
                tmps['post'] = s.post
                tmps['salary'] = s.salary
                tmps['date_create'] = s.date_create
                tmps['subordinates'] = []
                tmpdict['subordinates'].append(tmps)

                subordinates2 = Employee.objects.filter(boss=s)

                if len(subordinates2) != 0:
                    for s2 in subordinates2:
                        tmps2 = {}
                        tmps2['fio'] = s2.fio
                        tmps2['post'] = s2.post
                        tmps2['salary'] = s2.salary
                        tmps2['date_create'] = s2.date_create
                        tmps2['subordinates'] = []
                        tmps['subordinates'].append(tmps2)

                        subordinates3 = Employee.objects.filter(boss=s2)

                        if len(subordinates3) != 0:
                            for s3 in subordinates3:
                                tmps3 = {}
                                tmps3['fio'] = s3.fio
                                tmps3['post'] = s3.post
                                tmps3['salary'] = s3.salary
                                tmps3['date_create'] = s3.date_create
                                tmps3['subordinates'] = []
                                tmps2['subordinates'].append(tmps3)
        empl.append(tmpdict)

    return render(request, "tree_v1/tree.html", {'empl': empl})


# def general(request, **kwargs):
#     # return HttpResponse(f"Отображение отдела с id = {d_id}")
#     return render(request, "tree_v1/general.html", {'tree': Employee.objects.all()}, kwargs)


def data_entry(request):
    fake = Factory.create()
    fake.add_provider(person)
    fake.add_provider(job)
    fake.add_provider(date_time)

    for i in range(1000):
        # Первые три сотрудника будут руководителями для всех
        try:
            query = Employee.objects.get(empl_id=randint(1, 3))
        except:
            query = None

        new_empl = Employee(
            empl_id=i + 1,
            fio=fake.name(),
            post=fake.job(),
            date_create=fake.date_this_year(before_today=True, after_today=False),
            salary=randint(5000, 10000),
            boss=query
        )
        new_empl.save()
        # print(f'{i}  Создали - {new_empl}   BOSS - {query}')

    return HttpResponse(f"УСПЕШНО ЗАПИСАЛИ БАЗУ СОТРУДНИКОВ")


def delete_db(request):
    Employee.objects.all().delete()
    return HttpResponse(f"УСПЕШНО УДАЛИЛИ ВСЕХ СОТРУДНИКОВ")
