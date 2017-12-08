from flask import render_template, request, make_response, abort
from app import app
from urllib.request import urlopen
import json,logging 


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',
                           title='Home')                           

@app.route('/authors', methods=['GET'])
def authors():
	users_url = 'https://jsonplaceholder.typicode.com/users'
	resp = urlopen(users_url)				
	users_details = json.loads(resp.read().decode('utf-8'))
	uname_list = []	
	for euser in users_details:		
		uname_list.append(euser['name'])
	return str(uname_list)

@app.route('/posts', methods=['GET'])
def posts():
	posts_url = 'https://jsonplaceholder.typicode.com/posts'
	resp = urlopen(posts_url)	
	posts_details = json.loads(resp.read().decode('utf-8'))		
	return render_template('posts.html',title='Home',posts=posts_details)


@app.route('/postcount', methods=['GET'])
def postcount():
	users_url = 'https://jsonplaceholder.typicode.com/users'
	users_resp = urlopen(users_url)			
	users_details = json.loads(users_resp.read().decode('utf-8'))
	uid_uname_dict = {}
	for euser in users_details:
		uid_uname_dict[euser['id']] = euser['name'] 
	posts_url = 'https://jsonplaceholder.typicode.com/posts'
	posts_resp = urlopen(posts_url)	
	posts_details = json.loads(posts_resp.read().decode('utf-8'))		
	uid_post_count_dict = {}

	for uid in uid_uname_dict:
		pcnt = 0
		for epost in posts_details:			
			if epost['userId'] == uid:				
				pcnt += 1			
		uid_post_count_dict[uid] = pcnt
	uname_post_count_dict = {}
	for uid in uid_post_count_dict:
		uname_post_count_dict[uid_uname_dict[uid]] =  uid_post_count_dict[uid]

	return render_template('pcount.html',userpcount=uname_post_count_dict)
	
@app.route('/setcookie',methods = ['POST', 'GET'])
def setcookie():
	if request.method == 'POST':
		if 'userName' in request.cookies or 'age' in request.cookies:
			return "Cookie is already set"
		else:
			user = request.form['name']
			age = request.form['age']
			isEmptyFields = False 
			if user == '' or age == '':			
				isEmptyFields = True
				resp = make_response(render_template('readcookie.html',isEmptyFields=isEmptyFields))
				return resp						
			else:
				resp = make_response(render_template('readcookie.html',isEmptyFields=isEmptyFields))
				resp.set_cookie('userName',user)
				resp.set_cookie('age',age)		
				return resp
	if request.method == 'GET':
		return render_template('index.html')	 

@app.route('/getcookies', methods= ['GET'])
def getcookies():
	if request.method == 'GET':	
		cookielist=[]
		cookielist.append(request.cookies.get('userName'))
		cookielist.append(request.cookies.get('age'))
		return str(cookielist)

@app.errorhandler(401)
def page_forbidden(e):
	return render_template('401.html'),401
	
@app.route('/robots.txt', methods= ['GET'])
def deny_request():
	abort(401)

@app.route('/image', methods = ['GET'])
def display_image():
	return render_template('image.html')

@app.route('/input',methods = ['POST', 'GET'])
def input():
	if request.method == 'POST':
		feedback = request.form['feedback']
		if feedback == '':
			return "No feedback received. Please enter again"
		else:
			print("Feedback received is",feedback)
			resp = make_response(render_template('thankyou.html',feedback=feedback))
			return resp
	if request.method == 'GET':
		return render_template('input.html')
			









	