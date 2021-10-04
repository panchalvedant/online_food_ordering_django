from django.shortcuts import render,redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import auth
#check password
from django.contrib.auth.hashers import check_password

from OrderingOnline.models import customer,Account_user,alert,Item_feedback
from django.contrib.auth.models import User
from Restaurant1.models import restaurant,Item,cart,OrderProduct,Order_confirm,favourite

from delivery_boy.models import deliveryboy

#PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from OrderingOnline.decoders import unauthenticUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings

from decimal import *
import random
import os
from twilio.rest import Client
def save_otp(mobile):
        account_sid = 'AC75173bb622333cb934fbdb95b68e90ce'
        auth_token = 'd2de390e6a58a0df1b39370a63ed0bb6'
        otp=random.randrange(1000,5000)
        client = Client(account_sid, auth_token)
        number='+91'+mobile
        print(number)
        message = client.messages.create(
                body='your otp is {}'.format(otp),
                from_=+12242231053,
                to=number
        )
        print('otp')
        return otp
    
# ---------------------------------------notifiaction-----------------------------#
@login_required(login_url='/OrderingOnline/login') 
def show_notification(request):
    user=customer.objects.get(id=request.session['customer_id'])
    notes=alert.objects.filter(user=user)
    context={}
    context['notes']=notes
    return render(request,"OrderingOnline/notification.html",context)

@login_required(login_url='/OrderingOnline/login') 
def feedback(request,id):
    if request.method=="POST":
        rate=request.POST['rate']
        user=customer.objects.get(id=request.session['customer_id'])
        notes=alert.objects.get(id=id)
        order=Order_confirm.objects.get(id=notes.notification.id)
        if order:
 
            feedback_data=Item_feedback(userid=user,feedback=rate,Item=order.Item)
            feedback_data.save()
            counted_data=Item_feedback.objects.filter(Item=order.Item).count()
            counted=Item.objects.get(id=order.Item.id)
            if counted_data==1:
                counted.feedback=rate
            else:
                counted.feedback=(float(rate)+float(counted.feedback))/float(counted_data)
            counted.save()
            notes=alert.objects.filter(id=id)
        notes.delete()
        print(rate)
    return redirect("/OrderingOnline/home")  

# ---------------------------------------notifiaction-----------------------------#

def index(request):
    context={}
    rest=restaurant.objects.all().order_by('id')
    context['range']=range(1)
        
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    paginator=Paginator(rest,4)
    try:      
        page = request.GET.get('page', 1)
        rest = paginator.page(page)
    except PageNotAnInteger:
        rest = paginator.page(1)
    except EmptyPage:
        rest = paginator.page(paginator.num_pages)
    context['rest']=rest
    return render(request,"OrderingOnline/index.html",context)

def search(request):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    q=request.GET['dish']
    result=Item.objects.filter(pname=q).order_by('feedback','price') #by name
    result2=restaurant.objects.filter(Restaurant_name=q).order_by('feedback')  #by rest name
    result3=Item.objects.filter(category=q).order_by('feedback','price')  #by category
    result4=restaurant.objects.filter(city=q) #by city
    if result:
        paginator=Paginator(result,3)
        try:      
            page = request.GET.get('page', 1)
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
    if result2:
        paginator=Paginator(result2,3)
        try:      
            page = request.GET.get('page', 1)
            result2 = paginator.page(page)
        except PageNotAnInteger:
            result2 = paginator.page(1)
        except EmptyPage:
            result2 = paginator.page(paginator.num_pages)
    if result3:
        result=result3
        paginator=Paginator(result,3)
        try:      
            page = request.GET.get('page', 1)
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
    if result4:
        result2=result4
        paginator=Paginator(result2,3)
        try:      
            page = request.GET.get('page', 1)
            result2 = paginator.page(page)
        except PageNotAnInteger:
            result2 = paginator.page(1)
        except EmptyPage:
            result2 = paginator.page(paginator.num_pages)
    print(result)
    context['result']=result
    context['result2']=result2
    return render(request,"OrderingOnline/search.html",context)
    

def about(request):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    return render(request,"OrderingOnline/about.html",context)

def login_category(request):
    return render(request,"OrderingOnline/login_category.html")

def register_category(request):
    return render(request,"OrderingOnline/register_category.html")


