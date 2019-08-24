from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.template import Context, Template
from django.core import validators
from django.urls import reverse
from django.shortcuts import render,redirect
from django.db import connection
from django import forms
from myapp.forms import LoginForm
from myapp.models import userinfo,Userdata,Messages,Friends
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template import RequestContext
#from collections import dictfetchall
import smtplib
# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict



def approval(request):
       if (request.session['username']=='girish'):
        alldata=Userdata.objects.raw("select * from myapp_userdata where status='waiting'")
        return render(request, "myapp/approval.html", {'Users':alldata})
       else:
         return HttpResponseRedirect('/myapp/')
def approved(request):
   username = "not logged in"
   if request.method == "POST":
      #Get the posted form
      MyLoginForm = LoginForm(request.POST)
      print ("Entered")
      username=request.POST["username"]
      with connection.cursor() as cursor:
             cursor.execute("update myapp_userdata set status='accepted' where username=%s",[username])
   else: request.method == "POST"
   return render(request, "myapp/loggedin.html",{'username':username})
def sent(request):
#   send_mail('Subject','Text body',settings.EMAIL_HOST_USER,['pgirish1376@gmail.com'],fail_silently=False)
   try:
     server = smtplib.SMTP('smtp.gmail.com', 587)
     #Next, log in to the server
     server.login("girishcse11@gmail.com", "pgirish800")
     #Send the mail
     msg = "\nHello!" # The /n separates the message from the headers
#     server.sendmail("girishcse11@gmail.com", "girish.pappuchetty@onmobile.com", msg)
     print ("Successfully sent email")
   except :
     print ("Error: unable to send email")
   return render(request, "myapp/sent.html", {})
def contact(request):
   return render(request, "myapp/contact.html", {})
def index(request):
   return render(request, "myapp/index.html", {})
@login_required
def form(request):
   return render(request, "myapp/form.html", {})
def adduser(request):
	website=request.POST["website"]
	name=request.POST["name"]
	mail=request.POST["mail"]
	phonenumber=request.POST["phonenumber"]
	userinf=userinfo(website=website,name=name,mail=mail,phonenumber=phonenumber)
#	userinf.save()
	dbuser = userinfo.objects.filter(name = name)
	if not dbuser:
		raise forms.ValidationError("User does not exist in our db!")
		userinf.save()
	res ='Printing all Dreamreal entries in the DB : <br>'
	print ("Hello form is submitted")
	return render(request, "myapp/form.html", {})
def login(request):
   username = "not logged in"
   if request.method == "POST":
      #Get the posted form
      MyLoginForm = LoginForm(request.POST)
      if MyLoginForm.is_valid():
         print ("Entered")
         username = MyLoginForm.cleaned_data['username']
         password = MyLoginForm.cleaned_data['password']
         user=Userdata(username=username,password=password)
         query="select id from myapp_userdata where username=%s and password=%s and status='accepted'"
         params=[username,password]
         with connection.cursor() as cursor:
             cursor.execute(query,params)
             dbuser=cursor.fetchall()
         query1="select id from myapp_userdata where username=%s and password=%s "
         params=[username,password]
         with connection.cursor() as cursor:
             cursor.execute(query1,params)
             dbuser1=cursor.fetchall()
#         dbuser=Userdata.objects.raw("select id from myapp_userdata where username=%s and password=%s",[username,password])
#         print (dbuser.fetchone())
         if len(dbuser)>0:
            print ("USername "+username+" "+"Password "+password)
            user=authenticate(username=username,password=password)
            if(username=='girish'):
              alldata = Userdata.objects.filter(username = username)
              request.session['username'] = username
              request_context = RequestContext(request)
              return HttpResponseRedirect('/myapp/approval',{"User" : alldata})
            else:
              request.session['username'] = username
              print(request.session.get_expiry_age)
              query="select a.image from myapp_userdata a where a.username=%s and a.status='accepted'"
              params=[username]
              with connection.cursor() as cursor:
               cursor.execute(query,params)
               dbuser_pro=cursor.fetchall()
              alldata = Userdata.objects.filter(username = username)
              username="Hi "+username+"\n ,Your login is success"
              htmls='myapp/loggedin.html'
              return HttpResponseRedirect('/myapp/message',{"User" : dbuser_pro})
         elif len(dbuser1)>0:
            username="Hi "+username+"\n ,Waiting for the approval."
            htmls='myapp/faillogin.html'
            return render(request, htmls, {"username" : username})
         else:
            username="Hi "+username+"\n ,Entered Username or Password are wrong. Please try again."
            htmls='myapp/faillogin.html'
            response=render(request, htmls, {"username" : username})

            return response
#      username=dbuser
   else:
        pass
#      MyLoginForm = Loginform()

