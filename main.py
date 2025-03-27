import kintone
import curl

subdomain=''
id=1
json_path="out.json"
csv_main_path="kintone_fields.csv"
csv_lookup_path="kintone_lookup.csv"
csv_reference_path="kintone_reference_table.csv"

appList = kintone.loadCsv('appList.csv.sample')
apiToken = kintone.getAllApiToken(appList)
curl.getFieldsInfo(subdomain,id,apiToken,json_path)
kintone.createDocs(json_path,csv_main_path,csv_lookup_path, csv_reference_path)

