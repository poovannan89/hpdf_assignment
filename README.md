# hpdf_assignment Week1

Started this week1 task by creating virtual environment for flask and installed flask related packages using pip install. 
Then, created the project directory and implemented the tasks provided for week1. 
Followed the below tutorial for setting up flask in virtual environment : 
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world-legacy

#Functionalities Task1 : simply displays Hello world - 
My name. Index page has username and age text box which is used for setting cookies. 

Task2 : 
a) http://localhost:8080/authors URL end point fetches the list of authors from 
https://jsonplaceholder.typicode.com/users Returned the list of authors as list converted to string while returning response. 
b) http://localhost:8080/posts URL end point fetches list of posts from 
https://jsonplaceholder.typicode.com/posts Displayed the output in table format. 
c) http://localhost:8080/postcount URL end point provides number of posts each other has made. 
Used list and dict data structures and displayed output as table.

Task3 : http://localhost:8080/setcookie URL end point is used to set cookie with inputs as username and age. 
Form inputs are validated and cookie is set. If cookie is already set, it is also notified in response for the request.

Task4 : http://localhost:8080/getcookies URL end point is used to retrieve the list of cookies which is already set.

Task5 : http://localhost:8080/robots.txt URL end point denies user's request and custom message of 404 is displayed. 
Error handler and abort are used.

Task6 : http://localhost:8080/image URL end point displays a image which is stored in static directory of project.

Task7 : http://localhost:8080/input URL end point gets user input (feedback) and displays in stdout and shows the user feedback. 
User input is validated if it is empty or not.

