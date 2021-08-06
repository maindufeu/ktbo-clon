import pandas as pd
import os
from openpyxl import load_workbook
import re
import glob

listFiles = glob.glob("files/*.xlsx")

try:
    valid_columns = pd.read_csv("ValidColumnsReference.csv")
    real_columns = list(valid_columns["Valid Columns"])
except:
    real_columns = list(inData.columns)


#print(listFiles)

inData = pd.DataFrame()
dfBuffer = pd.DataFrame()
column_checker_list = pd.DataFrame()

inData2 = pd.DataFrame()
dfBuffer2 = pd.DataFrame()
column_checker_list2 = pd.DataFrame()

for file in listFiles:
    dffile = pd.read_excel("%s"%file,None, engine = "openpyxl")
    dfkeys = dffile.keys()
    for i in dfkeys:
        if re.match(i, "other campaigns", re.IGNORECASE):
            sheetname = i
    print("Attempting......", file, "\n")
    dfBuffer = pd.read_excel("%s"%file, sheet_name=sheetname, engine="openpyxl")
    dfBuffer["File"] = file
    column_checker_list = column_checker_list.append(pd.DataFrame({"Column Names": list(dfBuffer.columns), "File": file}))
    #print(dfBuffer[["End Date"]])
    inData = inData.append(dfBuffer, sort=False)
    print(file, "..... OK \n")


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

for file in listFiles:
    print(file)
    try:
        dfBuffer2 = pd.read_excel("%s"%file, sheet_name="Twitter campaigns", engine="openpyxl")
        dfBuffer2["File"] = file
        column_checker_list2 = column_checker_list2.append(pd.DataFrame({"Column Names": list(dfBuffer2.columns), "File": file}))
        #print(dfBuffer[["End Date"]])
        inData2 = inData2.append(dfBuffer2, sort=False)


        column_checker_list2["Ocurrence"] = 1
        columns_vs_files2 = column_checker_list2.pivot(index="File", columns="Column Names", values="Ocurrence")
        ok_columns = []

        for column in list(columns_vs_files2.columns):
            missingInFiles =  list(columns_vs_files2.loc[columns_vs_files2[column].isnull()].index)
            if len(missingInFiles) > 0:
                print(column, "is mising in: ", list(columns_vs_files2.loc[columns_vs_files2[column].isnull()].index))
            if column not in real_columns:
                print(column, " doesn't look like a valid column name... \n")
            if column in real_columns:
                ok_columns.append(column)
    except:
        pass
inData = inData.append(inData2, sort=False)
inData.to_csv("archivo_acumulado.csv", index=False)

inData = inData.drop_duplicates()

mediacomData = inData[~inData["Campaign"].str.contains("_BRA_", na=False)]
brasilData = inData[inData["Campaign"].str.contains("_BRA_", na=False)]

TwitterCampaigns = inData.loc[inData["Platform"] == "Twitter"][ok_columns]
OtherCampaigns = inData.loc[inData["Platform"] != "Twitter"][ok_columns]

TwitterCampaignsMediacom = mediacomData.loc[mediacomData["Platform"] == "Twitter"][ok_columns]
OtherCampaignsBrasil = brasilData.loc[brasilData["Platform"] != "Twitter"][ok_columns]

TwitterCampaignsBrasil = brasilData.loc[brasilData["Platform"] == "Twitter"][ok_columns]
OtherCampaignsMediacom = mediacomData.loc[mediacomData["Platform"] != "Twitter"][ok_columns]

OtherCampaigns.to_excel("pautas_locales_acumulado_other.xlsx", sheet_name="Other campaigns", index=False)
TwitterCampaigns.to_excel("pautas_locales_acumulado_twitter.xlsx", sheet_name="Twitter campaigns", index=False)

OtherCampaignsMediacom.to_excel("pautas_locales_acumulado_other_mediacom.xlsx", sheet_name="Other campaigns", index=False)
TwitterCampaignsMediacom.to_excel("pautas_locales_acumulado_twitter_mediacom.xlsx", sheet_name="Twitter campaigns", index=False)

OtherCampaignsBrasil.to_excel("pautas_locales_acumulado_other_brasil.xlsx", sheet_name="Other campaigns", index=False)
TwitterCampaignsBrasil.to_excel("pautas_locales_acumulado_twitter_brasil.xlsx", sheet_name="Twitter campaigns", index=False)
