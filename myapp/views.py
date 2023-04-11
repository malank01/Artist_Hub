from django.shortcuts import render,redirect
from  .models import User,Artist,Contacts,Transaction,Booking
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

def validate_email(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
		}
	return JsonResponse(data)

def initiate_payment(request):
   
		user=User.objects.get(email=request.session['email'])
		amount = int(request.POST['amount'])
		transaction = Transaction.objects.create(made_by=user, amount=amount)
		transaction.save()
		merchant_key = settings.PAYTM_SECRET_KEY
		params = (
        	('MID', settings.PAYTM_MERCHANT_ID),
        	('ORDER_ID', str(transaction.order_id)),
        	('CUST_ID', str(transaction.made_by.email)),
        	('TXN_AMOUNT', str(transaction.amount)),
        	('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        	('WEBSITE', settings.PAYTM_WEBSITE),
        	# ('EMAIL', request.user.email),
        	# ('MOBILE_N0', '9911223388'),
        	('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        	('CALLBACK_URL', 'http://localhost:8000/callback/'),
        	# ('PAYMENT_MODE_ONLY', 'NO'),
    	)

		paytm_params = dict(params)
		checksum = generate_checksum(paytm_params, merchant_key)

		transaction.checksum = checksum
		transaction.save()
		books=Booking.objects.filter(user=user,payment_status=False)
		for i in books:
			i.payment_status=True
			i.save()

		paytm_params['CHECKSUMHASH'] = checksum
		print('SENT: ', checksum)
		return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)

def index(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="customer":
			return render(request,'index.html')
		else:
			return render(request,'artist_index.html')
	except:	
		return render (request,'index.html')

def contact(request):
	if request.method=="POST":
		contact_customer=User.objects.get(email=request.session['email'])
		Contacts.objects.create(
			contact_customer=contact_customer,
			contact_name=request.POST['contact_name'],
			contact_email=request.POST['contact_email'],
			contact_subject=request.POST['contact_subject'],
			contact_message=request.POST['contact_message']

			)
		msg='Send Massege Successfully...'
		return render (request,'contact.html',{'msg':msg})
	else:
		return render(request,'contact.html')

def instructor(request):
	
	artists=Artist.objects.filter(artist_type="")
	
	return render (request,'instructor.html',{'artists':artists})

def course(request):
	return render(request,'course.html')

def blog_single(request,pk):
	artist=Artist.objects.get(pk=pk)
	return render (request,'blog-single.html',{'artist':artist})

def mybook(request):
	user=User.objects.get(email=request.session['email'])
	books=Booking.objects.filter(user=user,payment_status=True)
	return render (request,'mybook.html',{'books':books})	

def instructor_details(request,pk):
	artist=Artist.objects.get(pk=pk)
	artists=Artist.objects.filter()	
	return render(request,'instructor-details.html',{'artist':artist})

def booking(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	books=Booking.objects.filter(user=user,payment_status=False)	
	for i in books:
		net_price= net_price + i.artist_price
	return render(request,'mybooking.html',{'books':books,'net_price':net_price})

def book(request,pk):
	artist=Artist.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Booking.objects.create(
				user=user,
				artist=artist,
				artist_price=artist.artist_price,
				date=date,
				)
	books=Booking.objects.filter(user=user,payment_status=False)
	return redirect('booking')

def login(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=="customer":
					request.session['email']=user.email
					return render (request,'index.html')
				else:
					if user.permission==False:
						msg='your Registration Under Process..'
						return render(request,'login.html',{'msg':msg})
					else:
						request.session['email']=user.email
						return render(request,'artist_index.html')
			else:
				msg="password is invalid...."
				return render(request,'login.html',{'msg':msg})	

		except Exception as e:
			print(e)
			msg="email is dose not registered..."
			return render(request,'login.html',{'msg':msg})	

	else:
		return render(request,'login.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="email already registered..."
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(

					name=request.POST['name'],
					email=request.POST['email'],
					password=request.POST['password'],
					usertype=request.POST['usertype'],
				)
				msg="signup successfully..."
				return render(request,'login.html',{'msg':msg})	
			else:
				msg="password &confirm password dose not match..."
				return render (request,'signup.html',{'msg':msg})
	else:	
		return render(request,'signup.html')				
					
def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=="customer":
		if request.method=="POST":
			if user.password==request.POST['password']:
				if request.POST['newpassword']==request.POST['cnewpassword']:
					user.password=request.POST['newpassword']
					user.save()
					return redirect('logout')
				else:
					msg='new password & confirm new password dose not match... '
					return render(request,'change_password.html',{'msg':msg})
			else:
				msg='Old password dose not match...'
				return render(request,'change_password.html',{'msg':msg})
		else:
			return render(request,'change_password.html')
	else:
		if request.method=="POST":
			if user.password==request.POST['password']:
				if request.POST['newpassword']==request.POST['cnewpassword']:
					user.password=request.POST['newpassword']
					user.save()
					return redirect('logout')
				else:
					msg='new password & confirm new password dose not match... '
					return render(request,'artist-change-password.html',{'msg':msg})
			else:
				msg='Old password dose not match...'
				return render(request,'artist-change-password.html',{'msg':msg})
		else:
			return render(request,'artist-change-password.html')

def logout(request):
	try:
		del request.session['email']
		return render(request,'login.html')
	except:
		return render(request,'login.html')	

def artist_index(request):
	contacts_customer=Contacts.objects.filter()
	return render (request,'artist_index.html',{'contacts_customer':contacts_customer})

def singer(request):
	try:
		artist=Artist.objects.filter(artist_type="singer")
		return render(request,'singer.html',{'artist':artist})
	except:
		return render (request,'course.html')

def standup(request):
	try:
		artist=Artist.objects.filter(artist_type="standup")
		return render(request,'standup.html',{'artist':artist})
	except:
		return render (request,'course.html')

def dancer(request):
	try:
		artist=Artist.objects.filter(artist_type="dancer")
		return render (request,'dancer.html',{'artist':artist})
	except:
		return render(request,'dancer.html')

def influencer(request):
	try:
		artist=Artist.objects.filter(artist_type="influencer")
		return render (request,'influencer.html',{'artist':artist})
	except:
		return render(request,'influencer.html')

def photographer(request):
	try:
		artist=Artist.objects.filter(artist_type="photographer")
		return render (request,'photographer.html',{'artist':artist})
	except:
		return render (request,'photographer.html')	

def writer(request):
	try:
		artist=Artist.objects.filter(artist_type="writer")
		return render (request,'writer.html',{'artist':artist})
	except:
		return render(request,'writer.html')

def artist_details(request):
	if request.method=="POST":
		artist_artist=User.objects.get(email=request.session['email'])

		Artist.objects.create(
				artist_artist=artist_artist,
				artist_name=request.POST['artist_name'],
				artist_price=request.POST['artist_price'],
				artist_desc=request.POST['artist_desc'],
				artist_type=request.POST['artist_type'],
				artist_pic=request.FILES['artist_pic'],
			)
		msg='Add Details successfully...'
		return render (request,'artist-details.html',{'msg':msg})
	else:
		return render(request,'artist-details.html')
		
def artist_profile(request):
	artist_artist=User.objects.get(email=request.session['email'])
	#print(artist_artist.name)
	artist=Artist.objects.filter(artist_artist=artist_artist)
	return render(request,'artist_profile.html',{'artist':artist})

def odered(request):
		artist=Artist.objects.all()
		user=User.objects.filter()
		books=Booking.objects.filter()
		return render (request,'odered.html',{'books':books,'user':user,'artist':artist})

def artist_edit_details(request,pk):
	artist=Artist.objects.get(pk=pk)
	if request.method=="POST":
		artist.artist_name=request.POST['artist_name']
		artist.artist_desc=request.POST['artist_desc']
		artist.artist_price=int(request.POST['artist_price'])
		artist.artist_type=request.POST['artist_type']
		try:
			artist.artist_pic=request.FILES['artist_pic']
		except:
			pass
		artist.save()
		msg='Edit Details successfully..'
		return render (request,'artist-edit-details.html',{'artist':artist,'msg':msg})		
	else:
		return render (request,'artist-edit-details.html',{'artist':artist})

def contact_me(request):
	artist=Artist.objects.all()
	contacts_customer=Contacts.objects.filter()
	return render (request,'contact_me.html',{'contacts_customer':contacts_customer,'artist':artist})
