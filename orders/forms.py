from django import forms
from .models import Order
class CheckoutForm(forms.Form):
    address_id=forms.IntegerField(widget=forms.HiddenInput)
    payment_method=forms.ChoiceField(choices=Order.PAYMENT,widget=forms.RadioSelect)
