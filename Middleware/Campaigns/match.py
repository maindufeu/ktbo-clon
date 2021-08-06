import datetime as dt
import pandas as pd
import requests
import os
import fnmatch
import re

def mp_validate():
    print('working on it')
    path = 'sftp/'
    listOfFiles = os.listdir(path)
    pattern = '*.xlsx'
    valid_status = 1
    for i in listOfFiles:
        filename = os.path.splitext(i)[0]
        if fnmatch.fnmatch(i, pattern):
            mp = pd.read_excel(f'{path}{i}', sheet_name = 'MEDIA PLAN', skiprows = 10)
            adv = pd.read_excel(f'{path}{i}', sheet_name = 'MEDIA PLAN', skiprows = 10)
            excelOutput = f'result/{filename}.xlsx'
            df.to_excel(excelOutput, sheet_name= 'MEDIA PLAN', index = False, startrow = 10)
            print(excelOutput)


    if valid_status == 0:
        print('el match rate es de:')
        print(matchrate)
    else:
        print('el mediaplan contiene errores')
    return df




df1 = mp_validate()
print(df1)
