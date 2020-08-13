import mysql.connector
#  from mysql.connector import Error
from tkinter import *
import tkinter.ttk as ttk

# подключение к базе
conn = mysql.connector.connect(user='stock_admin', password='1001', host='127.0.0.1', database='stock')
cursor = conn.cursor()

# создаем окно приложения
window = Tk()  # окно
window.title('Склад')  # заголовок окна
window.geometry('800x350')  # начальный размер окна


def window_deleted():
    """Автоматически вызывается при закрытии приложения. Закрывает соединение с сервером mysql"""
    cursor.close()
    conn.close()
    window.quit()  # явное указание на выход из программы


def new_supply():
    """Вызывается при нажатии на кнопку "Оформить поставку"."""
    frame_new_purchase.grid_forget()
    frame_info.grid_forget()
    frame_report_supply.grid_forget()
    frame_report_purchase.grid_forget()
    frame_new_supply.grid(row=0, column=0)

    # Заполняем разворачиваемые списки информацией из БД
    cursor.execute('select name from products;')
    answer = cursor.fetchall()
    temp_list = []
    for row in answer:
        temp_list.append(row[0])
    combobox_product_newSupply['values'] = temp_list

    cursor.execute('select name from vendors;')
    answer = cursor.fetchall()
    temp_list = []
    for row in answer:
        temp_list.append(row[0])
    combobox_vendor_newSupply['values'] = temp_list

    label_headline_new_supply.grid(row=0, column=0, columnspan=2)  # Заголовок
    label_product_newSupply.grid(row=1, column=0, sticky='w')
    combobox_product_newSupply.grid(row=1, column=1, sticky='w')
    label_quantity_newSupply.grid(row=2, column=0, sticky='w')
    entry_quantity_newSupply.grid(row=2, column=1, sticky='w')
    button_include_newSupply.grid(row=3, column=0, sticky='w')
    button_clean_newSupply.grid(row=3, column=1, sticky='w')
    label_list_newSupply.grid(row=4, column=0, sticky='w')
    text_newSupply.grid(row=5, column=0, columnspan=2)
    label_vendor_newSupply.grid(row=6, column=0, sticky='w')
    combobox_vendor_newSupply.grid(row=6, column=1, sticky='w')
    button_execute_newSupply.grid(row=7, column=0, sticky='w')


def include_new_supply():
    """Вызывается при нажатии на кнопку "Добавиь в список" в разделе "Оформиление новой поставки"."""

    # добавляем пару элементов "название" и "количество" в список товаров
    list_products_newSupply.append([combobox_product_newSupply.get(), entry_quantity_newSupply.get()])

    # добавляем записи в текстовое поле
    text_newSupply.delete('1.0', END)  # очищаем старый текст перед добавлением нового
    temp_text = ''
    for row in list_products_newSupply:
        temp_text += row[0] + ' ' + row[1] + '\n'
    text_newSupply.insert(1.0, temp_text)


def clean_new_supply():
    """Вызывается при нажатии на кнопку "Очистить список" в разделе "Оформиление новой поставки"."""
    list_products_newSupply.clear()
    text_newSupply.delete('1.0', END)


def execute_new_supply():
    """Вызывается при нажатии на кнопку "Оформить поставку" в разделе "Оформиление новой поставки"."""

    # заменяем названия товаров в списке на их ID
    for row in list_products_newSupply:
        cursor.execute('select id_product from products where name="' + row[0] + '";')
        row[0] = str(cursor.fetchone()[0])

    # считываем название поставщика и заменяем на ID
    cursor.execute('select id_vendor from vendors where name="' + combobox_vendor_newSupply.get() + '";')
    id_current_vendor = str(cursor.fetchone()[0])

    # создаем запись о новой поставке в БД
    cursor.execute('insert into supplies (id_vendor) values (' + id_current_vendor + ');')
    conn.commit()

    # находим ID последней поставки
    cursor.execute('select max(id_supply) from supplies;')
    id_current_supply = str(cursor.fetchone()[0])

    # записываем в БД поставленные товары
    for row in list_products_newSupply:
        cursor.execute('''insert into products_in_supply (id_supply, id_product, quantity)
            values (''' + id_current_supply + ', ' + row[0] + ', ' + row[1] + ');')
        conn.commit()

    clean_new_supply()  # очищаем список товаров


