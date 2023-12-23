from django import forms #import django forms

CHARACTER_CHOICES = (       #specify choices as a tuple
    ('#1', 'Bar Chart'),    #when user selects "Bar Chart", it is sorted as "#1"
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
)

#define class-based Form imported from Django forms
class SalesSearchForm(forms.Form):
    book_title= forms.CharField(max_length=120)
    chart_type= forms.ChoiceField(choices=CHARACTER_CHOICES)

