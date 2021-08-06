cd ktbo-bi/Middleware

python3 sqlcompleteview.py
Rscript KWIN/kwin_completeeval.r

aws s3 cp KWIN/kwin_basecumulative.csv  s3://kwin/kwinbase.csv
git add .
git commit -m "kwin update"
git push
