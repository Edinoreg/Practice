from tkinter import ttk
import tkinter as tk
import json
from memory_profiler import memory_usage
from datetime import date

with open("Employers.json") as f:
    data = json.load(f)
    f.close()

with open("Works.json") as f:
    data_works_us = json.load(f)
    f.close()

with open("Work.json") as f:
    data_work_us = json.load(f)
    f.close()

data_emp_us = data
labels = []
mass_ent = []
mass_finder = []
flag = False
fl_place = False
fff = False
perem = 10

tabl1 = ('Код сотрудника', 'Фамилия', 'Имя', 'Отчество', 'Оклад')
tabl2 = ('Код вида', 'Описание', 'Оплата за день')
tabl3 = ('Код сотрудника', 'Код вида', 'Дата начала', 'Дата окончания')
months_f = [31, 28, 31, 30,
          31, 30, 31, 31,
          30, 31, 30, 31]

months_s = [31, 28, 31, 30,
          31, 30, 31, 31,
          30, 31, 30, 31]


def delet(labels):
    for label in labels:
        tk.Label.destroy(label)
    btn2.configure(state="disabled", background="#A9A9A9")
    btn1.configure(state="normal", background="#DCDCDC")


def show(x, tab1, tab2, tab3):
    global data_emp_us
    global data_works_us
    global data_work_us
    data_emp = data_emp_us["Employers"]
    data_works = data_works_us["Works"]
    data_work = data_work_us["Work"]
    data = {}
    fl = False
    max_len = max(len(data_emp), len(data_works), len(data_work))
    tabl = ('Выберите таблицу!', '')

    if x != 0:
        root.geometry("1400x400")

    if x == 1:
        data = data_emp
        tabl = tab1

    elif x == 2:
        data = data_works
        tabl = tab2

    elif x == 3:
        data = data_work
        tabl = tab3


    c = 0
    for i in range(0, len(tabl)):
        lb = tk.Label(second_frame, text=tabl[i], background="#FAEBD7",
                      font='Times 10',

                      width=20)
        labels.append(lb)
        if x == 0: lb.configure(bg="#FAF0E6")
        lb.grid(column=i, row=2)

    c1 = 3
    if data:
        for dat in data:
            c2 = 0
            for da in dat.values():
                if x == 3:
                    if c2 == 2 or c2 == 3:
                        da = da["Day"] + ' ' + da["Month"] + ' ' + da["Year"]
                l = tk.Label(second_frame,
                            width=20,
                             text=da,
                             bg="#FAF0E6")
                labels.append(l)
                l.grid(row=c1, column=c2)
                c2 += 1
            c1 += 1
    btn1.configure(state="disabled", background="#A9A9A9")
    btn2.configure(state="normal", background="#DCDCDC")

    div = str(memory_usage()[0]*1024)
    print('Потрачено: ' + div + ' кб или ' + str(memory_usage()[0]) + ' мб\n')

def changing(x):
    if sel.get() == 0:
        label_label["text"] = "Выберите таблицу"
        label_label.after(2000, lambda: label_label.configure(text=''))
    else:
        btn3.destroy()
        fr.destroy()


