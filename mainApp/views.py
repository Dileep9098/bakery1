from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from random import randrange
from django.conf import settings
from django.core.mail import send_mail
from bakery1.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
import razorpay
from .models import *


def home(Request):
    data = Product.objects.all().order_by('id').reverse()[:8]
    return render(Request, "index.html", {'data': data})

# product Page


def product(Request, fl, ct, sp):

    if (fl == 'All' and ct == 'All' and sp == 'All'):
        data = Product.objects.all().order_by('id').reverse()

    elif (fl != 'All' and ct == 'All' and sp == 'All'):
        data = Product.objects.filter(
            flavour=Flavour.objects.get(name=fl)).order_by('id').reverse()
    elif (fl == 'All' and ct != 'All' and sp == 'All'):
        data = Product.objects.filter(
            cakeType=CakeType.objects.get(name=ct)).order_by('id').reverse()

    elif (fl == 'All' and ct == 'All' and sp != 'All'):
        data = Product.objects.filter(
            shape=Shape.objects.get(name=sp)).order_by('id').reverse()

    elif (fl != 'All' and ct != 'All' and sp == 'All'):
        data = Product.objects.filter(flavour=Flavour.objects.get(
            name=fl), cakeType=CakeType.objects.get(name=ct)).order_by('id').reverse()

    elif (fl != 'All' and ct == 'All' and sp != 'All'):
        data = Product.objects.filter(flavour=Flavour.objects.get(
            name=fl), shape=Shape.objects.get(name=sp)).order_by('id').reverse()

    elif (fl == 'All' and ct != 'All' and sp != 'All'):
        data = Product.objects.filter(shape=Shape.objects.get(
            name=sp), cakeType=CakeType.objects.get(name=ct)).order_by('id').reverse()

    else:
        data = Product.objects.filter(shape=Shape.objects.get(
            name=sp), cakeType=CakeType.objects.get(name=ct),).order_by('id').reverse()

    flavour = Flavour.objects.all()
    cakeType = CakeType.objects.all()
    shape = Shape.objects.all()

    return render(Request, 'product.html', {'data': data, 'flavour': flavour, 'cakeType': cakeType, 'shape': shape, 'fl': fl, 'ct': ct, 'sp': sp})


def singleProduct(Request, id):
    data = Product.objects.get(id=id)
    return render(Request, "single-product.html", {'data': data})

# login Page


def loginPage(Request):
    if (Request.method == "POST"):
        username = Request.POST.get("username")
        password = Request.POST.get("password")
        user = authenticate(username=username, password=password)
        if (user is not None):
            login(Request, user)
            if (user.is_superuser):
                return redirect("/admin")
            else:
                return redirect("/profile")
        else:
            messages.error(Request, "Invalid Username or Password!!!")
    return render(Request, "loginPage.html")


# logout
def logoutPage(Request):
    logout(Request)
    return redirect("/login")
# SingUp


def signupPage(Request):
    if (Request.method == "POST"):
        p = Request.POST.get("password")
        cp = Request.POST.get("cpassword")
        if (p == cp):
            b = Buyer()
            b.name = Request.POST.get("name")
            b.username = Request.POST.get("username")
            b.phone = Request.POST.get("phone")
            b.email = Request.POST.get("email")
            user = User(username=b.username, email=b.email)
            if (user):
                user.set_password(p)
                user.save()
                b.save()
                subject = 'Your Account is Created !!! : Team Bakery'
                message = "Hello "+b.name + "🤗🤗" + \
                    "\nThanks to Create a Buyer Account With us \nYou Can Buy Our Letest Product\nTeam Bakery✌️✌️"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [b.email, ]
                send_mail(subject, message, email_from, recipient_list)
                return redirect("/login/")
            else:
                messages.error(Request, "Username Already Taken !!!")

        else:
            messages.error(
                Request, "Password And Confirm Password Doesn't Matched !!!")

    return render(Request, "singup.html")

# profile Page


@login_required(login_url='/login/')
def profilePage(Request):

    user = User.objects.get(username=Request.user)
    if (user.is_superuser):
        return redirect("/admin")
    else:
        buyer = Buyer.objects.get(username=user.username)
        wishlist = Wishlist.objects.filter(user=buyer)
        orders = Checkout.objects.filter(user=buyer)
        print(orders)

    return render(Request, "profile.html", {'user': buyer, 'wishlist': wishlist, 'orders': orders})

# Update Profile


