import requests,json
import datetime

# from trello_api import client_secret

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def airtable_patch():

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('D:/MyData/Desktop/Airtable/client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("NAY Fashion Batch Sales Upload").get_worksheet(0)
    # gulf_sheet = client.open("NAY SU21 - SALES").get_worksheet(2)

    # # Extract and print all of the values
    list_of_rows = sheet.get_all_records()
    print("Contents of the Sheet : {}".format(len(list_of_rows)))

    # Extract and print all of the values
    # gulf_list_of_rows = gulf_sheet.get_all_records()
    # print("Contents of the Sheet : {}".format(len(gulf_list_of_rows)))

    



    airtable_api_key = 'keyAu4L6lcnNMAg8o'
    
    final_records_list = []

    # Fashion Base ID : appeHcYmbc6eF7bxj
    # MIK _ PLM UAT Base ID : apppqYPiGYGafKi6K
    # Some new PLM ID : appdTgAAkCpBLtZA7

    # First call the Airtable GET records API. It returns only 100 records at a time.. Then, with the offset values, loop till you get all records... 
    all_records_url = 'https://api.airtable.com/v0/appeHcYmbc6eF7bxj/Fashion?view=Seasonal%20Product%20Performance'
    airtable_parameters = { 'Authorization' : 'Bearer {}'.format(airtable_api_key), 'Content-Type' : 'application/json'}
    response = requests.get( all_records_url,  headers = airtable_parameters)
    all_records = response.json()
    offset = all_records.get('offset')

    for record in all_records.get('records'):
        final_records_list.append(record)    

    while offset is not None : 

        # print("pre : {}".format(offset))
        offset_records_url = 'https://api.airtable.com/v0/appeHcYmbc6eF7bxj/Fashion?view=Seasonal%20Product%20Performance&offset={}'.format(offset)
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


                if record.get('fields').get('RMS Parent ID') == row.get('Item_Parent'):

                    print(row.get('Item_Parent'))


                    # try:

                    in_airtable = 1

                    
                    patch_url = 'https://api.airtable.com/v0/appeHcYmbc6eF7bxj/Fashion'

                    single_record = {}

                    fields_body = {}

                    # fields_body['CAD/Product Image'] = product_image_body
                    fields_body['NAYOMI ECOM QTY SALES'] = int(str(row.get('NAYOMI ECOM QTY SALES')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['NAYOMI ECOM NET SALES'] = float(str(row.get('NAYOMI ECOM NET SALES')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['KSA FULL PRICE QTY SOLD'] = int(str(row.get('KSA FULL PRICE QTY SOLD')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['GULF FULL PRICE QTY SOLD'] = int(str(row.get('GULF FULL PRICE QTY SOLD')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['KSA FULL PRICE NET SALES'] = float(str(row.get('KSA FULL PRICE NET SALES')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['GULF FULL PRICE NET SALES'] = float(str(row.get('GULF FULL PRICE NET SALES')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['KSA NET SALES VAT EXCL'] = float(str(row.get('KSA NET SALES VAT EXCL')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['GULF NET SALES VAT EXCLUSIVE'] = float(str(row.get('GULF NET SALES VAT EXCLUSIVE')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['KSA Cost of Sales'] = float(str(row.get('KSA Cost of Sales(Without FDC)')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['GULF Cost of Sales'] = float(str(row.get('GULF Cost of Sales(Without FDC)')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['MP REMARKS'] = str(row.get('MP REMARKS')).replace(",","").replace("-","0").replace("~","0000")
                    fields_body['RCVD QTY - KSA'] = int(str(row.get('RCVD QTY - KSA')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['RCVD QTY - UAE'] = float(str(row.get('RCVD QTY - UAE')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['DATE RCVD - KSA 1'] = str(row.get('DATE RCVD - KSA 1')).replace(",","").replace("-","0").replace("~","0000")
                    fields_body['DATE RCVD - KSA 2'] = str(row.get('DATE RCVD - KSA 2')).replace(",","").replace("-","0").replace("~","0000")
                    fields_body['DATE RCVD - UAE 1'] = str(row.get('DATE RCVD - UAE 1')).replace(",","").replace("-","0").replace("~","0000")
                    fields_body['DATE RCVD - UAE 2'] = str(row.get('DATE RCVD - UAE 2')).replace(",","").replace("-","0").replace("~","0000")
                    fields_body['MEGASALE QS'] = int(str(row.get('MEGASALE QS')).replace(",","").replace("-","0").replace("~","0000"))
                    # fields_body['MP REMARKS'] = str(row.get('MP REMARKS')).replace(",","").replace("-","0")

                    # fields_body['Final Image'] = final_image_body

                    filtered_fields_body = {k: v for k, v in fields_body.items() if (v != '0000' and v != 0 and v != 0.0)}

                    fields_body.clear()
                    fields_body.update(filtered_fields_body)

                    single_record['id'] = record.get('id')
                    single_record['fields'] = fields_body

                    records_body = []

                    records_body.append(single_record)

                    data_body = {}

                    data_body['records'] = records_body

                    print(json.dumps(data_body))
                    
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
                # else:
                #     supplier_error_skus.append(record.get('fields').get('RMS Parent ID'))
                #     # print(record.get('fields').get('RMS Parent ID'))


            if in_airtable == 0:
                not_in_airtable.append(str(row.get('Item_Parent')))
        # else:
        #     print("Emmpty")
        #     continue

    print(len(supplier_error_skus))
    print(supplier_error_skus)       
    print(i)
    print(len(not_in_airtable))
    print(not_in_airtable)



airtable_patch()