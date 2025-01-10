from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import models
from django.utils import timezone

class LottosConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lottos'

    def ready(self):
        post_migrate.connect(self.insert_initial_data, sender=self)


    def insert_initial_data(self, sender, **kwargs):

        from .models import LottoWinner,LottoAdmin

        if not LottoWinner.objects.exists():
            LottoWinner.objects.create(
                winning_numbers=[1, 2, 3, 4, 5, 6],
                extra_number=7
            )
            print("초기 LottoWinner 데이터가 삽입되었습니다.")

        if not LottoAdmin.objects.exists():
            LottoAdmin.objects.create(limit_number=10)
            print("초기 LottoAdmin 데이터가 삽입되었습니다.")
