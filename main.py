import kintone
import curl
import loadIni
import mkdt

# iniファイルからサブドメイン情報を取得
config = loadIni.readConfig('config.ini')

# appList.csvからアプリIDとAPIの情報を取得
appDict = kintone.loadCsv('appList.csv')

# 保存先フォルダを作成
dirPath = mkdt.mkdirDatetime()+'\\'

# appList.csvに記載されているアプリ情報から設計情報を取得する
for appId in list(appDict):
    exeFlg = True

    json_path = dirPath
    csv_main_path =dirPath
    csv_lookup_path =dirPath
    csv_reference_path =dirPath

    # アプリIDを取得
    json_path += appId+'_'
    csv_main_path += appId+'_'
    csv_lookup_path += appId+'_'
    csv_reference_path += appId+'_'

    # アプリ名を取得
    if(appDict[appId].get('name')):
        json_path += appDict[appId].get('name')+'_appDesignInfo.json'
        csv_main_path += appDict[appId].get('name')+'_kintone_fields.csv'
        csv_lookup_path += appDict[appId].get('name')+'_kintone_lookup.csv'
        csv_reference_path += appDict[appId].get('name')+'_kintone_reference_table.csv'
    else:
        exeFlg = False

    # APIがあるか確認
    if(appDict[appId].get('api')):
        apiToken = kintone.getRelationApiToken(appId,appDict)
    else:
        exeFlg = False

    # フィールド情報のJSONを取得＆JSONから設計CSVを出力
    if(exeFlg):
        curl.getFieldsInfo(config['subdomain'],appId,apiToken,json_path)
        kintone.createDocs(json_path,csv_main_path,csv_lookup_path,csv_reference_path)
