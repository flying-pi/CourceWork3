import inspect
import json
import math

from django.db.models import TextField
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView

from cw3 import models
from cw3.calc import Calculator
from cw3.models import Workspace, WorkspaceInputItem


def generate_response(data,status = 200):
    return Response(json.dumps(data),
                    content_type='application/json',
                    status=status,
                    headers={'Access-Control-Allow-Origin': '*'})


def generate_error_response(error: str):

    return generate_response({'error': error},status=400)


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
            return generate_error_response("can not found workspace with id=" + str(workspace_id))
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
            return generate_error_response("can not found workspace with id :: " + str(workspace_id))
        order = 0
        items = workspace.input_list.all()
        target_item = workspace.input_list.all().filter(id=workspace_item_id)
        if len(target_item) != 1:
            workspace_item_id = -1
        else:
            target_item = target_item[0]
            order = target_item.order + 1
        if workspace_item_id < 0:
            for i in items:
                if i.order < order:
                    order = i.order
            for index in range(len(items)):
                i = items[index]
                i.order += 1;
                i.save()
        else:
            for index in range(len(items)):
                i = items[index]
                if i.id == target_item.id:
                    continue
                if i.order > target_item.order:
                    i.order += 1
                    i.save()
        new_item = WorkspaceInputItem.create()
        new_item.order = order
        new_item.save()
        workspace.input_list.add(new_item)
        workspace.save()
        result = dict(newItem=new_item.to_dictionary(),
                      ID_OrderMap=[dict(id=i.id, order=i.order) for i in items])
        return generate_response(result)

    def delete(self, request):
        workspace_id = request.query_params['workspaceID']
        workspace_item_id = request.query_params['workspaceItemID']
        workspace: Workspace = Workspace.objects.filter(id=workspace_id)[0]
        if workspace is None:
            return generate_error_response("can not found workspace with id :: " + str(workspace_id))
        items = workspace.input_list.all()
        target_item = workspace.input_list.all().filter(id=workspace_item_id)
        if len(target_item) != 1:
            return generate_error_response("can not found item with id :: " + str(workspace_id))
        target_item = target_item[0]
        workspace.input_list.remove(target_item)
        for i in range(len(items)):
            if items[i].order > target_item.order:
                items[i].order -= 1
                items[i].save()
        target_item.delete()
        items = workspace.input_list.all()
        result = dict(removedItemID=workspace_item_id,
                      ID_OrderMap=[dict(id=i.id, order=i.order) for i in items])
        return generate_response(result)


class CodeApi(APIView):
    """
    POST
    Get workspace, or create a new item.
    """

    def post(self, request):
        workspace_id = request.data['workspaceID']
        workspace_item_id = request.data['workspaceItemID']
        code = request.data['code']

        workspace: Workspace = Workspace.objects.filter(id=workspace_id)[0]
        if workspace is None:
            return generate_error_response("can not found workspace with id :: " + str(workspace_id))
        target_item = workspace.input_list.all().filter(id=workspace_item_id)
        if len(target_item) != 1:
            return generate_error_response("can not found item with id :: " + str(workspace_id))
        target_item = target_item[0]
        target_item.itemText = code
        target_item.save()
        execute_result = Calculator([(str(i.id), i.itemText) for i in workspace.input_list.all()]).execute()
        return generate_response(execute_result)
