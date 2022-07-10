from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth import get_user_model
from jalali_date import date2jalali, datetime2jalali
from django.views.generic import  ListView, CreateView, UpdateView
from apps.core.mixins import CustomFormTemplateMixin, CustomListTemplateMixin
from apps.core.permissions import PermissionRequireMixin
from .models import UserTransaction, DepositRequest, UserDepositRequest
from .forms import (
    UserWalletDepositTransactionForm, UserWalletWithdrawTransactionForm,
    DepositRequestForm, UserTransactionForm
)



User = get_user_model()

    

class WalletDepositView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.ADMIN, User.Roles.USER]
    model = UserTransaction
    form_class = UserWalletDepositTransactionForm
    page_title = 'واریز اعتبار'
    success_url = reverse_lazy('institution:wallet_history')
    success_message = 'درخواست واریز اعتبار با موفقیت ثبت شد'
    cancel_url = reverse_lazy('users:dashboard')

    def get_page_subtitle(self):
        user = self.request.user
        return user.get_full_name()

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['user'] = user
        return initial

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.transaction_type = UserTransaction.TransactionTypes.DEPOSIT
        return super().form_valid(form)


class WalletWithdrawView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.ADMIN, User.Roles.USER]
    model = UserTransaction
    form_class = UserWalletWithdrawTransactionForm
    page_title = 'برداشت اعتبار'
    success_url = reverse_lazy('institution:wallet_history')
    success_message = 'درخواست برداشت اعتبار با موفقیت ثبت شد'
    cancel_url = reverse_lazy('users:dashboard')

    def get_page_subtitle(self):
        user = self.request.user
        return user.get_full_name()

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['user'] = user
        return initial

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.transaction_type = UserTransaction.TransactionTypes.WITHDRAW
        return super().form_valid(form)



class UserTransactionListView(PermissionRequireMixin, CustomListTemplateMixin, ListView):
    permissions = [User.Roles.ADMIN]
    model = UserTransaction
    page_title = 'تراکنش های کاربران'
    fields = ['id', 'user', 'amount', 'transaction_type', 'card_number', 'tracking_number', 'status', 'created_at']
    action_buttons = [
        {'title': 'ویرایش', 'url_name': 'institution:update_transaction', 'arg_field': 'id',
         'fa-icon': 'fa-pen', 'class': '', 'class_form_field': 'id'},
    ]

    def get_amount(self, obj):
        return "{:,.0f}".format(obj.amount)

    def get_transaction_type(self, obj):
        return obj.get_transaction_type_display()
    
    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d %H:%M:%S')

    
class UserTransactionUpdateView(PermissionRequireMixin, CustomFormTemplateMixin, UpdateView):
    permissions = [User.Roles.ADMIN]
    model = UserTransaction
    form_class = UserTransactionForm
    page_title = 'ویرایش تراکنش'
    success_url = reverse_lazy('institution:user_transactions')
    success_message = 'تراکنش با موفقیت ویرایش شد'
    cancel_url = reverse_lazy('institution:user_transactions')

    def get_page_subtitle(self):
        return self.get_object().user.get_full_name()


class WalletHistoryView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    permissions = [User.Roles.ADMIN, User.Roles.USER]
    page_title = 'تاریخچه تراکنش ‌های من'
    fields = ['id', 'amount', 'transaction_type', 'card_number', 'tracking_number', 'status', 'created_at']
    header_buttons = [
        {'title': 'وایز', 'url': reverse_lazy('institution:wallet_deposit'), 'icon': 'plus'},
        {'title': 'برداشت', 'url': reverse_lazy('institution:wallet_withdraw'), 'icon': 'minus'},
    ]

    def get_status(self, obj):
        return obj.get_status_display()

    def get_amount(self, obj):
        return "{:,.0f} تومان".format(obj.amount)

    def get_transaction_type(self, obj):
        return obj.get_transaction_type_display()

    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d %H:%M:%S')

    def get_card_number(self, obj):
        return obj.card_number or '-'

    def get_page_subtitle(self):
        user = self.get_object()
        return user.get_full_name()

    def get_queryset(self):
        user = self.request.user
        return user.transactions.all()


class DepositRequestListView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    permissions = [User.Roles.ADMIN]
    page_title = 'درخواست های واریز اعتبار'
    fields = ['id', 'amount', 'description', 'created_at']
    header_buttons = [
        {'title': 'ثبت درخواست', 'url': reverse_lazy('institution:deposit_request_new'), 'icon': 'plus'},
    ]

    def get_amount(self, obj):
        return "{:,.0f} تومان".format(obj.amount)

    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d')

    def get_page_subtitle(self):
        user = self.get_object()
        return user.get_full_name()

    def get_queryset(self):
        institution = self.request.user.institution
        return DepositRequest.objects.filter(institution=institution)


class DepositRequestCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.ADMIN]
    model = DepositRequest
    form_class = DepositRequestForm
    page_title = 'درخواست واریز اعتبار'
    success_url = reverse_lazy('institution:deposit_request_list')
    success_message = 'درخواست واریز اعتبار با موفقیت ثبت شد'
    cancel_url = reverse_lazy('users:dashboard')

    def get_page_subtitle(self):
        user = self.request.user
        return user.get_full_name()

    def form_valid(self, form):
        user = self.request.user
        diposit = form.instance
        diposit.created_by = user
        diposit.institution = user.institution
        form.save()
        diposit.generate_users_deposit_request()
        return super().form_valid(form)


class DepositRequestPayView(WalletDepositView):
    model = UserDepositRequest
    page_title = 'پرداخت درخواست واریز اعتبار'
    success_url = reverse_lazy('institution:my_deposit_request_history')
    success_message = 'درخواست واریز اعتبار با موفقیت پرداخت شد'

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['disable_amount'] = True
        kwargs['deposit_request'] = self.get_object().deposit_request
        kwargs['user'] = self.request.user
        return kwargs


    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['amount'] = self.get_object().deposit_request.amount * user.deposit_quantity
        return initial

    @transaction.atomic
    def form_valid(self, form):
        user = self.request.user
        deposit = form.instance
        user_deposit_request = self.get_object()
        deposit.user = user
        deposit.amount = user.deposit_quantity * user_deposit_request.deposit_request.amount
        deposit.transaction_type = UserTransaction.TransactionTypes.DEPOSIT_REQUEST
        deposit.save()
        user_deposit_request.deposit = deposit
        user_deposit_request.quantity = user.deposit_quantity
        user_deposit_request.save()
        return super().form_valid(form)


class MyDepositRequestHistoryView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    permissions = [User.Roles.ADMIN, User.Roles.USER]
    page_title = 'تاریخچه درخواست واریز اعتبار'
    fields = ['id', 'quantity', 'created_at']
    action_buttons = [
        {'title': 'پرداخت', 'url_name': 'institution:deposit_request_pay', 'arg_field': 'id',
         'fa-icon': 'fa-money', 'class': '', 'class_form_field': 'id'},
    ]
    

    def get_quantity(self, obj):
        if obj.deposit:
            return "{:,.0f} تومان".format(obj.deposit.amount)
        return 'پرداخت نشده'

    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d')

    def get_page_subtitle(self):
        user = self.get_object()
        return user.get_full_name()

    def get_queryset(self):
        user = self.request.user
        return user.assigned_deposit_requests.all()



