from configparser import ConfigParser
import datetime as dt
import pandas as pd
import requests
import os
import fnmatch
import re

parser = ConfigParser()
#parser.read('config.cfg')
#username = parser.get('','')
#password = parser.get('','')
#authentication_url =  parser.get('','')

def drive_checker(username,secret_client):
    print('working on it')
    mp = []
    return mp

def mail_checker(username,token):
    print('working on it')
    mp = []
    return(mp)

def mp_validate():
    print('working on it')
    path = 'drive_downloads/'
    listOfFiles = os.listdir(path)
    pattern = '*.xlsx'
    valid_status = 1
    mandatory_columns = ['Campaign Initiative', 'Format Type', 'Buy Type', 'Agency', 'Client', 'Brand','Region', 'City','Temporality', 'Total Cost','KPI Units','Media Cost','KPI Cost Type','Vendor','Network / Site', 'Start Date (DD/MM/YYYY)', 'End Date (DD/MM/YYYY)']
    for i in listOfFiles:
        filename = os.path.splitext(i)[0]
        if fnmatch.fnmatch(i, pattern):
            df = pd.read_excel(f'{path}{i}', sheet_name = 'MEDIA PLAN', skiprows = 10)
            cols = df.columns
            for i in mandatory_columns:
                columns_to_add = []
                if i not in cols:
                    print('falta la columna: ' + i)
                    columns_to_add.append(i)

            if len(columns_to_add) < 1:
                print(f'El plan de medios {filename} tiene todas las columnas')
                valid_status = 0
            else:
                print('faltan columnas revise el archivo')
                print('pito')
            if "2021" in filename:
                filename = '2021' + (re.split('2021', filename)[1])
            if "Cierre" in filename:
                filename = (re.split('Cierre', filename)[0])+(re.split('Cierre', filename)[1])
            filename = filename.strip(' ')
            df['Filename'] = filename
            cols = df.columns
            excelOutput = f'result/{filename}.xlsx'
            df.to_excel(excelOutput, sheet_name= 'MEDIA PLAN', index = False, startrow = 10)
            print(excelOutput)


    if valid_status == 0:
        print('el mediaplan contiene todos los parametros necesarios')
    else:
        print('el mediaplan contiene errores')
    return valid_status

def mail_sender(message):
    print('working on it')
    mail_receiver = ['belem.viniegra@mediacom.com', 'edher@ktbo.com']
    message_status = 0
    if message_status == 0:
        print(f'No se ha enviado un correo a {mail_receiver} con la siguiente información{message}')
    else:
        print(f'Se ha enviado un correo a {mail_receiver} con la siguiente información{message}')
    return message_status

def mp_enrich(mp):
    print('working on it')
    mp_status = 0
    if mp_status ==0:
        print('el plan de medios se ha actualizado correctamente')
    else:
        print('el plan de medios no se ha podido actualizar')
    return mp_status
