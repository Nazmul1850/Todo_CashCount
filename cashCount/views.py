

# Create your views here.


from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CashMemoForm,FixBudetForm
from .models import CashMemo,FixBudetModel


@login_required
def cashMemo(request):
    return render(request,'cashCount/cashHome.html')


@login_required
def getBudget(request):
    cashBud = get_object_or_404(FixBudetModel,userb=request.user)
    try:
        return cashBud
    except ValueError:
        return None





@login_required
def createCashMemo(request):
        if request.method == 'GET':
            return render(request,'cashCount/createCashMemo.html',{ 'form':CashMemoForm()})
        else:
            try:
                form = CashMemoForm(request.POST)
                memo = form.save(commit=False)
                memo.user = request.user
                memo.save()
                #updateBudget(request,memo.id)
                return redirect('cashCount:completedCashMemo')
            except ValueError:
                return render(request,'cashCount/createCashMemo.html',{ 'form':CashMemoForm(),'error':'Bad Data'})


@login_required
def showCashMemo(request,cash_pk):
    cash = get_object_or_404(CashMemo,pk=cash_pk,user=request.user)
    cashBud = get_object_or_404(FixBudetModel,userb=request.user)
    if request.method == 'GET':
        form = CashMemoForm(instance=cash)
        return render(request,'cashCount/cashview.html',{'cash':cash,'form':form})
    else:
        try:
            form = CashMemoForm(request.POST, instance=cash)
            form.save()
            #updateBudget(request,cash_pk)
            return redirect('cashCount:completedCashMemo')
        except ValueError:
            return render(request,'cashCount/cashview.html',{'cash':cash,'form':form,'error':'Bad Data'})


@login_required
def completedCashMemo(request):
    cash = CashMemo.objects.filter(user=request.user).order_by('-created')
    alltaken = 0
    allgiven = 0
    for x in cash:
        if x.taken:
            alltaken += x.cost
        if x.given:
            allgiven += x.cost
    return render(request,'cashCount/completedCashMemo.html',{'cash':cash,'alltaken':alltaken,'allgiven':allgiven})

@login_required
def deleteCashMemo(request,cash_pk):
    cash = get_object_or_404(CashMemo,pk=cash_pk,user=request.user)
    if request.method == 'POST':
        cash.delete()
        return redirect('cashCount:completedCashMemo')


@login_required
def FixBudget(request):
    if request.method == 'GET':
        cashBud = FixBudetModel.objects.all()
        for bud in cashBud:
            if bud.userb == request.user:
                cash = CashMemo.objects.filter(user=request.user).order_by('-created')
                alltaken = 0
                allgiven = 0
                for x in cash:
                    if x.taken:
                        alltaken += x.cost
                    if x.given:
                        allgiven += x.cost
                bud.budget = bud.budget - alltaken + allgiven
                return render(request,'cashCount/fixBudget.html',{ 'form':FixBudetForm(),'cashBudget':bud})
        return render(request,'cashCount/fixBudget.html',{ 'form':FixBudetForm()})
    else:
        try:
            cashBud = FixBudetModel.objects.all()
            for bud in cashBud:
                if bud.userb == request.user:
                    form = FixBudetForm(request.POST,instance=bud)
                    form.save()
                    return redirect('cashCount:FixBudget')
            form = FixBudetForm(request.POST)
            newbudget = form.save(commit=False)
            newbudget.userb = request.user
            newbudget.save()
            return redirect('cashCount:FixBudget')

        except ValueError:
            return render(request,'cashCount/fixBudget.html',{ 'form':FixBudetForm(),'cashBud':cashBud,'error':'Max limit Crossed'})
