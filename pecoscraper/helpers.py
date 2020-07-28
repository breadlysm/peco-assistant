import datetime
from urllib.parse import urlunsplit, urlencode
import re
import os
from utils.logger import info, error, debug

START_DATE = os.environ.get('START_DATE')

def get_today():
    today = datetime.datetime.now().isoformat()
    return today


def find_inputs(driver,name):
    #loops all inputs
    for input in driver.find_elements_by_tag_name('input'):
        # Matches the element name with the Passed argument
        if input.get_property('name') == name:
            # Attempts to interact with element. If impossible, find next
            try:
                input.clear()
            except:
                continue
            info('Found ' + name + ' input')
            return input

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

def days_to_seconds(days):
    return (24*60*60*days)


def usage_urls(account_id,end=get_today(),start=to_timestamp(START_DATE)):
    end = datetime.datetime.fromisoformat(end)
    start = datetime.datetime.fromisoformat(start)
    ranges = []
    usage_urls = []
    if (end.timestamp() - start.timestamp()) > days_to_seconds(30):
        range_end = end.timestamp()
        range_start = (end.timestamp() - days_to_seconds(30))
        while (range_end - start.timestamp()) > days_to_seconds(30):
            ranges.append({'end':datetime.datetime.fromtimestamp(range_end).isoformat()
            ,'start':datetime.datetime.fromtimestamp(range_start).isoformat()})
            range_end = (range_end - days_to_seconds(30))
            range_start = (range_start-days_to_seconds(30))
    for range in ranges:
        usage_urls.append(api_url(account_id,start=range['start'],end=range['end']))
    return usage_urls

