from django.shortcuts import render, redirect, get_object_or_404
import uuid
import json
from .models import LottoPurchase, LottoWinner, LottoAdmin
from django.contrib import messages
from django.http import HttpResponse

def generate_unique_id():
    return str(uuid.uuid4()).replace("-", "")[:8]

def check_lotto_result(user_lotto_numbers, winning_numbers, extra_number):

    matching_numbers = set(user_lotto_numbers).intersection(winning_numbers)
    matching_count = len(matching_numbers)

    if matching_count == 6:
        return "1등"
    elif matching_count == 5 and extra_number in user_lotto_numbers:
        return "2등"
    elif matching_count == 5:
        return "3등"
    elif matching_count == 4:
        return "4등"
    elif matching_count == 3:
        return "5등"
    else:
        return "꽝"

def index(request):
    context = {}

    if request.method == "POST":
        user_id = request.POST.get('user_id').strip()
        user = LottoPurchase.objects.filter(user_id=user_id).first()
        winner = LottoWinner.objects.latest('id')
        request.session['user_id'] = user_id
        if user is None:
            request.session['error'] = "해당 식별번호의 구입자가 존재하지 않습니다."
        else:
            request.session['result'] = check_lotto_result(user.lotto_numbers,winner.winning_numbers,winner.extra_number)
        return redirect('index')

    if 'result' in request.session:
        context["result"] = request.session['result']
        context["user_id"] = request.session['user_id']
        del request.session['result']
        del request.session['user_id']

    if 'error' in request.session:
        context["error"] = request.session['error']
        context["user_id"] = request.session['user_id']
        del request.session['error']
        del request.session['user_id']
    return render(request, 'lottos/index.html', context)

def buy(request):

    if request.method == "POST":
        lotto_admin = LottoAdmin.objects.latest('id')
        if lotto_admin.limit_number <= 0:
            response = """
                <script type="text/javascript">
                    alert("이미 구매 가능한 로또 수가 끝났습니다.");
                    window.history.back();
                </script>
                """
            return HttpResponse(response)

        lotto_admin = LottoAdmin.objects.latest('id')
        lotto_admin.limit_number -= 1
        lotto_admin.save()

        user_id = request.POST.get('id')
        lotto_numbers = request.POST.get('lotto_numbers')
        lotto_numbers = json.loads(lotto_numbers)
        lotto_purchase = LottoPurchase(user_id=user_id, lotto_numbers=lotto_numbers)
        lotto_purchase.save()
        return render(request,'lottos/index.html')
    context = {
        'first_range': range(1, 7),
        'second_range': range(1, 46),
        'id' : generate_unique_id()
    }
    return render(request,'lottos/buy.html',context)