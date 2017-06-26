import json

from django.http import HttpResponse

from cw3.models import Workspace


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_workspace(request):
    workspace_id = request.GET['id'] if 'id' in request.GET else ''
    if workspace_id == '' or workspace_id == '-1':
        test = Workspace.create("empty")
        print(str(test.to_json()))
    result = HttpResponse(json.dumps(test.to_json()), content_type='application/json', status=200)
    # result = HttpResponse(json.dumps(dict(test="tst")), content_type='application/json', status=200)
    result.__setitem__('Access-Control-Allow-Origin', '*')
    return result
