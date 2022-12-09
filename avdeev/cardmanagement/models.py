from django.db import models


# Create your models here.

class StatusCard(models.Model):
    Status_name = models.CharField(max_length=200, verbose_name='Название статуса')
    # статус карты (не активирована/активирована/просрочена

    def __str__(self):
        return self.Status_name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

class OperationCard(models.Model):
    Operation_name = models.CharField(max_length=200, verbose_name='Название статуса')
    # Операции: не Пополнение/Списание/Активация/деактивация

    def __str__(self):
        return self.Operation_name

    class Meta:
        verbose_name = 'Операция по карте'
        verbose_name_plural = 'Операции по картам'
#     Операции: Пополнение баланса(при создании 1 раз)(int)/списание(int)/полное погашение(date)/ активация(date)/деактивация(date)

class CardBaseTable(models.Model):
    card_series = models.IntegerField(verbose_name='Серия карты')
    card_number = models.IntegerField(verbose_name='Номер карты')
    card_create_date = models.DateTimeField(verbose_name='Дата выпуска карты')
    card_end_date = models.DateTimeField(verbose_name='Дата окончания карты')
    card_last_use = models.DateTimeField(verbose_name='Дата последнего использования карты')
    card_amount = models.IntegerField(verbose_name='Баланс')
    card_status = models.ForeignKey(StatusCard, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Статус')

    def __str__(self):
        return str(self.card_number)

    class Meta:
        verbose_name = 'Подарочная карта'
        verbose_name_plural = 'Подарочные карты'


class CardHistoryUse(models.Model):
    card_id = models.ForeignKey(CardBaseTable, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Номер карты')
    card_operation = models.ForeignKey(OperationCard, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Операция по карте')
    card_operation_detail = models.CharField(max_length=200,null=True, blank=True, verbose_name='Детали операции')