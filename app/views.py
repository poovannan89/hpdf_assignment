from flask import render_template
from app import app
from urllib.request import urlopen
import json

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Poovannan'}
	posts = [
		{
			'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
	
	return render_template('index.html',
                           title='Home',
                           user=user,posts=posts)

@app.route('/authors', methods=['GET'])
def authors():
	users_url = 'https://jsonplaceholder.typicode.com/users'
	resp = urlopen(users_url)	
	#return JSON.stringify(resp)
	#resp = urllib.request.urlopen(req)
	resp_data = resp.read().decode('utf-8')
	users_details = json.loads(resp_data)
	all_users = []
	for euser in users_details:
		print(euser['name'])			
		all_users.append(euser['name'])
	return str(all_users)
	
	#return users_details

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
			print('epost id is ',epost['id'])
			if epost['userId'] == uid:
				print('inside id matched is',uid)
				pcnt += 1
		posts_count_dict[uid] = pcnt
	author_post_count = {}
	for uid in posts_count_dict:
		author_post_count[users_dict[uid]] =  posts_count_dict[uid]

	return str(author_post_count)
	











	