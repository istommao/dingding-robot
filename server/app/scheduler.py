"""app scheduler."""
import logging
import json

import requests

from tornado.escape import json_decode, json_encode

from . import cache, conf

logging.basicConfig(level=logging.INFO, filename='main.log')


START_KEY = 'monitor:{}:{}'


def feedCard(datalist):
    """feedCard."""
    links = []
    for data in datalist:
        link = {'title': data.get('title', '告警'),
                'actionURL': data.get('url')}
        links.append(link)

    payload = {
        "actionCard": {
            "title": "sentry告警",
            "text": "sentry告警",
            "hideAvatar": "0", 
            "btnOrientation": "0", 
            "btns": links
        },
        "msgtype": "actionCard"
    }
    return payload


def handler_datalist(datalist):
    """handler_datalist."""

    if len(datalist) == 1:
        data = datalist[0]
        text = {
            "msgtype": "link",
            "link": {
                "title": "sentry告警 level: {}".format(data.get('level')),
                "text": data.get('message', 'sentry告警'),
                "picUrl": "",
                "messageUrl": data.get('url', 'http://sentry.tianzhus.com/tianzhus')
            }
        }
    else:
        text = feedCard(datalist)
    return json_encode(text)


def push2dingding(datalist):
    """Push data to dingding."""
    headers = {'Content-Type': 'application/json'}
    payload = handler_datalist(datalist)

    resp = requests.post(conf.DINGDING_URL, data=payload, headers=headers)

    return resp


def scheduler():
    """Timing schedule."""
    key = START_KEY.format('sentry', 'alarm')

    # operation to be atomic
    with cache.KVSTORE.pipeline() as pipe:
        pipe.lrange(key, 0, -1).delete(key)
        rlist = pipe.execute()[0]
        rlist.reverse()

    if not rlist:
        return

    datalist = []
    for item in rlist:
        try:
            data = json_decode(item)
            data = json.loads(data)
            datalist.append(data)
        except json.decoder.JSONDecodeError:
            logging.error('ERROR: json format error %s', item)
            continue

    if len(datalist) > 0:
        resp = push2dingding(datalist)
        logging.info('status_code: %s content: %s', resp.status_code, resp.content)
