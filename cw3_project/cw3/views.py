import json

from django.db.models import TextField
from django.http import HttpResponse
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView

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


class WorkspaceApi(APIView):
    """
    GET id:
    Get workspace, or create a new item.
    """
    id = TextField()

    @detail_route()
    def get(self, request):
        workspace_id = request.GET['id'] if 'id' in request.GET else ''
        workspace: Workspace = None
        if workspace_id == '' or workspace_id == '-1':
            workspace = Workspace.create("empty")
            print(str(workspace.to_json()))
        else:
            workspace = Workspace.objects.filter(id=id)
            if len(workspace) != 0:
                workspace = workspace[0]
        if workspace is None:
            json_data = json.dumps({'error': "can not found workset with id=" + workspace_id})
        else:
            json_data = json.dumps(workspace.to_json())
        return Response(json_data,
                        content_type='application/json',
                        status=200,
                        headers={'Access-Control-Allow-Origin': '*'})
