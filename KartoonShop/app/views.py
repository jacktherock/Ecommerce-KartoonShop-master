from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerProfileForm, SignupForm


""" this fetchs all products from Product and filter them by top wear, bottom wear, mobiles and renders on homepage by line """
class ProductView(View):
    def get(self, request):  # GET request does
        totalitem = 0
        topwears = Product.objects.filter(category="TW")  # Product->TW
        bottomwears = Product.objects.filter(category="BW")  # Product->BW
        mobiles = Product.objects.filter(category="M")  # Product->M

        """when customer is login then only customer can see cart and no. of items in cart"""
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        context = {
            "topwears": topwears,
            "bottomwears": bottomwears,
            "mobiles": mobiles,
            "totalitem": totalitem,
        }
        return render(request, "home.html", context)


""" when customer clicks on particular product then all the detailed info of products will render"""
class ProductDetailView(View):
    def get(self, request, pk):  # GET request does
        totalitem = 0

        """ gets all the products present in Product by their primary key i.e 'id' """
        product = Product.objects.get(pk=pk)

        """ when user is anonymous then on all products 'Add to Cart' will render """
        item_already_in_cart = False

        """ item_already_in_cart: when user is authenticated then if user already added a product in cart then again when user go to that product then 'Go to Cart' btn will render instead of 'Add to Cart' """
        """ totalitem: when customer is login then only customer can see cart and no. of items in cart """
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)
            ).exists()
            totalitem = len(Cart.objects.filter(user=request.user))

        context = {
            "product": product,
            "item_already_in_cart": item_already_in_cart,
            "totalitem": totalitem,
        }
        return render(request, "productdetail.html", context)


""" when user is logged in then only user can add products to cart """
@login_required
def add_to_cart(request):
    user = request.user  # logged in user
    product_id = request.GET.get(
        "prod_id"
    )  # 'prod_id' is html 'id' gets product id from js
    """ from the product_id user can add that product in cart """
    product = Product.objects.get(id=product_id)
    Cart(
        user=user, product=product
    ).save()  # logged in user can saves that product in cart
    messages.success(request, "Item Added In Cart Successfully ! ")
    return redirect("/cart")



""" when user is logged in then only user can view products in cart and add increase or decrease no. of that item , also by increse in no. of item price of item also increase and vice versa """

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user  # logged in user

        """ from Cart filter user by and only show that specific user products added in cart """
        cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount = 70.0

        """ List Comprihension- 
        fetched all carts of all users. Fetched 1st product will put in 2nd-'p' and then it matches that 1st product is present in logged-in user if YES then it stores that value in 1st-'p' then it run same for all products then all the fetched products_stored_in_cart==logged-in_user it stores that products in 'cart_product' """

        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)

        """ if products are available in cart then only do for loop for each product and as user increase items no. then product price will increse and vice versa else render empty-cart """

        if cart_product:
            for p in cart_product:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(
                request,
                "addtocart.html",
                {"carts": cart, "amount": amount, "totalamount": totalamount},
            )
        else:
            return render(request, "emptycart.html")


""" increase quantity of particular item no. which is available in cart of that specific user - ajax js used for this """
@login_required
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]  #'prod_id' is html 'id' gets product id from ajax js

        """ from Cart gets that product_id and only logged-in user are right then increase quantity and save in db """

        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount

        data = {
            "quantity": c.quantity,
            "amount": amount,
            "totalamount": amount + shipping_amount,
        }
        return JsonResponse(data)


""" decrease quantity of particular item no. which is available in cart of that specific user - ajax js used for this """
@login_required
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"] #'prod_id' is html 'id' gets product id from ajax js

        """ from Cart gets that product_id and only logged-in user are right then decrease quantity and save in db """

        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount

        data = {
            "quantity": c.quantity,
            "amount": amount,
            "totalamount": amount + shipping_amount,
        }
        return JsonResponse(data)


