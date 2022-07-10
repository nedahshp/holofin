from django import forms
from django.db.models import Q
from .models import UserDepositRequest, UserTransaction, DepositRequest


class UserTransactionForm(forms.ModelForm):
    class Meta:
        model = UserTransaction
        fields = ['tracking_number', 'status', 'reject_reason']


class UserWalletDepositTransactionForm(forms.ModelForm):
    class Meta:
        model = UserTransaction
        fields = ('amount', 'description', 'tracking_number', )

    def __init__(self, *args, **kwargs):
        disable_amount = kwargs.pop('disable_amount', False)
        self.deposit_request = kwargs.pop('deposit_request', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if disable_amount:
            self.fields['amount'].widget.attrs['class'] = 'form-control disabled'
            self.fields['amount'].disabled = True

    def clean(self):
        if self.deposit_request:
            if UserDepositRequest.objects.filter(
                Q(user=self.user) &
                Q(deposit_request=self.deposit_request) &
                Q(
                    Q(deposit__status=UserTransaction.Status.PENDING) |
                    Q(deposit__status=UserTransaction.Status.APPROVED)
                )
                    
            ).exists():
                raise forms.ValidationError('شما قبلا درخواست واریز اعتبار داده اید')
        return super().clean()



class UserWalletWithdrawTransactionForm(forms.ModelForm):
    class Meta:
        model = UserTransaction
        fields = ('amount', 'description', 'card_number')

class DepositRequestForm(forms.ModelForm):
    class Meta:
        model = DepositRequest
        fields = ('amount', 'description', )




