from django.db import models
from django.db.models.constraints import UniqueConstraint
from apps.core.models import AbstractModel


class Institution(AbstractModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    card_number = models.CharField(max_length=255, blank=True, null=True)
    bank_account_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'موسسه'
        verbose_name_plural = 'موسسه'




class UserTransaction(AbstractModel):
    class TransactionTypes(models.IntegerChoices):
        DEPOSIT = 0, 'واریز'
        WITHDRAW = 1, 'برداشت'
        INSTALLMENT = 2, 'قسط'
        DEPOSIT_REQUEST = 3, 'درخواست واریز'
        
    class Status(models.IntegerChoices):
        PENDING = 0, 'در انتظار'
        APPROVED = 1, 'تایید شده'
        REJECTED = 2, 'رد شده'
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='transactions')
    amount = models.PositiveIntegerField(verbose_name='مقدار')
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    tracking_number = models.CharField(max_length=50, verbose_name='شماره رهگیری', null=True, blank=True)
    transaction_type = models.IntegerField(choices=TransactionTypes.choices, verbose_name='نوع تراکنش')
    card_number = models.CharField(max_length=20, verbose_name='شماره کارت', null=True, blank=True)
    status = models.IntegerField(choices=Status.choices, verbose_name='وضعیت', default=Status.PENDING)
    reject_reason = models.TextField(verbose_name='دلیل رد', null=True, blank=True)


class DepositRequest(AbstractModel):
    amount = models.PositiveIntegerField(verbose_name='مقدار')
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='created_deposit_requests')
    institution = models.ForeignKey('institution.Institution', on_delete=models.PROTECT, related_name='deposit_requests')

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = 'درخواست واریز'
        verbose_name_plural = 'درخواست واریز'

    def generate_users_deposit_request(self):
        for user in self.institution.users.all():
            UserDepositRequest.objects.create(
                user=user,
                deposit_request=self,
            )


class UserDepositRequest(AbstractModel):
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='assigned_deposit_requests')
    deposit_request = models.ForeignKey('institution.DepositRequest', on_delete=models.PROTECT,
                                        related_name='user_deposit_requests')
    deposit = models.ForeignKey('institution.UserTransaction', on_delete=models.PROTECT,
                                related_name='user_deposit_requests', null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name='تعداد', default=1)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'درخواست واریز'
        verbose_name_plural = 'درخواست واریز'



