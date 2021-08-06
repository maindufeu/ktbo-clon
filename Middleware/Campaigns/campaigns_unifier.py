import pandas as pd
import glob
import os
import fnmatch
import subprocess


other = pd.read_excel("Campaigns/othercampaigns/acumulado_other.xlsx", usecols = ['Campaign'])
twitter = pd.read_excel("Campaigns/twitter/acumulado_twitter.xlsx", usecols = ['Campaign'])
other['Datasource'] = "Other Channels"
twitter['Datasource'] = "Twitter"

twitter = twitter['Campaign'].str.upper().str.strip(" ").unique().tolist()
tw =pd.DataFrame({'Campaign Name':twitter})
print("Twitter length:")
print(len(twitter))

other = other['Campaign'].str.upper().str.strip(" ").unique().tolist()
ot = pd.DataFrame({'Campaign Name':other})
print("Other Campaigns length:")
print(len(other))

########
path = 'Campaigns/**'
pattern = '*.csv'

sizmek = []
google = []
facebook = []

si_df = pd.DataFrame(({'Campaign Name' : []}))
fb_df = pd.DataFrame(({'Campaign Name' : []}))
go_df = pd.DataFrame(({'Campaign Name' : []}))


for filename in glob.iglob(path, recursive=True):
    if os.path.isfile(filename): # filter dirs
        if fnmatch.fnmatch(filename, pattern):
            if fnmatch.fnmatch(filename, '*sizmek*'):
                print(filename)
                si = pd.read_csv(filename, usecols = ['Temp Campaign Name', 'Date'])
                si['Campaign Name']= si['Temp Campaign Name']
                si= si[['Campaign Name','Date']]
                #si=si.reindex(columns=['Temp Campaign Name', 'Date'])
                si['Datasource'] = "Sizmek Sas"
                si[(si['Date'] > '2021-01-01') & (si['Date'] < '2022-04-31')]
                si_l = si['Campaign Name'].unique().tolist()
                sizmek.append(si_l)
                si_df = pd.concat([si_df, si])
                #si_df = si_df.append(si, ignore_index = True)
                #print("si")
                #print(si.head())
                #print(len(si_df))

            elif fnmatch.fnmatch(filename, '*google*'):
                print(filename)
                go = pd.read_csv(filename, usecols = ['Campaign', 'date_copy'])
                go.columns = ['Campaign Name', 'Date']
                go['Datasource'] = "Google Adwords"
                go[(go['Date'] > '2021-01-01') & (go['Date'] < '2022-04-31')]
                go_l = go['Campaign Name'].unique().tolist()
                google.append(go_l)
                go_df = pd.concat([go_df, go])
                #print("go")
                #print(go.head())
                #print(len(go_df))

            elif fnmatch.fnmatch(filename, '*facebook*'):
                print(filename)
                fb = pd.read_csv(filename, usecols = ['Temp Campaign Name', 'date_copy'])
                fb.columns = ['Campaign Name', 'Date']
                fb['Datasource'] = "Facebook Ads Insights"
                fb[(fb['Date'] > '2021-01-01') & (fb['Date'] < '2022-04-31')]
                fb_l = fb['Campaign Name'].unique().tolist()
                facebook.append(fb_l)
                fb_df = pd.concat([fb_df, fb])
                #print("fb")
                #print(fb.head())
                #print(len(fb_df))
######
print(si_df.columns)
print(si_df.head())

df_u = pd.concat([fb_df, go_df, si_df, ot, tw])
print(df_u.head())
df_u = df_u.drop_duplicates('Campaign Name')
df_u.to_csv('Campaigns/campaigns_unified.csv', index = False)

print("lista de campañas únicas:")
print(df_u)

subprocess.call('git add .', shell=True)
subprocess.call('git commit -m "campaigns unified update"', shell=True)
subprocess.call('git push', shell=True)