def confirm(but, label_suc):
    global data_emp_us
    global data_works_us
    global data_work_us
    global fl_place
    global perem
    global fff
    count = 0
    cot = 199
    perem2 = sel.get()
    file_names = ['Employers.json', 'Works.json', 'Work.json']
    razd_names = ['Employers', 'Works', 'Work']
    tabl_names = [['Code', 'Last', 'First', 'Third', 'Salary'],
                  ['CodeVid', 'Description', 'Payment'],
                  ['Code', 'CodeVid', 'Begin', 'End'],
                  ['Day', 'Month', 'Year']
                  ]

    if perem2 != perem:
        return 100
    with open(file_names[perem-1], 'r') as f:
        am = razd_names[perem-1]
        data = json.load(f)
        data = data[am]
        f.close()

    if len(mass_ent) > 0:
        ap = {}
        beg = {}
        en = {}
        hi = {}
        for x in mass_ent:
            if count % 2 != 0 and count < len(mass_ent)-1:
                if perem != 3:
                    y = {tabl_names[perem-1][int(count/2)]: x.get()}
                    ap = {**ap, **y}
                    if sel.get() == 1:
                        hi = data_emp_us["Employers"]
                    elif sel.get() == 2:
                        hi = data_works_us["Works"]
                else:
                    hi = data_work_us["Work"]
                    if count < 5:
                        y = {tabl_names[perem - 1][int(count / 2)]: x.get()}
                        ap = {**ap, **y}
                    elif count < 10:
                        u = {tabl_names[3][int((count-5) / 2)]: x.get()}
                        beg = {**beg, **u}
                    else:
                        z = {tabl_names[3][int((count-10) / 2)]: x.get()}
                        en = {**en, **z}
            count += 1
        if beg:
            beg = {"Begin": beg}
            en = {"End": en}

            ap = {**ap, **beg}
            ap = {**ap, **en}

        cot = correct(ap, label_suc, hi, but)
        data.append(ap)
    if (perem == 1 and cot == 5) or (perem == 2 and cot == 3) or \
            (perem == 3 and cot == 8):
        if perem == 1:
            fl_place = True
        elif perem == 2:
            fl_place = True

        if fl_place == True:
            with open(file_names[perem - 1], 'w') as f:
                data_fin = {razd_names[sel.get()-1]: data}
                json.dump(data_fin, f)
                if perem == 1:
                    data_emp_us = data_fin
                elif perem == 2:
                    data_works_us = data_fin
                elif perem == 3:
                    data_work_us = data_fin
                f.close()
            but.destroy()
            if label_suc:
                if fff == False:
                    label_suc.configure(text="Успешно", width=20)
                else:
                    fff = True
            fl_place = False

def correct(arg, label_suc, hi, but):
    calc = c = 0
    mas = []


    spisok = []
    spisok_dop = []
    for h in hi:
        if sel.get() == 1:
            spisok.append(h["Code"])
        if sel.get() == 2:
            spisok.append(h["CodeVid"])
        if sel.get() == 3:
            spisok.append(h["Code"])
            spisok_dop.append(h["CodeVid"])

    for i in arg.values():
        if sel.get() == 1:
            if c == 0:
                if i in spisok:
                    but.configure(text='Код занят')
                    but.after(1500, lambda: but.configure(text='Подтвердить'))
                    break
            if c == 0 or c == 4:
                if all('0' <= x <= '9' for x in i) and i != '':
                    calc += 1
                    if int(i) > 10_000_000:
                        label_suc.configure(text="Слишком большое значение", width=30)
                        return 199
            else:
                if all('a' <= x <= 'z' for x in i.lower()) and i != '':
                    calc += 1
                    if len(i) > 15:
                        label_suc.configure(text="Длинный инициал", width=30)
                        return 199

        elif sel.get() == 2:
            if c == 0:
                if i in spisok:
                    but.configure(text='Код занят')
                    but.after(1500, lambda: but.configure(text='подтвердить'))
                    break
            if c == 0 or c == 2:
                if all('0' <= x <= '9' for x in i) and i != '':
                    calc += 1
                    if int(i) > 10_000_000:
                        label_suc.configure(text="Слишком большое значение", width=30)
                        return 199
            else:
                if all('a' <= x <= 'z' for x in i.lower()) and i != '':
                    calc += 1
                    if len(i) > 15:
                        label_suc.configure(text="Длинный инициал", width=30)
                        return 199

        else:
            if c < 2:
                mas.append(i)
            else:
                for y in i.values():
                    mas.append(y)


        c += 1
    if sel.get() == 3:

        if mas[0] in spisok:
            if mas[1] in spisok_dop:
                ind1 = spisok.index(mas[0])
                ind2 = spisok_dop.index(mas[1])
                if ind1 == ind2:
                    but.configure(text='Код занят')
                    but.after(1500, lambda: but.configure(text='Подтвердить'))
                    return 3
        if all(x != '' for x in mas):
            m1 = int(mas[3])
            m2 = int(mas[6])

            if int(mas[4]) % 400 == 0:
                months_f[1] = 29
            else:
                if int(mas[4]) % 4 == 0:
                    if int(mas[4]) % 100 != 0:
                        months_f[1] = 29
            if int(mas[7]) % 400 == 0:
                months_s[1] = 29
            else:
                if int(mas[7]) % 4 == 0:
                    if int(mas[7]) % 100 != 0:
                        months_s[1] = 29

            if m1 > 12 or m2 > 12:
                return 199
            else:
                if int(mas[2]) > months_f[m1-1] or int(mas[5]) > months_s[m2-1]:
                    return 199
                else:
                    fir = date(int(mas[4]), m1, int(mas[2]))
                    sec = date(int(mas[7]), m2, int(mas[5]))
                    th = sec - fir
                    th2 = th
                    th = th.total_seconds()
                    if th < 0:
                        return 199
                    else:
                        record(arg, th2.days, spisok, spisok_dop)

            for y in mas:
                if all('0' <= x <= '9' for x in y) and y != '':
                    calc += 1
    return calc


