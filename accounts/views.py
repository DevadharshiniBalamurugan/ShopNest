from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect,render
from .forms import AddressForm,ProfileForm,RegisterForm,UserEditForm
from .models import Address,Profile

def register(request):
    form=RegisterForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.save(); Profile.objects.create(user=user,role=form.cleaned_data['role']); login(request,user)
        messages.success(request,'Welcome to ShopNest! Your account is ready.')
        return redirect('accounts:profile')
    return render(request,'accounts/register.html',{'form':form})

@login_required
def profile(request):
    profile,_=Profile.objects.get_or_create(user=request.user)
    return render(request,'accounts/profile.html',{'profile':profile,'recent_orders':request.user.orders.prefetch_related('items')[:4]})

@login_required
def edit_profile(request):
    profile,_=Profile.objects.get_or_create(user=request.user)
    uform=UserEditForm(request.POST or None,instance=request.user); pform=ProfileForm(request.POST or None,request.FILES or None,instance=profile)
    if request.method=='POST' and uform.is_valid() and pform.is_valid(): uform.save(); pform.save(); messages.success(request,'Profile updated.'); return redirect('accounts:profile')
    return render(request,'accounts/edit_profile.html',{'uform':uform,'pform':pform})

@login_required
def addresses(request): return render(request,'accounts/addresses.html',{'addresses':request.user.addresses.all()})
@login_required
def address_form(request,pk=None):
    address=get_object_or_404(Address,pk=pk,user=request.user) if pk else None; form=AddressForm(request.POST or None,instance=address)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.user=request.user
        if obj.is_default: request.user.addresses.update(is_default=False)
        obj.save(); messages.success(request,'Address saved.'); return redirect('accounts:addresses')
    return render(request,'accounts/address_form.html',{'form':form,'address':address})
@login_required
def address_delete(request,pk):
    if request.method=='POST': get_object_or_404(Address,pk=pk,user=request.user).delete(); messages.success(request,'Address removed.')
    return redirect('accounts:addresses')
@login_required
def address_default(request,pk):
    address=get_object_or_404(Address,pk=pk,user=request.user); request.user.addresses.update(is_default=False); address.is_default=True; address.save(update_fields=['is_default']); return redirect('accounts:addresses')