@login_required(login_url='/login/')
def updateProfile(Request):
    user = User.objects.get(username=Request.user)
    if (user.is_superuser):
        return redirect("/admin")
    else:
        buyer = Buyer.objects.get(username=user.username)
        if (Request.method == "POST"):
            buyer.name = Request.POST.get("name")
            buyer.email = Request.POST.get("email")
            buyer.phone = Request.POST.get("phone")
            buyer.addressline1 = Request.POST.get("addressline1")
            buyer.addressline2 = Request.POST.get("addressline2")
            buyer.addressline3 = Request.POST.get("addressline3")
            buyer.pin = Request.POST.get("pin")
            buyer.city = Request.POST.get("city")
            buyer.state = Request.POST.get("state")
            # print(Request.FILES.get("pic"),"\n\n\n\n")
            if (Request.FILES.get("pic")):
                buyer.pic = Request.FILES.get("pic")
            buyer.save()
            return redirect("/profile")

    return render(Request, "update-profile.html", {'user': buyer})


def addToCart(Request, id):
    #   Request.session.flush()
    cart = Request.session.get('cart', None)
    p = Product.objects.get(id=id)
    if (cart is None):
        cart = {str(p.id): {'pid': p.id, 'pic': p.pic1.url, 'name': p.name, 'color': p.color, 'price': p.finalprice,
                            'total': p.finalprice, 'qty': 1, 'cakeTpye': p.cakeType.name, 'flavour': p.flavour.name, 'shape': p.shape.name}}
    else:
        if (str(p.id) in cart):
            item = cart[str(p.id)]
            item['qty'] = item['qty']+1
            item['total'] = item['total']+item['price']
            cart[str(p.id)] = item
        else:
            cart.setdefault(str(p.id), {'pid': p.id, 'pic': p.pic1.url, 'name': p.name, 'color': p.color, 'price': p.finalprice,
                            'total': p.finalprice, 'qty': 1, 'cakeTpye': p.cakeType.name, 'flavour': p.flavour.name, 'shape': p.shape.name, 'weight': p.weight})
    Request.session['cart'] = cart
    Request.session.set_expiry(60*60*24*45)
    return redirect("/cart")

# Cart PAge


def cartPage(Request):
    cart = Request.session.get('cart', None)
    c = []
    total = 0
    shipping = 0
    if (cart is not None):
        for value in cart.values():
            total = total+value['total']
            c.append(value)
        if (total < 1000 and total > 0):
            shipping = 150
        final = total+shipping
    return render(Request, "cart.html", {'cart': c, 'total': total, 'shipping': shipping, 'final': final})

# Delete Cart


def deleteCart(Request, pid):
    cart = Request.session.get('cart', None)
    if (cart):
        for key in cart.keys():
            if (str(pid) == key):
                del cart[key]
                break
        Request.session['cart'] = cart
    return redirect("/cart")

# Update CArt


def updateCart(Request, pid, op):
    cart = Request.session.get('cart', None)
    if (cart):
        for key, value in cart.items():
            if (str(pid) == key):
                if (op == "inc"):
                    value['qty'] = value['qty']+1
                    value['total'] = value['total']+value['price']
                elif (op == 'dec' and value['qty'] > 1):
                    value['qty'] = value['qty']-1
                    value['total'] = value['total']-value['price']
                cart[key] = value
                break
        Request.session['cart'] = cart
    return redirect("/cart")


@login_required(login_url='/login/')
def addToWishlist(Request, pid):
    try:
        user = Buyer.objects.get(username=Request.user.username)
        p = Product.objects.get(id=pid)
        try:
            w = Wishlist.objects.get(user=user, product=p)
        except:
            w = Wishlist()
            w.user = user
            w.product = p
            w.save()
        return redirect("/profile")
    except:
        return redirect("/admin")


@login_required(login_url='/login/')
def deleteWishlist(Request, id):
    cart = Request.session.get('cart', None)
    try:
        user = Buyer.objects.get(username=Request.user.username)
        p = Product.objects.get(id=id)
        try:
            w = Wishlist.objects.get(user=user, product=p)
            w.delete()
        except:
            pass
    except:
        pass
    return redirect("/profile")


@login_required(login_url='/login/')
def checkout(Request):
    try:
        buyer = Buyer.objects.get(username=Request.user)
        cart = Request.session.get('cart', None)
        c = []
        total = 0
        shipping = 0
        if (cart is not None):
            for value in cart.values():
                total = total + value['total']
                c.append(value)
            if (total < 1000 and total > 0):
                shipping = 150
        final = total+shipping
        return render(Request, "checkout.html", {'user': buyer, 'cart': c, 'total': total, 'shipping': shipping, 'final': final})
    except:
        return redirect("/admin")


client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))


