# iSi_Technology Simple Chat Test
## Description


The application is designed to provide functionality for creating and managing threads and 
messages between two participants. The app contains two models: Thread and Message. 
The Thread model has fields for participants, created and updated dates. The Message 
model has fields for sender, text, thread, created date, and whether it has been read or not.

The application provides a set of REST endpoints for creating, retrieving, and updating 
threads and messages. The endpoints allow for the creation of a thread and message, retrieval 
of threads for any user, marking a message as read, and retrieving the number of unread 
messages for a user. The application also provides pagination where needed using the 
PageNumberPagination class.

The app has been customized to provide functionality for Django admin to help manage threads and 
messages. The application has been secured using Simple JWT or Django Token authentication.

The database used in this app is SQLite. To run the app, users can follow the instructions 
provided in the README file. Additionally, a database dump has been created to help with loading 
test data for the application.

Overall, the app provides a comprehensive solution for managing threads 
and messages between two participants.

## Install and run app for development:

Dependence: Python3.10

```sh
git clone https://github.com/ninnnnnnr/iSi_Technology.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python SimpleChat/manage.py runserver
```

## Routings

 *Account:*
 - api/register/
 - api/token/
 - api/token/refresh/

  *ThreadListApiView:*
 - api/threads_list
 
  *MessageListApiView:*
 - api/messages_list
 
  *UnreadMessagesApiView:*
 - api/unread







