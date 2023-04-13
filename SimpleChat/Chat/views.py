from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer
from account.models import UserData
from rest_framework import pagination


class ThreadListApiView(APIView):
    """
        A view for interacting with Thread objects.
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get(self, request, *args, **kwargs):
        """
        Return a list of all threads.
        If there are no threads, return a message indicating so.
        Returns:
        - A list of Thread objects serialized to JSON.
        - If there are no threads, a message indicating so.
        """
        thread = Thread.objects.all()
        serializer = ThreadSerializer(thread, many=True)
        if not serializer.data:
            return Response('No threads')
        else:
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
         Create a new thread.
         If the thread already exists, return the existing thread.
         Returns:
            If the thread already exists, the title of the existing thread.
         """
        data = {
            'title': request.data.get('title'),
        }
        serializer = ThreadSerializer(data=data)
        thread = Thread.objects.filter(title=data.get('title'), participants = request.user.id).first()
        if thread:
            return Response(thread.title)
        if serializer.is_valid():
            thread = serializer.save()
            thread.add_participant(request.user.id)
            if request.data.get('participants'):
                new_user = UserData.objects.filter(username=request.data.get('participants')).first()
                if new_user:
                    thread.add_participant(new_user.id)
                    return Response(serializer.data)
                else:
                    return Response('Participant not exist')
        return Response(serializer.errors)

    def put(self, request, *args, **kwargs):
        """
        Add a user to an existing thread
        If the thread already has two participants, return an error message
        Returns:
        - If the user is successfully added to the thread, a success message.
        - If the thread already has two participants, an error message.
        - If the user is not authorized to add participants, an error message.
        """
        thread = Thread.objects.filter(title=request.data.get('title'), participants=request.user.id).first()
        new_user = UserData.objects.filter(username=request.data.get('username')).first()
        if thread.participants.count() == 2:
            return Response("Thread can't have more than 2 participants.")
        try:
            thread.add_participant(new_user.id)
            return Response(f'User {new_user.username} add to thread {thread.title}')
        except:
            return Response('You are not root thread')

    def delete(self, request, *args, **kwargs):
        """
        Delete a thread
        Returns:
        - If the thread is successfully deleted, a success message.
        - If the user is not authorized to delete the thread, an error message.
        - If there is an unexpected error, the error message.
        """
        thread = Thread.objects.filter(title=request.data.get('title'), participants=request.user.id).first()
        try:
            thread.delete()
            return Response(f'thread {thread.title} deleted')
        except TypeError:
            return Response('You are not root thread')
        except Exception as e:
            return Response(e)


class MessageListApiView(APIView):
    """
        API View for listing and creating messages.
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get(self, request, *args, **kwargs):
        """
        Retrieves messages for a given thread and marks them as read
        for the user if the user is a participant.
        Returns:
            Response: A list of message objects.
        """

        thread_title = request.data.get('title')
        thread = Thread.objects.filter(title=thread_title).first()
        if not thread:
            return Response("Thread doesn't exist.")

        user = request.user
        if not thread.participants.filter(id=user.id).exists():
            return Response("User isn't a participant in the thread.")

        messages = thread.messages.all()
        for message in messages:
            if user.id != message.sender.id and not message.is_read:
                message.is_read = True
                message.save()

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Creates a new message in a given thread, if the user is a participant.
        Returns:
            Response: The newly created message object, if successful.
        """
        thread_title = request.data.get('title')
        thread = Thread.objects.filter(title=thread_title).first()
        if not thread:
            return Response("Thread doesn't exist.")

        user = request.user
        if not thread.participants.filter(id=user.id).exists():
            return Response("User isn't a participant in the thread.")

        data = {
            'thread': thread.id,
            'sender': user.id,
            'content': request.data.get('content'),
        }
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class UnreadMessagesApiView(APIView):
    """
        API View that returns the number of unread messages for the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieves the number of unread messages for the authenticated user.
        Returns:
            Response: A dictionary containing the number of unread messages for
            each thread the user is a participant of.
        """
        user = request.user
        threads = Thread.objects.filter(participants=user)
        unread_counts = {}
        for thread in threads:
            unread_count = Message.objects.filter(thread=thread, is_read=False).exclude(
                sender=user).count()
            unread_counts[thread.title] = unread_count
        return Response(unread_counts)