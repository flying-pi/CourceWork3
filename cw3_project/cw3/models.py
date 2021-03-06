from django.db import models


# Create your models here.

class WorkspaceInputItem(models.Model):
    itemText = models.TextField()
    isEditable = models.BooleanField()
    order = models.IntegerField()

    @classmethod
    def create(cls, data='', editable=True):
        result = cls(itemText=data, isEditable=editable, order=0)
        result.save()
        return result

    def to_dictionary(self):
        return dict(itemText=self.itemText, isEditable=self.isEditable, id=self.id, order=self.order)


class Workspace(models.Model):
    title = models.CharField(max_length=100)
    input_list = models.ManyToManyField(WorkspaceInputItem)

    @classmethod
    def create(cls, title):
        result = cls(title=title)
        result.save()
        empty_input = WorkspaceInputItem.create('''p(x) = x*cos(x)
q(x) = -exp(x)
u(x) = 1+x
equation = Eq.Diff.marginal('y``+q(x)*y+p(x)*y`-u(x)',0,1,1,4)
print(equation.source)
print(equation.conditions)
equation.calculate()
''')
        result.input_list.add(empty_input)
        return result

    def to_dictionary(self):
        return dict(id=self.id, title=self.title, inputList=[i.to_dictionary() for i in self.input_list.all()])
