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
    sheet = client.open("MHR_SALES").get_worksheet(0)
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
    all_records_url = 'https://api.airtable.com/v0/appcheD4BtfvJHmpI/PRODUCTS?view=Vinay%20View'
    airtable_parameters = { 'Authorization' : 'Bearer {}'.format(airtable_api_key), 'Content-Type' : 'application/json'}
    response = requests.get( all_records_url,  headers = airtable_parameters)
    all_records = response.json()
    offset = all_records.get('offset')

    for record in all_records.get('records'):
        final_records_list.append(record)    

    while offset is not None : 

        # print("pre : {}".format(offset))
        offset_records_url = 'https://api.airtable.com/v0/appcheD4BtfvJHmpI/PRODUCTS?view=Vinay%20View&offset={}'.format(offset)
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
        

        if record.get('fields').get('RMS Parent ID') is not None:

            in_airtable = 0

        
            for row in list_of_rows:
        # for record in final_records_list:

            # print(str(row.get('SKU')))

                if record.get('fields').get('RMS Parent ID') == row.get('Product Code'):

                    # try:

                    in_airtable = 1

                    
                    patch_url = 'https://api.airtable.com/v0/appcheD4BtfvJHmpI/PRODUCTS'

                    single_record = {}

                    fields_body = {}

                    print(row.get('Sold Qty'))
                    print(row.get('Product Code')) 
                    # print(fields_body['Net Sales (DW)'])

                    

                    # fields_body['CAD/Product Image'] = product_image_body

                    fields_body['RCVD QTY - KSA'] = float(str(row.get('RCVD QTY - KSA')).replace(",","").replace("-","0").replace("~","0000"))
                    # fields_body['ORDER VALUE'] = float(str(row.get('ORDER VALUE')).replace(",",""))
                    fields_body['FP QTY SOLD'] = float(str(row.get('FP QTY SOLD')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['FP NET SALES(DW) VAT Ex'] = float(str(row.get('FP NET SALES(DW) VAT Ex')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['Cost of Sales (DW)'] = float(str(row.get('Cost of Sales (DW)')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['Order Cost (DW)'] = float(str(row.get('Order Cost (DW)')).replace("SAR ","").replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['FP Net Sales (DW) VAT In'] = float(str(row.get('FP Net Sales (DW) VAT In')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['Order Cost (FDC)'] = float(str(row.get('Order Cost (FDC)')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['Store Qty Sales'] = float(str(row.get('Store Qty Sales')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['Online Qty Sales'] = float(str(row.get('Online Qty Sales')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['Store Gross Sales'] = float(str(row.get('Store Gross Sales')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['Online Gross Sales'] = float(str(row.get('Online Gross Sales')).replace(",","").replace("-","0").replace("~","0000"))
                    fields_body['MP Remarks'] = str(row.get('MP Remarks')).replace(",","").replace("-","0").replace("~","0000")
                    fields_body['COST OF SALES FDC'] = float(str(row.get('COST OF SALES FDC')).replace(",","").replace("-","0").replace("-","0").replace("~","0000"))

                    filtered_fields_body = {k: v for k, v in fields_body.items() if (v != '0000' and v != 0 and v != 0.0)}

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
                        supplier_error_skus.append(row.get('Product Code'))
                        print(patch_response.json())
                        break
                    # except:
                    #     print('exception')
                    #     break
            

            if in_airtable == 0:
                not_in_airtable.append(str(row.get('Product Code')))
        # else:
        #     print("Emmpty")
        #     continue

    print(len(supplier_error_skus))
    print(supplier_error_skus)       
    print(i)
    print(len(not_in_airtable))
    print(not_in_airtable)



airtable_patch()