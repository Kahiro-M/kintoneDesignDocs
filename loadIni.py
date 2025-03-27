# iniファイルから設定を読み込む
def readConfig(filePath='config.ini'):
    import configparser

    #ConfigParserオブジェクトを生成
    config = configparser.ConfigParser()

    #設定ファイル読み込み
    config.read(filePath,encoding='utf8')

    configData = {}

    #設定情報取得
    if(config.has_option('kintone','subdomain')):
        configData['subdomain'] = config.get('kintone','subdomain')
    else:
        configData['subdomain'] = ''

    return configData

