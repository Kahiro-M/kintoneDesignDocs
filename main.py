import kintone
import curl
import loadIni

config = loadIni.readConfig('config.ini')

appList = kintone.loadCsv('appList.csv')
apiToken = kintone.getAllApiToken(appList)
curl.getFieldsInfo(subdomain,id,apiToken,json_path)
kintone.createDocs(json_path,csv_main_path,csv_lookup_path, csv_reference_path)