def new_purchase():
    """Вызывается при нажатии на кнопку "Оформить покупку"."""
    frame_new_supply.grid_forget()
    frame_info.grid_forget()
    frame_report_supply.grid_forget()
    frame_report_purchase.grid_forget()
    frame_new_purchase.grid(row=0, column=0)

    # Заполняем разворачиваемый список информацией из БД
    cursor.execute('select name from products;')
    answer = cursor.fetchall()
    temp_list = []
    for row in answer:
        temp_list.append(row[0])
    combobox_product_newPurchase['values'] = temp_list

    label_headline_new_purchase.grid(row=0, column=0, columnspan=2)  # Заголовок
    label_product_newPurchase.grid(row=1, column=0, sticky='w')
    combobox_product_newPurchase.grid(row=1, column=1, sticky='w')
    label_quantity_newPurchase.grid(row=2, column=0, sticky='w')
    entry_quantity_newPurchase.grid(row=2, column=1, sticky='w')
    button_include_newPurchase.grid(row=3, column=0, sticky='w')
    button_clean_newPurchase.grid(row=3, column=1, sticky='w')
    label_list_newPurchase.grid(row=4, column=0, sticky='w')
    text_newPurchase.grid(row=5, column=0, columnspan=2)
    button_execute_newPurchase.grid(row=6, column=0, sticky='w')


def include_new_purchase():
    """Вызывается при нажатии на кнопку "Добавиь в список" в разделе "Оформиление новой покупки"."""

    # добавляем пару элементов "название" и "количество" в список товаров
    list_products_newPurchase.append([combobox_product_newPurchase.get(), entry_quantity_newPurchase.get()])
    # добавляем записи в текстовое поле
    text_newPurchase.delete('1.0', END)  # очищаем старый текст перед добавлением нового
    temp_text = ''
    for row in list_products_newPurchase:
        temp_text += row[0] + ' ' + row[1] + '\n'
    text_newPurchase.insert(1.0, temp_text)


def clean_new_purchase():
    """Вызывается при нажатии на кнопку "Очистить список" в разделе "Оформиление новой покупки"."""
    list_products_newPurchase.clear()
    text_newPurchase.delete('1.0', END)


def execute_new_purchase():
    """Вызывается при нажатии на кнопку "Оформить покупку" в разделе "Оформиление новой покупки"."""

    # заменяем названия товаров в списке на их ID
    for row in list_products_newPurchase:
        cursor.execute('select id_product from products where name="' + row[0] + '";')
        row[0] = str(cursor.fetchone()[0])

    # создаем запись о новой покупке в БД
    cursor.execute('insert into purchases (purchase_date) values (current_timestamp);')
    conn.commit()

    # находим ID последней покупки
    cursor.execute('select max(id_purchase) from purchases;')
    id_current_purchase = str(cursor.fetchone()[0])

    # записываем в БД купленные товары
    for row in list_products_newPurchase:
        cursor.execute('''insert into products_in_purchase (id_purchase, id_product, quantity)
                values (''' + id_current_purchase + ', ' + row[0] + ', ' + row[1] + ');')
        conn.commit()

    clean_new_purchase()  # очищаем список товаров


def product_info():
    """Вызывается при нажатии на кнопку "Найти информацию о товаре"."""
    frame_new_supply.grid_forget()
    frame_new_purchase.grid_forget()
    frame_report_supply.grid_forget()
    frame_report_purchase.grid_forget()
    frame_info.grid(row=0, column=0)

    # Заголовок
    label_headline_info.grid(row=0, column=0)

    # Разворачиваемый список
    cursor.execute('select name from products;')
    answer = cursor.fetchall()
    names_list = []
    for row in answer:
        names_list.append(row[0])
    combobox_list_products['values'] = names_list
    combobox_list_products.grid(row=1, column=0)

    # кнопка "Отобразить"
    button_product_info.grid(row=1, column=1)


