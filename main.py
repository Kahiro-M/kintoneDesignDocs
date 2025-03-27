import kintone
import curl
import loadIni
import mkdt

# iniファイルからサブドメイン情報を取得
config = loadIni.readConfig('config.ini')

# appList.csvからアプリIDとAPIの情報を取得
appList = kintone.loadCsv('appList.csv')
apiToken = kintone.getAllApiToken(appList)

# 保存先フォルダを作成
dirPath = mkdt.mkdirDatetime()+'\\'

# appList.csvに記載されているアプリ情報から設計情報を取得する
for appDict in appList:
    exeFlg = True

    json_path = dirPath
    csv_main_path =dirPath
    csv_lookup_path =dirPath
    csv_reference_path =dirPath

    # アプリIDを取得
    if(appDict.get('id')):
        json_path += appDict.get('id')+'_'
        csv_main_path += appDict.get('id')+'_'
        csv_lookup_path += appDict.get('id')+'_'
        csv_reference_path += appDict.get('id')+'_'
    else:
        exeFlg = False

    # アプリ名を取得
    if(appDict.get('name')):
        json_path += appDict.get('name')+'_appDesignInfo.json'
        csv_main_path += appDict.get('name')+'_kintone_fields.csv'
        csv_lookup_path += appDict.get('name')+'_kintone_lookup.csv'
        csv_reference_path += appDict.get('name')+'_kintone_reference_table.csv'
    else:
        exeFlg = False

    # APIがあるか確認
    if(appDict.get('api')==None):
        exeFlg = False

    # フィールド情報のJSONを取得＆JSONから設計CSVを出力
    if(exeFlg):
        curl.getFieldsInfo(config['subdomain'],appDict.get('id'),apiToken,json_path)
        kintone.createDocs(json_path,csv_main_path,csv_lookup_path,csv_reference_path)
