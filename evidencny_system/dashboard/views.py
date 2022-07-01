from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Item, Borrowed_item


@login_required(login_url='user-login')
def index(request):
    item = Item.objects.all()

    context = {
        'item': item,
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='user-login')
def borrowed(request):
    borrowed = Borrowed_item.objects.all()
    user = User.objects.filter(groups=2)
    item = Item.objects.all()

    context = {
        'borrowed': borrowed,
        'user': user,
        'item': item,
    }
    return render(request, 'dashboard/borrowed.html', context)


@login_required(login_url='user-login')
def detail(request, item_PN):
    item = Item.objects.get(item_PN=item_PN)
    if 'borrow' in request.POST:
        if item.item_stock == 'Yes':
            item.item_stock = 'No'
            item.save()
            Borrowed_item.objects.create(item=item, user=request.user)
        else:
            messages.info(request, 'There are no more free items of this type')
        return redirect('dashboard-borrowed')
    if 'return' in request.POST:
        Borrowed_item.objects.filter(item=item).delete()
        item.item_stock = 'Yes'
        item.save()
        return redirect('dashboard-index')
    return render(request, 'dashboard/detail.html', {'item': item})


@login_required(login_url='user-login')
def scan(request):
    return render(request, 'dashboard/scan.html')


