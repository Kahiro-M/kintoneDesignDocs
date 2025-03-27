import kintone
import curl
import loadIni

config = loadIni.readConfig('config.ini')

appList = kintone.loadCsv('appList.csv')
apiToken = kintone.getAllApiToken(appList)
for appDict in appList:
    exeFlg = True
    json_path = ''
    csv_main_path="kintone_fields.csv"
    csv_lookup_path="kintone_lookup.csv"
    csv_reference_path="kintone_reference_table.csv"
    if(appDict.get('id')):
        json_path = appDict.get('id')+'_'
        csv_main_path = appDict.get('id')+'_'
        csv_lookup_path = appDict.get('id')+'_'
        csv_reference_path = appDict.get('id')+'_'
    else:
        exeFlg = False
    if(appDict.get('name')):
        json_path += appDict.get('name')+'_appDesignInfo.json'
        csv_main_path += appDict.get('name')+'_kintone_fields.csv'
        csv_lookup_path += appDict.get('name')+'_kintone_lookup.csv'
        csv_reference_path += appDict.get('name')+'_kintone_reference_table.csv'

    else:
        exeFlg = False
    if(appDict.get('api')==None):
        exeFlg = False

    if(exeFlg):
        curl.getFieldsInfo(config['subdomain'],appDict.get('id'),apiToken,json_path)
        kintone.createDocs(json_path,csv_main_path,csv_lookup_path,csv_reference_path)
