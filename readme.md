kintoneアプリのフィールド情報取得ツール
========================================

kintoneのアプリごとにフィールド情報を取得し、csv形式で出力します。

## 使い方
### 事前準備
1. 設定情報を取得したいkintoneアプリで閲覧権限のAPIトークンを発行
2. 以下のファイルに情報を記載
    - config.ini  
        接続先のkintoneのサブドメインを指定する
        ```
        [kintone]
        subdomain=sub_domain
        ```
    - appList.csv  
        取得したいアプリごとにアプリID、APIトークン、アプリ名、ルックアップor関連レコード一覧で参照しているアプリIDを指定する
        ```
        id,api,name,relation-id
        1,"SampleApp001ApiTokenSampleApp001ApiToken","サンプルアプリ1","2,3"
        2,"SampleApp002ApiTokenSampleApp002ApiToken","サンプルアプリ2","3"
        3,"SampleApp003ApiTokenSampleApp003ApiToken","サンプルアプリ3",
        ```
        relation-idで適切なアプリIDが含まれていない場合、参照先の情報を取得できません。  
        例）

        |フィールドコード|ラベル|必須|重複禁止|デフォルト値|選択肢|備考|
        |:--|:--|:--:|:--:|:--:|:--:|:--:|
        |サンプルアプリ2 |サンプルアプリ2 |いいえ |いいえ|なし|なし|-- 関連レコード一覧情報の取得に失敗|


### 実行
```
$ python main.py 
✅ JSONファイルを保存しました: C:\current\path\YYYYMMDD_HHMM_SS\1_サンプルアプリ1_appDesignInfo.json
CSV出力が完了しました。
✅ JSONファイルを保存しました: C:\current\path\YYYYMMDD_HHMM_SS\2_サンプルアプリ2_appDesignInfo.json
CSV出力が完了しました。
✅ JSONファイルを保存しました: C:\current\path\YYYYMMDD_HHMM_SS\3_サンプルアプリ3_appDesignInfo.json
CSV出力が完了しました。

$ ls YYYYMMDD_HHMM_SS
    1_サンプルアプリ1_appDesignInfo.json    1_サンプルアプリ1_kintone_fields.csv    1_サンプルアプリ1_kintone_lookup.csv    1_サンプルアプリ1_kintone_reference_table.csv
    2_サンプルアプリ2_appDesignInfo.json    2_サンプルアプリ2_kintone_fields.csv    2_サンプルアプリ2_kintone_lookup.csv    2_サンプルアプリ2_kintone_reference_table.csv
    3_サンプルアプリ3_appDesignInfo.json    3_サンプルアプリ3_kintone_fields.csv    3_サンプルアプリ3_kintone_lookup.csv    3_サンプルアプリ3_kintone_reference_table.csv
```