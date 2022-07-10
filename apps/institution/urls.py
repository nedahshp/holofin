from django.urls import path
from .views import (
    WalletDepositView, WalletHistoryView, WalletWithdrawView,
    DepositRequestListView, DepositRequestCreateView, DepositRequestPayView,
    MyDepositRequestHistoryView, UserTransactionUpdateView, UserTransactionListView
)


app_name = 'institution'

urlpatterns = [
    path('transaction/', UserTransactionListView.as_view(), name='user_transactions'),
    path('transaction/<pk>/update/', UserTransactionUpdateView.as_view(), name='update_transaction'),
    path('wallet/history/', WalletHistoryView.as_view(), name='wallet_history'),
    path('wallet/deposit/', WalletDepositView.as_view(), name='wallet_deposit'),
    path('wallet/withdraw/', WalletWithdrawView.as_view(), name='wallet_withdraw'),
    path('deposit-request/', DepositRequestListView.as_view(), name='deposit_request_list'),
    path('deposit-request/new/', DepositRequestCreateView.as_view(), name='deposit_request_new'),
    # path('deposit-request/<pk>/users/', DepositRequestUsersListView.as_view(), name='deposit_request_users'),
    path('deposit-request/history/', MyDepositRequestHistoryView.as_view(), name='my_deposit_request_history'),
    path('deposit-request/<pk>/pay/', DepositRequestPayView.as_view(), name='deposit_request_pay'),
]