@login_required(login_url='/login/')
def orderPage(Request):
    # data = Product.objects.get(id=id)
    # Request.session.flush()
    if (Request.method == "POST"):
        mode = Request.POST.get("mode")
        user = Buyer.objects.get(username=Request.user.username)
        cart = Request.session.get('cart', None)
        if (cart is None):
            return redirect("/cart")
        else:
            check = Checkout()
            check.user = user
            total = 0
            shipping = 0
            for value in cart.values():
                total = total + value['total']
            if (total < 1000 and total > 0):
                shipping = 150
            final = total+shipping
            check.total = total
            check.shipping = shipping
            check.final = final
            check.save()
            for value in cart.values():
                cp = CheckoutProducts()
                cp.checkout = check
                cp.p = Product.objects.get(id=value['pid'])
                cp.qty = value['qty']
                cp.total = value['total']
                cp.save()
            Request.session['cart'] = {}
            subject = 'Your Order has been Placed !!! Team Bakery'
            message = f"Thanks to purchese Product With us \nYou Has been Placed \nNow You Can Tract Your Orders in Profile Page\n------------Product Details----------\nCake Name : {cp.p.name}\nFlavour       : {cp.p.flavour}\nCake Type  : {cp.p.cakeType}\nShape        : {cp.p.shape}\nWeight       : {cp.p.weight} gram\nPrice          : ₹{cp.p.finalprice}\nTeam Bakery ✌️✌️"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            if (mode == "COD"):
                return redirect("/confirmation")
            else:
                orderAmount = check.final*100
                orderCurrency = "INR"
                paymentOrder = client.order.create(
                    dict(amount=orderAmount, currency=orderCurrency, payment_capture=1))
                paymentId = paymentOrder['id']
                check.mode = "Net Banking"
                check.save()
                return render(Request, "pay.html", {
                    "amount": orderAmount,
                    "api_key": RAZORPAY_API_KEY,
                    "order_id": paymentId,
                    "User": user
                })

    else:
        return redirect("/chekout")


@login_required(login_url='/login/')
def paymentSuccess(request, rppid, rpoid, rpsid):
    buyer = Buyer.objects.get(username=request.user)
    check = Checkout.objects.filter(buyer=buyer)
    check = check[::-1]
    check = check[0]
    check.rppid = rppid
    # check.rpoid=rpoid
    # check.rpsid=rpsid
    check.paymentstatus = 1
    check.save()
    return redirect('/confirmation/')


def confirmation(Request):
    return render(Request, "confirmation.html")


def contact(Request):
    if (Request.method == "POST"):
        c = Contact()
        c.name = Request.POST.get("name")
        c.email = Request.POST.get("email")
        c.phone = Request.POST.get("phone")
        c.subject = Request.POST.get("subject")
        c.message = Request.POST.get("message")
        c.save()
        messages.success(
            Request, "Thanks To Shere Your Query With US !! Our Team Will Contact You Soon !!! ")
    return render(Request, "contact.html")


def searchPage(Request):
    search = Request.POST.get('search')
    data = Product.objects.filter(
        Q(name__icontains=search) | Q(color__icontains=search))
    flavour = Flavour.objects.all()
    cakeType = CakeType.objects.all()
    shape = Shape.objects.all()
    return render(Request, 'product.html', {'data': data, 'flavour': flavour, 'cakeType': cakeType, 'shape': shape, 'fl': 'All', 'ct': 'All', 'sp': 'All'})


def forgetUsername(Request):
    if (Request.method == "POST"):
        username = Request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            if (user.is_superuser):
                return redirect("/admin")
            else:
                buyer = Buyer.objects.get(username=username)
                otp = randrange(100000, 999999)
                buyer.otp = otp
                buyer.save()
                subject = 'OTP for Password Reset : Team Bakery'
                message = "OTP for Password Reset is "+str(otp)+"\nTeam Bakery"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [buyer.email, ]
                send_mail(subject, message, email_from, recipient_list)
                Request.session['resetuser'] = username
                return redirect("/forget-otp")
        except:
            messages.error(Request, "Invalid Username!!!!")
    return render(Request, "forget-username.html")


def forgetOTP(Request):
    if (Request.method == "POST"):
        otp = Request.POST.get('otp')
        username = Request.session.get('resetuser', None)
        if (username):
            buyer = Buyer.objects.get(username=username)
            if (int(otp) == buyer.otp):
                return redirect("/forget-password")
            else:
                messages.error(Request, "Invalid OTP!!!!")
        else:
            messages.error(Request, "UnAuthorized!!!!")
    return render(Request, "forget-otp.html")


def forgetPassword(Request):
    if (Request.method == "POST"):
        password = Request.POST.get('password')
        cpassword = Request.POST.get('cpassword')
        username = Request.session.get('resetuser', None)
        if (username):
            if (password == cpassword):
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                return redirect("/login")
            else:
                messages.error(
                    Request, "Password and Confirm Password Doesn't Matched!!!!")
        else:
            messages.error(Request, "UnAuthorized!!!!")
    return render(Request, "forget-password.html")
