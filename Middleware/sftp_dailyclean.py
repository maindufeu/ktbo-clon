import pysftp
import pandas as pd
import datetime

con = pysftp.Connection('sftp.adverity.com',username='ktbo',password='Eemaa9eiF4aeteigheiyu3Mae0piej')
con.chdir('uploads/test')
dstreams = con.listdir()
print(dstreams)
year = str(datetime.date.today().strftime("%Y"))
today = str(datetime.date.today().strftime("%Y-%m-%d"))

for ds in dstreams:
    filelist = []
    l = con.listdir_attr(ds)
    for i in l:
        filelist.append(str(i))
        print(str(i))
    if len(filelist) > 0 :
        f = pd.DataFrame(filelist)
        s = f[0].str.split(expand=True)
        s.columns = ['permissions','x1','puid','x', 'size','day','month','time','name']
        s = s[['day','month','time','name']]
        #s.to_csv("sftpfiles_test.csv")
        s['date']=s['day'].astype(str)+"/"+s['month'] + "/" + year
        s['date']=pd.to_datetime(s['date'], format="%d/%b/%Y")
        s = s[['date','name']]
        oldfiles = list(s['name'][s['date']!= today])
        for i in oldfiles:
            deletionfile = f'{ds}/{i}'
            print(deletionfile,"to be removed")
            con.remove(deletionfile)
    else:
        print(f'no hay archivos viejos en {ds}')

con.close()