def login(request):
    context={}
    if request.method=="POST":
       username=request.POST['email']
       password=request.POST['password']
       user = auth.authenticate(username=username,password=password)
       if user is not None:
            if customer.objects.filter(uname=username).exists():
                user1=customer.objects.get(uname=username)
                print("yes")
                if user1 is not None:
                    auth.login(request,user)
                    request.session['customer_id']=user1.id
                    request.session['user_id']=user.id
                    return render(request,"OrderingOnline/index.html")
                else:
                    context['not_exist'] ="User is not exist"
                    return render(request,'OrderingOnline/login.html',context)
            else:
                context['not_exist'] ="User is not exist"
                return render(request,'OrderingOnline/login.html',context)   
       else:
             context['not_exist'] ="User is not exist"
             return render(request,'OrderingOnline/login.html',context)             
    return render(request,'OrderingOnline/login.html',context)
       
    
def signup(request):
    if request.method=="POST":
       uname=request.POST['username']
       email=request.POST['email']
       mobileno=request.POST['mobileno']
       cpassword=request.POST['password']
       password=request.POST['cpassword']
       address=request.POST['address']
       state=request.POST['state']
       city=request.POST['city']
       if cpassword==password:
           user1=auth.authenticate(username=uname,password=password)
           print(user1)
           if user1 is None:
                print("no")
                user1=User.objects.create_user(username=uname,email=email,password=password)
                if user1 is not None:
                    user=customer(uname=uname,email=email,mobile=mobileno,password=cpassword,address=address,state=state,city=city)
                    if user is not None:
                        print("yes")
                        user1.save()
                        user.save()
                        return render(request,"OrderingOnline/login.html")
                    else:
                        return render(request,"OrderingOnline/register.html")
                else:
                    return render(request,'OrderingOnline/register.html')
       else:
          return render(request,'OrderingOnline/register.html')
    return render(request,'OrderingOnline/register.html')
 
    
@login_required(login_url='/OrderingOnline/login')  
def profile_show_customer(request):
    context={}
    try:
        user=customer.objects.get(id=request.session['customer_id'])
        context['user']=customer.objects.get(id=request.session['customer_id'])
        print(request.session['customer_id'])
    except:
        print("not exist")
    # user=customer.objects.get(id=request.session['customer_id'])
    # print(user)  
    return render(request,"OrderingOnline/profile.html",context)


# logout
@login_required(login_url='/OrderingOnline/login') 
def logout_cutomer(request):
    request.session.flush()
    auth.logout(request)
    return HttpResponseRedirect("/OrderingOnline/login")   
    
# update customer profile 
@login_required(login_url='/OrderingOnline/login')
def update(request):
    context={}
    try:
        user=customer.objects.get(id=request.session['customer_id'])
        context['user']=customer.objects.get(id=request.session['customer_id'])
        if request.method=="POST":     
            if restaurant.objects.filter(id=request.session['customer_id']).exists():
                user=customer.objects.get(id=request.session['customer_id'])
                print("yes")
                if user is not None:          
                    user.mobile=request.POST['mobileno']
                    user.state=request.POST['state']
                    user.city=request.POST['city']
                    user.address=request.POST['address']    
                    user.save() 
                    context['success']="successfully updated"   
                    context['user']=customer.objects.get(id=request.session['customer_id'])     
                    return render(request,'OrderingOnline/profile.html',context)
                else:
                    return render(request,"/OrderingOnline/signup")
    except:
        return render(request,'OrderingOnline/profile.html',context)
    return render(request,'OrderingOnline/profile.html',context)
  
  
#delete account
@login_required(login_url='/OrderingOnline/login')
def delete_customer(request):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    user=customer.objects.get(id=request.session['customer_id'])
    context['user']=customer.objects.get(id=request.session['customer_id'])
    context['sure']="Are you sure? Do you want to account delete? "
    if request.method=='POST':
        delete=request.POST['yes']
        if delete is not None:
            cust=customer.objects.get(id=request.session['customer_id'])
            user=User.objects.get(username=cust.uname)
            data=cart.objects.filter(userdata=cust)     
            data.delete()
            user.delete()
            cust.delete()
            request.session.flush()
            auth.logout(request)
            context['sure']=''
            return render(request,"OrderingOnline/index.html") 
                  
    return render(request,'OrderingOnline/index.html',context)

  
#==================================== change password==========================#