def show_product_info():
    """Вызывается при нажатии на кнопку "Отобразить" в разделе "Информация о товаре"."""
    product_name = combobox_list_products.get()
    cursor.execute('select id_department, in_stock from products where name="' + product_name + '";')
    answer1 = cursor.fetchall()
    cursor.execute('select name from departments where id_department=' + str(answer1[0][0]) + ';')
    answer2 = cursor.fetchall()
    label_department_name['text'] = 'Отдел: ' + str(answer2[0][0])
    label_department_name.grid(row=2, column=0)
    label_in_stock['text'] = 'В наличии: ' + str(answer1[0][1])
    label_in_stock.grid(row=3, column=0)


def supply_report():
    """Вызывается при нажатии на кнопку "Отчет о поставках"."""
    frame_new_supply.grid_forget()
    frame_new_purchase.grid_forget()
    frame_info.grid_forget()
    frame_report_purchase.grid_forget()
    frame_report_supply.grid(row=0, column=0)

    # Заголовок
    label_headline_report_supply.grid(row=0, column=0, columnspan=9)

    # Выбор дат
    label_from_report_supply.grid(row=1, column=0)
    combobox_day_from_repSupply.grid(row=1, column=1)
    combobox_month_from_repSupply.grid(row=1, column=2)
    combobox_year_from_repSupply.grid(row=1, column=3)
    label_to_report_supply.grid(row=1, column=4)
    combobox_day_to_repSupply.grid(row=1, column=5)
    combobox_month_to_repSupply.grid(row=1, column=6)
    combobox_year_to_repSupply.grid(row=1, column=7)

    # кнопка "Отобразить"
    button_report_supply.grid(row=1, column=8)


def show_report_supply():
    """Вызывается при нажатии кнопки "Отобразить" в разделе "Отчет о поставках"."""
    first_date = combobox_year_from_repSupply.get() + '-' + combobox_month_from_repSupply.get() + '-' + combobox_day_from_repSupply.get() + ' 00:00:00'
    second_date = combobox_year_to_repSupply.get() + '-' + combobox_month_to_repSupply.get() + '-' + combobox_day_to_repSupply.get() + ' 00:00:00'
    cursor.execute('''select v.name, p.name, pis.quantity, DATE_FORMAT(supply_date, '%d.%m.%Y %H:%i:%s')
        from vendors as v, supplies as s, products as p, products_in_supply as pis
        where v.id_vendor=s.id_vendor
        and p.id_product=pis.id_product
        and s.id_supply=pis.id_supply
        and supply_date>"''' + first_date + '''"
        and supply_date<"''' + second_date + '''"
        ;''')
    result = cursor.fetchall()
    temp_text = ''
    for row in result:
        temp_text += row[0] + '   ' + row[1] + '   ' + str(row[2]) + '   ' + str(row[3]) + '\n'
    text_report_supply.delete('1.0', END)  # очищаем старый текст перед добавлением нового
    text_report_supply.insert(1.0, temp_text)
    text_report_supply.grid(row=2, column=0, columnspan=9)


def purchase_report():
    """Вызывается при нажатии на кнопку "Отчет о покупках"."""
    frame_new_supply.grid_forget()
    frame_new_purchase.grid_forget()
    frame_info.grid_forget()
    frame_report_supply.grid_forget()
    frame_report_purchase.grid(row=0, column=0)

    # Заголовок
    label_headline_report_purchase.grid(row=0, column=0, columnspan=9)

    # Выбор дат
    label_from_report_purchase.grid(row=1, column=0)
    combobox_day_from_repPurchase.grid(row=1, column=1)
    combobox_month_from_repPurchase.grid(row=1, column=2)
    combobox_year_from_repPurchase.grid(row=1, column=3)
    label_to_report_purchase.grid(row=1, column=4)
    combobox_day_to_repPurchase.grid(row=1, column=5)
    combobox_month_to_repPurchase.grid(row=1, column=6)
    combobox_year_to_repPurchase.grid(row=1, column=7)

    # кнопка "Отобразить"
    button_report_purchase.grid(row=1, column=8)


