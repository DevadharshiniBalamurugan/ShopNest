from django import forms
from django.utils.text import slugify
from store.models import Product,Seller
class ProductForm(forms.ModelForm):
    class Meta: model=Product; fields=['name','slug','description','price','original_price','category','brand','sku','stock','main_image','image','specifications','is_active','is_featured']
    def __init__(self,*a,**kw): super().__init__(*a,**kw); [f.widget.attrs.update({'class':'form-input'}) for f in self.fields.values()]
    def clean_slug(self): return self.cleaned_data.get('slug') or slugify(self.cleaned_data['name'])
class SellerForm(forms.ModelForm):
    class Meta: model=Seller; fields=['store_name','description']
    def __init__(self,*a,**kw): super().__init__(*a,**kw); [f.widget.attrs.update({'class':'form-input'}) for f in self.fields.values()]
