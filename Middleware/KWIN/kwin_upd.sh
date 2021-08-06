Rscript kwin_eval.r
now=`date +%y%m%d`
aws s3 cp kwin2.csv  s3://testingmidktbo/kwin_upd${now}.csv
aws s3 cp kwinnew.csv  s3://testingmidktbo/kwinnew.csv
aws s3 cp kwin_basecumulative.csv  s3://kwin/kwinbase.csv
