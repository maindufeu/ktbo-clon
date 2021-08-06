import pandas as pd
import glob
import os
import fnmatch
import subprocess
from datetime import date
from datetime import timedelta
from datetime import datetime

today = date.today()
d = timedelta(days = 15)
d2 = timedelta(days = 105)

endDate = str(today-d)
endDate = f'{endDate}'
print(endDate)

startDate = str(today-d2)
startDate = f'{startDate}'
print(startDate)

########
path = 'Campaigns/**'
pattern = '*.csv'

sizmek = []
google = []
facebook = []
si_df = pd.DataFrame()
fb_df = pd.DataFrame()
go_df = pd.DataFrame()

for filename in glob.iglob(path, recursive=True):
    if os.path.isfile(filename): # filter dirs
        if fnmatch.fnmatch(filename, pattern):
            if fnmatch.fnmatch(filename, '*sizmek*'):
                print(filename)
                si = pd.read_csv(filename, usecols = ['Campaign Name', 'Date','Brand','Initiative', 'Platform', 'Campaign Label', 'Platform Cost', 'Impressions (Gross)', 'Clicks (Net)', 'Video Fully Played', 'Video Started', 'Campaign ID'])
                #si.columns = ['Campaign Name', 'Date', 'Brand', 'Initiative', 'Platform', 'Campaign Label', 'Platform Cost', 'Impressions', 'Clicks', 'Video Completions', 'Video Views']
                si['Datasource'] = "Sizmek Sas"
                si['Engagements'] = ""
                si = si[(si['Date'] >= startDate) & (si['Date'] < endDate)]
                si_df = pd.concat([si_df, si])
                #print(si_df['Date'].unique())
                #print("inicio:",min(si_df['Date']))
                #print("fin:",max(si_df['Date']))

            elif fnmatch.fnmatch(filename, '*google*'):
                print(filename)
                go = pd.read_csv(filename, usecols = ['Campaign', 'date_copy', 'Datasource','Brand','Initiative', 'Platform', 'Campaign_duplicate', 'platform_cost', 'Impressions', 'Clicks', 'Video Plays 100%', 'Engagements', 'Views','Campaign ID'])
                #go.columns = ['Campaign Name', 'Date', 'Datasource', 'Brand', 'Initiative', 'Platform', 'Campaign Label', 'Platform Cost', 'Impressions', 'Clicks', 'Video Completions', 'Engagements', 'Video Views']
                go = go[(go['date_copy'] >= startDate) & (go['date_copy'] < endDate)]
                go_df = pd.concat([go_df, go])
                #print(go_df['date_copy'].unique())
                #print("inicio:",min(go_df['date_copy']))
                #print("fin:",max(go_df['date_copy']))

            elif fnmatch.fnmatch(filename, '*facebook*'):
                print(filename)
                fb = pd.read_csv(filename, usecols = ['Temp Campaign Name', 'date_copy','Datasource','Brand_portfolio','Initiative', 'Platform', 'campaign_label', 'platform_cost', 'impressions', 'clicks', 'video_p100_watched_actions.video_view', 'actions.post_engagement','actions.video_view','campaign_id'])
                #fb.columns = ['Campaign Name', 'Date', 'Datasource', 'Brand', 'Initiative', 'Platform', 'Campaign Label', 'Platform Cost', 'Impressions', 'Clicks', 'Video Completions', 'Engagements', 'Video Views']
                #print(type(fb['Date'][1]))
                fb = fb[(fb['date_copy'] > startDate) & (fb['date_copy'] < endDate)]
                fb_df = pd.concat([fb_df, fb])
                #print(fb_df['date_copy'].unique())
                #print("inicio:",min(fb_df['date_copy']))
                #print("fin:",max(fb_df['date_copy']))

si_df.drop_duplicates( inplace=True)
print(si_df.columns)
print(fb_df.columns)
print(go_df.columns)
si_df.columns = ['clicks', 'platform_id', 'Video100', 'impressions' ,'video_views','campaign_name', 'daily', 'campaign_label','initiative','platform', 'platform_cost','brand','datasource','engagements']
print("sizmek:",len(si_df))
si_df.to_csv('Campaigns/kwincampaigns_si_unified.csv', index = False)
#print("sizmekdates:",si_df['Daily'].unique())
fb_df.drop_duplicates(inplace=True)
fb_df.columns = ['impressions', 'clicks', 'video_views', 'platform_id', 'engagements', 'Video100','brand', 'initiative', 'platform', 'platform_cost', 'campaign_label', 'datasource','campaign_name', 'daily' ]
print("facebook:",len(fb_df))
fb_df.to_csv('Campaigns/kwincampaigns_fb_unified.csv', index = False)
#print("facebookdates:", fb_df['Daily'].unique())
#print(go_df.columns)
go_df.drop_duplicates( inplace=True)
go_df.columns = ['platform_id','campaign_name','clicks','engagements', 'impressions','video_views', 'Video100', 'campaign_label', 'platform','initiative','brand', 'datasource',  'daily', 'platform_cost' ]
print("google:",len(go_df))
go_df.to_csv('Campaigns/kwincampaigns_go_unified.csv', index = False)
#print(go_df['Daily'].unique())


df_total = pd.concat([fb_df, si_df, go_df])
len(df_total)
print("ds:",df_total['datasource'].unique())
#print("dates:",df_total['Daily'].unique())
df_total.to_csv('Campaigns/adverity_last90.csv', index = False)
#cols = ['campaign_id','Campaign Name', 'Campaign Label', 'Platform','Initiative','Brand', 'Datasource', 'Daily', 'Engagements']
cols = ['platform_id','campaign_name', 'campaign_label', 'platform','initiative','brand', 'datasource', 'daily', 'engagements']
df_sum = df_total.groupby(by = cols).sum().reset_index()
print("ds:",df_sum['datasource'].unique())
print(len(df_sum))
df_sum = df_sum[df_sum['campaign_name'].str.contains('KTBOBRAZIL')==False]
print(df_sum)

#print(len(df_sum))
#print("summarized", df_sum['Daily'].unique())
df_sum.to_csv('Campaigns/stagging.csv', index = False)

print("start date:", min(df_sum['daily'].unique()))
print("end date:", max(df_sum['daily'].unique()))
print("days reported:", len(df_sum['daily'].unique()))

subprocess.call('git add .', shell=True)
subprocess.call('git commit -m "campaigns kwinunified update"', shell=True)
subprocess.call('git push', shell=True)
