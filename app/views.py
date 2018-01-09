from flask import render_template, request, make_response, abort, jsonify
from app import app
from urllib.request import urlopen
import json,logging 
import paypalrestsdk
paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AQBhEyJ3eHxZjct02KmnC9tuItCtW9W1CLjNvUk-XJJPvQ-CcUEUcYMf_Hf7ladliImxa1o5RXdP7PZf",
  "client_secret": "EHRbkvOjUB1xzWXxwV_Y74Klbz0omO63xin9dWF174e8HEPH9VXQgedxzOSn7K5yn4hrg6knXQr7YmBI" })

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

@app.route('/paymentcs',methods= ['POST', 'GET'])
def paymentcs():
	if request.method == 'GET':
		return render_template('paypal.html')


@app.route('/paymentss')
def paymentss():	
		return render_template('paypalss.html')	

@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:8080/payment/execute",
            "cancel_url": "http://localhost:8080/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "5001.00",
                    "currency": "INR",
                    "quantity": 1}]},
            "amount": {
                "total": "5001.00",
                "currency": "INR"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})

	