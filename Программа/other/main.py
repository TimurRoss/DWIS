from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from json import dump as JSON_dump
from json import load as JSON_load
import os

BACKGROUND = 'white'


def save_data():
    try:
        x = ent1.get().strip().replace(',', '.').replace(' ', '')
        #y = ent2.get().strip().replace(',', '.').replace(' ', '')
        z = ent3.get().strip().replace(',', '.').replace(' ', '')
        n = ent4.get().strip().replace(',', '.').replace(' ', '')
        v = combobox.get().replace(' мл', '')
        print(v)
        if float(x) > 180 or float(z) > 180 or int(n) > 2:
            messagebox.showerror('Ошибка', 'Вы ввели слишком большое число')
            return
        print(len(x[x.find('.') + 1:]))
        if '.'not in x:
            x += '.0'
        if '.'not in z:
            z += '.0'
    except ValueError:
        messagebox.showerror('Ошибка', 'Вы ввели не число')
        return

    data = {'x': str(x),
            'z': str(z),
            'n': str(n),
            'v': str(v)}
    print(data)

    directory = filedialog.asksaveasfilename(title='Сохранение файла',
                                             filetypes=(('json files', '*.json'), ('all files', '*.*')))
    if '.json' not in directory:
        directory += '.json'
    with open(directory, 'w') as file:
        JSON_dump(data, file, indent=4)
        file.close()


def open_data():
    directory = filedialog.askopenfilename(title='Открыть файл',
                                           filetypes=(('json files', '*.json'), ('all files', '*.*')))

    with open(directory, 'r') as file:
        data = JSON_load(file)
        file.close()

    print(data)
    ent1.delete(0, END)
    ent1.insert(0, data['x'])
    ent3.delete(0, END)
    ent3.insert(0, data['z'])
    ent4.delete(0, END)
    ent4.insert(0, data['n'])
    combobox.delete(0, END)
    combobox.insert(0, data['v'] + ' мл')


def send():
    try:
        x = ent1.get().strip().replace(',', '.')
        #y = ent2.get().strip().replace(',', '.')
        z = ent3.get().strip().replace(',', '.')
        n = ent4.get().strip().replace(',', '.')
        v = combobox.get().replace(' мл', '')
        print(v)
        if float(x) > 180 or float(z) > 180 or int(n) > 2:
            messagebox.showerror('Ошибка', 'Вы ввели слишком большое число')
            return
        print(len(x[x.find('.') + 1:]))
        if '.'not in x:
            x += '.0'
        if '.'not in z:
            z += '.0'
    except ValueError:
        messagebox.showerror('Ошибка', 'Вы ввели не число')
        return

    data = {'x': str(x),
            'z': str(z),
            'n': str(n),
            'v': str(v)}
    print(data)

    with open("data.json", 'w') as file:
        JSON_dump(data, file, indent=4)
        file.close()
    #os.system(f'cd {os.getcwd()}')
    os.system('python send.py')


#Окно
root = Tk()
root.title("Настройка модуля")
root.iconbitmap('icon.ico')
root.geometry("500x500")
root.resizable(False, False)
root.config(background=BACKGROUND)


#Меню
mainmenu = Menu(root)
root.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть...", command=open_data)
filemenu.add_command(label="Сохранить...", command=save_data)
filemenu.add_command(label="Выход", command=root.destroy)

mainmenu.add_cascade(label="Файл",
                     menu=filemenu)

#Граница
lf1 = LabelFrame(root, bg=BACKGROUND)
lf1.place(x=10, y=10, height=420, width=480)


#Текст "координаты"
lb1 = Label(lf1, text="Координаты", font="helvetica 14 bold", background=BACKGROUND)
lb1.grid(column=0, row=0, padx=5, pady=5)


#координата x
ent1 = ttk.Entry(lf1,)
ent1.grid(column=0, row=1)

lb = Label(lf1, text="Широта", font="helvetica 14 bold", background=BACKGROUND)
lb.grid(column=1, row=1, padx=5, pady=5)


#координата y
'''ent2 = Entry(lf1,)


ent2.grid(column=0, row=2)

lb = Label(lf1, text="y", font="helvetica 14 bold")
lb.grid(column=1, row=2)'''

#координата z
ent3 = ttk.Entry(lf1)
ent3.grid(column=0, row=3)

lb = Label(lf1, text="Долгота", font="helvetica 14 bold", background=BACKGROUND)
lb.grid(column=1, row=3, padx=5, pady=5)


#Текст "Глубина сбора воды"
lb = Label(lf1, text="Глубина сбора", font="helvetica 14 bold", background=BACKGROUND)
lb.grid(column=0, row=4, padx=5, pady=5)
#Глубина сбора воды
ent4 = ttk.Spinbox(lf1, width=10, from_=1, to=2, font="helvetica 14 bold", textvariable=StringVar())
ent4.grid(column=0, row=5, padx=5, pady=5)

lb = Label(lf1, text="м.", font="helvetica 14 bold", background=BACKGROUND)
lb.grid(column=1, row=5, padx=5, pady=5, ipadx=1)

#Текст "Глубина сбора воды"
lb = Label(lf1, text="Обьем емкости", font="helvetica 14 bold", background=BACKGROUND)
lb.grid(column=0, row=6)
#Кол-во милилитров
list_V = ['500 мл', '1000 мл']
combobox = ttk.Combobox(lf1, values=list_V)
combobox.grid(column=0, row=7, padx=5, pady=5)


#Кнопка завершения настроек
but = Button(root, text="Завершить", font="helvetica 14 bold", background=BACKGROUND, command=send)
but.place(x=350, y=435)


ent1.insert(0, '0')
ent3.insert(0, '0')
ent4.insert(0, '1')
combobox.insert(0, '500 мл')

if __name__ == "__main__":
    root.mainloop()