def record(ap, th, sp1, sp2):
    global data_emp_us
    global data_works_us
    global data_work_us
    global fl_place
    global fff

    code = ap["Code"]
    codevid = ap["CodeVid"]
    price = ''

    with open('Works.json') as f:
        da = json.load(f)['Works']
        for x in da:
            if int(codevid) == int(x["CodeVid"]):
                fl_place = True
                price = x["Payment"]
                price = int(price)
                break

        if code in sp1:
            if codevid in sp2:
                fl_place = False
        f.close()
    if price == '':
        labelka = tk.Label(second_frame, text="Нет вида работы", width=20, bg="#FAF0E6")
        labelka.grid(column=8, row=11)
        labelka.after(1200, labelka.destroy)

    if price != '':
        pri = price*th
        s = []
        with open('Employers.json') as f:
            dd = json.load(f)['Employers']
            for d in dd:
                s.append(d['Code'])
            f.close()
        if code in s:
            with open('Employers.json', 'w') as f:
                data_emp = data_emp_us["Employers"]
                c = 0
                for dat in data_emp:
                    if int(dat["Code"]) == int(code):
                        data_emp[c]["Salary"] = int(dat["Salary"]) + pri

                    c += 1
                data_emp_us = {"Employers": data_emp}
                json.dump(data_emp_us, f)
                f.close()
        else:
            fff = True

    #КРЧ ОСТАНОВИЛСЯ НА ТОМ, ЧТО ВВОДИШЬ CODE В ПОЛЕ ЛЮБУЮ, И ОН СЧИТАЕТ ДАЖЕ ДЛЯ НЕСУЩЕСТВУЮЩЕГО


def adding(x, tab1, tab2, tab3):
    global data_emp_us
    global data_works_us
    global data_work_us
    global flag
    global perem

    perem = sel.get()
    flag = False
    tab = ''
    i = 2
    label_label.destroy()

    if len(mass_finder) > 0:
        clean_master()

    com.grid_forget()
    btn6.grid_forget()
    en.grid_forget()
    ent.grid_forget()
    if ent12["state"] == "normal":
        ent12.configure(state="disabled")
        tk.Entry.grid_forget(ent12)

    if len(mass_ent) > 0:
        for mass in mass_ent:
            tk.Label.destroy(mass)
        mass_ent.clear()

    if btn5["state"] == "disabled":
        btn5.configure(state="normal", bg='#DCDCDC')
    if btn7["text"] == "Повторить":
        btn7.configure(text="Редактировать")
    if x != 0:
        if x == 1:
            tab = tab1
        if x == 2:
            tab = tab2
        if x == 3:
            tab = ('Код сотрудника', 'Код вида', 'День начала', 'Месяц начала', 'Год начала',
                   'День конца', 'Месяц конца', 'Год конца')

        for i in range(2, len(tab)+2):
            l = tk.Label(second_frame, text=tab[i-2], bg="#FAF0E6", width=20)
            mass_ent.append(l)
            l.grid(column=7, row=i)
            e = tk.Entry(second_frame, width=20)
            mass_ent.append(e)
            e.grid(column=8, row=i)

        label_suc = tk.Label(second_frame, text='', bg="#FAF0E6", width=20)
        mass_ent.append(label_suc)
        label_suc.grid(column=8, row=i + 1)
        but = tk.Button(second_frame, text="подтвердить", command=lambda: confirm(but, label_suc))
        mass_ent.append(but)
        but .grid(column=7, row=i+1)
    btn4.configure(text="Очистить")


def audio():
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load("hehe.mp3")
    pygame.mixer.music.play()


