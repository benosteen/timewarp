import time
from libmproxy.script import concurrent

from dateutil.parser import parse as dateutil_parser

@concurrent
def request(context, flow):
    #print "handle request: %s - %s" % (flow.request.host, flow.request.path)
    # http://web.archive.org/web/19981212031357
    fluxcapacitor_setting = "19981201052808"
    if flow.request.headers["accept-datetime"]:
        # eg Accept-Datetime: Thu, 31 May 2007 20:35:00 GMT
        parsed_date = dateutil_parser(flow.request.headers["accept-datetime"])
        fluxcapacitor_setting = parsed_date.strftime("%Y%m%d%H%M%S")
    if not "id_/http" in flow.request.path:
        flow.request.path = "/web/%sid_/http://%s%s" % (fluxcapacitor_setting, flow.request.host, flow.request.path)
    flow.request.scheme = "http"
    flow.request.host = "web.archive.org"
    flow.request.headers["Host"] = ["web.archive.org"]
