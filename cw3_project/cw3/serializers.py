from rest_framework import serializers

from cw3.models import WorkspaceInputItem, Workspace


class WorkspaceInputItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkspaceInputItem
        fields = ('itemText', 'isEditable')


class WorkspaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Workspace
        fields = ('title', 'input_list')
