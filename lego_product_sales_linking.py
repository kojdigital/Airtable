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
    # sheet = client.open("MIK_SALES").sheet1
    gulf_sheet = client.open("LEGO SALES").get_worksheet(3)
    # # Extract and print all of the values
    # list_of_rows = sheet.get_all_records()
    # print("Contents of the Sheet : {}".format(len(list_of_rows)))

    # Extract and print all of the values
    gulf_list_of_rows = gulf_sheet.get_all_records()
    print("Contents of the Sheet : {}".format(len(gulf_list_of_rows)))

    



    airtable_api_key = 'keyAu4L6lcnNMAg8o'
    
    final_records_list = []

    # Fashion Base ID : appeHcYmbc6eF7bxj
    # MIK _ PLM UAT Base ID : apppqYPiGYGafKi6K
    # Some new PLM ID : appdTgAAkCpBLtZA7

    # First call the Airtable GET records API. It returns only 100 records at a time.. Then, with the offset values, loop till you get all records... 
    all_records_url = 'https://api.airtable.com/v0/apppuzzh5nGCUb5Nn/Products?view=Vinay%20Stock%20View'
    airtable_parameters = { 'Authorization' : 'Bearer {}'.format(airtable_api_key), 'Content-Type' : 'application/json'}
    response = requests.get( all_records_url,  headers = airtable_parameters)
    all_records = response.json()
    offset = all_records.get('offset')

    for record in all_records.get('records'):
        final_records_list.append(record)    

    while offset is not None :

        # print("pre : {}".format(offset))
        offset_records_url = 'https://api.airtable.com/v0/apppuzzh5nGCUb5Nn/Products?view=Vinay%20Stock%20View&offset={}'.format(offset)
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
    print("RUNNING KSA")
    

    i=0
    not_in_airtable = []

    # FP NAME UPDATES : 

    # for record in final_records_list:
    for row in gulf_list_of_rows:

        for record in final_records_list: 

            if record.get('fields').get('PARENT ITEM') is not None and record.get('fields').get('PARENT ITEM') != 0:

                in_airtable = 0

                if record.get('fields').get('PARENT ITEM') == float(row.get('RMS PARENT ITEM')):

                    airtable_product_id = record.get('id')

                    # try:
                    
                    in_airtable = 1

                    #POST Request : 

                    post_url = 'https://api.airtable.com/v0/apppuzzh5nGCUb5Nn/Sales'

                    single_record = {}

                    print(str(row.get('RMS PARENT ITEM')))

                    payload = {
                        "records": [
                            {
                                "fields": {
                                    "Month": "{}".format(row.get('Month')),
                                    "Year": "{}".format(row.get('Year')),
                                    "District": "{}".format(row.get('District')),
                                    "Store": "{}".format(row.get('Store')),
                                    "Product": ["{}".format(airtable_product_id)],
                                    "Sold QTY": float(str(row.get('Sold QTY')).replace('None', '').replace(',', '').replace('-', '0')),
                                    "Cost of Sales": float(str(row.get('Cost of Sales')).replace('None', '').replace(',', '').replace('-', '0')),
                                    "Net Sales" : float(str(row.get('Net Sales')).replace('None', '').replace(',', '').replace('-', '0'))
                                    
                                }}]}

                    

                    patch_response = requests.request("POST", post_url, headers=airtable_parameters, data = json.dumps(payload))
                    # patch_response = requests.patch(patch_url, headers = airtable_parameters, data= json.dumps(data_body))

                    print(patch_response.status_code)
                    # print(patch_response.json())

                    i=i+1


                    if patch_response.status_code == 200:
                        break
                    else:
                        supplier_error_skus.append(str(row.get('RMS PARENT ITEM')) + '_' + str(row.get('Month')) + '_' + str(row.get('Year')))
                        print(patch_response.json())
                        break
                    # except:
                    #     print('exception')
                    #     break
                

            if in_airtable == 0:
                not_in_airtable.append(str(row.get('RMS PARENT ITEM')))
            # else:
            #     print("Emmpty")
            #     continue

    print(len(supplier_error_skus))
    print(supplier_error_skus)       
    print(i)
    print(len(not_in_airtable))
    print(not_in_airtable)



airtable_patch()