@login_required(login_url='/OrderingOnline/login')
def changingpassword_cust(request):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    if request.method=='POST':
        current=request.POST['Oldpassword']
        new_pass=request.POST['Newpassword']
        new_verify=request.POST['NewConfirmpassword']
        if(new_pass==new_verify):
            user=User.objects.get(id=request.session['user_id'])
            check=check_password(current,user.password)
            # print(check)
            if check==True:
                # print(check)
                user1=customer.objects.get(id=request.session['customer_id'])
                user1.password=new_pass
                user1.save()
                user.set_password(new_pass)
                user.save()
                print(user.password)
                context["success"]="Successfully change password"      
            else:
                context["fail"]="Incorrect password"    
        else:
            context['not_same']="password is not same"    
    return render(request,"OrderingOnline/changingpassword.html",context)

 
 
 
 
#  ------------------------------------------dishes show by filter-------------------------------------------#

def show_dish_by_search(request,id):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    Item_data=Item.objects.get(id=id)
    context['Item_data']=Item_data
    rest=Item_data.rdata.get()
    print(Item_data.id,rest.id)
    context['rest_id']=rest.id
    return render(request,"OrderingOnline/show_dish.html",context)   

# -------------------------------------------food dish show------------------------------------#
def show_dish(request,id,rest_id):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    Item_data=Item.objects.get(id=id)
    context['Item_data']=Item_data
    context['rest_id']=rest_id
    return render(request,"OrderingOnline/show_dish.html",context)


# -----------------------------------------------show restaurnat items-------------------------------#

def show_restaurant(request,id):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    items=Item.objects.filter(rdata=id)
    context['items']=items
    context['rest_id']=id
    context['restaurant']=restaurant.objects.get(id=id)
    return render(request,"OrderingOnline/show_restaurant_items.html",context)



# ----------------------------------------------cart related fuctions-------------------#

@login_required(login_url='/OrderingOnline/login')
def cart_show(request):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    cust=customer.objects.get(id=request.session['customer_id'])
    cartuser=cart.objects.filter(userdata=cust)
    context['cart']=cartuser
    price=0.0
    for x in cartuser:
        price+=(float(x.final_amount))
        print(x.Items_data.pname)
    context['price']=price
    return render(request,"OrderingOnline/cart.html",context)


@login_required(login_url='/OrderingOnline/login')
def cart_increase(request,id):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    cust=customer.objects.get(id=request.session['customer_id'])
    cartuser=cart.objects.filter(userdata=cust)
    price=0.0
    if request.method=='POST':
        print(id)
        context['cart_count']=cart.objects.all().count
        cust=customer.objects.get(id=request.session['customer_id'])
        cartuser=cart.objects.filter(userdata=cust)
        context['cart']=cartuser
        cart_item=cart.objects.get(id=id)
        print(cart_item)
        if request.POST['increase']=='+':
            cart_item.quantity=Decimal((request.POST['quantity']))
            cart_item.final_amount=float(cart_item.quantity)*float(cart_item.Items_data.price)+float(cart_item.delivery_charge)                                                                                      
            cart_item.save()
            context['price']=cart_item.final_amount
        return render(request,"OrderingOnline/cart.html",context)
    return render(request,"OrderingOnline/cart.html",context)




   
   
   
#adding data in cart 
@login_required(login_url='/OrderingOnline/login')
def add_to_cart(request,rest_id,id,page):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    Item_data=Item.objects.get(id=id)
    print(Item_data.id)
    cust=customer.objects.get(id=request.session['customer_id'])
    print(cust.id)
    check_data=cart.objects.filter(userdata=cust,Items_data=Item_data)
    print(check_data)
    quantity=1
    if check_data:
        try:
            print(page)
            if page == 'show_restaurant_items':
                messages.info(request,Item_data)
                messages.warning(request, "You have already this dish in cart")
                return HttpResponseRedirect("/OrderingOnline/show_restaurant/{}".format(rest_id))
            if page == 'show_dish':
                messages.info(request,Item_data)
                messages.warning(request, "You have already this dish in cart")
                return HttpResponseRedirect("/OrderingOnline/showdetails/{0},{1}".format(id,rest_id))
        except:
            return HttpResponseRedirect("/OrderingOnline/showdishes/{0}".format(id))
    else:
        final_amount=(float(Item_data.price)-float(Item_data.discount))
        print(final_amount)
        percentage=20
        charge=float(Item_data.price)*(percentage/100)
        if charge<10:
            charge=10
        final_amount=float(quantity)*(final_amount)+charge
        print(final_amount)
        cartItem=cart(userdata=cust,Items_data=Item_data,quantity=quantity,final_amount=final_amount,delivery_charge=charge)
        cartItem.save() 
    # print(cartItem)
    return HttpResponseRedirect("/OrderingOnline/cartdetails")
  



