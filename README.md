# PexipHomework
Dropbox assignment for Pexip

The only 'high level' level libraries used was Flask and requests and the libraries that come with them. They are given in the requirements.txt file.

Much of Flasks functionality was not used, but because I was comfortable using it allowed to quicker prototyping than using the built in http module.

All the required base functionality (1.1 and 1.2) has been implement and partially unit tested. The Observer for client and dropboxService for server was unit tested, the other features were deemed simple enough to manually review. 

Bonus 1 was implemented as files/folders are only uploaded if change occurs, so the same data is sent across.

The final bonus of partial file was attempted but not fully implemented. I have the code to hash and maintain the partial register for each file, 
but to implement the full soft rolling checksum outlined by https://rsync.samba.org/tech_report/node3.html would have taken more time and I didn't want to spend too long on it.

I really wanted the solution to be cross platform so using built in libraries for the client (and requests). The basic overview is os.stat is used to maintain a hash map of file and folder {id's -> (stat, path)}, at intervals the Observer object searches for new, change or deleted files/folders and these changes translated to instructions by the EventHandler and then are dispatched to the server.

# File Structure
* Client
    * client.py - main file to set up client app and run it, simple
    * eventHandler.py - object takes the path to changes and either formats them and if required loads data to then dispatch.
    * observer.py - object to listen for changes and run the event functions defined in the given eventHandler object
    * dispatcher.py - routes data to server
    * partialTransfer.py - Attempt at maintaining hash of file by chunks so only the modified chunks have to be uploaded.
    
* Server
    * server.py - flask network interface to receive the data
    * dropboxService.py - service to translate instructions and or data to changes in the server file system

* testrunner.py - run unit tests for client & server functionality, the tests can also be run individually 

# Run system
Requires Python 3+.

Need to be in the directory of <code>client/</code> and <code>server/</code> respectively.

    python client.py <dir to watch> <optional url to server>
    e.g. python client.py listen/

    python server.py <dir to store>
    e.g. python server.py server_data/

# Asumptions
1. The initial folder is empty, it is any easy change to copy the init folder on launch/empty.
2. Compressing files not required/provide speed up
3. Not worried about system endianness
4. Flask server address is edited in code
5. Server url can be given in command line but default is local host on port 5000

# Tests
The units tests ensure the Observer detects the required changes and server is able to recreate them on file system using the dropboxService, the link between them was tested manually multiple times using a variety of folders and files and file types.

# Issues
1. Unit tests use very short timer so sometimes too quick on move/modification and observer does not pick up on it when scanning files, 
have not experienced this in manual testing since its using a longer delay.
2. Possibility user deletes file mid scan is an issue which may be easy to fix, i.e. system detects file modified and as the process is reading to upload changes the user deletes files.
This can be rerouted to a delete signal.
3. Some slightly odd behavior with windows and folder capitalization, not functionality breaking
4. This is a possible issue, may need to consider big endianness when dealing with files being transferred

# Possible improvements
1. User model, each client has an ID/JSON web token and server has folders for each user.
3. Don't need to store ALL the files stats, just modified time is used
4. More extensive testing i.e. Event handler and dispatcher, API testing using postman automated testing?
5. Better use of pythons package system, using __init__ etc, not sure how they work, easier in Java/C# with packages/namespaces

# Time Log
2 hours to figure out design and OS, pathlib libraries

4 hours to implement system with bonus 1

2 hours to unit test and refactor

# Final remarks
The task was daunting at first but as soon I as figured out the <code>os.stats()</code> function and that file systems give folders/file unique id's it was quite fun to implement and if I wasn't restricted by time would very much like to implement the rsync algorithm.