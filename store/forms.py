from django import forms
from .models import Review
class ReviewForm(forms.ModelForm):
    class Meta: model=Review; fields=['rating','title','body']; widgets={'rating':forms.Select(choices=[(i,f'{i} star'+('s' if i>1 else '')) for i in range(5,0,-1)])}
    def __init__(self,*a,**kw): super().__init__(*a,**kw); [f.widget.attrs.update({'class':'form-input'}) for f in self.fields.values()]