#---------------------------deleteitems from cart and order----------------------------#

@login_required(login_url='/OrderingOnline/login')
def delete_item_from_cart(request,id):
    user=customer.objects.get(id=request.session['customer_id'])
    Item_data=Item.objects.get(id=id)
    data=cart.objects.get(Items_data=Item_data,userdata=user)
    Item_deleted_id=data.return_items_id()
    print(data.Items_data)
    print(data.userdata)
    print(Item_deleted_id)
    data.delete()
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    context['cart_item_success']="successfully deleted"
    cartuser=cart.objects.filter(userdata=user)
    context['cart']=cartuser
    price=0
    for x in cartuser:
        item=Item.objects.get(id=x.Items_data_id)
        item.total=float(item.price)-float(item.discount)
        item.save()
        print(item.total)
        price+=float(item.price)-float(item.discount) 
    context['price']=price 
    return render(request,"OrderingOnline/cart.html",context)



#-------------------------------------------favourite dishes code-----------------------------------------#
def show_favourite_dish(request,id):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    try:
        Item_data=Item.objects.get(id=id)
        context['Item_data']=Item_data
        context['rest_id']=1
        return render(request,"OrderingOnline/show_dish.html",context)
    except:
        return redirect("/OrderingOnline/favourites")
    
def show_favourite(request):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    cust=customer.objects.get(id=request.session['customer_id'])
    favourite_dish=favourite.objects.filter(userdata=cust)
    print(favourite_dish)
    context['favourite']=favourite_dish
    for x in favourite_dish:
        rest=restaurant.objects.get(rest_items=x.Items_data)
        print(rest)
    return render(request,"OrderingOnline/favourite.html",context)
    
def add_to_favourite(request,id,page,rest_id):                   #here page is checking which page in we are
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    Item_data=Item.objects.get(id=id)
    print(Item_data.id)
    cust=customer.objects.get(id=request.session['customer_id'])
    print(cust.id)
    check_data=favourite.objects.filter(userdata=cust,Items_data=Item_data)
    print(check_data)
    if check_data:
        try:
            print(page)
            if page == 'show_restaurant_items':
                messages.info(request,Item_data)
                print("rest")
                messages.warning(request, "You have already this dish in favourite")
                return HttpResponseRedirect("/OrderingOnline/show_restaurant/{}".format(rest_id))
            if page == 'show_dish':
                messages.info(request,Item_data)
                print("dish")
                messages.warning(request, "You have already this dish in favourite")
                return HttpResponseRedirect("/OrderingOnline/showdetails/{0},{1}".format(id,rest_id))
        except:
            return HttpResponseRedirect("/OrderingOnline/showdishes/{0}".format(id))
    else:
        final_amount=(float(Item_data.price)-float(Item_data.discount))
        print(final_amount)
        added_dish=favourite(userdata=cust,Items_data=Item_data,final_amount=final_amount)
        added_dish.save() 
        context['success']="successfully inserted"
    # print(cartItem)
    cartuser=favourite.objects.filter(userdata=cust)
    context['favourite']=cartuser
    return redirect("/OrderingOnline/favourites")

def delete_from_favourite(request,id):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    cust=customer.objects.get(id=request.session['customer_id'])
    deleted_data=favourite.objects.filter(id=id)
    if deleted_data:
        deleted_data.delete()
        context['success']="successfully deleted"
    cartuser=favourite.objects.filter(userdata=cust)
    context['favourite']=cartuser
    return HttpResponseRedirect("/OrderingOnline/favourites")

#-------------------------------------------favourite dishes code-----------------------------------------#



