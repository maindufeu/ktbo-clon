cd ktbo-bi/Middleware

python3 sftp_dailyclean.py
./sftp_download.sh
python3 campaignskwin_unifier.py
python3 sqlinsert.py
Rscript KWIN/kwin_eval.r

aws s3 cp kwin_basecumulative.csv  s3://kwin/kwinbase.csv
