# THANK YOU DAVID
#### Video Demo:  <To be added soon>
#### Live Demo:  https://thankyou-david.onrender.com/
#### Description:
CS50 Final Proyect.

The app is made using Flask, Python, SQLite, JavaScript, HTML, CSS, and Bootstrap. It is designed for CS50 students currently enrolled or those who have completed CS50's course.

Users are required to select one of David's humorous images and then compose a thank-you message. These images were created in Photoshop using photomanipulation techniques, with many being inspired by actual CS50 homework assignments like Fiftyville, as well as references to Harry Potter and The Office from some lectures

To submit a message, users must be logged in. If a user doesn't have an account, they can register by providing a username and password. The password is encrypted using the 'bcrypt' library.
 
The SQL database is used to store USERS login data and to store MESSAGES written by users. The messages table is associated with the users' table through the user id.

The /messages route contains all messages submitted by users and has a limit of 20 messages per page. If there are more messages, additional pages are created to display older messages.

There is also a /myprofile route where users can view the messages they have submitted and delete them if needed. This feature was added in case users were testing the app, allowing them to delete test messages or to rectify any regrets about a message.

There is also a /myprofile route where the user can see the messages he/she has submited, and can also delete the message/s. This was added incase the user was just testing the app, so the test message can be deleted. OR if the user regretted his/her message. 

Finally, users have the option to log out.

