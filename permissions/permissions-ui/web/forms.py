from django import forms

class BamForm(forms.Form):
    choices = [("PUBLIC", "PUBLIC"), ("CONTROLLED", "CONTROLLED"), ("REGISTERED", "REGISTERED")]    
    Datasets = forms.ChoiceField(choices=choices, help_text="<span class='hovertext' data-hover='Choose what type of datasets you want to manage'>Datasets type:</span>", label="")