def show_report_purchase():
    """Вызывается при нажатии кнопки "Отобразить" в разделе "Отчет о покупках"."""
    first_date = combobox_year_from_repPurchase.get() + '-' + combobox_month_from_repPurchase.get() + '-' + combobox_day_from_repPurchase.get() + ' 00:00:00'
    second_date = combobox_year_to_repPurchase.get() + '-' + combobox_month_to_repPurchase.get() + '-' + combobox_day_to_repPurchase.get() + ' 00:00:00'
    cursor.execute('''select p.name, pip.quantity, purchase_date
        from purchases as pur, products as p, products_in_purchase as pip
        where p.id_product=pip.id_product
        and pur.id_purchase=pip.id_purchase
        and purchase_date>"''' + first_date + '''"
        and purchase_date<"''' + second_date + '''"
        ;''')
    result = cursor.fetchall()
    temp_text = ''
    for row in result:
        temp_text += row[0] + '   ' + str(row[1]) + '   ' + str(row[2]) + '\n'
    text_report_purchase.delete('1.0', END)  # очищаем старый текст перед добавлением нового
    text_report_purchase.insert(1.0, temp_text)
    text_report_purchase.grid(row=2, column=0, columnspan=9)


window.protocol('WM_DELETE_WINDOW', window_deleted)  # обработчик закрытия окна

# списки товаров в поставке/покупке
list_products_newPurchase = []
list_products_newSupply = []

# заполняем окно
# Frames (рамки)
left_frame = Frame(window, bd=10)
left_frame.grid(row=0, column=0)
vborder = Frame(window, bg='black')
vborder.grid(row=0, column=1, ipady=170)
hborder = Frame(window, bg='black')
hborder.grid(row=1, column=2, ipadx=311)
right_frame = Frame(window, bd=10)
right_frame.grid(row=0, column=2)
frame_new_supply = Frame(right_frame)
frame_new_purchase = Frame(right_frame)
frame_info = Frame(right_frame)
frame_report_supply = Frame(right_frame)
frame_report_purchase = Frame(right_frame)


# виджеты левой рамки
# кнопки
button1 = Button(left_frame, text='Оформить поставку', width=20, command=new_supply).grid(row=0)
button2 = Button(left_frame, text='Оформить покупку', width=20, command=new_purchase).grid(row=1)
button3 = Button(left_frame, text='Найти информацию\nо товаре', width=20, command=product_info).grid(row=2)
button4 = Button(left_frame, text='Отчет о поставках', width=20, command=supply_report).grid(row=3)
button5 = Button(left_frame, text='Отчет о покупках', width=20, command=purchase_report).grid(row=4)

# виджеты правой рамки
# Надписи
label_headline_new_supply = Label(frame_new_supply, text='Оформление новой поставки')  # Заголовок
label_vendor_newSupply = Label(frame_new_supply, text='Поставщик: ')
label_product_newSupply = Label(frame_new_supply, text='Товар: ')
label_quantity_newSupply = Label(frame_new_supply, text='Количество: ')
label_list_newSupply = Label(frame_new_supply, text='Список товаров в поставке:')

label_headline_new_purchase = Label(frame_new_purchase, text='Оформление новой покупки')  # Заголовок
label_product_newPurchase = Label(frame_new_purchase, text='Товар: ')
label_quantity_newPurchase = Label(frame_new_purchase, text='Количество: ')
label_list_newPurchase = Label(frame_new_purchase, text='Список товаров в покупке:')

label_headline_info = Label(frame_info, text='Информация о товаре')  # Заголовок
label_department_name = Label(frame_info)  # Отдел: <>
label_in_stock = Label(frame_info)  # В наличии: <>

label_headline_report_supply = Label(frame_report_supply, text='Отчет о поставках')  # Заголовок
label_from_report_supply = Label(frame_report_supply, text='С ')
label_to_report_supply = Label(frame_report_supply, text='По ')

