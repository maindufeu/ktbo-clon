import pandas as pd
import os
from openpyxl import load_workbook

def generarAcumulado()

listFiles = os.listdir("files/")

print(listFiles)

inData = pd.DataFrame()
dfBuffer = pd.DataFrame()
column_checker_list = pd.DataFrame()
for file in listFiles:
    dfBuffer = pd.read_excel("files/%s"%file)
    column_checker_list = column_checker_list.append(pd.DataFrame({"Column Names": list(dfBuffer.columns), "File": file}))
    #print(dfBuffer[["End Date"]])
    inData = inData.append(dfBuffer, sort=False)
    

column_checker_list["Ocurrence"] = 1
columns_vs_files = column_checker_list.pivot(index="File", columns="Column Names", values="Ocurrence")
ok_columns = []
for column in list(columns_vs_files.columns):
    missingInFiles =  list(columns_vs_files.loc[columns_vs_files[column].isnull()].index)
    if len(missingInFiles) > 0:
        print(column, "is mising in: ", list(columns_vs_files.loc[columns_vs_files[column].isnull()].index))
    if column not in real_columns:
        print(column, " doesn't look like a valid column name... \n")
    if column in real_columns:
        ok_columns.append(column)
        

real_columns = []
try:
    valid_columns = pd.read_csv("ValidColumnsReference.csv")
    real_columns = list(valid_columns["Valid Columns"])
except:
    real_columns = list(inData.columns)
    
inData.to_csv("archivo_acumulado.csv", index=False)