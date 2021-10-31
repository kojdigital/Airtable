import requests,json
import datetime

# from trello_api import client_secret

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def airtable_patch():

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/vinay/Downloads/client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("LEGO STOCK_DATA").get_worksheet(0)
    # gulf_sheet = client.open("NAY SU21 - SALES").get_worksheet(2)

    # # Extract and print all of the values
    list_of_rows = sheet.get_all_records()
    print("Contents of the Sheet : {}".format(list_of_rows[:5]))

    # Extract and print all of the values
    # gulf_list_of_rows = gulf_sheet.get_all_records()
    # print("Contents of the Sheet : {}".format(len(gulf_list_of_rows)))


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

    print(all_records)
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

    for record in final_records_list:
    # for row in gulf_list_of_rows[]:
        

        if record.get('fields').get('PARENT ITEM') is not None and record.get('fields').get('PARENT ITEM') != 0:

            in_airtable = 0

        
            for row in list_of_rows:
        # for record in final_records_list:

            # print(str(row.get('SKU')))

                if record.get('fields').get('PARENT ITEM') == float(row.get('RMS PARENT ITEM')):

                    # try:

                    in_airtable = 1

                    
                    patch_url = 'https://api.airtable.com/v0/apppuzzh5nGCUb5Nn/Products'

                    single_record = {}

                    fields_body = {}

                    # print(row.get('Sold Qty'))
                    print(row.get('RMS PARENT ITEM')) 
                    # print(fields_body['Net Sales (DW)'])

                    

                    # fields_body['CAD/Product Image'] = product_image_body

                    fields_body['KSA VIRTUAL WAREHOUSE - NET'] = float(str(row.get('KSA VIRTUAL WAREHOUSE NET')).replace(",","").replace("~","ignore"))
                    fields_body['KSA VIRTUAL WAREHOUSE - SOH'] = float(str(row.get('KSA VIRTUAL WAREHOUSE')).replace(",","").replace("~","ignore"))
                    fields_body['KSA ECOM VIRTUAL WAREHOUSE - NET'] = float(str(row.get('KSA ECOM VIRTUAL WAREHOUSE NET')).replace(",","").replace("~","ignore"))
                    fields_body['KSA ECOM VIRTUAL WAREHOUSE - SOH'] = float(str(row.get('KSA ECOM VIRTUAL WAREHOUSE')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - DHAHRAN - MALL OF DHAHRAN - NET'] = float(str(row.get('LGO - DHAHRAN - MALL OF DHAHRAN NET')).replace("SAR ","").replace(",","").replace("~","ignore"))
                    fields_body['LGO - DHAHRAN - MALL OF DHAHRAN - SOH'] = float(str(row.get('LGO - DHAHRAN - MALL OF DHAHRAN')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - RIYADH - NAKHEEL MALL 2 - NET'] = float(str(row.get('LGO - RIYADH - NAKHEEL MALL 2 NET')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - RIYADH - NAKHEEL MALL 2 - SOH'] = float(str(row.get('LGO - RIYADH - NAKHEEL MALL 2')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - RIYADH - GRANADA CENTER - NET'] = float(str(row.get('LGO - RIYADH - GRANADA CENTER NET')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - RIYADH - GRANADA CENTER - SOH'] = float(str(row.get('LGO - RIYADH - GRANADA CENTER')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - JEDDAH - RED SEA MALL - NET'] = float(str(row.get('LGO - JEDDAH - RED SEA MALL NET')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - JEDDAH - RED SEA MALL - SOH'] = float(str(row.get('LGO - JEDDAH - RED SEA MALL')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - JEDDAH - SOUQ.COM - NET'] = float(str(row.get('LGO - JEDDAH - SOUQ.COM NET')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - JEDDAH - SOUQ.COM - SOH'] = float(str(row.get('LGO - JEDDAH - SOUQ.COM')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - RIYADH - PARK MALL - NET'] = float(str(row.get('LGO - RIYADH - PARK MALL NET')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - RIYADH - PARK MALL - SOH'] = float(str(row.get('LGO - RIYADH - PARK MALL')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - KSA - WINTER WONDERLAND(SEASONAL) - NET'] = float(str(row.get('LGO - KSA - WINTER WONDERLAND(SEASONAL) - NET')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - KSA - WINTER WONDERLAND(SEASONAL) – SOH'] = float(str(row.get('LGO - KSA - WINTER WONDERLAND(SEASONAL) - SOH')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - MAKKAH - MAKKAH MALL - NET'] = float(str(row.get('LGO - MAKKAH - MAKKAH MALL - NET')).replace(",","").replace("~","ignore"))
                    fields_body['LGO - MAKKAH - MAKKAH MALL - SOH'] = float(str(row.get('LGO - MAKKAH - MAKKAH MALL - SOH')).replace(",","").replace("~","ignore"))

                    filtered_fields_body = {k: v for k, v in fields_body.items() if (v != 'ignore')}

                    fields_body.clear()
                    fields_body.update(filtered_fields_body)

                    single_record['id'] = record.get('id')
                    single_record['fields'] = fields_body

                    records_body = []

                    records_body.append(single_record)

                    data_body = {}

                    data_body['records'] = records_body

                    # print(json.dumps(data_body))
                    
                    patch_response = requests.patch(patch_url, headers = airtable_parameters, data= json.dumps(data_body))
                   

                    print(patch_response.status_code)
                    # print(patch_response.json())

                    i=i+1


                    if patch_response.status_code == 200:
                        break
                    else:
                        supplier_error_skus.append(row.get('RMS PARENT ITEM'))
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