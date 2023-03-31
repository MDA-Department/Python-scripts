import civis
import os
import requests
import json
import pandas as pd
import urllib.parse
from pathlib import Path


# headers needed for GET requests & GLOBALS
GET_HEADERS = {'X-Knack-REST-API-KEY':'1a210580-315e-11ea-a6a4-bb031a9e1ba1', 'X-Knack-Application-Id':'5e13989941e72c0e039e117f'}
POST_HEADERS = GET_HEADERS.copy()
POST_HEADERS.update({'content-type': 'application/json'})


# Knack entity mappings for readability
knackmappingdict = {'Affiliate':['object_25',{'affiliateid':'field_126'}], 
                    'Chapter':['object_26',{'chapterid':'field_148'}],
                    'EmployerType':['object_18',{'employertypeid':'field_254'}],
                    'Division':['object_17',{'divisionid':'field_108'}],
                    'UnitType':['object_36',{'unittypeid':'field_309'}],
                    'StatePerCapita':['object_39',{'statepercapitaid':'field_438'}],
                    'NationalJobClass':['object_20',{'nationaljobclassid':'field_329'}],
                    'NationalPerCapita':['object_40',{'nationalpercapitaid':'field_425'}],
                    'LocalAgreementType':['object_35',{'localagreementtypeid':'field_282'}],
                    'WorkLocationType':['object_19',{'worklocationtypeid':'field_366'}],
                    'WorkStructureType':['object_30',{'workstructuretypeid':'field_401'}],
                    'NationalInstitutionType':['object_38',{'nationalinstitutiontypeid':'field_377'}],
                    'Employer':['object_16',
                                {
                                    'employerid':'field_263',
                                    'employerguid':'field_264',
                                    'employername':'field_265',
                                    'Entity-EmployerType':'field_261',
                                    'Entity-ParentEmployer':'field_278',
                                    'acronym':'field_266',
                                    'employercode':'field_267',
                                    'Entity-Chapter':'field_262',
                                    'hasprivatesector':'field_268',
                                    'area':'field_269',
                                    'websiteurl':'field_270',
                                    'isstructural':'field_271',
                                    'isunknown':'field_272',
                                    'createdby':'field_273',
                                    'createdat':'field_274',
                                    'updatedby':'field_275',
                                    'updatedat':'field_276',
                                    'deletedat':'field_277',
                                    'Entity-Affiliate':'field_588'
                                }
                               ],
                    'LocalDuesCategory':['object_37',
                                         {
                                            'localduescategoryid':'field_451',
                                            'localduescategoryname':'field_452',
                                            'Entity-NationalPerCapita':'field_450',
                                            'Entity-StatePerCapita':'field_449',
                                            'Entity-Affiliate':'field_448',
                                            'localduesamount':'field_453',
                                            'localduespercentage':'field_454',
                                            'paymentfrequencyid':'field_455',
                                            'startdate':'field_456',
                                            'enddate':'field_457',
                                            'createdby':'field_458',
                                            'createdat':'field_459',
                                            'updatedby':'field_460',
                                            'updatedat':'field_461',
                                            'deletedat':'field_462'
                                         }
                                        ],
                    'WorkLocation':['object_28',
                                         {
                                            'worklocationid':'field_389',
                                            'worklocationguid':'field_390',
                                            'worklocationname':'field_391',
                                            'Entity-WorkLocationType':'field_387',
                                            'Entity-ParentWorkLocation':'field_388',
                                            'worklocationcode':'field_392',
                                            'worklocationarea':'field_393',
                                            'ispubliclyaccessible':'field_394',
                                            'Entity-NationalInstitutionType':'field_386',
                                            'Entity-Employer':'field_385',
                                            'createdby':'field_395',
                                            'createdat':'field_396',
                                            'updatedby':'field_397',
                                            'updatedat':'field_398',
                                            'deletedat':'field_399',
                                            'Entity-Affiliate':'field_598'
                                         }
                                        ],
                    'WorkStructure':['object_29',
                                         {
                                            'workstructureid':'field_412',
                                            'workstructureguid':'field_413',
                                            'workstructurename':'field_414',
                                            'Entity-Employer':'field_409',
                                            'Entity-WorkStructureType':'field_410',
                                            'Entity-ParentWorkStructure':'field_411',
                                            'workstructurecode':'field_415',
                                            'createdby':'field_416',
                                            'createdat':'field_417',
                                            'updatedby':'field_418',
                                            'updatedat':'field_419',
                                            'deletedat':'field_420',
                                            'Entity-Affiliate':'field_599'
                                         }
                                        ],
                    'LocalAgreement':['object_23',
                                         {
                                            'localagreementid':'field_291',
                                            'localagreementname':'field_292',
                                            'Entity-Employer':'field_289',
                                            'gradestepname':'field_293',
                                            'gradestatus':'field_294',
                                            'Entity-LocalAgreementType':'field_290',
                                            'localagreementratificationdate':'field_295',
                                            'localagreementeffectivestartdate':'field_296',
                                            'localagreementeffectiveenddate':'field_297',
                                            'localagreementexpirationdate':'field_298',
                                            'fileurl':'field_299',
                                            'isstructural':'field_300',
                                            'isunknown':'field_301',
                                            'createdby':'field_302',
                                            'createdat':'field_303',
                                            'updatedby':'field_304',
                                            'updatedat':'field_305',
                                            'deletedat':'field_306',
                                            'Entity-Affiliate':'field_589'
                                         }
                                        ],
                    'Unit':['object_22',
                                         {
                                            'unitid':'field_319',
                                            'unitguid':'field_320',
                                            'unitname':'field_321',
                                            'Entity-UnitType':'field_316',
                                            'Entity-LocalAgreement':'field_317',
                                            'Entity-Division':'field_318',
                                            'isstructural':'field_322',
                                            'isunknown':'field_323',
                                            'createdby':'field_324',
                                            'createdat':'field_325',
                                            'updatedby':'field_326',
                                            'updatedat':'field_327',
                                            'deletedat':'field_328',
                                            'Entity-Affiliate':'field_590'
                                         }
                                        ],
                    'LocalJobClass':['object_21',
                                         {
                                            'localjobclassid':'field_343',
                                            'localjobclassguid':'field_344',
                                            'localjobclassname':'field_345',
                                            'Entity-NationalJobClass':'field_341',
                                            'localjobclasscode':'field_346',
                                            'Entity-Unit':'field_342',
                                            'isstructural':'field_347',
                                            'isunknown':'field_348',
                                            'createdby':'field_349',
                                            'createdat':'field_350',
                                            'updatedby':'field_351',
                                            'updatedat':'field_352',
                                            'deletedat':'field_353',
                                            'Entity-Affiliate':'field_591'
                                         }
                                        ],
                    'JobTitle':['object_24',
                                         {
                                            'jobtitleid':'field_355',
                                            'jobtitlename':'field_356',
                                            'compensationid':'field_357',
                                            'Entity-LocalJobClass':'field_354',
                                            'isstructural':'field_358',
                                            'isunknown':'field_359',
                                            'createdby':'field_360',
                                            'createdat':'field_361',
                                            'updatedby':'field_362',
                                            'updatedat':'field_363',
                                            'deletedat':'field_364',
                                            'Entity-Affiliate':'field_597'
                                         }
                                        ]
                   }



