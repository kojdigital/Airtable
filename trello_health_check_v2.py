import requests,json
import datetime

# from trello_api import client_secret

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from googleapiclient import discovery


# class TrelloManager(): 


# @staticmethod
def duplicate_lists():

# appCH2pWwhSkriTyi/ELC
# apppDz879lxPVKCAV    

    print('HI')

   
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S.%f") # Current Date Time.

    # print(date_time)


    

    region_specific_list = []

    i = 2


    airtable_api_key = 'keyAu4L6lcnNMAg8o'
    
    final_records_list = []

    errors = []

    # Fashion Base ID : appeHcYmbc6eF7bxj
    # MIK _ PLM UAT Base ID : apppqYPiGYGafKi6K
    # Some new PLM ID : appdTgAAkCpBLtZA7


    # MIK - appyMVZdbRBAo9YeR

    # First call the Airtable GET records API. It returns only 100 records at a time.. Then, with the offset values, loop till you get all records... 
    all_records_url = 'https://api.airtable.com/v0/appCH2pWwhSkriTyi/ELC?view=Grid%20View'
    airtable_parameters = { 'Authorization' : 'Bearer {}'.format(airtable_api_key), 'Content-Type' : 'application/json'}
    response = requests.get( all_records_url,  headers = airtable_parameters)
    all_records = response.json()
    print(all_records)
    offset = all_records.get('offset')

    for record in all_records.get('records'):
        final_records_list.append(record)    

    while offset is not None : 

        # print("pre : {}".format(offset))
        offset_records_url = 'https://api.airtable.com/v0/appCH2pWwhSkriTyi/ELC?view=Grid%20View&offset={}'.format(offset)
        # airtable_parameters = { 'Authorization' : 'Bearer {}'.format(airtable_api_key), 'Content-Type' : 'application/json'}
        offset_response = requests.get( offset_records_url,  headers = airtable_parameters)
        offset_response = offset_response.json()
        print(offset_response)
        # final_records_list.append(offset_response.get('records'))
        offset = offset_response.get('offset')
        # print("post : {}".format(offset))
        for record in offset_response.get('records'):
            final_records_list.append(record)


    # print(len(final_records_list))

    # try:

    for row in final_records_list:

        print(len(final_records_list))

        # try:
            

        region_specific_list.append(row.get('fields').get('Trello Link'))
        board_id = row.get('fields').get('Trello Link')

        print("THIS is the board we are checking now ------------: " + str(board_id))
        url = "https://trello.com/b/{}".format(board_id[21:]) + ".json"

        headers = {"Accept": "application/json"}

        # print(url)
        query = {
                    'key': '6f4a1f510eb5f2f66917c8d322ec3cb8',
                    'token': '8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f'
                }

        response = requests.request('GET', url, headers=headers, params=query)
        res = response.text

        # print(response.status_code)
        # print(response.json())

        


        # print(response.json()['id'])

        print(res)

        try:

            b_id = response.json()['id']
           

        except:
            errors.append(b_id)
            continue 


        url = "https://api.trello.com/1/boards/{}".format(b_id)

        headers = {"Accept": "application/json"}

        # print(url)
        query = {
            'fields': 'all',
            'key': '6f4a1f510eb5f2f66917c8d322ec3cb8',
            'token': '8ed88f5844ec6a137a8614f9aa88994e5da4c146495275ee87ac1ead818c1a1f'
        }
        print(url)

        new_response = requests.request('GET', url, headers=headers, params=query)
        res = new_response.text

        # print(new_response.status_code)
        # print(res)
        # print(new_response.json())

        try:

            b_dateLastActivity = new_response.json()['dateLastActivity']
            # b_dateLastView = new_response.json()['dateLastView']
            # print(b_dateLastActivity)

            if b_dateLastActivity is not None:
                b_dateLastActivity = datetime.datetime.strptime(b_dateLastActivity, "%Y-%m-%dT%H:%M:%S.%fZ")
            # b_dateLastActivity = b_dateLastActivity.replace(hour=0, minute=0, second=0, microsecond=0)
            # b_dateLastView = datetime.datetime.strptime(b_dateLastView, "%Y-%m-%dT%H:%M:%S.%fZ")

        except:
            errors.append(b_id)
            continue 

        current_date_time = datetime.datetime.strptime('2021-09-30 12:30:00.000000', "%Y-%m-%d %H:%M:%S.%f")
        # Accept a Range of Date

        list_name = "ELC OUTDOOR FUN CAMPAIGN"
        
        # Getting List ID
        list_id_url = "https://api.trello.com/1/boards/"+b_id+"/lists"
        list_response = requests.request("GET", list_id_url, params=query)
        res = (list_response.json())

        status = 100

        for lis in res:
            lis_name = (lis["name"])
            # print(lis_name)
            
            if list_name in lis_name :
                matching_list_id = (lis["id"])
                print('List ID : {}'.format(matching_list_id))
                print("HERE IS THE LIST CHECKED: " + str(lis_name))

                # Getting All Cards in the list
                list_details_url = "https://api.trello.com/1/lists/"+matching_list_id+"/cards"
                list_response = requests.request("GET", list_details_url, params=query)
                res = (list_response.json())
                
                # print('List Details : {}'.format(res))
                # print('Total Cards = {}'.format(len(res)))
                attachment_urls = []
                total_checklists = 0
                completed_checklist = 0
                # print("------------------------------")
                # print(res)
                # print("------------------------------")
                for card in res:

                    card_id = (card["id"])
                    

                    # Getting Only Attachments : 
                    attachments_url = "https://api.trello.com/1/cards/"+card_id+"/attachments"
                    list_response = requests.request("GET", attachments_url, params=query)
                    res = (list_response.json())
                    # print(res)

                    for attachment in res:

                        a_url = (attachment["url"])
                        a_date = (attachment["date"])

                        a_date = datetime.datetime.strptime(a_date, "%Y-%m-%dT%H:%M:%S.%fZ")

                        # print(res["url"])
                        if a_url not in attachment_urls and (('jpg' in a_url) or ('jpeg' in a_url)) and a_date > current_date_time:
                            attachment_urls.append(a_url)


                    
                    # Getting Only checklists : 
                    checklists_url = "https://api.trello.com/1/cards/"+card_id+"/checklists"
                    checklists_response = requests.request("GET", checklists_url, params=query)
                    res = (checklists_response.json())

                    # print('Checklist Response : {}'.format(res))

                    if len(res) != 0 :
                        total_checklists += len(res[0]["checkItems"]) 

                        for check_item in res[0]["checkItems"]:

                            if check_item["state"] == 'complete':
                                completed_checklist += 1



                    # for attachment in res:

                    #     a_url = (attachment["url"])

                    #     # print(res["url"])
                    #     if a_url not in attachment_urls and ('jpg' or 'JPG' in a_url):
                    #         attachment_urls.append(a_url)

                # print(attachment_urls)

                # print(completed_checklist)
                # print(total_checklists)

                # percentage_completion = 1
                # print("TOTAL CHECKLIST: " + str(total_checklists))

                if total_checklists == 0:
                    percentage_completion = 1*100
                else:
                    percentage_completion = (completed_checklist/ total_checklists)*100


                final_image_body = ''

                for link in attachment_urls:

                    final_image = {}
                    final_image['url'] = link

                    final_image_body = final_image_body + link + ',' + ' '

                patch_url = 'https://api.airtable.com/v0/appCH2pWwhSkriTyi/ELC'

                single_record = {}

                fields_body = {}
                fields_body['Attachments'] = str(final_image_body)

                # fields_body['Attachment URLs'] = final_image_body

                # if total_checklists == 0 :
                #     b_dateLastActivity = b_dateLastActivity.replace(hour=0, minute=0, second=0, microsecond=0)
                #     # print(b_dateLastActivity)
                #     fields_body['Comments'] = 'No Checklists were added for this Guideline'
                #     if b_dateLastActivity > current_date_time :
                #     # if (percentage_completion) > 0.4:
                #         status = 101
                    
                #     if status == 101 : 

                #         fields_body['Status'] = 'ACTIVE'
                #         fields_body['Last Activity Date'] = '{}'.format(b_dateLastActivity)

                #     elif status == 100 : 
                #         fields_body['Status'] = 'PASSIVE'
                #         fields_body['Last Activity Date'] = '{}'.format(b_dateLastActivity)

                # else : 
                #     fields_body['Comments'] = 'Checklist Completion : {}%'.format(percentage_completion)
                #     if (percentage_completion) > 0.4:
                #         status = 101
                    
                #     if status == 101 : 

                #         fields_body['Status'] = 'ACTIVE'
                #         fields_body['Last Activity Date'] = '{}'.format(b_dateLastActivity)

                #     elif status == 100 : 
                #         fields_body['Status'] = 'PASSIVE'
                #         fields_body['Last Activity Date'] = '{}'.format(b_dateLastActivity)

                #     fields_body['Task Completion Rate'] = 'Checklist Completion : {}%'.format(str(round(percentage_completion,2)))



                if total_checklists == 0 :
                    # b_dateLastActivity = b_dateLastActivity.replace(hour=0, minute=0, second=0, microsecond=0)
                    # print(b_dateLastActivity)
                    fields_body['Comments'] = 'No Checklists were added for this Guideline'
                    fields_body['Task Completion Rate'] = 'No Checklists were added for this Guideline'
                    if b_dateLastActivity > current_date_time :
                    # if (percentage_completion) > 0.4:
                        status = 101
                    
                    if status == 101 : 

                        just_date = str(b_dateLastActivity)

                        fields_body['Status'] = 'ACTIVE'
                        fields_body['Last Activity Date'] = '{}'.format(just_date[:10])
                        # print("STATUS : " + str(status))
                        # print("JUST_DATE : " + str(just_date))
                        print("JUST_DATE -------------------- : " + str(fields_body['Last Activity Date']))
                        print(b_dateLastActivity)


                    elif status == 100 : 

                        just_date = str(b_dateLastActivity)
                        fields_body['Status'] = 'PASSIVE'
                        fields_body['Last Activity Date'] = '{}'.format(just_date[:10])
                        print("STATUS : " + str(status))
                        # print("JUST_DATE : " + str(just_date))
                        # print("JUST_DATE : " + str(fields_body['Last Activity Date']))

                    

                else : 
                    fields_body['Comments'] = 'Checklist Completion : {}%'.format(str(round(percentage_completion,2)))
                    fields_body['Task Completion Rate'] = 'Checklist Completion : {}%'.format(str(round(percentage_completion,2)))
                    
                    if (percentage_completion) > 0.4:
                        status = 101
                        # PRINT("ITH EPDI------------------------")
                    
                    if status == 101 : 

                        just_date = str(b_dateLastActivity)

                        fields_body['Status'] = 'ACTIVE'
                        fields_body['Last Activity Date'] = '{}'.format(just_date[:10])
                        # print("STATUS : " + str(status))
                        # print("JUST_DATE : " + str(just_date))
                        # print("JUST_DATE : " + str(fields_body['Last Activity Date']))
                        

                    elif status == 100 : 

                        just_date = str(b_dateLastActivity)
                        fields_body['Status'] = 'PASSIVE'
                        fields_body['Last Activity Date'] = '{}'.format(just_date[:10])
                        print("ACTIVITY DATE: " + str(b_dateLastActivity))
                        # print("STATUS : " + str(status))
                        # print("JUST_DATE : " + str(just_date))
                        # print("JUST_DATE : " + str(fields_body['Last Activity Date']))
                





                single_record['id'] = row.get('id')
                single_record['fields'] = fields_body

                # print("single_record['id'] = row.get('id') : ")
                # print(single_record['id'])

                # print("single_record['fields'] = fields_body : ")
                # print(single_record['id'])

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
                    continue
                else:
                    # supplier_error_skus.append(row.get('Item_Parent'))
                    print(patch_response.json())
                    break

                
                    

                break
            else:
                pass
                

        # break

        print(errors)
        # except: 
        #     break


duplicate_lists()

       