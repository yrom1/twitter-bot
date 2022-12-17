source ~/PRIVATE/STAR_SCHEMA_PRIVATE.sh
source ~/PRIVATE/TWITTER_BOT_PRIVATE.sh
mysql -h $RDS_ENDPOINT -u $RDS_USER -p$RDS_PASSWORD -P $RDS_PORT < schama.sql
python3 -m pip install -r dev-requirements.txt
python3 main.py