def clear():
    global flag
    flag = False
    varss = ['Работники', 'Виды работ', 'Работы']
    if len(mass_ent) > 0:
        for x in mass_ent:
            tk.Label.destroy(x)
        mass_ent.clear()
    if btn4["text"] == "Очистить":
        btn4.configure(text="Добавить")
    if btn7["text"] == "Повторить":
        btn7.configure(text='Редактировать')
    if len(mass_finder) > 0:
        clean_master()
    lab_com.grid(column=7, row=2)
    lab_com.after(8000, lab_com.grid_forget)
    com.configure(values=varss)
    com.grid(column=8, row=2)
    btn5.configure(state="disabled", bg='#A9A9A9')
    btn6.configure(text='удалить')
    com.bind("<<ComboboxSelected>>", lab_change)
    btn6.grid(column=7, row=4)
    ent.grid_forget()

def lab_change(event):
    global flag

    get = event.widget.get()
    la = ''
    if get == "Работники":
        la = "Код сотрудника:"
        if ent12["state"] == "normal":
            ent12.configure(state="disabled")
            tk.Entry.grid_remove(ent12)
    elif get == "Виды работ":
        la = "Код вида работы:"
        if ent12["state"] == "normal":
            ent12.configure(state="disabled")
            tk.Entry.grid_forget(ent12)
    elif get == "Работы":
        la = "Код сотрудника и вида работы:"
        if ent12["state"] == "disabled":
            ent12.configure(state="normal")
            ent12.grid(column=9, row=3)
    if not flag:
        en.grid(column=8, row=3)
        lab_en = tk.Label(second_frame, text=la, bg="#FAF0E6")
        mass_ent.append(lab_en)
        lab_en.grid(column=7, row=3)
        flag = True
    else:
        m = mass_ent[-1]
        tk.Label.destroy(m)
        mass_ent.remove(m)
        lab_en = tk.Label(second_frame, text=la, bg="#FAF0E6")
        mass_ent.append(lab_en)
        lab_en.grid(column=7, row=3)


def conf_del(var, ident):
    vars = ['Работники', 'Виды работ', 'Работы']
    nmes1 = ['Фамилия', 'Имя', 'Отчество', 'Оклад']
    nmes2 = ['Описание', 'Оклад']
    nmes3 = ['Код вида', 'Д начала', 'М начала', 'Г начала', 'Д конца', 'М конца', 'Г конца']
    if var == vars[0]:
        num(ident, "Code")
    elif var == vars[1]:
        num(ident, "CodeVid")
    elif var == vars[2]:
        id = [ident, varr.get()]
        num(id, "Code CodeVid")
    else:
        if sel.get() == 1:
            nmes = nmes1
        if sel.get() == 2:
            nmes = nmes2
        if sel.get() == 3:
            nmes = nmes3

        if var in nmes:
            edit_act(var, ident, nmes)
        else:
            la = tk.Label(second_frame, text="Выберите параметр", bg="#FAF0E6")
            la.grid(column=7, row=5)
            la.after(5000, la.destroy)


def num(ident, word):
    global data_emp_us
    global data_works_us
    global data_work_us

    fir, sec = '1', '2'

    codes = []
    if word == "Code":
        dat = data_emp_us["Employers"]
        for x in dat:
            codes.append(x[word])

    elif word == "CodeVid":
        dat = data_works_us["Works"]
        for x in dat:
            codes.append(x[word])

    elif word == "Code CodeVid":
        dat = data_work_us["Work"]
        for x in dat:
            fir = "Code"
            sec = "CodeVid"
            fin = [x[fir], x[sec]]
            codes.append(fin)

    if ident in codes:
        if word != 'Code CodeVid':
            for x in dat:
                if ident == x[word]:
                    dat.remove(x)
        else:
            for x in dat:
                if ident[0] == x[fir] and ident[1] == x[sec]:
                    dat.remove(x)

        if word == "Code":
            data_emp_us = {"Employers": dat}
            with open("Employers.json", 'w') as f:
                json.dump(data_emp_us, f)
                la = tk.Label(second_frame, text="Успешно удалено", bg="#FAF0E6")
                la.grid(column=7, row=5)
                la.after(4000, la.destroy)
                f.close()

        elif word == "CodeVid":
            data_works_us = {"Works": dat}
            with open("Works.json", 'w') as f:
                json.dump(data_works_us, f)
                la = tk.Label(second_frame, text="Успешно удалено", bg="#FAF0E6")
                la.grid(column=7, row=5)
                la.after(4000, la.destroy)
                f.close()
        elif word == "Code CodeVid":
            data_work_us = {"Work": dat}
            with open("Work.json", 'w') as f:
                json.dump(data_work_us, f)
                la = tk.Label(second_frame, text="Успешно удалено", bg="#FAF0E6")
                la.grid(column=7, row=5)
                la.after(4000, la.destroy)
                f.close()

    else:
        la = tk.Label(second_frame, text="Идент не найден", bg="#FAF0E6")
        la.grid(column=7, row=5)
        la.after(5000, la.destroy)


