./git_update.sh

python3 Middleware/transformation_validate.py
aws s3 cp Middleware/transformations.json s3://testingmidktbo/transformations.json
