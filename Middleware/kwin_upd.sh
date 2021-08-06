Rscript kwin_eval.r
now=`date +%y%m%d`
aws s3 cp resultsfinalDB2020.csv  s3://testingmidktbo/kwin_upd${now}.csv