def edit(x):
    global flag
    flag = False
    varss1 = ['Имя', 'Фамилия', 'Отчество', 'Оклад']
    varss2 = ['Описание', 'Оклад']
    varss3 = ['Код вида', 'Д начала', 'М начала', 'Г начала',
              'Д конца', 'М конца', 'Г конца']
    if x == 1:
        varss = varss1
    elif x == 2:
        varss = varss2
    elif x == 3:
        varss = varss3

    if len(mass_ent) > 0:
        for mass in mass_ent:
            tk.Label.destroy(mass)
        mass_ent.clear()
    if len(mass_finder) > 0:
        clean_master()
    if btn4["text"] == "Очистить":
        btn4.configure(text="Добавить")
    if btn5["state"] == "disabled":
        btn5.configure(state="normal", bg="#DCDCDC")
    btn6.configure(text="применить")
    lab_com.grid(column=7, row=2)
    lab_com.after(8000, lab_com.grid_forget)
    com.configure(values=varss)
    com.grid(column=8, row=2)
    com.bind("<<ComboboxSelected>>", lab_change)
    btn6.grid(column=7, row=4)
    label_edit.grid(column=9,row=2)
    label_edit.after(8000, label_edit.grid_forget)
    ent.grid(column=9, row=3)

def edit_act(var, ident, names):
    global data_emp_us
    global data_works_us
    global data_work_us
    g = False
    x = sel.get()
    numb = 10
    da = 'd'
    if x == 1:
        data_time = data_emp_us["Employers"]
        numb = 0
        da = "Employers"
    elif x == 2:
        data_time = data_works_us["Works"]
        numb = 1
        da = "Works"
    elif x == 3:
        data_time = data_work_us["Work"]
        numb = 2
        da = "Work"

    tabl_names = [['Code', 'Last', 'First', 'Third', 'Salary'],
                  ['CodeVid', 'Description', 'Payment'],
                  ['Code', 'CodeVid', 'Begin', 'End']
                  ]
    number = 1
    for i in names:
        if i == var:
            break
        number += 1
    if numb < 2 or number < 2:
        name = tabl_names[numb][number]
    try:
        id_edit = str(ide.get())
    except:
        return 0
    count = 0
    for data_t in data_time:
        if data_t[tabl_names[numb][0]] == id_edit:
            if x == 1:
                if name == "Salary":
                    if all('0' <= k <= '9' for k in ident) and ident != '':
                        data_emp_us[da][count][name] = ident
                        g = True
                else:
                    if all('a' <= k <= 'z' for k in ident.lower()) and ident != '':
                        data_emp_us[da][count][name] = ident
                        g = True
            elif x == 2:
                if name == "Payment":
                    if all('0' <= k <= '9' for k in ident) and ident != '':
                        data_works_us[da][count][name] = ident
                        g = True
                else:
                    if all('a' <= k <= 'z' for k in ident.lower()) and ident != '':
                        data_works_us[da][count][name] = ident
                        g = True
            elif x == 3:
                if all('0' <= k <= '9' for k in ident) and ident != '':
                    if var == "Код вида":
                        data_work_us[da][count][name] = ident
                    elif var == "Д начала":
                        if int(ident) < 32:
                            data_work_us[da][count]['Begin']['Day'] = ident
                    elif var == "М начала":
                        if int(ident) < 13:
                            data_work_us[da][count]['Begin']['Month'] = ident
                    elif var == "Г начала":
                        if int(ident) > 2020:
                            data_work_us[da][count]['Begin']['Year'] = ident
                    elif var == "Д конца":
                        if int(ident) < 32:
                            data_work_us[da][count]['Begin']['Day'] = ident
                    elif var == "М конца":
                        if int(ident) < 13:
                            data_work_us[da][count]['Begin']['Month'] = ident
                    elif var == "Г конца":
                        if int(ident) > 2020:
                            data_work_us[da][count]['Begin']['Year'] = ident
                    else:
                        print("что-то не так")
            if g == True:
                lab_edit.grid(column=8, row=5)
                lab_edit.after(2300, lab_edit.grid_forget)
        count += 1

    if x == 1:
        with open("Employers.json", 'w') as f:
            json.dump(data_emp_us, f)
            f.close()
    elif x == 2:
        with open("Works.json", 'w') as f:
            json.dump(data_works_us, f)
            f.close()
    elif x == 3:
        with open("Work.json", 'w') as f:
            print("DSA")
            json.dump(data_work_us, f)
            f.close()


