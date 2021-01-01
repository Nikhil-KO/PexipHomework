# PexipHomework
Dropbox assignment for Pexip

# Strucure
* Client
    * client.py - main file to set up client app, contains functions for each event, i.e. create, delete, modify and move
    * observer.py - object to listen for changes and run the event functions defined in client
    * dipatcher.py - given the information of change in the file system, efficiently extract change and dispatch to server

* Server
    * server.py - network interface to receive the data
    * dropboxService.py - service to efficiently translate data to changes in the file system

* Tests - run unit tests for client & server functionality

# TODO
1. move detail inito observer class 

# Possible improvements
1. User model, each client has an ID/JSON web token and server has folders for each user.
2. Watchdog library to monitor
3. Don't need to store ALL the files stats, just modified time