@login_required(login_url='/OrderingOnline/login')
def placeorder(request):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        print("n")
        pass
    user=customer.objects.get(id=request.session['customer_id'])
    # this is for if user go back and not payment and again place same it will show duplicate data
    print("hello")
    order_check=OrderProduct.objects.filter(userdata=request.session['customer_id'])
    if order_check:
        print("hello")
        order_check.delete()
        
    cart_data=cart.objects.filter(userdata=user)
    
    print("chekc_place")
    context['total']=0.0
    context['cart']=cart_data
    context['confirm']="Do You want to order? "
    if request.method=='POST':
        context['confirm']=''
        for x in cart_data:         # for fetching data from order
            # item=Item.objects.get(id=x.Items_data_id)
            delivery_boy=deliveryboy.objects.filter(city=user.city)
            if delivery_boy:
                try:
                    rest=restaurant.objects.get(rest_items=x.Items_data)
                    print(rest.city,user.city)
                    if rest.city==user.city:
                        print("rest")
                        if rest.status==True:
                            print(x.final_amount)
                            order_place=OrderProduct(price=x.final_amount,userdata=user,cartdata=x)
                            order_place.save()
                            order=OrderProduct.objects.filter(userdata=user)
                            print("confirm")
                            context['total']+=float(x.final_amount)
                            print("confirm")
                            context['order']=order
                        else:
                            context['Closed']="True"
                            print("not")
                            return render(request,"OrderingOnline/cart.html",context)
                    else:
                        context['Can_not_order']="True"
                        print("not1")
                        return render(request,"OrderingOnline/cart.html",context)
                except:
                    context['can_not_order']="True"
                    print("not2")
                    return render(request,"OrderingOnline/cart.html",context)
            else:
                context['Occupid']="True"
                return render(request,"OrderingOnline/cart.html",context)
        return render(request,"OrderingOnline/confirmation_order.html",context)
    
    return render(request,"OrderingOnline/cart.html",context)
    

#-----------------------------cancel order------------------------#
@login_required(login_url='/OrderingOnline/login')
def cancelOrder(request,id):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    context['confirm']="confirm"
    order=Order_confirm.objects.get(id=id)
    context['id']=order.id
    context['delete_order']=order
    order=Order_confirm.objects.filter(user=request.session['customer_id'])
    context['order']=order  
    if request.method=='POST':
         cancel=request.POST['yes']
         try:
             order=Order_confirm.objects.get(id=id)
             print(order)
             if order.status=='Ordered':
                 context['canceled']="Your order is canceled. "
                 print(order.delivery_boy_id)
                 delivery_boy=deliveryboy.objects.get(id=order.delivery_boy_id)
                 delivery_boy.status="Available"
                 delivery_boy.save()
                 print(delivery_boy)
                 order.delete()
                 context['confirm']=""
                 orders=Order_confirm.objects.filter(user=request.session['customer_id'])
                 context['order']=orders  
                 return render(request,"OrderingOnline/order.html",context)
             else:
                 context['not_allowed']='Cancelation time is over.'
                 context['confirm']=""
         except:
             context['error']="something going to be wrong." 
    return render(request,"OrderingOnline/order.html",context)

# delete from place order
# @login_required(login_url='/OrderingOnline/login')
# def delete_item_from_order(request,id,order_id):
#     user=customer.objects.get(id=request.session['customer_id'])
#     print("cart-id",id)
#     cartdata=cart.objects.get(id=id)
#     data=OrderProduct.objects.get(id=order_id,cartdata=cartdata,userdata=user.id)
#     data.delete()
#     context={}
#     context['cart_item_success']="successfully deleted"
#     order=OrderProduct.objects.filter(userdata=user)
#     context['order']=order
#     for y in order:
#         price+=float(y.price)
#         print("order-total ",price)
#     context['total']=price
#     return HttpResponseRedirect('/OrderingOnline/placeorder/')



# ============================================payment releted functions========================

@login_required(login_url='/OrderingOnline/login')
def charge_pay(request):
    return render(request,'OrderingOnline/payment.html')


@login_required(login_url='/OrderingOnline/login')
def payment(request):
    context={}
    if request.method=="POST":
        try:
            user=customer.objects.get(id=request.session['customer_id'])
            uname=request.POST['uname']
            account=request.POST['account_no']
            print(uname,account)
            if user.uname==uname:
                try:
                    user_data=customer.objects.get(uname=uname)
                    try:  
                        user=Account_user.objects.get(user_account=user_data)
                        if user:
                            account_user=Account_user.objects.get(account_no=account)
                            print(account_user)
                            otp=save_otp(user_data.mobile)
                            request.session['otp']=otp
                            # print("s1",otp)
                            context['otp']=otp
                        else:
                            context['detail']="Account no is wrong"
                    except Account_user.DoesNotExist:
                        print("no")
                        context['detail']="Account no is wrong"       
                except:
                    context['not_saved']=['Not saved']
            else:
                context['not_register']="Your username is wrong"
        except:
            context['not_register']="Your username is wrong"
    return render(request,'OrderingOnline/payment.html',context)

