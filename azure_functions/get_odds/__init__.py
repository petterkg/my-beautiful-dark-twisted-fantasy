import datetime
import logging
import requests
import azure.functions as func
import json


def main(mytimer: func.TimerRequest, outputblob: func.Out[bytes]):
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'


    fpl_json = requests.get(url).json() 
    download_time = str(datetime.datetime.now())
    fpl_json["download_time"]= download_time

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    outputblob.set(json.dumps(fpl_json, indent=4, ensure_ascii=False))