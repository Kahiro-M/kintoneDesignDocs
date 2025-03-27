#------------------------------------------------#
# 現在時刻のフォルダ作成
#------------------------------------------------#
def mkdirDatetime(folder_start='',folder_end=''):
    #日付を取得
    import datetime as dt
    #フォルダの存在確認
    import os

    dt_now = dt.datetime.now()
    timestamp_str = dt_now.strftime('%Y%m%d_%H%M_%S')
    # 現在のフォルダパス
    currentDir = os.getcwd()
    # 作成フォルダ名
    resultDirName = folder_start + timestamp_str + folder_end
    # フォルダのフルパス
    resultDirFullPath = currentDir + '\\' + resultDirName

    if(not (os.path.exists(resultDirFullPath))):
        os.mkdir(resultDirFullPath)
    
    return resultDirFullPath

#------------------------------------------------#
# 今日の日付を取得
#------------------------------------------------#
def getToday(split_str='/'):
    #日付を取得
    import datetime as dt

    dt_now = dt.datetime.now()
    timestamp_str = dt_now.strftime('%Y'+split_str+'%m'+split_str+'%d')
    return timestamp_str

#------------------------------------------------#
# 時刻を取得
#------------------------------------------------#
def getNow(split_str=':'):
    #日付を取得
    import datetime as dt

    dt_now = dt.datetime.now()
    timestamp_str = dt_now.strftime('%H'+split_str+'%M'+split_str+'%S')
    return timestamp_str

if __name__ == '__main__':
    mkdirDatetime()