def saved_account(request):
    context={}
    if request.method=="POST":
        account=request.POST['account_no']
        try:
            customer_data=customer.objects.get(id=request.session['customer_id'])
            if customer_data is not None:
                account_user=Account_user(user_account=customer_data,account_no=account,bank_password=0)
                print(account_user)
                account_user.save()
        except:
            context['not_register']="your are entering non register username"
    return render(request,'OrderingOnline/payment.html',context)

def reset_account(request):
    context={}
    context['reset']="reset"
    if request.method=='POST':
         account=request.POST['reset']
         user=customer.objects.get(id=request.session['customer_id'])
         if user:
             account_user=Account_user.objects.get(user_account=user)
             account_user.account_no=account
             account_user.save()
             conetxt['success']="Successfully changed"
         return render(request,'OrderingOnline/payment.html',context)
    return render(request,'OrderingOnline/payment.html',context)
    
    
def final_payment(request):
    context={}
    user=customer.objects.get(id=request.session['customer_id'])
    cart1=cart.objects.filter(userdata=user)
    if request.method == 'POST':
        otp=request.session['otp']
        print("s",otp," ",request.POST['otp'])
        if otp == int(request.POST['otp']):
            context['successfully']="successfully ordered"
            for x in cart1:
                order=OrderProduct.objects.filter(cartdata=x,userdata=user)
                occupid_deliveryboy=deliveryboy.objects.filter(city=user.city,status="Available").first()
                if occupid_deliveryboy:
                     occupid_deliveryboy.status="Not Available"
                     occupid_deliveryboy.save()
                     waiting_status=False
                     print(waiting_status)
                     context['delivery_boy']=occupid_deliveryboy
                else:
                     waiting_status=True           
                order_final=Order_confirm(user=user,delivery_charge=x.delivery_charge,Item=x.Items_data,price=x.final_amount,quantity=x.quantity,delivery_boy=occupid_deliveryboy,waiting_status=waiting_status)
                order_final.save()
                print(order)
                print(occupid_deliveryboy)
                order.delete()
                x.delete()
                order=Order_confirm.objects.filter(user=request.session['customer_id'])
                context['order']=order
            return render(request,"OrderingOnline/order.html",context)
        else:
            context['resend']="resend"
            for x in cart1:
                print("delete")
                order=OrderProduct.objects.filter(cartdata=x,userdata=user)
                order.delete()
            return render(request,'OrderingOnline/payment.html',context)
    return render(request,'OrderingOnline/payment.html',context)




#----------------------order page current order status:--------------------------------
def orderpage(request):
    context={}
    try:
         context['cart_count']=cart.objects.filter(userdata=request.session['customer_id']).count()
         print(context['cart_count'])
         context['notification_count']=alert.objects.filter(user=request.session['customer_id']).count()
    except:
        pass
    order=Order_confirm.objects.filter(user=request.session['customer_id']).order_by('-id')
    context['order']=order
    return render(request,"OrderingOnline/order.html",context)

# import stripe

# # Create your views here.
    
# # stripe  key
# stripe.api_key = settings.STRIPE_SECRET_KEY

# class product_landing(TemplateView):
#     template_name='OrderingOnline/payment.html'
    
#     def get_context_data(self,**kwargs):
        
#         context=super(product_landing,self).get_context_data(**kwargs)
#         context.update({
#               'STRIPE_PUBLIC_KEY':settings.STRIPE_PUBLIC_KEY
#         })    
#         return context
    
    
    
    
# class CreateCheckoutSessionView(View):
#     def post(self,request,*args,**kwargs):
#         YOUR_DOMAIN = 'http://127.0.0.1:8000'
#         product_id=self.kwargs['pk']
#         product=Item.objects.get(id=product_id)
#         print(product)
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'inr',
#                         'unit_amount': product.price,
#                         'Product_data': {
#                             'name': product.pname,
#                             # 'images': ['https://i.imgur.com/EHyR2nP.png'],
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#         )
#         return JsonResponse({
#             'id': checkout_session.id
#         })
# if __name__ == '__main__':
#     app.run(port=4242)

