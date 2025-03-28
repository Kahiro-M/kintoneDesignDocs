# 指定されたCSVファイルを読み込み、連想配列（辞書のリスト）として返す
def loadCsv(file_path, encoding='utf-8-sig'):
    import csv

    """
    指定されたCSVファイルを読み込み、連想配列（辞書のリスト）として返す

    :param file_path: CSVファイルのパス
    :param encoding: ファイルのエンコーディング（デフォルト: 'utf-8-sig'）
    :return: 辞書のリスト
    """
    records = []
    with open(file_path, newline='', encoding=encoding) as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))
    return transDict(records)

# アプリAPIデータを作成する
def transDict(records):
    """
    配列の各要素に辞書型を辞書型に辞書型へ変換する
    :param records: 配列の各要素に辞書型
        [
            {
                'id': 'app-id',
                'api': 'random-api-token',
                'name': 'app-name',
                'relation-id': 'app-id,app-id'
            },
            {
                'id': 'app-id',
                'api': 'random-api-token',
                'name': 'app-name',
                'relation-id': 'app-id,app-id'
            }
        ]
    :return:
        {
            'app-id': {
                'api': 'random-api-token',
                'name': 'app-name',
                'relation-id': 'app-id,app-id'
            },
            'app-id': {
                'api': 'random-api-token',
                'name': 'app-name',
                'relation-id': 'app-id,app-id'
            }
        }
    """
    result = {}
    for item in records:
        key = item['id']
        value = item.copy()
        del value['id']
        result[key] = value
    return result

# アプリAPIデータから連携先のAPI-Tokenを返す
def getRelationApiToken(appId,appDict):
    """
    アプリAPIデータから連携先のAPI-Tokenを連結して返す

    :param dict: 連想配列
    :return: 連結されたAPI-Token
    """
    apiTokens = [appDict[appId].get('api')]

    if(appDict[appId].get('relation-id') != ''):
        relationList = appDict[appId].get('relation-id').split(',')

        for rAppId in relationList:
            apiTokens.append(appDict[rAppId].get('api'))
    return ",".join(apiTokens)


def createDocs(json_path="out.json",csv_main_path="kintone_fields.csv",csv_lookup_path="kintone_lookup.csv", csv_reference_path="kintone_reference_table.csv"):
    import json
    import csv

    """
    指定されたkintoneのフィールド情報jsonファイルを読み込み、解析結果をcsvに保存

    :param json_path: jsonファイルのパス
    :param csv_main_path        : フィールド情報の出力csvファイルパス
    :param csv_lookup_path      : ルックアップフィールド情報の出力csvファイルパス
    :param csv_reference_path   : 関連レコード一覧情報の出力csvファイルパス
    :return: void
    """

    # JSON読み込み
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = data["properties"]

    # 出力用データ格納リスト
    main_fields = []
    lookup_fields = []
    reference_tables = []

    for code, info in fields.items():
        field_type = info.get("type", "")
        label = info.get("label", "")
        required = info.get("required", False)
        unique = info.get("unique", False)
        default_value = info.get("defaultValue", "")

        # 選択肢
        options_data = ""
        if "options" in info:
            options = info["options"]
            options_data = "; ".join([
                f"{opt['label']} (index: {opt['index']})"
                for opt in options.values()
            ])

        # 備考生成
        notes = []
        if info.get("enabled") is False:
            notes.append("無効化されている")
        if field_type in ["RECORD_NUMBER", "CREATOR", "MODIFIER", "CREATED_TIME", "UPDATED_TIME"]:
            notes.append("自動フィールド")
        if "options" in info:
            notes.append("選択肢あり")

        # ルックアップ情報

        if "lookup" in info:
            lookup = info.get("lookup")
            if lookup is None:
                notes.append("-- ルックアップ情報の取得に失敗")
            else:
                app_id = lookup["relatedApp"].get("app", "")
                related_key = lookup.get("relatedKeyField", "")
                sort = lookup.get("sort", "")
                mappings = "; ".join([
                    f"{m['field']} ← {m['relatedField']}"
                    for m in lookup.get("fieldMappings", [])
                ])
                lookup_fields.append([
                    code, label, app_id, related_key, sort, mappings, field_type
                ])
                notes.append(f"ルックアップ（app:{app_id}、key:{related_key}）")

        # 関連レコード一覧フィールド情報

        if field_type == "REFERENCE_TABLE":
            ref = info.get("referenceTable")
            if ref is None:
                notes.append("-- 関連レコード一覧情報の取得に失敗")
            else:
                app_id = ref["relatedApp"].get("app", "")
                condition = ""
                if "condition" in ref and isinstance(ref["condition"], dict):
                    condition = f"{ref['condition'].get('field', '')} = {ref['condition'].get('relatedField', '')}"
                display_fields = "; ".join(ref.get("displayFields", []))
                sort = ref.get("sort", "")
                size = ref.get("size", "")

                reference_tables.append([
                    code, label, app_id, condition, display_fields, sort, size
                ])
                notes.append(f"関連レコード一覧（app:{app_id}、条件:{condition}）")

        # メインフィールド情報に追加
        main_fields.append([
            code,
            label,
            field_type,
            "はい" if required else "いいえ",
            "はい" if unique else "いいえ",
            default_value if default_value else "なし",
            options_data if options_data else "なし",
            "、".join(notes)
        ])

    # CSV出力（メインフィールド）
    with open(csv_main_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["フィールドコード", "ラベル", "タイプ", "必須", "重複禁止", "デフォルト値", "選択肢", "備考"])
        writer.writerows(main_fields)

    # CSV出力（ルックアップ詳細）
    if lookup_fields:
        with open(csv_lookup_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["フィールドコード", "ラベル", "関連アプリID", "関連キー", "ソート条件", "フィールドマッピング", "フィールドタイプ"])
            writer.writerows(lookup_fields)

    # CSV出力（関連レコード一覧フィールド）
    if reference_tables:
        with open(csv_reference_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["フィールドコード", "ラベル", "関連アプリID", "条件", "表示フィールド", "ソート条件", "表示件数"])
            writer.writerows(reference_tables)

    print("CSV出力が完了しました。")
