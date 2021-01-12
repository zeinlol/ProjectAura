import PySimpleGUI as sg
import os
import socket
import json
from time import sleep
import wakeonlan
import threading
import shutil
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_folder = '/home/pi/Documents/SmartHub/'
data_file = 'data.txt'
log_file = 'logs.txt'
sg.theme('Light Blue')
Connected = False

# # # # # # # # # # # # # # # # LAYOUTS
layout_sing_in = [[sg.Text('You can find your ID in bot -> Settings -> Account info', size=(40, 1))],
                  [sg.Text('Telegram ID: ', size=(10, 1)), sg.InputText()],
                  [sg.Text(size=(40, 1), key='-OUTPUT-')],
                  [sg.Button('Ok'), sg.Button('Cancel')]]
layout_main = [[sg.Text('Welcome!', key='-COMMAND-')],
               [sg.Button('Add this Raspberry')],
               [sg.Text(size=(40, 1), key='-OUTPUT_ADD_PC-')],
               [sg.Button('Remove this Raspberry')],
               [sg.Text(size=(40, 1), key='-OUTPUT_REMOVE_PC-')],
               [sg.Button('Delete info')]]
layout_error_con = [[sg.Text('Sorry, no connection with server', size=(40, 1))],
                    [sg.Button('Ok'), sg.Button('Cancel')]]
host = '159.65.206.216'
localhost = '192.168.0.113'

def connect():
    global sock
    global Connected
    # try:
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     sock.connect((host, 8888))
    #     Connected = True
    # except:
    #     Connected = False
    #     pass
    try:
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, 8888))
        print('Connected to the server')
        info = ['dev_onl', get_mac(), get_tg_id()]  # comm, mac, user_id
        sock.send(json.dumps(info).encode('ascii'))
        Connected = True
    except:
        Connected = False
        print('Server not responding')
        sleep(60)
        pass


# # # # # # # # # # # # # # # # GET SYSTEM INFO
def get_sys_info():
    systeminfo_res = get_pc_name()
    mac_list = get_mac()[0]
    info = [systeminfo_res, mac_list, ' ']
    return info


def get_pc_name():
    b = bytes(os.popen('uname -n').read(), "cp1251")
    data = str(b, "cp866").split()
    return data[0]


# # # # # # # # # # # # # # # # WORK WITH IPCONFIG FUNCTION
def get_ip_v4(info):
    ip_temp = []
    for i in info:
        if len(i) > 6:
            ip_temp.append(i)
    temp = [i for i in ip_temp if i[3] == '.' and i[:7] == '192.168' and i != '192.168.0.1' and i[:7] != '255.255']
    return temp


# # # # # # # # # # # # # # # # WORK WITH SYSTEM INFO FUNCTION
def get_mac():
    mac_list = []
    data = os.popen('ifconfig').read().split()
    for i in data:
        if len(i) == 17 and i[2] == ':':
            mac_list.append(i)
    a = 0
    for i in mac_list:
        i = i.upper()
        mac_list[a] = i.replace(":", "-")
        a += 1
    return mac_list


def shut_down_pc():
    os.system("sudo shutdown -h now")


def reset_pc():
    os.system("sudo reboot")


def delete_info():
    if os.path.exists(data_folder):
        shutil.rmtree(data_folder)
    pass


def check_file(file):
    if os.path.exists(data_folder + file):
        return True
    else:
        try:
            os.mkdir(data_folder)
        except FileExistsError:
            pass
        f = open(data_folder + file, 'w')
        f.write('n')
        f.close()
        return True


def check_reg():
    try:
        file = open(data_folder + data_file, "r")
        if file.read()[0] == 'r':
            file.close()
            return True
        else:
            file.close()
            return False
    except:
        return False


def save_id(tg_id):
    file = open(data_folder + data_file, "w")
    file.write('r' + tg_id + '!')
    file.close()


def save_data(file, data):
    try:
        f = open(data_folder + file, 'a')
        f.write('\n' + data)
        f.close()
    except:
        pass


