from helpers import get_today,to_timestamp,timestamp_to_iso,days_to_seconds,api_url,START_DATE
import datetime
import json
import time
from utils.logger import info, error, debug

def usage_urls(account_id, days_per_range, end=get_today(), start=START_DATE):
    dt = datetime.datetime
    end = dt.fromisoformat(end)
    start = dt.fromisoformat(start)
    ranges = []
    usage_urls = []
    if (end.timestamp() - start.timestamp()) > days_to_seconds(days_per_range):
        range_end = end.timestamp()
        range_start = (end.timestamp() - days_to_seconds(days_per_range))
        while (range_end - start.timestamp()) > days_to_seconds(days_per_range):
            ranges.append({
                'end': timestamp_to_iso(range_end), 'start': timestamp_to_iso(range_start)
            })
            range_end = (range_end - days_to_seconds(days_per_range))
            range_start = (range_start-days_to_seconds(days_per_range))
    for range in ranges:
        usage_urls.append(
            api_url(account_id, start=range['start'], end=range['end']))
    return usage_urls


def process_urls(urls,driver):
    usage = []
    length = len(urls)
    for url in urls:
        info(f"Making request to {url}.")
        driver.get(url)
        data = driver.find_elements_by_xpath("//pre")[0].text
        data = json.loads(data)
        data = data['reads']
        for line in data:
            usage.append(line)
        index = urls.index(url) + 1
        info(f'Processed {index} of {length} urls')
        time.sleep(.5)
    return(usage)


def get_data(account_id,driver):
    data = process_urls(usage_urls(account_id,10),driver)
    return data