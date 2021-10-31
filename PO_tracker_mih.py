import requests,json
import datetime

# from trello_api import client_secret

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def airtable_patch():

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("D:/MyData/Desktop/Airtable/client_secret.json", scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("MHR - PO Tracker").get_worksheet(0)
    # sheet = client.open("ELC Catalog").get_worksheet(3)

    # # Extract and print all of the values
    list_of_rows = sheet.get_all_records()
    print("Contents of the Sheet : {}".format(len(list_of_rows)))

    # Extract and print all of the values
    # gulf_list_of_rows = gulf_sheet.get_all_records()
    # print("Contents of the Sheet : {}".format(len(gulf_list_of_rows)))

    
    airtable_api_key = 'keyAu4L6lcnNMAg8o'  #VInay

    # airtable_api_key = 'apppcPc0I0oiI7UkU'
    
    final_records_list = []

    # Fashion Base ID : appeHcYmbc6eF7bxj
    # MIK _ PLM UAT Base ID : apppqYPiGYGafKi6K
    # Some new PLM ID : appdTgAAkCpBLtZA7

    # First call the Airtable GET records API. It returns only 100 records at a time.. Then, with the offset values, loop till you get all records... 
    all_records_url = 'https://api.airtable.com/v0/apppcPc0I0oiI7UkU/PRODUCTS?view=PO%20TRACKER%20VIEW'
    airtable_parameters = { 'Authorization' : 'Bearer {}'.format(airtable_api_key), 'Content-Type' : 'application/json'}
    response = requests.get( all_records_url,  headers = airtable_parameters)
    print(response.text)
    all_records = response.json()
    offset = all_records.get('offset')

    for record in all_records.get('records'):
        final_records_list.append(record)    

    while offset is not None : 

        # print("pre : {}".format(offset))
        offset_records_url = 'https://api.airtable.com/v0/apppcPc0I0oiI7UkU/PRODUCTS?view=PO%20TRACKER%20VIEW&offset={}'.format(offset)
        # airtable_parameters = { 'Authorization' : 'Bearer {}'.format(airtable_api_key), 'Content-Type' : 'application/json'}
        offset_response = requests.get( offset_records_url,  headers = airtable_parameters)
        offset_response = offset_response.json()

        # final_records_list.append(offset_response.get('records'))
        offset = offset_response.get('offset')
        # print("post : {}".format(offset))
        for record in offset_response.get('records'):
            final_records_list.append(record)


    print(len(final_records_list))

    
    supplier_error_skus = []
    print(list_of_rows[:5])
    

    i=0
    not_in_airtable = []

    # FP NAME UPDATES : 

    for record in final_records_list:
    # for row in gulf_list_of_rows[]:
        

        if record.get('fields').get('RMS Parent ID') is not None:

            in_airtable = 0

        
            for row in list_of_rows:
        # for record in final_records_list:


                if record.get('fields').get('RMS Parent ID') == row.get('PARENT CODE'):

                    # print(row.get('UAE_WH_STATUS'))


                    in_airtable = 1

                    
                    patch_url = 'https://api.airtable.com/v0/apppcPc0I0oiI7UkU/PRODUCTS'

                    single_record = {}

                    fields_body = {}

                    fields_body['PO# KSA'] = '{}'.format(row.get('PO# KSA'))
                    # fields_body['PO QTY- KSA'] = '{}'.format(row.get('PO QTY (KSA)'))
                    fields_body['PO QTY- KSA'] =row.get('PO QTY (KSA)')
                    fields_body['Pricing'] = '{}'.format(row.get('PRICING'))
                    fields_body['RCVD QTY - KSA'] = '{}'.format(row.get('RCVD QTY (KSA)'))
                    fields_body['RCVD QTY - KSA'] =row.get('RCVD QTY (KSA)')
                    fields_body['Date RCVD - KSA'] = '{}'.format(row.get('DATE RCVD'))
                    # fields_body['FOB (Supplier Currency)'] = '{}'.format(row.get('UNIT COST ($)'))
                    fields_body['FOB (Supplier Currency)'] = float(str(row.get('UNIT COST ($)')).replace('$',''))


                    # fields_body['PO# KSA'] = row.get('PO# KSA')
                    # fields_body['PO QTY- KSA'] = row.get('PO QTY (KSA)')
                    # fields_body['Pricing'] = row.get('PRICING')
                    # fields_body['RCVD QTY - KSA'] = row.get('RCVD QTY (KSA)')
                    # fields_body['Date RCVD - KSA'] = row.get('DATE RCVD')
                    # # fields_body['FOB (Supplier Currency)'] = '{}'.format(row.get('UNIT COST ($)'))
                    # fields_body['FOB (Supplier Currency)'] = float(str(row.get('UNIT COST ($)')).replace('$',''))


                    single_record['id'] = record.get('id')
                    single_record['fields'] = fields_body

                    records_body = []

                    records_body.append(single_record)

                    data_body = {}

                    data_body['records'] = records_body

                    # print(json.dumps(data_body))
                    
                    patch_response = requests.patch(patch_url, headers = airtable_parameters, data= json.dumps(data_body))
                    # patch_response = requests.request("POST", patch_url, headers=airtable_parameters, data = json.dumps(payload))
                    # patch_response = requests.patch(patch_url, headers = airtable_parameters, data= json.dumps(data_body))

                    print(patch_response.status_code)
                    # print(patch_response.json())

                    i=i+1


                    if patch_response.status_code == 200:
                        break
                    else:
                        supplier_error_skus.append(row.get('Item_Parent'))
                        print(patch_response.json())
                        break
                    # except:
                    #     print('exception')
                    #     break

            
            

        # if in_airtable == 0:
        #     not_in_airtable.append(str(record.get('fields').get('Parent ID (Internal)')))
        #     patch_url = 'https://api.airtable.com/v0/appOvbpsWt8HjCzPi/Product%20Data'

        #     single_record = {}

        #     fields_body = {}

        #     fields_body['eComm Listed'] = 'No'

        #     single_record['id'] = record.get('id')
        #     single_record['fields'] = fields_body

        #     records_body = []

        #     records_body.append(single_record)

        #     data_body = {}

        #     data_body['records'] = records_body

        #     # print(json.dumps(data_body))
            
        #     patch_response = requests.patch(patch_url, headers = airtable_parameters, data= json.dumps(data_body))
        #     # patch_response = requests.request("POST", patch_url, headers=airtable_parameters, data = json.dumps(payload))
        #     # patch_response = requests.patch(patch_url, headers = airtable_parameters, data= json.dumps(data_body))

        #     print(patch_response.status_code)
        #     # print(patch_response.json())

        #     i=i+1


        #     if patch_response.status_code == 200:
        #         continue
        #     else:
        #         supplier_error_skus.append(record.get('fields').get('Parent ID (Internal)'))
        #         print(patch_response.json())
        #         continue
        # # else:
        # #     print("Emmpty")
        # #     continue

    print(len(supplier_error_skus))
    print(supplier_error_skus)       
    print(i)
    print(len(not_in_airtable))
    print(not_in_airtable)



airtable_patch()