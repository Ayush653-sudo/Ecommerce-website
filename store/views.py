from django.shortcuts import render,redirect,HttpResponseRedirect
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
from decimal import Decimal
#from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from store.middlewares.auth import auth_middleware

# Create your views here.
def index(request):
    if request.method=='GET':
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
       
        crds = Category.get_all_catrgories()
        gategoryid=request.GET.get('categorie')
        if gategoryid:
            prds = Product.get_all_products_by_gategory_id(gategoryid)
        else:
            prds = Product.get_all_products()
        data={}
        data['products']= prds
        data['categories'] = crds
        print(request.session.get('email'))

        return render(request,'index.html', data)

    else:
        product = request.POST.get('product')
        cart=request.session.get('cart')
        remove= request.POST.get('remove')
        if cart:
            qu=cart.get(product)
            if qu:
                if remove:
                    if qu<=1:
                        cart.pop(product)
                    else:
                        cart[product]=qu-1

                else:
                    cart[product]=qu+1
            else:
                cart[product]=1

        else:
            cart={}
            cart[product]=1
        request.session['cart']=cart
        return redirect('jjh')

def signup(request):
    if request.method =='GET':
        return render(request,'signup.html')
    else:
        dat = request.POST
        first_name = dat.get('first_name')
        last_name = dat.get('last_name')
        phone = dat.get('phone')
        email = dat.get('email')
        password = dat.get('password')
        errorm = None
        if len(first_name)<4:
            errorm="FILL CORRECTLY GREATER THAN 4!!!"

        elif len(password)<8:
            errorm="MAKE PASSWORD STORNG!!!"

        elif len(phone) < 10:
            errorm = "ENTER PHONE NO CORRECTLY "


        if errorm==None :

            customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
            customer.password=make_password(customer.password)
            customer.save()
            return redirect('jjh')
        else:
            return render(request,'signup.html',{ 'error': errorm})


def login(request):
    return_url=None
    if request.method=='GET':
        return_url=request.GET.get('return_url')
        return render(request,'login.html')
    else:
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=Customer.get_customer_by_email(email)
        errorm=None
        if customer:
            f=check_password(password,customer.password)
            if f:
                request.session['customer_id']=customer.id
                request.session['email'] = customer.email
               
                return redirect('jjh')
            else:
                errorm = 'Email or password invalid!!!'
        else:
            errorm = 'Email or password invalid!!!'
        return render(request,'login.html', {'error': errorm})

def logout(request):
    request.session.clear()
    return render(request,'login.html')

def cart(request):
    if request.method=='GET':
        ids=list(request.session.get('cart').keys())
        prod=Product.get_product_by_id(ids)
        print(prod)
        return render(request,'cart.html',{'products': prod})

def checkout(request):
    if request.method=='POST':
        address= request.POST.get('address')
        phone= request.POST.get('phone')
        email=request.POST.get('email')
        pincode=request.POST.get('pincode')
        online=request.POST.get('online')
        cart=request.session.get('cart')
        products=Product.get_product_by_id(list(cart.keys()))
        for product in products:
            order=Order.objects.create(email=email,
                        product=product,
                        price=product.price,
                        address=address,
                        phone=phone,
                        pincode=pincode,
                        quantity=cart.get(str(product.id)))
            order.save()
       
       
        subject='Thanks for shopping from our website'
        message='Hi user your order is prepared we hope! you will enjoy it  Our website provide so many facility to users!!!'
                  
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(subject,message, email_from , recipient_list)
        request.session['cart'] = {}
        if online:
            uv=request.POST.get('uv')
            print(uv)
            return render(request,'process_payment.html',{'uv':uv})
        
        
        return render(request,'cart.html')



def ordered(request):
    
    email=request.session.get('email')
    orders= Order.objects.filter(email=email)
    return render(request,'orders.html',{'orders':orders})














