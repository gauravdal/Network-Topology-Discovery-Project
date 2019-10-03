import xlsxwriter
import re
with open('output','r') as out_f:

    workbook = xlsxwriter.Workbook('neighbors_details.xlsx')

    worksheet = workbook.add_worksheet('device')

    worksheet.write('A1','device-Id')
    worksheet.write('B1','Local-Interface')
    worksheet.write('C1','Capability')
    worksheet.write('D1','Port-ID')
    row = 1
    for i,line in enumerate(out_f):
        column = 0
        if(5<=i<=13):
            line = line.strip()
            if(re.match(r'(s\d\..+?)',line,re.I)):
                remote_device_name = line

            elif(line.startswith('Gig')):
                temp_value = re.search(r'(.+?)\s{2,}(\d{1,3}?) +(.+)\s{2,}(.+)',line)
                egress_intf = temp_value.group(1)
                Capability = temp_value.group(3)
                ingress_intf = temp_value.group(4)

                row_content = [remote_device_name,egress_intf, Capability, ingress_intf]
                for each_content in row_content:
                    worksheet.write(row,column,each_content)
                    column +=1
        row +=1
    workbook.close()