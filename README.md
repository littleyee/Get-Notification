# NotificationListener


Here is the notification listener program Yiqing started; waits for notification to be posted into the status bar, grabs information, and stores in a SQLite database.

## Current Features:

1. Prompts user to give the app necessary elevated privileges. 
2. Captures notifications posted to the phone from any source.
3. Stores the relevant details (name of the apps that sending notification, timestamp of posting, title and content) about the notification in an SQLite database for future extraction.

## Next Steps:

1. We will need to find some method of extracting the data from the virtual phones to a real device at some point.
2. We will need to start looking into methods for simulating/automating user input to carry out the tests.

