import pysftp
import pandas as pd
import datetime

con = pysftp.Connection('sftp.adverity.com',username='ktbo',password='Eemaa9eiF4aeteigheiyu3Mae0piej')
con.chdir('uploads/test')
dstreams = con.listdir()

for ds in dstreams:
    print(ds)
    l = con.listdir_attr(ds)
    print(l)
    for i in l:
        print("extractos:",str(i))
con.close()