label_headline_report_purchase = Label(frame_report_purchase, text='Отчет о покупках')  # Заголовок
label_from_report_purchase = Label(frame_report_purchase, text='С ')
label_to_report_purchase = Label(frame_report_purchase, text='По ')

# поля ввода
entry_quantity_newSupply = Entry(frame_new_supply, width=5)
entry_quantity_newPurchase = Entry(frame_new_purchase, width=5)

# поле вывода текста
text_newSupply = Text(frame_new_supply, height=10, width=75, wrap=WORD)
text_newPurchase = Text(frame_new_purchase, height=10, width=75, wrap=WORD)
text_report_supply = Text(frame_report_supply, height=16, width=75, wrap=WORD)
text_report_purchase = Text(frame_report_purchase, height=16, width=75, wrap=WORD)


# разворачиваемые списки
combobox_vendor_newSupply = ttk.Combobox(frame_new_supply, width=40)
combobox_product_newSupply = ttk.Combobox(frame_new_supply, width=40)

combobox_product_newPurchase = ttk.Combobox(frame_new_purchase, width=40)

combobox_list_products = ttk.Combobox(frame_info, width=40)

combobox_day_from_repSupply = ttk.Combobox(frame_report_supply, width=2)
combobox_day_to_repSupply = ttk.Combobox(frame_report_supply, width=2)
combobox_month_from_repSupply = ttk.Combobox(frame_report_supply, width=2)
combobox_month_to_repSupply = ttk.Combobox(frame_report_supply, width=2)
combobox_year_from_repSupply = ttk.Combobox(frame_report_supply, width=4)
combobox_year_to_repSupply = ttk.Combobox(frame_report_supply, width=4)

combobox_day_from_repPurchase = ttk.Combobox(frame_report_purchase, width=2)
combobox_day_to_repPurchase = ttk.Combobox(frame_report_purchase, width=2)
combobox_month_from_repPurchase = ttk.Combobox(frame_report_purchase, width=2)
combobox_month_to_repPurchase = ttk.Combobox(frame_report_purchase, width=2)
combobox_year_from_repPurchase = ttk.Combobox(frame_report_purchase, width=4)
combobox_year_to_repPurchase = ttk.Combobox(frame_report_purchase, width=4)


# заполнение некоторых из разворачиваемых списков
numbers = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
combobox_month_from_repSupply['values'] = numbers
combobox_month_to_repSupply['values'] = numbers
combobox_month_from_repPurchase['values'] = numbers
combobox_month_to_repPurchase['values'] = numbers
numbers += ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
            '25', '26', '27', '28', '29', '30', '31']
combobox_day_from_repSupply['values'] = numbers
combobox_day_to_repSupply['values'] = numbers
combobox_day_from_repPurchase['values'] = numbers
combobox_day_to_repPurchase['values'] = numbers
numbers = []
for i in range(2019, 2030):
    numbers.append(str(i))
combobox_year_from_repSupply['values'] = numbers
combobox_year_to_repSupply['values'] = numbers
combobox_year_from_repPurchase['values'] = numbers
combobox_year_to_repPurchase['values'] = numbers

# кнопки
button_include_newSupply = Button(frame_new_supply, text='Добавить в список', width=15, command=include_new_supply)
button_clean_newSupply = Button(frame_new_supply, text='Очистить список', width=15, command=clean_new_supply)
button_execute_newSupply = Button(frame_new_supply, text='Оформить поставку', width=15, command=execute_new_supply)

button_include_newPurchase = Button(frame_new_purchase, text='Добавить в список', width=15, command=include_new_purchase)
button_clean_newPurchase = Button(frame_new_purchase, text='Очистить список', width=15, command=clean_new_purchase)
button_execute_newPurchase = Button(frame_new_purchase, text='Оформить покупку', width=15, command=execute_new_purchase)

button_product_info = Button(frame_info, text='Найти', width=15, command=show_product_info)
button_report_supply = Button(frame_report_supply, text='Сформировать отчет', command=show_report_supply)
button_report_purchase = Button(frame_report_purchase, text='Сформировать отчет', command=show_report_purchase)


window.mainloop()  # запускает интерпретатор окна и передает ему управление
