import datetime
from urllib.parse import urlunsplit, urlencode
import re
import os

START_DATE = os.environ.get('START_DATE')

def get_today():
    today = datetime.datetime.now().isoformat()
    return today


def to_timestamp(start):
    timestamp = datetime.datetime.strptime(start, "%Y-%m-%d").isoformat()
    return timestamp

def api_url(account_id, start=to_timestamp(START_DATE),
            end=get_today(),
            agg_type='hour'):
    scheme = 'https'
    netloc = 'peco.opower.com'
    path = f"/ei/edge/apis/DataBrowser-v1/cws/cost/utilityAccount/{account_id}"
    query = urlencode(dict(startDate=start,endDate=end,aggregateType=agg_type))
    return urlunsplit((scheme,netloc,path, query, ""))

def get_uuid(txt):
    return re.findall(r"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b",txt)[0]