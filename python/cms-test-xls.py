import requests
import xmltodict
import json
import xlrd
import sys

apiuser = 'apiadmin'
apipassword = '2011cmca'
my_headers = {'content-type': "application/x-www-form-urlencoded"}

def system_status_ok():
    cms_url = 'https://10.97.3.44:445/api/v1/system/status'
    response = requests.request("GET", cms_url,
                                    auth=(apiuser, apipassword), verify=False)
    if not response.status_code // 100 == 2:
        print("Error: Unexpected response {}".format(response))
        return False
    else:
        return True


def get_coSpaces():
    cms_url = 'https://10.97.3.44:445/api/v1/cospaces?limit=20&ffset=20'
    response = requests.request("GET", cms_url,
                                    auth=(apiuser, apipassword), verify=False)

    #pepe = response.json()
    out = xmltodict.parse(response.text)
    out2 = out['coSpaces']['coSpace']
    print (out2)

def get_coSpace_by_callid(callid):
    cms_url= 'https://10.97.3.44:445/api/v1/cospaces?filter='+callid
    coSpace_id = None
    response = requests.request("GET",cms_url, auth=(apiuser,apipassword), verify=False)
    doc = xmltodict.parse(response.text)
    if doc['coSpaces']['@total'] == '0':
            print('CoSpace' + callid + ' no encontrado.')
    elif doc['coSpaces']['coSpace']['callId'] == callid:
            coSpace_id = doc['coSpaces']['coSpace']['@id']
    return coSpace_id


def set_coSpace_passcode(id,passcode):
    cms_url = 'https://10.97.3.44:445/api/v1/cospaces/' + id
    print (cms_url)
    data = {'passcode': passcode }
    response = requests.put(cms_url,data=data, auth=(apiuser, apipassword), verify=False)



loc = str(sys.argv[1])
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
rows = sheet.nrows
for i in range(1,rows):
        row = sheet.row_values(i)
        uuid = get_coSpace_by_callid(str(int(row[0])))
        if uuid != None:
            set_coSpace_passcode(uuid,str(int(row[1])))
