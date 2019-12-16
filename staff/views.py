from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from game.models import ExtendUser
from .forms import AwardForm

@staff_member_required
def award(request):
    scanform = AwardForm(prefix='scan')
    keyinform = AwardForm(prefix='keyin')
    return render(request, "award.html", {'scanform':scanform, 'keyinform':keyinform})