""" remove particular item which is available in cart of that specific user - ajax js used for this """
@login_required
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]

        """ from Cart gets that product_id and only logged-in user are right then remove product from cart """

        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount

        data = {"amount": amount, "totalamount": amount + shipping_amount}
        return JsonResponse(data)


""" buy_now function not used instead of this integrated PayPal payment system """
@login_required
def buy_now(request):
    return render(request, "buynow.html")


""" when any customer logins then firstly renders a blank address form """
@method_decorator(login_required, name="dispatch")
class ProfileView(View):

    """ if request is GET then only view address form """
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "profile.html", {"form": form, "active": "btn-primary"})

    """ if customer fills create new address form and submit then POST request will happen then only all the data in fields save in db """
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            zipcode = form.cleaned_data["zipcode"]
            state = form.cleaned_data["state"]
            country = form.cleaned_data["country"]
            reg = Customer(
                user=usr,
                name=name,
                locality=locality,
                city=city,
                zipcode=zipcode,
                state=state,
                country=country,
            )
            reg.save()
            messages.success(request, "New Address Created Successfully!!")
        return render(request, "profile.html", {"form": form, "active": "btn-primary"})


""" when specific customer logins then all that customer address's will fetches from db & render """
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "address.html", {"add": add, "active": "btn-primary"})


""" when specific customer logins then all that customer orders will fetches from db & render """
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, "orders.html", {"order_placed": op})


""" from Product mobiles are categorized by their brand and price """
def mobile(request, data=None):

    """ if None data is pass then all mobiles will render else if customer clicks on that category then only that categorized mobiles will render and that prices mobiles will render"""
    if data == None:
        mobiles = Product.objects.filter(category="M")
    elif (
        data == "Vivo"
        or data == "Oppo"
        or data == "Realme"
        or data == "Xiaomi"
        or data == "Iphone"
    ):
        """ from Product categorize mobiles by their brand """
        mobiles = Product.objects.filter(category="M").filter(brand=data)

        """ from Product categorize mobiles if their price is less than or equal to 13000 """
    elif data == "below":
        mobiles = Product.objects.filter(category="M").filter(discounted_price__lte=13000)

        """ from Product categorize mobiles by their price is greater than or equal to 13000 """
    elif data == "above":
        mobiles = Product.objects.filter(category="M").filter(discounted_price__gt=13000)
    context = {"mobiles": mobiles}
    return render(request, "mobile.html", context)


""" New Customer registration form """
class Signup(View):
    """ if GET request happen then blank SignUpform renders """
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})

    """ if user fills all the required fields and submit then POST request happen and all the data will save in db """
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login !")
            # return redirect('accounts/login/')
        return render(request, "signup.html", {"form": form})


""" when customer wants to buy a product in the cart the customer places order then checkout page will render all the product info and customers address will render """
@login_required
def checkout(request):
    user = request.user # specific logged-in user
    add = Customer.objects.filter(user=user) # specific logged-in users address
    cart_items = Cart.objects.filter(user=user) # specific logged-in users cart products

    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(
        request,
        "checkout.html",
        {"add": add, "totalamount": totalamount, "cart_items": cart_items},
    )


""" when order is placed by customer and payment is done by PayPal payment method then it redirects to '/orders/' """
@login_required
def payment_done(request):
    user = request.user  # specific logged-in user
    custid = request.GET.get("custid") # specific logged-in user's customer id gets using js
    """if custid matches with Customer id in model that value stores in 'customer' """
    customer = Customer.objects.get(id=custid) 
    cart = Cart.objects.filter(user=user)  # specific logged-in users cart products

    """ when order is placed by user and user dones payment method then all the products in cart are deleted and all the products in cart shifts in OrderPlaced model and redirect to '/order/' """
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


""" user can delete address """
@login_required
def deleteAddress(request, id):
    if request.method == "POST":
        pi = Customer.objects.get(pk=id)
        pi.delete()
        return redirect("/address/")

def Contact(request):
    return render(request, 'contact.html')
