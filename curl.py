# kintone REST APIからJSONを取得してファイルに保存
def fetch_kintone_json(subdomain, api_token, api_path, params, output_file):
    """
    kintone REST APIからJSONを取得してファイルに保存する関数

    :param subdomain: 例）"example"
    :param api_token: KintoneのAPIトークン（読み取り権限が必要）
    :param api_path: APIのパス（例："/k/v1/app/form/fields.json"）
    :param params: APIのクエリパラメータ（json形式）
    :param output_file: 出力するJSONファイル名（例："out.json"）
    """
    import requests
    import json

    url = f"https://{subdomain}.cybozu.com{api_path}"

    headers = {
        "X-Cybozu-API-Token": api_token,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, json=params)

    if response.status_code == 200:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=2)
        print(f"✅ JSONファイルを保存しました: {output_file}")
    else:
        print("❌ エラーが発生しました")
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス内容: {response.text}")


# アプリ情報取得
def getAppInfo(subdomain,id,api,output):
    params = {
        'id': id,
    }
    fetch_kintone_json(subdomain, api, '/k/v1/app.json', params, output)


# フィールド情報取得
def getFieldsInfo(subdomain,id,api,output):
    params = {
        'app': id,
        'lang': 'ja',
    }
    fetch_kintone_json(subdomain, api, '/k/v1/app/form/fields.json', params, output)

