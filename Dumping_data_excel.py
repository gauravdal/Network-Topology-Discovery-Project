import xlsxwriter
import re



def desired_parameter_for_excel():

    excel_content = []

    #Putting each ip in a list
    with open('output_files','r') as out_fs:
        out_fs_list = out_fs.read().splitlines()

    #Looping each file and extracting data
    for each_output_file in out_fs_list:
        row_content = []
        output_file_name = each_output_file
        with open(each_output_file,'r') as out_f:
            remote_device_name = 0
            egress_intf = 0
            Capability = 0
            ingress_intf = 0

            for i, line in enumerate(out_f):



                if (5 <= i <= 13):

                    line = line.strip()
                    #print(line)
                    if (re.match(r'(s\d\..+?)', line, re.I)):
                        remote_device_name = line
                        print(remote_device_name)
                        temp_remote_device_name = re.search(r'(.\w?).',remote_device_name)
                        remote_device_name = temp_remote_device_name.group(1)
                        print(remote_device_name)

                    elif (line.startswith('Gig')):
                        temp_value = re.search(r'(.+?)\s{2,}(\d{1,3}?) +(.+)\s{2,}(.+)', line)
                        egress_intf = temp_value.group(1)
                        Capability = temp_value.group(3).strip('  ')
                        ingress_intf = temp_value.group(4)
                        #print(egress_intf, Capability, ingress_intf,sep='\n')
                    if (bool(remote_device_name) == True and
                        bool(egress_intf) == True and
                        bool(Capability) == True and
                        bool(ingress_intf) == True):
                            row_content.append((remote_device_name, egress_intf, Capability, ingress_intf))

                            remote_device_name = 0
                            egress_intf = 0
                            Capability = 0
                            ingress_intf = 0
            feeding_data_To_excel(row_content,output_file_name)
            #print(row_content)

            #for each_row in row_content:
                #print(each_row[0])

        #print(row_content)
        #feeding_data_To_excel(row_content)


def feeding_data_To_excel(row_content,output_file_name):


    workbook = xlsxwriter.Workbook('neigbors_details_'+output_file_name+'.xlsx')
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'device-Id', bold)
    worksheet.write('B1', 'Local-Interface', bold)
    worksheet.write('C1', 'Capability', bold)
    worksheet.write('D1', 'Port-ID', bold)

    row = 1
    column = 0
    for each_line in row_content:

        for each_element in each_line:
            worksheet.write(row,column, each_element)
            column = column + 1
        row = row + 1
        column = 0
    workbook.close()
if __name__ == '__main__':
    desired_parameter_for_excel()