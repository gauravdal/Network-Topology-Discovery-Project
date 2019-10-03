from netmiko import ConnectHandler
from pprint import pprint
from getpass import getpass
import json
import re
import xlsxwriter

def access_switch(switch_ip_addr_file):
    username = input('Enter the username for SSH Connection: ')
    password = getpass()

    with open(switch_ip_addr_file,'r') as switch_ip:
        switch_ip_list= switch_ip.read().splitlines()

        pprint(switch_ip_list)

    print('Accessing each switch\n ')
    print('\n\n')
    for each_ip in switch_ip_list:
        print('Accessing switch: '+each_ip)
        ios_device = {
            'device_type':'cisco_ios',
            'host':each_ip,
            'username': username,
            'password': password
        }

        session = ConnectHandler(**ios_device)
        #session.send_config_set('no ip domain-name')
        #session.send_command('wr')

        device_hostname = json.dumps(session.send_command('show run | section include hostname'))
        device_hostname = json.loads(device_hostname)
        output = json.dumps(session.send_command('show cdp neighbors'))
        output = json.loads(output)

        write_switch_config_in_file(output,each_ip)

def write_switch_config_in_file(output, each_ip):

        with open('switch_'+each_ip, 'a') as switch_output:
            switch_output.write(output)



if __name__ == '__main__':

    access_switch('switch_ip_addr_file')