import requests,json
import datetime

# from trello_api import client_secret

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def airtable_patch():

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/VINAY/Documents/TRELLO/LOCAL/src/trello/client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    # sheet = client.open("MIK_SALES").sheet1
    gulf_sheet = client.open("NAY_CORE_SALES").sheet1

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
    all_records_url = 'https://api.airtable.com/v0/appj5KvA8Ux4OAyLh/Products?view=Product%20Performance%20View'
    airtable_parameters = { 'Authorization' : 'Bearer {}'.format(airtable_api_key), 'Content-Type' : 'application/json'}
    response = requests.get( all_records_url,  headers = airtable_parameters)
    all_records = response.json()
    offset = all_records.get('offset')

    for record in all_records.get('records'):
        final_records_list.append(record)    

    while offset is not None : 

        # print("pre : {}".format(offset))
        offset_records_url = 'https://api.airtable.com/v0/appj5KvA8Ux4OAyLh/Products?view=Product%20Performance%20View&offset={}'.format(offset)
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

            in_airtable = 0

            if row.get('Product Code+Color') == record.get('fields').get('Unique ID'):

                airtable_product_id = record.get('id')

                # try:

                in_airtable = 1

                #POST Request : 

                post_url = 'https://api.airtable.com/v0/appj5KvA8Ux4OAyLh/SALES'

                single_record = {}

                print(str(row.get('Parent Code')))

                payload = {
                    "records": [
                        {
                            "fields": {
                                "Month": "{}".format(row.get('Month')),
                                "Year": "{}".format(row.get('Year')),
                                "Region": "{}".format(row.get('Region')),
                                "Color": "{}".format(row.get('Color')),
                                "Item Code": "{}".format(row.get('Item Code')),
                                "Parent Code": "{}".format(row.get('Parent Code')),
                                "Products": ["{}".format(airtable_product_id)],
                                "Sold QTY": str(row.get('Sold Qty')).replace('None', ''),
                                "Cost Value": str(row.get('Cost Value')).replace('None', ''),
                                "Net Sales(excl VAT)" : str(row.get('Net Sales(excl VAT)')).replace('None', ''),
                                "Net Sales INC VAT" : str(row.get('Net Sales INC VAT')).replace('None', ''),
                                "Margin" : str(row.get('Margin')).replace('None', '')
                            }}]}

                

                # single_record['id'] = record.get('id')
                # single_record['fields'] = fields_body

                # records_body = []

                # records_body.append(single_record)


                # data_body = {}

                # data_body['records'] = records_body

                # print(json.dumps(data_body))
                

                patch_response = requests.request("POST", post_url, headers=airtable_parameters, data = json.dumps(payload))
                # patch_response = requests.patch(patch_url, headers = airtable_parameters, data= json.dumps(data_body))

                print(patch_response.status_code)
                # print(patch_response.json())

                i=i+1


                if patch_response.status_code == 200:
                    break
                else:
                    supplier_error_skus.append(row.get('Product Code'))
                    print(patch_response.json())
                    break
                # except:
                #     print('exception')
                #     break
            

        if in_airtable == 0:
            not_in_airtable.append(str(row.get('Parent Code')))
        # else:
        #     print("Emmpty")
        #     continue

    print(len(supplier_error_skus))
    print(supplier_error_skus)       
    print(i)
    print(len(not_in_airtable))
    print(not_in_airtable)



airtable_patch()