#   return render(request, htmls, {"username" : username})
def logout(request):
    try:
        del request.session['username']
        return HttpResponseRedirect('/myapp')
    except KeyError:
        pass
        return render(request, 'myapp/index.html',{})
def sformView(request):
   if request.session.has_key('username'):
      username = request.session['username']
      print(request.session.get_expiry_age)
#      request.session.set_expiry(100)
      if(username=='girish'):
        return render(request, 'myapp/approval.html', {"username" : username})
      else:
        return HttpResponseRedirect('/myapp/message')
   else:
      return render(request, 'myapp/index.html', {})
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def signup(request):
   username = "not logged in"
   htmls=""
   if request.method == "POST":
      #Get the posted form
      MyLoginForm = LoginForm(request.POST)
      if MyLoginForm.is_valid():
         username = MyLoginForm.cleaned_data['username']
         password = MyLoginForm.cleaned_data['password']
         user=Userdata(username=username,password=password)
         dbuser=Userdata.objects.filter(username = username)
         if not dbuser:
#            user=User.objects.create_user(username=username,password=password)
            user.save()
            username=username+" Your signup success"
            htmls='myapp/signedup.html'
         else:
            username="Username already exist in our db! Try with other usernmame"
            htmls="myapp/signedup.html"
   else:
#      MyLoginForm = Loginform()
       pass
   return render(request, htmls, {"username" : username})
class Indexmanager():
    def indexmet(request):
        username = "not logged in"
        htmls=""
        if request.method == "POST":
            if(request.POST['log']=='SIGNUP'):
                username = MyLoginForm.cleaned_data['username']
                password = MyLoginForm.cleaned_data['password']
                user=Userdata(username=username,password=password)
                dbuser=Userdata.objects.filter(username = username)
                if not dbuser:
                    user.save()
                    username=username+" Your signup success"
                    htmls='myapp/signedup.html'
                else:
                    username="Username already exist in our db! Try with other usernmame"
                    htmls="myapp/signedup.html"
        else:
            pass


class Messagescls():
	def messagemet(request):
		if (request.session.has_key('username')):
			send_req_response=""
			send_response=""
			from_user_sess=""
			res=""
			id=""
			passwd=""
			usermsgs=""
			waiting=[]
			selmsg="SELECT FRIENDS FROM LEFT"
			Frnds=[]
			Request=[]
			params=[request.session['username']]
			dbuser=Userdata.objects.raw("select * from myapp_userdata where username=%s",params)
			print (dbuser)
			for i in dbuser:
				id=i.id
				passwd=i.password
			print (id)
			query="select a.* from myapp_userdata a where a.username=%s and a.status='accepted'"

			login_user=request.session['username']
			dbuser_pro=Userdata.objects.raw("select a.* from myapp_userdata a where a.username=%s and a.status='accepted'",[request.session['username']])
			cc=0
			for klk in dbuser_pro:
				cc=cc+1
			if (cc==0):
				dbuser_pro=Userdata.objects.raw("select a.* from myapp_userdata a where a.username=%s and  a.status='accepted'",['girish'])
			mesgs=Messages.objects.raw("select * from myapp_messages where to_username=%s or from_username=%s order by id ",[request.session['username'],request.session['username']])
			mesgs_count=Messages.objects.raw("select id,count(*) as count from myapp_messages where to_username=%s or from_username=%s ",[request.session['username'],request.session['username']])
			mcc=0
			for mc in mesgs_count:
			    mcc=mc.count
			for lk in mesgs:
				print (lk.send_time)
			paramsf=[request.session['username'],request.session['username']]

			db_frpro=Userdata.objects.raw("select b.image,a.* from (select id,status,case when requested_to=%s then requested_from  when requested_from=%s and status<>'waiting' then requested_to else 'b' end  as username from myapp_friends where status in ('waiting','accepted')) a, myapp_userdata b where a.username<>'b' and b.username=a.username",paramsf)
#			frnds1="select c.id,image,c.username from myapp_userprofile b , myapp_userdata c where c.username in (select a.username from (select id,status,case when requested_to=%s then requested_from  when requested_from=%s and status<>'waiting' then requested_to else 'b' end  as username from myapp_friends where status in ('waiting','accepted')) a where username<>'b') and b.username_id=c.id"

#			with connection.cursor() as cursor:
#			    cursor.execute(frnds1,paramsf)
#			    db_frpro=dictfetchall(cursor)

			frndss=Friends.objects.raw("select a.* from (select id,status,case when requested_to=%s and status <> 'waiting' then requested_from  when requested_from=%s then requested_to else 'b' end  as username from myapp_friends where status in ('waiting','accepted')) a where username<>'b'",paramsf)
			infofrnds=Friends.objects.raw("select a.* from (select id,status,case when requested_to=%s and status <> 'waiting' then requested_from  when requested_from=%s then requested_to else 'b' end  as username from myapp_friends where status in ('accepted')) a where username<>'b'",paramsf)
			if request.method == "POST":
				if(request.POST['action']=="UPDATE"):
				 print("Yes")
				 img=request.FILES["img"]
				 print (img)
