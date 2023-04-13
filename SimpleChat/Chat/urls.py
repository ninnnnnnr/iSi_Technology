from django.urls import path
from .views import ThreadListApiView, MessageListApiView, UnreadMessagesApiView

urlpatterns = [
    path('api/threads_list', ThreadListApiView.as_view()),
    path('api/messages_list', MessageListApiView.as_view()),
    path('api/unread', UnreadMessagesApiView.as_view()),
]
