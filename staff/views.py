from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from game.models import ExtendUser
from .models import CheckIn, Prize, OwnPrize
from .forms import AwardForm

@staff_member_required
def search(request):
    if request.method == 'POST':
        if 'scan' in request.POST:
            scanform = AwardForm(request.POST.copy(), prefix='scan')
            keyinform = AwardForm(prefix='keyin')

            scanform.data['scan-nid'] = scanform.data['scan-nid'][:-1].upper() #學號轉成大寫且去掉最後一個字(掃描機會自動在最後加0)

            if scanform.is_valid():
                nid = scanform.cleaned_data.get('nid')
                return HttpResponseRedirect(reverse('detail', args=[nid]))
                scanform = AwardForm(prefix='scan')
        elif 'keyin' in request.POST:
            keyinform = AwardForm(request.POST.copy(), prefix='keyin')
            scanform = AwardForm(prefix='scan')

            keyinform.data['keyin-nid'] = keyinform.data['keyin-nid'].upper() #學號轉成大寫

            if keyinform.is_valid():
                nid = keyinform.cleaned_data.get('nid')
                return HttpResponseRedirect(reverse('detail', args=[nid]))
                keyinform = AwardForm(prefix='keyin')
    else:
        scanform = AwardForm(prefix='scan')
        keyinform = AwardForm(prefix='keyin')
    return render(request, "search.html", {'scanform':scanform, 'keyinform':keyinform})

@staff_member_required
def detail(request, nid):
    checkin = CheckIn.objects.filter(studentId=nid).all()
    prize = OwnPrize.objects.filter(studentId=nid).all()
    score = 0
    try:
        for i in ExtendUser.objects.filter(studentId=nid).first().history.all():
            score = score + i.score
    except:
        score = 0
    return render(request, "detail.html", {'nid': nid, 'checkin': checkin, 'prize': prize, 'score': score})

@staff_member_required
def checkin(request, nid):
    CheckIn(studentId=nid).save()
    return HttpResponseRedirect(reverse('detail', args=[nid]))

@staff_member_required
def prize(request, nid):
    if request.method == 'POST':
        prize = Prize.objects.filter(name=request.POST['item']).first()
        OwnPrize(prize=prize, studentId=nid).save()
        prize.last =  prize.last - 1
        prize.save()
        return HttpResponseRedirect(reverse('detail', args=[nid]))
    else:
        prize = Prize.objects.all()
    return render(request, "prize.html", {'nid': nid, 'prize': prize})