def get_tg_id():
    file = open(data_folder + data_file, "r")
    text = file.read()
    st = False
    tg_id = ''
    for i in text:
        if i == 'r':
            st = True
        if st is True:
            tg_id += i
        if i == '!':
            st = False
    return tg_id[1:-1]


def show_gui():
    window_sing_in = sg.Window('Smart Home Hub', layout_sing_in, finalize=True)
    check_file(data_file)
    check_file(log_file)
    if check_reg():
        window_sing_in.Hide()
        run_main_interface()
    else:
        window_main_active = False
        window_sing_in.UnHide()
        try:
            get_sys_info()
            while True:
                event, values = window_sing_in.read()
                print(str(event))
                if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                    #socket_fun.close()
                    sock.close()
                    break
                if window_main_active is False and values[0].isnumeric() is True:
                    save_id(values[0])
                    window_main_active = True
                else:
                    window_sing_in['-OUTPUT-'].update('Incorrect user id!')
                if window_main_active is True:
                    window_sing_in.Hide()
                    run_main_interface()
                    print('interdase closed')
                    show_gui()
                    break
        except Exception as e:
            save_data(log_file, "163" + str(e))
            #show_gui()
    window_sing_in.close()
    sock.close()


def run_main_interface():
    global sock
    tg_id = get_tg_id()
    window_main = sg.Window('Smart Home Hub', layout_main, finalize=True)
    while True:
        event_main, values_main = window_main.read()
        if event_main == sg.WIN_CLOSED or event_main == 'Cancel':  # if user closes window or clicks cancel
            break
        if event_main == 'Add this Raspberry':
            try:
                get_sys_info()
                name = ['pc_name', get_pc_name(), tg_id, get_mac()[0], 'ras']  # comm, pc_name, user_id, mac
                print(name)
                sock.send(json.dumps(name).encode('ascii'))
                window_main['-OUTPUT_ADD_PC-'].update('Success')
            except Exception as e:
                sock.close()
                connect()
                save_data(log_file, "184" + str(e))
                window_main['-OUTPUT_ADD_PC-'].update('Ops! Error!')
                pass
        if event_main == 'Remove this Raspberry':
            name = ['del_pc', get_pc_name(), tg_id, get_mac()[0]]  # comm, pc_name, user_id, mac
            try:
                sock.send(json.dumps(name).encode('ascii'))
                window_main['-OUTPUT_REMOVE_PC-'].update('Success')
            except Exception as e:
                save_data(log_file, "193" + str(e))
                sock.close()
                connect()
                window_main['-OUTPUT_REMOVE_PC-'].update('Error!')
        if event_main == 'Delete info':
            delete_info()
            sg.popup('All info deleted')
            window_main.Hide()
            return
            #windows_main.Hide()
            # show_gui()
            # break
        if event_main == 'Add program to autorun folder':
            sg.popup('Program is added to autorun')


def socket_listener():
    global sock
    while check_reg() is False:
        sleep(10)
    tg_id = get_tg_id()
    mac = get_mac()[0]
    while True:
        sleep(3)
        info = ['queue', mac, tg_id]
        data = ['res']
        if Connected is True:
            try:
                sock.send(json.dumps(info).encode('ascii'))
            except:
                connect()
                pass
            try:
                data = json.loads(sock.recv(1024).decode('ascii'))
            except Exception as e:
                data = ['res']
                save_data(log_file, "215" + str(e))
                pass
            if data[0] == 'res':
                pass
            elif data[0] == 'com':
                run_local_command(data[1])
                run_group_command(data[2])
            else:
                pass
            pass
        else:
            connect()
    sock.close()


def run_local_command(data):
    for command in data:
        if command[:2] == 'tf':
            shut_down_pc()
        if command == 'rs':
            reset_pc()


def run_group_command(data):  # run command, data[0] is not used, start from data[1]
    for command in data:
        if command == '0':
            pass
        if command[:2] == 'to':
            wakeonlan.send_magic_packet(command[2:], 'FFFFFFFFFFFF')

def main():
    threading.Thread(target=show_gui).start()
    threading.Thread(target=socket_listener).start()
if __name__ == '__main__':
    #connect()
    main()