# Find object_id of a given knack object
def find_object_id(knack_object):
    return knackmappingdict[knack_object][0]


# Find field_id of a given knack object and field_name
def find_field_id(knack_object, field_name):
    return knackmappingdict[knack_object][1][field_name]


# Tries to get knackId of given object with match params. Returns val if found blank otherwise
def getKnackID(knack_object, field_to_match, match_value):
    #Convert to IDs
    knack_object_id = find_object_id(knack_object)
    field_to_match_id = find_field_id(knack_object, field_to_match)
    
    #Get Id
    match_filter = {'match':'and', 'rules':[{'field':field_to_match_id, 'operator':'is', 'value': match_value}]}
    filter_for_url = urllib.parse.quote(json.dumps(match_filter))
    request_url = "https://api.knack.aft.org/v1/objects/" + knack_object_id + "/records?filters=" + filter_for_url
    r = requests.get(url = request_url, headers = GET_HEADERS)
    #print(json.dumps(r.json(), indent=4))
    res_json_dict = json.loads(json.dumps(r.json()))
    if res_json_dict["total_records"] == 0:
        return ''
    elif res_json_dict["total_records"] == 1:
        return res_json_dict["records"][0]["id"]
    else:
        return ''


# GET and format json from requestURL
def getJson(request_url):
    r = requests.get(url = request_url, headers = GET_HEADERS)
    return json.dumps(r.json(), indent=4)


