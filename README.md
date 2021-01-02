# PexipHomework
Dropbox assignment for Pexip

# Structure
* Client
    * client.py - main file to set up client app, contains functions for each event, i.e. create, delete, modify and move
    * observer.py - object to listen for changes and run the event functions defined in client
    * dispatcher.py - given the information of change in the file system, efficiently extract change and dispatch to server

* Server
    * server.py - network interface to receive the data
    * dropboxService.py - service to efficiently translate data to changes in the file system

* Tests - run unit tests for client & server functionality

# TODO
1. Compress data
2. coroutines/threads

# Issues
1. Unit tests use very short timer so sometimes too quick on move/modification and observer does not pick up on it when scanning files, 
have not experienced this in manual testing since using a longer delay
2. Possibility user deletes file mid scan is an issue which may be easy to fix

# Possible improvements
1. User model, each client has an ID/JSON web token and server has folders for each user.
2. Watchdog library to monitor
3. Don't need to store ALL the files stats, just modified time
4. More extensive testing i.e. Event handler and dispatcher
5. Better use of pythons package system, using __init__ etc, not sure how they work, easier in Java/C# with packages/namespaces

# Log
2 hours to figure out design and OS, pathlib libraries
3 hours to implement system with bonus 1
2 hours to unit test and refactor