import paramiko
from tkinter import *
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
def save_data(selected_items, filename):
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w',encoding='utf-8') as file:
        file.write('\n'.join(selected_items))

#выбор данный для сохранения, их сохранение
def save_selected_items(listbox):
    selected_items = []
    for index in listbox.curselection():
        selected_item = listbox.get(index)
        if selected_item not in selected_items:
            selected_items.append(selected_item)
    save_data(selected_items, "disk_info.txt")

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

    # Создаём список с информацией о накопителях
    listbox = Listbox(root,width=40, height=20, selectmode="extended")
    for i in range(len(output)):
        listbox.insert(END, f"{output[i]}")
    listbox.pack()
    
    # Добавляем кнопку для сохранения выбранных элементов
    button = Button(root, text="Сохранить", command=lambda: save_selected_items(listbox))
    button.pack()

    root.mainloop()


if __name__ == '__main__':
    main()

