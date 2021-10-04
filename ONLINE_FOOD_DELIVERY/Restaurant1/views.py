from django.shortcuts import render,redirect
# Create your views here.
import filetype
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from Restaurant1.models import restaurant,Category,Item,Order_confirm
from OrderingOnline.models import Item_feedback
# for authenticate page
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/restaurant/r_login/')
def home(request):
    context={}
    order=Order_confirm.objects.filter().order_by('-id')
    context['order']=[]
    print(order)
    try:
        user=restaurant.objects.get(uname=request.session['r_user'])
        if user.status==False:
            context['status']=False
        else:
            context['status']=True
        for x in order:
            try:
                if x.status=='Ordered':
                    rdata=Item.objects.get(rdata=request.session['rest_id'],id=x.Item.id)
                    print(rdata.rdata.all())
                    if x.Item==rdata:
                        print("yes")
                        context['order'].append(x)
                        print(rdata)
            except:
                pass
    except:
          return redirect("/restaurant/r_login")
    return render(request,"Restaurant1/rHome.html",context)

def r_login(request):
    context={}
    if request.method=="POST":
         uname=request.POST['email']
         password=request.POST['password']
         print(uname)
         user1 = auth.authenticate(username=uname,password=password)
         print(user1)
         if user1 is not None:
            print("yes")
            try:
                user=restaurant.objects.get(uname=uname)
                auth.login(request,user1)
                request.session["r_name"]=user.Restaurant_name
                request.session["r_user"]=user.uname
                request.session['r_city']=user.city
                request.session['r_state']=user.state
                request.session['r_address']=user.address
                request.session['r_status']=user.status
                request.session['r_mobile']=user.mobile
                request.session['r_email']=user.email
                request.session['rest_id']=user.id              
                print(user.Restaurant_photo)
                request.session['r_photo']=str(user.Restaurant_photo) 
                return render(request,"Restaurant1/rHome.Html")  
            except:
                    context['not_exist'] ="User is not exist"
                    return render(request,'Restaurant1/r_login.html',context)             
            else:
                context['not_exist'] ="User is not exist"
                return render(request,'Restaurant1/r_login.html',context)
    return render(request,'Restaurant1/r_login.html',context)
        
        
def r_signup(request):
    context={}
    if request.method=="POST":
        restname=request.POST['restname']
        restphoto=''
        uname=request.POST['username']
        email=request.POST['email']
        mobileno=request.POST['mobileno']
        cpassword=request.POST['password']
        password=request.POST['cpassword']
        address=request.POST['address']
        state=request.POST['state']
        city=request.POST['city']
        user_check = auth.authenticate(username=uname)
        if user_check is not None:
                context['error']="Username is already exist please try different username"  
        else:
            if cpassword==password:
                    user1=User.objects.create_user(username=uname,email=email,password=password)
                    user=restaurant(Restaurant_name=restname,uname=uname,email=email,mobile=mobileno,password=cpassword,address=address,state=state,city=city)
                    if user is not None:
                        if "restphoto" in request.FILES:
                            if filetype.is_image(request.FILES['restphoto']):
                                user.Restaurant_photo=request.FILES['restphoto']
                                user1.save()
                                user.save()
                                context['success']=messages="successfully inserted"
                                print(user)
                                print("yes")
                                return render(request,"Restaurant1/r_login.html")
                            else:
                                context['error']="Please enter Image file"  
    return render(request,'Restaurant1/r_register.html',context)


@login_required(login_url='/restaurant/r_login/')
def update(request):
    context={}
    context['error']=''
    context['success']=''
    if request.method=="POST":
       restname=request.POST['restname']
       restphoto=''
       mobileno=request.POST['mobileno']
       address=request.POST['address']
       state=request.POST['state']
       city=request.POST['city']  
       email=request.session['r_email']
       if restaurant.objects.filter(email=email).exists():
           user=restaurant.objects.get(email=email)
           if user is not None:          
               user.Restaurant_name=restname
               user.mobileno=mobileno
               user.state=state
               user.city=city
               user.address=address
               if "restphoto" in request.FILES:
                   if filetype.is_image(request.FILES['restphoto']):
                         user.Restaurant_photo=request.FILES['restphoto']
                         user.save()
                         context['success']=messages="successfully updated"
                         request.session['r_photo']=str(user.Restaurant_photo)
                   else:
                        context['error']="Please enter Image file"
               #  print(request.session['r_photo'])
               request.session["r_name"]=user.Restaurant_name
               request.session["r_user"]=user.uname
               request.session['r_city']=user.city
               request.session['r_state']=user.state
               request.session['r_address']=user.address
               request.session['r_mobile']=user.mobile 
              
               return render(request,'Restaurant1/profile.html',context)
           else:
               return render(request,"/")
    else:
        return render(request,'Restaurant1/profile.html')
    
    
    
