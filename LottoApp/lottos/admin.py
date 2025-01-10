from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import LottoPurchase, LottoWinner, LottoAdmin
import random
from collections import defaultdict
from django import forms
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse

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

@admin.register(LottoWinner)
class LottoWinnerAdmin(admin.ModelAdmin):

    actions = ['generate_winning_numbers', 'check_all_members']

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST':
            action_name = request.POST.get('action')
            if action_name == 'generate_winning_numbers':
             
                queryset = self.get_queryset(request).none()
                self.generate_winning_numbers(request, queryset)
                
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return super().changelist_view(request, extra_context)

    def check_all_members(self, request, queryset):

        users = LottoPurchase.objects.all()  
        result_count = defaultdict(int)
        
        for winner in queryset:
            winner_result_count = defaultdict(int)
            for user in users:
                result = check_lotto_result(user.lotto_numbers, winner.winning_numbers, winner.extra_number)
                winner_result_count[result] += 1 
            result_message = f"<li><strong>총 참여 수 : </strong>{users.count()}명</li>"
            result_message += "".join(
                f"<li><strong>{rank}</strong> : {count}명</li>" for rank, count in winner_result_count.items()
            )
            
            winning_numbers_message = f"<p><strong>당첨 번호 - </strong> {', '.join(map(str, winner.winning_numbers))}</p>"
            extra_number_message = f"<p><strong>추가 번호 - </strong> {winner.extra_number}</p>"
            description_message = f"<p><strong>전체 당첨 결과입니다.</strong></p>"
            full_message = description_message + winning_numbers_message + extra_number_message + f"<ul>{result_message}</ul>"
            self.message_user(request, mark_safe(f"<strong>추첨 날짜 - {winner.winning_date}</strong> {full_message}"), level=messages.SUCCESS)

    check_all_members.short_description = "전체 사용자 당첨 여부 확인"


    def generate_winning_numbers(self, request, queryset):
       
        numbers = random.sample(range(1, 46), 6)
        extra_number = random.choice([num for num in range(1, 46) if num not in numbers])
        winner = LottoWinner.objects.create(winning_numbers=numbers,extra_number=extra_number)
        winner.save()
        message = mark_safe("✅ <strong>관리자에 의해 당첨 번호가 자동으로 추가되었습니다.</strong>")
        self.message_user(request, message, level=messages.INFO)

    generate_winning_numbers.short_description = "당첨 번호 추첨"

admin.site.register(LottoPurchase)
admin.site.register(LottoAdmin)