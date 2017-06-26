from django.db import models


# Create your models here.

class WorkspaceInputItem(models.Model):
    itemText = models.TextField()
    isEditable = models.BooleanField()

    @classmethod
    def create(cls, data, editable=True):
        result = cls(itemText=data, isEditable=editable)
        result.save()
        return result

    def to_json(self):
        return dict(itemText=self.itemText, isEditable=self.isEditable, id=self.id)


class Workspace(models.Model):
    title = models.CharField(max_length=100)
    input_list = models.ManyToManyField(WorkspaceInputItem)

    @classmethod
    def create(cls, title):
        result = cls(title=title)
        result.save()
        empty_input = WorkspaceInputItem.create("")
        result.input_list.add(empty_input)
        return result

    def to_json(self):
        return dict(id=self.id, title=self.title, inputList=[i.to_json() for i in self.input_list.all()])