# to show profile    
@login_required(login_url='/restaurant/r_login/')  
def profile_show(request):   
    return render(request,"Restaurant1/profile.html")



#account delete
@login_required(login_url='/restaurant/r_login/')
def deleteaccount(request):
    user=User.objects.get(username=request.session['r_user'])
    user_rest=restaurant.objects.get(uname=request.session['r_user'])
    #relation view delete--->check remainning
    Items=Item.objects.filter(rdata=user)
    user_rest.Item_set.clear()
    Items.delete()
    user_rest.delete()
    user.delete()
    return redirect("/")
    

@login_required(login_url='/restaurant/r_login/') 
def logout_rest(request):
    request.session.flush()
    auth.logout(request)
    return HttpResponseRedirect("/restaurant/r_login")

# change password
@login_required(login_url='/restaurant/r_login/') 
def changingpassword(request):
    context={}
    if request.method=='POST':
        current=request.POST['Oldpassword']
        new_pass=request.POST['Newpassword']
        new_verify=request.POST['NewConfirmpassword']
        if(new_pass==new_verify):
            print(True)
            user=User.objects.get(username=request.session["r_user"])
            print(user.password)
            check=check_password(current,user.password)
            # print(check)
            if check==True:
                # print(check)
                user1=restaurant.objects.get(uname=request.session["r_user"])
                user1.password=new_pass
                user1.save()
                request.session["r_pass"]=new_pass
                user.set_password(new_pass)
                user.save()
                print(user.password)
                context["success"]="Successfully change password"
                context['color']="alert-success"
                # print(user.password)         
            else:
                context["fail"]="Incorrect password"
                context['color']="alert-danger"         
    return render(request,"Restaurant1/changingpassword.html",context)


#add item in resaturant
@login_required(login_url='/restaurant/r_login/') 
def add_items(request):
    context={}
    cat=Category.objects.all()
    context['cat']=cat
    if request.method=="POST":
        rdata=restaurant.objects.get(uname=request.session['r_user'])
        print(rdata)
        food=request.POST['foodname']
        category=request.POST.getlist('category',None)
        desc=request.POST['desc']
        price=request.POST['price']
        image=request.FILES['foodphoto']
        if filetype.is_image(image):
            data_item=Item(pname=food,pdesc=desc,price=price,pimage=image,category=category[0])
            data_item.save()
            data_item.rdata.add(rdata)
            context['success']="Successfully added"
        else:
            context['error']="Please enter Image file"           
    return render(request,"Restaurant1/additems.html",context)

@login_required(login_url='/restaurant/r_login/') 
def manageitems(request):
    context={}
    rdata=restaurant.objects.get(id=request.session['rest_id'])
    data=Item.objects.filter(rdata=rdata.id)
    print("dt")
    print(data)
    context['data']=data
    return render(request,"Restaurant1/manage_items.html",context)


#update items
@login_required(login_url='/restaurant/r_login/') 
def itemdetails(request,id):
    context={}
    context['error']=''
    context['success']=''
    data=Item.objects.get(id=id)
    data_category=Category.objects.all()
    print(data_category)
    context['data_category']=data_category
    context['data']=data
    if request.method=='POST':
        data.pname=request.POST['foodname']
        cat=request.POST.getlist('category',None)
        data.category=cat[0]
        data.pdesc=request.POST['desc']
        data.price=request.POST['price']
        data.discount=request.POST['discount']
        if "foodphoto" in request.FILES:
            image=request.FILES['foodphoto']
            if filetype.is_image(image):
                data.pimage=image
            else:
                context['error']="Please enter Image file" 
        data.save()            
        context['success']="Successfully Updated details"             
    return render(request,"Restaurant1/itemdetails.html",context)


@login_required(login_url='/restaurant/r_login/') 
def deleteitems(request,id):
    context={}
    context['success']='successfully deleted'
    data=Item.objects.get(id=id)
    data.delete()  
    return render(request,"Restaurant1/manage_items.html",context)



@login_required(login_url='/restaurant/r_login/') 
def status_update(request):
    context={}
    if request.method=="POST":
        rdata=restaurant.objects.get(uname=request.session['r_user'])
        if rdata.status==False:
            rdata.status=True
            rdata.save()
        elif rdata.status==True:
            rdata.status=False
            print("open to close")
            rdata.save()
        print(rdata.status)
    return redirect("/restaurant/home/")
