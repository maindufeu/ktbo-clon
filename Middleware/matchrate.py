import glob
import match
import pandas as pd
import os
import csv
import fnmatch
from datetime import date
import subprocess
import re

mp_path = 'Mediaplan/result/*'
#files = os.listdir(mp_path)
mpfiles = []
mp_frames =[]

vendornetworkmap =  pd.read_csv('Mediaplan/vendor-network-id-mapping.csv')
reg = vendornetworkmap['Match'].values.tolist()
val = vendornetworkmap['Value'].values.tolist()
#print(vendornetworkmap)

#mediafacts = pd.DataFrame(columns = ["Campaign Name", "Mediaplan", "Campaign Mp Label", 'Datasource'])
mediaplans = pd.DataFrame(columns = ['Vendor', 'Network / Site', 'Campaign Mp Label', 'Mediaplan','Campaign Name', 'VendorNetworkID', 'Datasource'])
#df = pd.read_excel('Mediaplan/result/2021​_ktbo_kube_Adverity​_Mediaplan_Abril-Caricam.csv', sheet_name = 'MEDIA PLAN', skiprows = 10)
#print(df)

def taxonomytrim(campaign, datasource):
    campaigntrimmed = "undefined"
    if datasource == "Facebook Ads Insights":
        campaigntrimmed = "_". join(campaign.split("_")[0:12])
    elif datasource == "Google Adwords":
         campaigntrimmed= "_". join(campaign.split("_")[0:12])
    elif datasource == "Other Channels":
         campaigntrimmed= "_". join(campaign.split("_")[0:11])
    elif datasource == "Sizmek Sas":
         campaigntrimmed= "_". join(campaign.split("_")[0:10])
    elif datasource == "Twitter":
         campaigntrimmed= "_". join(campaign.split("_")[0:12])
    else:
        print("something went wrong")
        print(datasource)
    return(campaigntrimmed)

for filename in glob.iglob(mp_path, recursive=True):
    if os.path.isfile(filename): # filter dirs
        print(filename)
        mpfiles.append(filename)
        df = pd.read_excel(filename, usecols = ['Campaign Initiative', 'Filename', 'Vendor', 'Network / Site'], sheet_name = 'MEDIA PLAN', skiprows = 10)
        df.columns = ['Vendor', 'Network / Site','Campaign Mp Label', 'Mediaplan' ]
        df['Campaign upper'] = df['Campaign Mp Label'].str.upper().str.replace(" ", "")
        df['VendorNetworkID'] = df['Vendor'].str.upper().str.cat(df['Network / Site'].str.upper(), sep = "_")
        mapping_id = list(range(11))
        for i in mapping_id:
            df.loc[df['VendorNetworkID'].str.match(reg[i]), 'Datasource'] = val[i]
        df.loc[df['Datasource'].isnull(), 'Datasource']='Other Channels'
        print(df['Datasource'].unique())
        df['Campaign Name'] = df.apply(lambda row : taxonomytrim(row['Campaign upper'], row['Datasource']), axis = 1)
        mediaplans = pd.concat([mediaplans, df])

mediaplans[['Vendor', 'Network / Site', 'VendorNetworkID', 'Datasource', 'Mediaplan','Campaign Mp Label','Campaign upper', 'Campaign Name']].to_csv("mpcampaigns.csv", index=False)

#Mediafacts creation using a pd concat between a export from the explorer view and the other channels file
mediafactsexport = pd.read_csv('Campaigns/campaigns_unified.csv', usecols = ['Datasource', 'Campaign Name'])
mediafactsother = pd.read_excel('OtherCampaigns/pautas_locales_acumulado_other.xlsx', usecols = ['Campaign'])
mediafactsother['Datasource'] = 'Other Channels'
mediafactsother['Datastream'] = 'OtherCampaigns'
mediafactsother['Campaign upper'] = mediafactsother['Campaign'].str.upper().str.replace(" ", "")
mediafactsother['Campaign Name'] = mediafactsother.apply(lambda row : taxonomytrim(row['Campaign upper'], row['Datasource']), axis = 1)

mediafacts =  pd.concat([mediafactsother, mediafactsexport])
#mediaplans =  pd.read_csv('Mediaplan/mp_processed/Adverity-export_Plan.csv')

print('Mediaplan')
print(mediaplans)

print('Mediafacts')
print(mediafacts)

mr = match.mp_match(mediaplans, mediafacts)
print(mr)

subprocess.call('aws s3 cp matching_campaigns.csv s3://testingmidktbo/matched.csv >> aws_upd.log', shell=True)
subprocess.call('aws s3 cp unmatching_campaigns.csv s3://testingmidktbo/unmatched.csv >> aws_upd.log', shell=True)

today = date.today()
print(today)


#file = open('unmatched.csv', 'w+', newline ='')
#write = csv.writer(file)
#write.writerows(mr)
