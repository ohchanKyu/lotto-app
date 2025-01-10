from django.db import models
import json

class LottoPurchase(models.Model):
    user_id = models.CharField(max_length=8)
    lotto_numbers = models.JSONField() 
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User Id: {self.user_id} - Lotto Numbers: {self.lotto_numbers} - Date: {self.date}"

 
class LottoAdmin(models.Model):

    limit_number = models.IntegerField()

    def __str__(self):
        return f"로또 판매 제한 수 : {self.limit_number}"


class LottoWinner(models.Model):
    winning_date = models.DateField(auto_now_add=True)
    winning_numbers = models.JSONField()
    extra_number = models.IntegerField()

    def __str__(self):
        return f"추첨 날짜: {self.winning_date} - 당첨 번호: {self.winning_numbers} - 추가 번호: {self.extra_number}"