## ------------------------------------------------------------------------------
## Helper methods per entity. Logic based on mappings and parent/child structure
## ------------------------------------------------------------------------------

    
# Adds localduescategory
def add_localduescategory(payload_dict):
    exists_id = getKnackID("LocalDuesCategory", "localduescategoryid", payload_dict["localduescategoryid"])

    affiliate_knack_id = getKnackID("Affiliate", "affiliateid", payload_dict["affiliateid"])
    statepercapita_knack_id = getKnackID("StatePerCapita", "statepercapitaid", payload_dict["statepercapitaid"])
    nationalpercapita_knack_id = getKnackID("NationalPerCapita", "nationalpercapitaid", payload_dict["nationalpercapitaid"])
    
    payload_dict.pop('affiliateid')
    payload_dict.pop('statepercapitaid')
    payload_dict.pop('nationalpercapitaid')

    if payload_dict["localduesamount"] != '':
        payload_dict.pop('localduespercentage')
    else:
        payload_dict.pop('localduesamount')
    
    payload_dict.update({'Entity-Affiliate':affiliate_knack_id,
                         'Entity-StatePerCapita':statepercapita_knack_id,
                         'Entity-NationalPerCapita':nationalpercapita_knack_id,})
    #print(payload_dict)
    out = {}
    for k , v in payload_dict.items():
        newk = knackmappingdict["LocalDuesCategory"][1][k]
        out.update({newk:v})
    #print(out)
    
    if exists_id == '':
        print("Creating new record with id: " + payload_dict["localduescategoryid"])
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["LocalDuesCategory"][0] + "/records"
        r = requests.post(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)
    else:
        print(payload_dict["localduescategoryid"] + " exists! updating record...")
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["LocalDuesCategory"][0] + "/records/" +  exists_id
        r = requests.put(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)

    if r.status_code != 200:
        print(json.dumps(r.json(), indent=4))

# Adds employers
def add_employer(payload_dict):
    exists_id = getKnackID("Employer", "employerid", payload_dict["employerid"])
    
    affiliate_knack_id = getKnackID("Affiliate", "affiliateid", payload_dict["affiliateid"])
    chapter_knack_id = getKnackID("Chapter", "chapterid", payload_dict["chapterid"])
    employertype_knack_id = getKnackID("EmployerType", "employertypeid", payload_dict["employertypeid"])
    parentemployer_knack_id = getKnackID("Employer", "employerid", payload_dict["parentemployerid"])
    
    payload_dict.pop('affiliateid')
    payload_dict.pop('chapterid')
    payload_dict.pop('parentemployerid')
    payload_dict.pop('employertypeid')
    
    payload_dict.update({'Entity-Affiliate':affiliate_knack_id,
                         'Entity-Chapter':chapter_knack_id,
                         'Entity-EmployerType':employertype_knack_id,
                         'Entity-ParentEmployer':parentemployer_knack_id})
    #print(payload_dict)
    out = {}
    for k , v in payload_dict.items():
        newk = knackmappingdict["Employer"][1][k]
        out.update({newk:v})
    #print(out)
    
    if exists_id == '':
        print("Creating new record with id: " + payload_dict["employerid"])
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["Employer"][0] + "/records"
        r = requests.post(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)
    else:
        print(payload_dict["employerid"] + " exists! updating record...")
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["Employer"][0] + "/records/" +  exists_id
        r = requests.put(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)

    if r.status_code != 200:
        print(json.dumps(r.json(), indent=4))


# Adds worklocation    
def add_worklocation(payload_dict):
    exists_id = getKnackID("WorkLocation", "worklocationid", payload_dict["worklocationid"])
    
    affiliate_knack_id = getKnackID("Affiliate", "affiliateid", payload_dict["affiliateid"])
    employer_knack_id = getKnackID("Employer", "employerid", payload_dict["employerid"])
    worklocationtype_knack_id = getKnackID("WorkLocationType", "worklocationtypeid", payload_dict["worklocationtypeid"])
    parentworklocation_knack_id = getKnackID("WorkLocation", "worklocationid", payload_dict["parentworklocationid"])
    nationalinstitutiontype_knack_id = getKnackID("NationalInstitutionType", "nationalinstitutiontypeid", payload_dict["nationalinstitutiontypeid"])
    
    payload_dict.pop('affiliateid')
    payload_dict.pop('employerid')
    payload_dict.pop('worklocationtypeid')
    payload_dict.pop('parentworklocationid')
    payload_dict.pop('nationalinstitutiontypeid')
    
    payload_dict.update({'Entity-Affiliate':affiliate_knack_id,
                         'Entity-Employer':employer_knack_id,
                         'Entity-WorkLocationType':worklocationtype_knack_id,
                         'Entity-ParentWorkLocation':parentworklocation_knack_id,
                         'Entity-NationalInstitutionType':nationalinstitutiontype_knack_id})
    #print(payload_dict)
    out = {}
    for k , v in payload_dict.items():
        newk = knackmappingdict["WorkLocation"][1][k]
        out.update({newk:v})
    #print(out)
    
    if exists_id == '':
        print("Creating new record with id: " + payload_dict["worklocationid"])
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["WorkLocation"][0] + "/records"
        r = requests.post(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)
    else:
        print(payload_dict["worklocationid"] + " exists! updating record...")
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["WorkLocation"][0] + "/records/" +  exists_id
        r = requests.put(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)

    if r.status_code != 200:
        print(json.dumps(r.json(), indent=4))


