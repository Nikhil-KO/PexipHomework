from clientTest import run as clientTests
from serverTests import run as serverTests

if __name__ == "__main__":
    # These tests ensure the observer picks up on the required file system changes
    clientTests()
    # These tests ensure the functionality of the dropboxService is met
    serverTests()