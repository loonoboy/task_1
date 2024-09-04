import paramiko
from tkinter import *
from tkinter import ttk
import getpass
import os

#подключение по ssh и получение даннх
def get_disk_info(hostname,port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command('lsblk -o name,size,model')
        output = stdout.read().decode('utf-8').split('\n')
        return output
    except Exception as e:
        print("err", e)
        return None

#функция записи в txt файл
def save_data(selected_items, entry1, entry2):
    direct = entry1.get()
    filename = entry2.get()
    if not os.path.exists(direct):
        os.makedirs(os.path.dirname(direct), exist_ok=True)
    with open(filename, 'w',encoding='utf-8') as file:
        file.write('\n'.join(selected_items))

#выбор данный для сохранения, их сохранение
def save_selected_items(listbox, entry1, entry2):
    selected_items = []
    for index in listbox.curselection():
        selected_item = listbox.get(index)
        if selected_item not in selected_items:
            selected_items.append(selected_item)
    save_data(selected_items, entry1, entry2)

#основная
def main():
    hostname = input("Введите имя хоста: ")
    port = input("Введите имя порта: ")
    username = input("Введите логин: ")
    password = getpass.getpass("Введите пароль: ")

    output = get_disk_info(hostname, port, username, password)

    #вывод в консоль
    for i in range(len(output)):
        print(f"{output[i]}")

    root = Tk()
    entry1 = Entry(root, width=40)
    entry2 = Entry(root, width=40)
    # Создаём список с информацией о накопителях
    listbox = Listbox(root, width=40, height=20, selectmode="extended")
    for i in range(len(output)):
        listbox.insert(END, f"{output[i]}")
    
    # Добавляем кнопку для сохранения выбранных элементов
    button = Button(root, text="Сохранить", command=lambda: save_selected_items(listbox, entry1, entry2))
    
    listbox.pack(anchor='center')
    label1 = ttk.Label(text="Введите директорию сохранения")
    label1.pack()
    entry1.pack()
    label2= ttk.Label(text="Введите название файла вместе с расширением")
    label2.pack()
    entry2.pack()
    button.pack()

    root.mainloop()


if __name__ == '__main__':
    main()