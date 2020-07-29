from helpers import get_today,to_timestamp,timestamp_to_iso,days_to_seconds,api_url
import datetime

def usage_urls(account_id, end=get_today(), start=to_timestamp(START_DATE)):
    dt = datetime.datetime
    end = dt.fromisoformat(end)
    start = dt.fromisoformat(start)
    ranges = []
    usage_urls = []
    if (end.timestamp() - start.timestamp()) > days_to_seconds(30):
        range_end = end.timestamp()
        range_start = (end.timestamp() - days_to_seconds(30))
        while (range_end - start.timestamp()) > days_to_seconds(30):
            ranges.append({
                'end': timestamp_to_iso(range_end), 'start': timestamp_to_iso(range_start)
            })
            range_end = (range_end - days_to_seconds(30))
            range_start = (range_start-days_to_seconds(30))
    for range in ranges:
        usage_urls.append(
            api_url(account_id, start=range['start'], end=range['end']))
    return usage_urls


def process_usage(usage):
    energy_use = []
    for hour in usage:
        energy_use.append({
            "measurement": "energy_usage",
            "time": parse(hour['startTime']).isoformat(),
            "fields": {
                "Kwh": float(hour['value']),
                "cost": float(hour['providedCost'])
            }
        })