# Adds workstructure
def add_workstructure(payload_dict):
    exists_id = getKnackID("WorkStructure", "workstructureid", payload_dict["workstructureid"])
    
    affiliate_knack_id = getKnackID("Affiliate", "affiliateid", payload_dict["affiliateid"])
    employer_knack_id = getKnackID("Employer", "employerid", payload_dict["employerid"])
    workstructuretype_knack_id = getKnackID("WorkStructureType", "workstructuretypeid", payload_dict["workstructuretypeid"])
    parentworkstructure_knack_id = getKnackID("WorkStructure", "workstructureid", payload_dict["parentworkstructureid"])
 
    payload_dict.pop('affiliateid')
    payload_dict.pop('employerid')
    payload_dict.pop('workstructuretypeid')
    payload_dict.pop('parentworkstructureid')
    
    payload_dict.update({'Entity-Affiliate':affiliate_knack_id,
                         'Entity-Employer':employer_knack_id,
                         'Entity-WorkStructureType':workstructuretype_knack_id,
                         'Entity-ParentWorkStructure':parentworkstructure_knack_id})
    #print(payload_dict)
    out = {}
    for k , v in payload_dict.items():
        newk = knackmappingdict["WorkStructure"][1][k]
        out.update({newk:v})
    #print(out)

    if exists_id == '':
        print("Creating new record with id: " + payload_dict["workstructureid"])
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["WorkStructure"][0] + "/records"
        r = requests.post(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)
    else:
        print(payload_dict["workstructureid"] + " exists! updating record...")
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["WorkStructure"][0] + "/records/" +  exists_id
        r = requests.put(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)

    if r.status_code != 200:
        print(json.dumps(r.json(), indent=4))


# Adds localagreement
def add_localagreement(payload_dict):
    exists_id = getKnackID("LocalAgreement", "localagreementid", payload_dict["localagreementid"])
    
    affiliate_knack_id = getKnackID("Affiliate", "affiliateid", payload_dict["affiliateid"])
    employer_knack_id = getKnackID("Employer", "employerid", payload_dict["employerid"])
    localagreementtype_knack_id = getKnackID("LocalAgreementType", "localagreementtypeid", payload_dict["localagreementtypeid"])
 
    payload_dict.pop('affiliateid')
    payload_dict.pop('employerid')
    payload_dict.pop('localagreementtypeid')
    
    payload_dict.update({'Entity-Affiliate':affiliate_knack_id,
                         'Entity-Employer':employer_knack_id,
                         'Entity-LocalAgreementType':localagreementtype_knack_id})
    #print(payload_dict)
    out = {}
    for k , v in payload_dict.items():
        newk = knackmappingdict["LocalAgreement"][1][k]
        out.update({newk:v})
    #print(out)

    if exists_id == '':
        print("Creating new record with id: " + payload_dict["localagreementid"])
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["LocalAgreement"][0] + "/records"
        r = requests.post(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)
    else:
        print(payload_dict["localagreementid"] + " exists! updating record...")
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["LocalAgreement"][0] + "/records/" +  exists_id
        r = requests.put(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)

    if r.status_code != 200:
        print(json.dumps(r.json(), indent=4))