#				 query="insert into myapp_userdata values (%s,%s,%s,%s,%s,%s)"
#				 params=[img,id]
#				 with connection.cursor() as cursor:
#				  cursor.execute(query,params)
				 user=Userdata(id=id,username=request.session['username'],password=passwd,status='accepted',image=img)
				 user.save()
				 dbuser_pro=Userdata.objects.raw("select a.* from myapp_userdata a where a.username=%s and a.status='accepted'",[request.session['username']])
				elif(request.POST['action']=="SEND"):
				  from_user=request.session['username']
				  to_user=request.POST["username"]
				  message=request.POST["message"]
				  paramsf=[request.session['username'],request.session['username']]
				  fruser=Friends.objects.raw("select id,case when requested_to=%s then requested_from  when requested_from=%s then requested_to end  as username from myapp_friends ",paramsf)
				  c=0
				  for kk in fruser:
				   if (kk.username==to_user):
				    c=c+1
				  if c>0:
				    mesg=Messages(from_username=from_user,to_username=to_user,message=message)
				    mesg.save()
				    send_response="Message sent"
				    mesgs=Messages.objects.raw("select * from myapp_messages where to_username=%s or from_username=%s order by id ",[request.session['username'],request.session['username']])
				    mesgs_count=Messages.objects.raw("select id,count(*) as count from myapp_messages where to_username=%s or from_username=%s ",[request.session['username'],request.session['username']])
				    mcc=0
				    for mc in mesgs_count:
				        mcc=mc.count

				  else:
				    send_response="Please select Friend from the list"
				elif(request.POST['action']=="GO"):
				  search=request.POST["search"]
				  a="%"+search+"%"
				  if " " in search:
				   bb=search.split(" ")
				   b="%"+bb[0]+"%"
				   c="%"+bb[1]+"%"
				   params=[a,b,c,request.session['username']]
				   res=Userdata.objects.raw("select * from myapp_userdata where username LIKE %s or username LIKE %s or username LIKE %s and status='accepted' and username <> %s ;",params)
				  else:
				   res=Userdata.objects.raw("select * from myapp_userdata where username LIKE %s and status='accepted' and username <> %s ;",[a,request.session['username']])
				elif(request.POST['action']=="RESPONSE_ACCEPT"):
				 requested_to=request.session['username']
				 requested_from=request.POST["res_usname"]
				 query="update myapp_friends set status='accepted' where requested_to=%s and requested_from=%s and status='waiting'"
				 params=[requested_to,requested_from]
				 with connection.cursor() as cursor:
				  cursor.execute(query,params)
				elif(request.POST['action']=="RESPONSE_REJECT"):
				 requested_to=request.session['username']
				 requested_from=request.POST["res_usname"]
				 query="update myapp_friends set status='rejected' where requested_to=%s and requested_from=%s and status='waiting'"
				 params=[requested_to,requested_from]
				 with connection.cursor() as cursor:
				  cursor.execute(query,params)
				elif(request.POST['action']=="SEND_REQUEST"):
					requested_to=request.POST["req_usname"]
					requested_from=request.session['username']
					print (requested_to+"and"+requested_from)
					send_req=Friends(requested_from=requested_from,requested_to=requested_to)
					send_req.save()
					send_req_response="Friend request has sent to "+requested_to
				elif(request.POST['action']=="USER_CHAT") :
				    from_user_sess=request.POST["from_usname"]
				    login_user=request.session['username']
				    selmsg=""
