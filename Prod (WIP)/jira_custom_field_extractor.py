import requests
import json

MAX_RESULTS = 100
MAX_PAGES = 43

# JSON PRINT HELPER #
def jprint(output):
    print(json.dumps(output, indent=4))

# Write to $ delimited text file (commas caused issues as some values include commas)
def write_to_file(f, json_data):
    for record in json_data:
        jid = record['id']
        jvalue = record['value']
        joption = record['optionId'] if 'optionId' in record else ''

        output = f'{jid}${jvalue}${joption}\n'
        f.write(output)
    
# ---------------------------------------------------------------------------------------------#
f = open("id_file.txt", "a")

start_record = 0
while start_record <= MAX_PAGES:
    url = f'https://aftmda.atlassian.net/rest/api/3/field/customfield_10066/context/10219/option?startAt={start_record*MAX_RESULTS}'
    headers = {"Authorization": "Basic {BASE64_ENCODED_API_KEY}"}
    response = requests.get(url, headers=headers)
    json_data = response.json()
    
    current = json_data["startAt"]
    print(f'start at: {current}')
    write_to_file(f, json_data['values'])
    
    start_record+= 1
f.close()
