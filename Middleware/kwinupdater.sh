python3  sftp_dailyclean.py
./sftp_download.sh
python3 campaignskwin_unifier.py
#./KWIN/kwin_upd.sh
Rscript KWIN/kwin_eval.r
now=`date +%y%m%d`
aws s3 cp KWIN/kwin2.csv  s3://testingmidktbo/kwin_upd${now}.csv
aws s3 cp KWIN/kwinnew.csv  s3://testingmidktbo/kwinnew.csv
aws s3 cp KWIN/kwin_basecumulative.csv  s3://kwin/kwinbase.csv
