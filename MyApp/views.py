from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from django.contrib import auth
from django.contrib.messages import success,error
from django.contrib.auth.forms import User
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.core.mail import send_mail
from GuptaIndustries import settings
from django.db.models import Q
from .models import *
from MyApp.forms import *
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin





class ordersummaryview(View):
    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object': order

            }
            return render(self.request, 'cartk.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an order")
            return redirect("/")

class wishlistview(View):
    def get(self, *args, **kwargs):
        try:
            order=Wishlist.objects.get(user=self.request.user)
            context={
                'object': order

            }
            return render(self.request, 'wishlist.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an wishlist")
            return redirect("/")



# Create your views here.
def email_send(request,email,name):
    subject = 'Thanks '+name+' for registering to our site'
    message = ' it  means a lot to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )


def home(request):

    return render(request,"index.html")

def product(request,cn):
    cat = Category.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('Search')
        data = Product.objects.filter(Q(name__icontains=sr))
    else:
        if(cn=="all"):
            data = Product.objects.all()
        else:
            data=Product.objects.filter(cat__cname=cn)
    return render(request,"menuk.html",{"Data":data,"Cat":cat})

def login(request):
    if(request.method=='POST'):
        uname = request.POST.get('uname')
        pward = request.POST.get('psw')
        user = auth.authenticate(username=uname, password=pward)
        if (user is not None):
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            error(request, "Invalid User")
    return render(request, "login.html")

def signup(request):
    if(request.method=='POST'):
        uname=request.POST.get('uname')
        try:
            match=User.objects.get(username=uname)
            if(match):
                error(request,"Username already exist")
        except:
            uname=request.POST.get('uname')
            fname=request.POST.get('first_name')
            lname=request.POST.get('last_name')
            email=request.POST.get('email')
            pward=request.POST.get('psw')
            cpward=request.POST.get('psw-repeat')
            if (pward == cpward):
                User.objects.create_user(username=uname,
                                         first_name=fname,
                                         last_name=lname,
                                         email=email,
                                         password=pward
                                         )
                success(request, "Account is created")
                email_send(request, email, uname)
                return render(request,"login.html")
            else:
                error(request, "Password and Confirm Password not Matched")
    return render(request,"signup.html")

def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


@login_required
def wishlist(request):
    data=Wishlist.objects.filter(user=request.user)
    return render(request,"wishlist.html",{"Data":data})




@login_required
def cart(request,num):
     item=get_object_or_404(Product, id=num)
     '''created cuz returning tuple'''
     order_item, created = Orderproduct.objects.get_or_create(
         item=item,
         user=request.user,
         ordered=False,)

     order_qs =Order.objects.filter(user=request.user, ordered=False)
     if order_qs.exists():
         order=order_qs[0]
         #check if the order items is in order
         if order.items.filter(item_id=item.id).exists():
             order_item.quantity += 1
             order_item.save()
         else:
             order.items.add(order_item)
     else:
         ordered_date = timezone.now()
         order=Order.objects.create(user=request.user, ordered_date=ordered_date)
         order.items.add(order_item)
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def removesingle(request, num):
    item = get_object_or_404(Product, id=num)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order items is in order
        if order.items.filter(item_id=item.id).exists():
            order_item=Orderproduct.objects.filter(
            item=item,
            user=request.user,
            ordered= False
            ) [0]
            if order_item.quantity >1 :
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.info(request,"This item was updated")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request,"this item was not in your cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request,"you donot have an active order")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def addsingle(request, num):
    item = get_object_or_404(Product, id=num)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order items is in order
        if order.items.filter(item_id=item.id).exists():
            order_item=Orderproduct.objects.filter(
            item=item,
            user=request.user,
            ordered= False
            )[0]
            order_item.quantity += 1
            order_item.save()

            messages.info(request,"This item was updated")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request,"this item was not in your cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request,"you donot have an active order")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def wish(request,num):
    item = get_object_or_404(Product, id=num)
    '''created cuz returning tuple'''
    order_item, created = Wishp.objects.get_or_create(
        items=item,
        user=request.user,
        )

    order_qs = Wishlist.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order items is in order
        if order.wish_items.filter(items_id=item.id).exists():
            messages.info(request, "this item already exsists")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            order.wish_items.add(order_item)
            messages.info(request, "this item has been added")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:

        order = Wishlist.objects.create(user=request.user)
        order.wish_items.add(order_item)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def wremove(request, num):
    item = get_object_or_404(Product, id=num)
    order_qs =  Wishlist.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order items is in order
        if order.wish_items.filter(items_id=item.id).exists():
            order_item=Wishp.objects.filter(
            items=item,
            user=request.user,

            )[0]
            order.wish_items.remove(order_item)


            messages.info(request,"this item was removed")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request,"this item was not in your wishlist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request,"you donot have an active wishlist")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def remove(request, num):
    item = get_object_or_404(Product, id=num)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order items is in order
        if order.items.filter(item_id=item.id).exists():
            order_item=Orderproduct.objects.filter(
            item=item,
            user=request.user,
            ordered= False
            )[0]
            order_item.delete()


            messages.info(request,"this item was removed")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request,"this item was not in your cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request,"you donot have an active order")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




@login_required
def check(request):
    check = Checkout()
    if (request.method == 'GET'):
        check.chname = request.POST.get('name')
        check.mobile = request.POST.get('mobile')
        check.email = request.POST.get('email')
        check.state = request.POST.get('state')
        check.city = request.POST.get('city')
        check.address = request.POST.get('address')
        check.pin = request.POST.get('zip')
        check.comment = request.POST.get('comment')
        check.save()



    return render(request, 'checkout3.html')

    '''data=Cart.objects.filter(cart_user=request.user)

    order = Order.objects.get(user=request.user, ordered=False)
    context = {
        'object': order

    } choice = request.POST.get('choice')
        if (choice == "COD"):
            check.save()
            success(request, "Order Placed")
            return HttpResponseRedirect('/checkout/')
        else:
            success(request, "pay with paypal")
            return HttpResponseRedirect('/payment/process/')'''





def about(request):
     return render(request,'aboutk.html')

def contact(request):
    if(request.method=='POST'):
        c=ContactForm()
        c.name=request.POST.get('name')
        c.email=request.POST.get('email')
        c.message=request.POST.get('message')
        c.save()
    return render(request,"contactk.html")

def ch(request):
    return render(request,'checkout2.html')


def news(request):
    news=newsletter()
    news.email=email=request.POST.get('email')
    news.save()
    email_s(request, email)

def faq(request):
    return render(request,'faq.html')