# Adds unit
def add_unit(payload_dict):
    exists_id = getKnackID("Unit", "unitid", payload_dict["unitid"])
    
    affiliate_knack_id = getKnackID("Affiliate", "affiliateid", payload_dict["affiliateid"])
    localagreement_knack_id = getKnackID("LocalAgreement", "localagreementid", payload_dict["localagreementid"])
    unitype_knack_id = getKnackID("UnitType", "unittypeid", payload_dict["unittypeid"])
    division_knack_id = getKnackID("Division", "divisionid", payload_dict["divisionid"])
 
    payload_dict.pop('affiliateid')
    payload_dict.pop('localagreementid')
    payload_dict.pop('unittypeid')
    payload_dict.pop('divisionid')
    
    payload_dict.update({'Entity-Affiliate':affiliate_knack_id,
                         'Entity-LocalAgreement':localagreement_knack_id,
                         'Entity-Division':division_knack_id,
                         'Entity-UnitType':unitype_knack_id})
    #print(payload_dict)
    out = {}
    for k , v in payload_dict.items():
        newk = knackmappingdict["Unit"][1][k]
        out.update({newk:v})
    #print(out)

    if exists_id == '':
        print("Creating new record with id: " + payload_dict["unitid"])
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["Unit"][0] + "/records"
        r = requests.post(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)
    else:
        print(payload_dict["unitid"] + " exists! updating record...")
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["Unit"][0] + "/records/" +  exists_id
        r = requests.put(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)

    if r.status_code != 200:
        print(json.dumps(r.json(), indent=4))


# Adds localjobclass
def add_localjobclass(payload_dict):
    exists_id = getKnackID("LocalJobClass", "localjobclassid", payload_dict["localjobclassid"])
    
    affiliate_knack_id = getKnackID("Affiliate", "affiliateid", payload_dict["affiliateid"])
    unit_knack_id = getKnackID("Unit", "unitid", payload_dict["unitid"])
    nationaljobclass_knack_id = getKnackID("NationalJobClass", "nationaljobclassid", payload_dict["nationaljobclassid"])
 
    payload_dict.pop('affiliateid')
    payload_dict.pop('unitid')
    payload_dict.pop('nationaljobclassid')
    
    payload_dict.update({'Entity-Affiliate':affiliate_knack_id,
                         'Entity-Unit':unit_knack_id,
                         'Entity-NationalJobClass':nationaljobclass_knack_id})
    #print(payload_dict)
    out = {}
    for k , v in payload_dict.items():
        newk = knackmappingdict["LocalJobClass"][1][k]
        out.update({newk:v})
    #print(out)

    if exists_id == '':
        print("Creating new record with id: " + payload_dict["localjobclassid"])
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["LocalJobClass"][0] + "/records"
        r = requests.post(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)
    else:
        print(payload_dict["localjobclassid"] + " exists! updating record...")
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["LocalJobClass"][0] + "/records/" +  exists_id
        r = requests.put(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)

    if r.status_code != 200:
        print(json.dumps(r.json(), indent=4))


# Adds jobtitles
def add_jobtitle(payload_dict):
    exists_id = getKnackID("JobTitle", "jobtitleid", payload_dict["jobtitleid"])
    
    affiliate_knack_id = getKnackID("Affiliate", "affiliateid", payload_dict["affiliateid"])
    localjobclass_knack_id = getKnackID("LocalJobClass", "localjobclassid", payload_dict["localjobclassid"])
 
    payload_dict.pop('affiliateid')
    payload_dict.pop('localjobclassid')
    
    payload_dict.update({'Entity-Affiliate':affiliate_knack_id,
                         'Entity-LocalJobClass':localjobclass_knack_id})
    #print(payload_dict)
    out = {}
    for k , v in payload_dict.items():
        newk = knackmappingdict["JobTitle"][1][k]
        out.update({newk:v})
    #print(out)

    if exists_id == '':
        print("Creating new record with id: " + payload_dict["jobtitleid"])
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["JobTitle"][0] + "/records"
        r = requests.post(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)
    else:
        print(payload_dict["jobtitleid"] + " exists! updating record...")
        request_url = "https://api.knack.aft.org/v1/objects/" + knackmappingdict["JobTitle"][0] + "/records/" +  exists_id
        r = requests.put(url = request_url, headers = POST_HEADERS, data = json.dumps(out))
        print(r)

    if r.status_code != 200:
        print(json.dumps(r.json(), indent=4))

# Runner helper function for each entity
def runner(entity):
    print("--------------------------------")
    print("Uploading" + entity + "...")
    table_name = input_schema + entity
    f = civis.io.read_civis(table=table_name,
                            database="American Federation of Teachers",
                            use_pandas=True)

    df = pd.DataFrame()
    df = f.astype(str)
    df.fillna('', inplace=True)
    
    for payload_dict in df.to_dict('records'):
        command = 'add_' + entity + '(payload_dict)'
        eval(command)
    print("--------------------------------")
    
# Main Class that can be used to trigger all helpers at once
def main():
    #Read Params
    input_schema = 'aftdb_entitycleanup' + '.toHub_'
    for val in ['localdues','employer','worklocation','workstructure','localagreement','unit','jobclass','jobtitle']:
      runner(val)

main()