def finder():
    if len(mass_finder) != 0:
        clean_master()
    if len(mass_ent) > 0:
        for mass in mass_ent:
            tk.Label.destroy(mass)
        mass_ent.clear()
    com.grid_forget()
    btn6.grid_forget()
    en.grid_forget()
    ent.grid_forget()
    label_label.destroy()
    if btn5["state"] == "disabled":
        btn5.configure(state="normal", bg="#DCDCDC")
    lab_com.grid_forget()

    id = tk.StringVar(value='Код')
    entr = tk.Entry(second_frame, textvariable=id)
    entr.grid(column=8, row=2)
    mass_finder.append(entr)
    perez = sel.get()
    bitton = tk.Button(second_frame, text='Найти!', command= lambda: finder_fin(id.get(), bitton, perez))
    bitton.grid(column=7, row=2)
    mass_finder.append(bitton)
    lebel.configure(text='табл' + str(perez))
    lebel.grid(column=7, row=2)
    mass_finder.insert(0, lebel)
    if perez == 3:
        en_finder.grid(column=9, row=2)
        mass_finder.insert(0, en_finder)

def finder_fin(id, bitton, perez):
    global data_emp_us
    global data_works_us
    global data_work_us

    s = []
    data_finder = []
    lest = []
    sel1 = ['Код р.', 'Фамилия', 'Имя', 'Отчество', 'Оклад']
    sel2 = ['Код в.', 'Описание', 'зп за день']
    sel3 = ['Код р.', 'Код в.', 'Д начала', 'М начала', 'Г начала', 'Д конца', 'М конца', 'Г конца']
    lll = ''
    lll2 = ''
    end = 0
    if perez == 1:
        end = 5
        s = sel1
        lll = 'Code'
        with open('Employers.json') as f:
            data_finder = json.load(f)['Employers']
            f.close()
    elif perez == 2:
        end = 3
        s = sel2
        lll = 'CodeVid'
        with open('Works.json') as f:
            data_finder = json.load(f)['Works']
            f.close()
    elif perez == 3:
        end = 8
        s = sel3
        lll = 'Code'
        lll2 = 'CodeVid'
        with open('Work.json') as f:
            data_finder = json.load(f)['Work']
            f.close()

    kount = 0
    for d in data_finder:
        if perez != 3:
            if d[lll] == id:
                break
        else:
            if d[lll] == id:
                if d[lll2] == id_finder.get():
                    break
        kount += 1

    app = []
    if perez != 3:
        cod = []
        for bb in data_finder:
            cod.append(bb[lll])
        if id not in cod:
            return 154
        for b in data_finder[kount].values():
            app.append(b)
    else:
        try:
            app.append(data_finder[kount]["Code"])
            app.append(data_finder[kount]["CodeVid"])
            for n in data_finder[kount]["Begin"].values():
                app.append(n)
            for n in data_finder[kount]["End"].values():
                app.append(n)
        except:
            return 100
    r = 0
    m = 0
    for r in range(end):
        l1 = tk.Label(second_frame, text=s[r], width=20, bg="#FAF0E6", anchor='e')
        l1.grid(column=7, row=r+3)
        mass_finder.append(l1)
        l2 = tk.Label(second_frame, text=app[r], width=15, bg="#d1b6a6", anchor='w')
        l2.grid(column=8, row=r + 3)
        mass_finder.append(l2)
    bitton.grid_forget()


def clean_master():
    j = 0
    i = 0
    print(mass_finder)
    for i in range(2):
        mass_finder[0].grid_forget()
        mass_finder.pop(0)
    print(mass_finder)
    if len(mass_finder) > 1:
        for j in range(2):
            mass_finder[0].destroy()
            mass_finder.pop(0)
    else:
        mass_finder[0].destroy()
        mass_finder.pop()
    print(mass_finder)
    for n in mass_finder:
        tk.Label.destroy(n)
    mass_finder.clear()


