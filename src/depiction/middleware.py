import sys
import cProfile as profile
from cStringIO import StringIO

from django.conf import settings
from django.template import Template, Context

PROFILE_HTML = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Template Documentation</title>
    <style>
        body {
            font-family: Helvetica;
            font-size: 12px;
            color: #777;
        }

        .marker {
            display: block;
            height: 12px;
            background-image: -moz-linear-gradient(center bottom, rgb(41,176,239) 2%, rgb(70,212,255) 51%);
            background-image: -webkit-gradient(linear, left bottom, left top, color-stop(0.21, rgb(101,188,248)), color-stop(0.61, rgb(132,226,255)));
        }

        table { margin: 0px 40px; }

        tr.main td {
            font-size: 16px;
            font-weight: bold;
            padding-top: 25px;
            padding-bottom: 10px;
            border-bottom: 1px solid #999;
        }

        tr.subs td:first-child {
            width: 200px;
        }

        tr.subs td {
            border-bottom: 1px solid #eee;
        }

        .lineno {
            color: rgb(101,188,255);
            font-weight: bold;
        }

        .time, td.lineno {
            text-align: right;
        }
    </style>
</head>
<body>
    <table>
        {% for annotation in annotations %}
            <tr class="main">
                <td colspan="5"><span class="lineno">{{ annotation.ep.code.co_firstlineno }}</span> 
                {{ annotation.ep.code.co_filename }}</td>
            </tr>
            {% for sub in annotation.subs %}
                <tr class="subs">
                    <td><span style="width: {{ sub.width }}px;" class="marker"></span></td>
                    <td class="time">{{ sub.time }}</td>
                    <td class="lineno">{{ sub.ep.code.co_firstlineno }}</td>
                    <td>{{ sub.ep.code.co_filename|default:sub.ep.code }}</td>
                </tr>
            {% endfor %}
        {% endfor %}
    </table>
</body>
</html>
"""


def pull_entry_point(ep):
    subs = []
    if ep.calls:
        for cl in ep.calls:
            maxtt = 0
            for cl in ep.calls:
                maxtt = cl.totaltime if cl.totaltime > maxtt else maxtt

        if maxtt:
            coef = 180 / maxtt
        else:
            coef = 0

        for cl in ep.calls:
            subs.append({'width': int(coef * cl.totaltime),
                         'time': 1000 * cl.totaltime,
                         'ep': cl})
            
    return {'ep': ep, 'subs': subs}


class ProfilerMiddleware(object):
    def can(self, request):
        return settings.PROFILING and 'prof' in request.GET \
            and (not settings.INTERNAL_IPS or \
            request.META['REMOTE_ADDR'] in settings.INTERNAL_IPS)
    
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if self.can(request):
            self.profiler = profile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if self.can(request):
            filter = request.GET.get('prof')
            self.profiler.create_stats()
            annotations = []
            for ep in self.profiler.getstats():
                try:
                    if filter and not filter in ep.code.co_filename:
                        continue
                    annotations.append(pull_entry_point(ep))
                except AttributeError:
                    pass
            template = Template(PROFILE_HTML)
            context = Context({'annotations': annotations})
            response.content = template.render(context)
        return response
