import json

from django.db.models import TextField
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView

from cw3.models import Workspace, WorkspaceInputItem


def generate_response(data):
    return Response(json.dumps(data),
                    content_type='application/json',
                    status=200,
                    headers={'Access-Control-Allow-Origin': '*'})


def generate_error_response(error: str):
    return generate_response({'error': error})


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
            print(str(workspace.to_dictionary()))
        else:
            workspace = Workspace.objects.filter(id=id)
            if len(workspace) != 0:
                workspace = workspace[0]
        if workspace is None:
            return generate_error_response("can not found workspace with id=" + workspace_id)
        return generate_response(workspace.to_dictionary())


class WorkspaceElementApi(APIView):
    """
    POST
    Get workspace, or create a new item.
    """

    def post(self, request):
        workspace_id = request.data['workspaceID']
        workspace_item_id = request.data['workspaceItemID']
        workspace: Workspace = Workspace.objects.filter(id=workspace_id)[0]
        if workspace is None:
            return generate_error_response("can not found workspace with id :: " + workspace_id)
        new_item = WorkspaceInputItem.create()
        workspace.input_list.add(new_item)
        workspace.save()
        is_after_target = False
        for i in workspace.input_list.all():
            if i.id == workspace_item_id:
                is_after_target = True
                new_item.order = i.order+1
                new_item.save()
            elif is_after_target:
                i.order = i.order + 1
                i.save()
        return generate_response(new_item.to_dictionary())

    # def options(self, request):
    #     return Response(json.dumps({'status': 'ok'}),
    #                     content_type='application/json',
    #                     status=200,
    #                     headers={'Access-Control-Allow-Origin': '*',
    #                              'Access-Control-Allow-Headers': '*',
    #                              'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'})
