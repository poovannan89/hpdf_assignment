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
	resp_data = resp.read().decode('utf-8')
	users_details = json.loads(resp_data)
	all_users = []	
	for euser in users_details:
		print(euser['name'])			
		all_users.append(euser['name'])
	return str(all_users)

@app.route('/posts', methods=['GET'])
def posts():
	posts_url = 'https://jsonplaceholder.typicode.com/posts'
	resp = urlopen(posts_url)
	resp_data = resp.read().decode('utf-8')
	posts_details = json.loads(resp_data)		
	return render_template('posts.html',title='Home',posts=posts_details)


@app.route('/count', methods=['GET'])
def count():
	users_url = 'https://jsonplaceholder.typicode.com/users'
	users_resp = urlopen(users_url)		
	user_resp_data = users_resp.read().decode('utf-8')
	users_details = json.loads(user_resp_data)
	users_dict = {}
	for euser in users_details:
		users_dict[euser['id']] = euser['name'] 
	posts_url = 'https://jsonplaceholder.typicode.com/posts'
	posts_resp = urlopen(posts_url)
	post_resp_data = posts_resp.read().decode('utf-8')
	posts_details = json.loads(post_resp_data)		
	posts_count_dict = {}

	for uid in users_dict:
		pcnt = 0
		for epost in posts_details:			
			if epost['userId'] == uid:				
				pcnt += 1			
		posts_count_dict[uid] = pcnt
	author_post_count = {}
	for uid in posts_count_dict:
		author_post_count[users_dict[uid]] =  posts_count_dict[uid]
	return str(author_post_count)
	
@app.route('/setcookie',methods = ['POST', 'GET'])
def setcookie():
	if request.method == 'POST':
		user = request.form['name']
		age = request.form['age']
		resp = make_response(render_template('readcookie.html'))
		resp.set_cookie('userName',user)
		resp.set_cookie('age',age)
		print("Before returning response")
		return resp 

@app.route('/getcookies', methods= ['POST', 'GET'])
def getcookies():
	print("Dict is",request.cookies)	
	cookielist=[]
	cookielist.append(request.cookies.get('userName'))
	cookielist.append(request.cookies.get('age'))
	return str(cookielist)

@app.errorhandler(401)
def page_forbidden(e):
	return render_template('401.html'),401
	
@app.route('/robots.txt', methods= ['POST', 'GET'])
def deny_request():
	abort(401)

@app.route('/image', methods = ['POST', 'GET'])
def display_image():
	return render_template('image.html')

@app.route('/input',methods = ['POST', 'GET'])
def input():
	if request.method == 'POST':
		feedback = request.form['feedback']
		print("Feedback received is",feedback)
		resp = make_response(render_template('thankyou.html',feedback=feedback))
		return resp
	if request.method == 'GET':
		return render_template('input.html')
			









	