root = tk.Tk()
root.title('ExtraWork')
root.geometry("1350x300")
main_frame = tk.Frame(root, bg="")
main_frame.pack(fill=tk.BOTH, expand=1)
my_canvas = tk.Canvas(main_frame, background="#FAF0E6")
my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
y_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL,command=my_canvas.yview)
y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
my_canvas.configure(yscrollcommand=y_scrollbar.set)
my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion= my_canvas.bbox(tk.ALL)))
second_frame = tk.Frame(my_canvas, background="#FAF0E6")

my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
sel = tk.IntVar()
rad1 = tk.Radiobutton(second_frame, text="Работники", value=1,variable=sel, width=20, bg="#FAF0E6")
rad2 = tk.Radiobutton(second_frame, text="Виды работ", value=2,variable=sel, width=20, bg="#FAF0E6")
rad3 = tk.Radiobutton(second_frame, text="Работы", value=3,variable=sel, width=20, bg="#FAF0E6")
rad1.grid(row=0, column=0)
rad2.grid(row=0, column=1)
rad3.grid(row=0, column=2)


btn1 = tk.Button(second_frame, text="Показать", width=20, background="#DCDCDC", command=lambda: show(sel.get(), tabl1,
                                                                                                     tabl2, tabl3))
btn1.grid(column=3, row=0, padx=10, pady=10)
btn2 = tk.Button(second_frame, text="Очистить", width=20, background="#A9A9A9", command=lambda: delet(labels),
                 state="disabled")
btn2.grid(column=3, row=1, padx=10, pady=10)

btn3 = tk.Button(second_frame, text="Действия", width=20, background="#DCDCDC", command=lambda: changing(sel.get()))
btn3.grid(column=4, row=0, padx=10, pady=10)

label_label = tk.Label(second_frame, text="", width=20, bg="#FAF0E6")
label_label.grid(column=7, row=2)


btn4 = tk.Button(second_frame, text="Добавить", width=20, background="#DCDCDC", command=lambda: adding(sel.get(),
                                                                                                       tabl1,
                                                                                                       tabl2,
                                                                                                       tabl3))
tk.Label(second_frame, width=10, text="", bg="#FAF0E6").grid(column=6, row=0)
btn4.grid(column=7, row=0, padx=10, pady=10)
btn5 = tk.Button(second_frame, text="Удалить эл", width=20, background="#DCDCDC", command=lambda: clear())
btn5.grid(column=7, row=1, padx=10, pady=10)
btn7 = tk.Button(second_frame, text="Редактировать", width=20, background="#DCDCDC", command=lambda: edit(sel.get()))
btn7.grid(column=8, row=0, padx=10, pady=10)
btn8 = tk.Button(second_frame, text="Поиск", width=20, background="#DCDCDC", command=lambda: finder())
btn8.grid(column=8, row=1, padx=10, pady=10)
fr = tk.Canvas(second_frame, bg="#FAF0E6", width=316, height=80)
fr.grid(column=7, row=0, rowspan=2, columnspan=2)
varr = tk.StringVar()
ent12 = tk.Entry(second_frame, state="disabled", textvariable=varr)

var = tk.StringVar(value='')
ident = tk.StringVar(value='значение')
btn6 = tk.Button(second_frame, text="удалить", command=lambda: conf_del(var.get(), ident.get()))
en = tk.Entry(second_frame, textvariable=ident)
vars = ['Работники', 'Виды работ', 'Работы']
com = ttk.Combobox(second_frame, values=vars, textvariable=var, background="#FAF0E6", state='readonly')
ide = tk.IntVar(value='')
ent = tk.Entry(second_frame, textvariable=ide)
label_edit = tk.Label(second_frame, width=10, text="Введите код", bg="#FAF0E6")
lab_edit = tk.Label(second_frame, width=10, text="выполнено", bg="#FAF0E6")
lab_com = tk.Label(second_frame, text="Выберите:", bg="#FAF0E6")
lebel = tk.Label(second_frame, width=20, text='', bg="#FAF0E6", anchor='e')
id_finder = tk.StringVar(value='Номер работы')
en_finder = tk.Entry(second_frame, textvariable=id_finder)

dat1 = data_emp_us["Employers"]
dat2 = data_works_us["Works"]
dat3 = data_work_us["Work"]
dat = max(len(dat1), len(dat2), len(dat3))

for i in range(dat+4):
    tk.Label(second_frame, text="").grid(column=15, row=i)

root.mainloop()