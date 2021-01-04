from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    allow_group_login = forms.BooleanField()
    group_size = forms.IntegerField(label="Group_Size")