#				    params=[to_user,from_user]
#				    usermsgs=Messages.objects.raw("select * from myapp_messages where to_username=%s and from_username=%s",params)
				elif (request.POST['action']=="REPLY") :
				    from_user_sess=request.POST["username"]
				    from_user=request.session['username']
				    to_user=request.POST["username"]
				    message=request.POST["message"]
				    paramsf=[request.session['username'],request.session['username']]
				    fruser=Friends.objects.raw("select id,case when requested_to=%s then requested_from  when requested_from=%s then requested_to end  as username from myapp_friends ",paramsf)
				    c=0
				    for kk in fruser:
				        if (kk.username==to_user):
				            c=c+1
				    if c>0:
				        mesg=Messages(from_username=from_user,to_username=to_user,message=message)
				        mesg.save()
				        send_response="Message sent"
				        mesgs=Messages.objects.raw("select * from myapp_messages where to_username=%s or from_username=%s order by id ",[request.session['username'],request.session['username']])
				        mesgs_count=Messages.objects.raw("select id,count(*) as count from myapp_messages where to_username=%s or from_username=%s ",[request.session['username'],request.session['username']])
				        mcc=0
				        for mc in mesgs_count:
				            mcc=mc.count
				    else:
				        send_response="Please select Friend from the list"
				elif(request.POST['action'] == "DELETEMESG"):
				    to_user=request.POST['username1']
				    if(request.POST["username"] == request.session['username']):
				        from_user_sess=request.POST["username1"]
				    else:
				        from_user_sess=request.POST["username"]
				    mesgs_count=Messages.objects.raw("select id,count(*) as count from myapp_messages where to_username=%s or from_username=%s ",[request.session['username'],request.session['username']])
				    mcc=0
				    for mc in mesgs_count:
				        mcc=mc.count
				    from_user=request.POST["username"]
				    message=request.POST["message"]
				    idd=request.POST["idd"]
				    query="delete from myapp_messages where id=%s"
				    params=[idd]
				    print (params)
				    with connection.cursor() as cursor:
				        cursor.execute(query,params)
				    mesgs=Messages.objects.raw("select * from myapp_messages where to_username=%s or from_username=%s order by id ",[request.session['username'],request.session['username']])
				    mesgs_count=Messages.objects.raw("select id,count(*) as count from myapp_messages where to_username=%s or from_username=%s ",[request.session['username'],request.session['username']])
				    mcc=0
				    for mc in mesgs_count:
				        mcc=mc.count


			if(res!=""):
				waiting=[]
				Frnds=[]
				Request=[]
				print (res)
				print(db_frpro)
				for i in res:
				 c=0
				 k=0
				 for j in frndss:
				    print (j.username)
				    if((i.username==j.username) and  str(j.status)=='accepted'):
				     c=c+1
				    elif(i.username==j.username and str(j.status)=='waiting'):
				     k=k+1
				 if(c>0):
				  Frnds.append(i.username)
				  print ("Friends "+i.username)
				 elif(k>0):
				  waiting.append(i.username)
				  print ("waiting" + i.username)
				 else:
				  Request.append(i.username)
				  print ("Request "+i.username)
				print (waiting)
			return render(request,'myapp/message.html',{'from_user_ses':from_user_sess,'User':dbuser_pro,'selmsgs':selmsg,'mesg_count':mcc,'usermesgs':usermsgs,'messages':mesgs,'friends':db_frpro,'user':login_user,'sr':send_response,'response':res,'waiting':waiting,'Request':Request,'Frnds':Frnds,'send_req_response':send_req_response,'Infofrnds':infofrnds})
		else:
			return HttpResponseRedirect('/myapp/')
	def sendmessage(request):
		if (request.session.has_key('username')):
		 if request.method == "POST":
		   from_user=request.session['username']
#		   print ("Yes")
		   to_user=request.POST["username"]
		   message=request.POST["message"]
		   mesg=Messages(from_username=from_user,to_username=to_user,message=message)
		   mesg.save()
		   return render(request,'myapp/message.html')
#		   return redirect('/myapp/message')
	def delmesgs(request):
		if (request.method=="POST"):
		  to_user=request.session['username']
		  from_user_sess=request.POST["username"]
		  from_user=request.POST["username"]
		  message=request.POST["message"]
#		  print(request.POST["message"])
#		  idd=request.POST["id"]
		  idd=request.POST["idd"]
		  query="delete from myapp_messages where id=%s"
		  params=[idd]
		  print (params)
		  with connection.cursor() as cursor:
		    cursor.execute(query,params)
		  print("YEs")
		return redirect('/myapp/message',{"from_user_se":from_user})
	def frndreq(request):
		if request.method == "POST":
		 print (request.session['username'])
		 search=request.POST["search"]
		 a="%"+search+"%"
		 if " " in search:
		   print ("yes")
		   bb=search.split(" ")
		   b="%"+bb[0]+"%"
		   c="%"+bb[1]+"%"
		   params=[a,b,c]
		   res=Userdata.objects.raw("select * from myapp_userdata where username LIKE %s or username LIKE %s or username LIKE %s and status='accepted' ;",params)
#		   query="select * from myapp_userdata where username LIKE %s or username LIKE %s or username LIKE %s and status='accepted' ;"
#		   params=[a,b,c]
		 else:
		  res=Userdata.objects.raw("select * from myapp_userdata where username LIKE %s and status='accepted' ;",[a])
#		  query="select * from myapp_userdata where username LIKE %s and status='accepted' ;"
#		  params=[a]
#		 with connection.cursor() as cursor:
#                    cursor.execute(query,params)
#                    rows = cursor.fetchall()
		 print ("yes")
		 for k in res:
		  print (k.username)
		 print (res)
		 print (search)
		 return redirect('/myapp/message',{'results':res})
#		 return render(request,'myapp/message.html',{'results':res})
#		 return HttpResponseRedirect(reverse('/myapp/message'))
