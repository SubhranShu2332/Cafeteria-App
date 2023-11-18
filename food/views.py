from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.cache import never_cache
from food.models import Food,Category,Type,Order,Feedback
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date,timedelta
from django.core.mail import send_mail
from django.core.paginator import Paginator
import razorpay
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime



from Cafeteria.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
# Create your views here.

def all_foods(request):
    
        foods=Food.objects.all()

        ratings={}
        for food in foods:
            print(food.id)
            feedbacks=Feedback.objects.filter(food=food)
            sum=0
            flen=len(feedbacks)
            food.noRating=flen
            for f in feedbacks:
                sum+=f.rating
            if flen!=0:
                # print(sum/flen)
                food.rating=sum/flen
                ratings[food.id]=sum/flen
                print(food.rating)
            else:
                food.rating=0
                ratings[food]=0

        page=Paginator(foods,5)
        page_number=request.GET.get("page")
        foods_final=page.get_page(page_number)
        total_pages=foods_final.paginator.num_pages

        types=Type.objects.all()
        categories=Category.objects.all().order_by('id')
        cart={}
        if request.session.get("cart_items"):
                cart=request.session.get("cart_items")
        # if request.session.get('cart_items'):
        #     if request.session.get('cart_items').get(str(id)):
        #         quantity=request.session.get('cart_items')[str(id)]
        # print(cart['4'])

        content={
            "foods":foods_final,
            "categories":categories,
            "types":types,
            "cart":cart,
            "no":len(cart),
            "page_list":[n+1 for n in range(total_pages)]
        }
        return render(request,'food/foods.html',content)
    
    

def category_food(request,cid):
    foods=Food.objects.filter(category=cid)

    ratings={}
    for food in foods:
            print(food.id)
            feedbacks=Feedback.objects.filter(food=food)
            sum=0
            flen=len(feedbacks)
            food.noRating=flen
            for f in feedbacks:
                sum+=f.rating
            if flen!=0:
                # print(sum/flen)
                food.rating=sum/flen
                ratings[food.id]=sum/flen
                print(food.rating)
            else:
                food.rating=0
                ratings[food]=0

    types=Type.objects.all()
    categories=Category.objects.all().order_by('category')

    #Cart
    cart={}
    if request.session.get("cart_items"):
        cart=request.session.get("cart_items")

    context={
        "foods":foods,
        "categories":categories,
        "types":types,
        "no":len(cart)
    }
    return render(request,'food/foods.html',context)

def type_food(request,tid):
    foods=Food.objects.filter(type=tid)

    ratings={}
    for food in foods:
            print(food.id)
            feedbacks=Feedback.objects.filter(food=food)
            sum=0
            flen=len(feedbacks)
            food.noRating=flen
            for f in feedbacks:
                sum+=f.rating
            if flen!=0:
                # print(sum/flen)
                food.rating=sum/flen
                ratings[food.id]=sum/flen
                print(food.rating)
            else:
                food.rating=0
                ratings[food]=0
    
    types=Type.objects.all()
    categories=Category.objects.all().order_by('category')

    #cart
    cart={}
    if request.session.get("cart_items"):
        cart=request.session.get("cart_items")
    context={
        "foods":foods,
        "types":types,
        "categories":categories,
        "no":len(cart)
    }
    return render(request,'food/foods.html',context)

def food_details(request,fid):
    food=get_object_or_404(Food,id=fid)
    context={
        "food":food,
    }
    return render(request,'food/food.html',context)

def add_to_cart(request):
    if request.method == "POST":
        print("y")
        name=(request.POST.get("foodname"))
        food_id =(request.POST.get("foodid"))
        quantity=int(request.POST.get("quantity"))
        foods=Food.objects.all()

        ratings={}
        for food in foods:
            print(food.id)
            feedbacks=Feedback.objects.filter(food=food)
            sum=0
            flen=len(feedbacks)
            food.noRating=flen
            for f in feedbacks:
                sum+=f.rating
            if flen!=0:
                # print(sum/flen)
                food.rating=sum/flen
                ratings[food.id]=sum/flen
                print(food.rating)
            else:
                food.rating=0
                ratings[food]=0
        
        types=Type.objects.all()
        categories=Category.objects.all().order_by('id')
        cart={}
        if request.session.get("cart_items"):
                cart=request.session.get("cart_items")
        cart_items={}
        if request.session.get("cart_items"):
            cart_items=request.session.get("cart_items")
        
        cart_items[food_id]=quantity
        request.session["cart_items"]=cart_items
        print(cart_items)
        context={
            "name":name,
            "quantity":quantity,
            "foods":foods,
            "categories":categories,
            "types":types,
            "cart":cart,
            "no":len(cart_items)
        }
    return render(request,'food/foods.html',context)
    # redirect("all_foods")

def get_cart_details(request):
    total_price=0
    cart_details=[]
    if not request.session.get('cart_items'):
        return cart_details,total_price
    cart_items=request.session.get('cart_items')
    foods=Food.objects.filter(id__in=list(cart_items.keys()))
    total_price=0
    
    for food in foods:
        quantity=int(cart_items[str(food.id)])
        price=quantity*food.price
        total_price+=price
        cart_details.append({
            "id":food.id,
            "name":food.name,
            "quantity":quantity,
            "image":food.image,
            "price":price,
            "counter":food.counter
        })
    return cart_details,total_price

@never_cache
def cart(request):
    cart_details,total_price=get_cart_details(request)

    #cart
    cart={}
    if request.session.get("cart_items"):
        cart=request.session.get("cart_items")
    content={
        "foods":cart_details,
        "total_price":total_price,
        "no":len(cart)
    }
    return render(request,'food/cart.html',content)

def remove_from_cart(request,id):
    cart_items=request.session.get("cart_items")
    del cart_items[str(id)]
    request.session["cart_items"]=cart_items
    return redirect("cart")

def update_cart(request):
    if request.method == "POST":
        print("y")
        food_id =(request.POST.get("foodid"))
        quantity=int(request.POST.get("quantity"))
        cart_items={}
        if request.session.get("cart_items"):
            cart_items=request.session.get("cart_items")
        cart_items[food_id]=quantity
        request.session["cart_items"]=cart_items
        print(cart_items)
    return redirect("cart")

def check_out(request):
    if request.user.is_authenticated:
        cart_details,total_price=get_cart_details(request)
        DATA = {
                "amount": total_price*100,
                "currency": "INR",
                "receipt": "receipt#1",
            }
        payment_order=client.order.create(data=DATA)
        payment_id=payment_order['id']
        content={
            "foods":cart_details,
            "total_price":total_price,
            "order_id":payment_id,
            "api_key":RAZORPAY_API_KEY
        }
        return render(request,'food/checkout.html',content)
    else:
        a={
            "flag":1
        }
        return render(request,'user/signin.html',a)

@csrf_exempt
def place_order(request):
    
        cart_details,total_price=get_cart_details(request)
        user=request.user
        payment_mode=request.POST.get("payment_mode")
        payment_mode="ONLINE"
        orders=[]
        for food in cart_details:
            order=Order(
                food=Food.objects.get(id=food['id']),
                user=user,
                quantity=food['quantity'],
                price=food['price'],
                counter=food['counter'],
                Payment_method=payment_mode
            )
            orders.append(order)
        Order.objects.bulk_create(orders)
        
        #Date
        d = datetime.now()
        # 👇️ convert string to datetime object
        dt = datetime.strftime(d, '%Y-%m-%d %H:%M:%S')
        da=datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

        print(dt)  # 👉️ 2023-11-24 09:30:00.000123

        result = da + timedelta(minutes=29)
        print(result)  
                
        mail_context={
            "username":request.user.first_name+" "+request.user.last_name,
            "foods":cart_details,
            "delivery_date":result,
            "total_price":total_price
        }
        subject = "Order is placed successfully"
        # body = f"Your Order is placed successfully. Amount {total_price}. Delivery Address: {address}"
        html_message = render_to_string('food/mail_template.html',mail_context)
        plain_message = strip_tags(html_message)
        to = [request.user.email, ]
        from_email = settings.EMAIL_HOST_USER
        # send_mail(subject=subject, message=body, from_email=from_email, recipient_list=to,fail_silently=False)
        send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=to,fail_silently=False, html_message=html_message)
        request.session['cart_items']={}
        return redirect("orders")
    
def orders(request):
    orders=Order.objects.filter(user=request.user).order_by('-id')
    content={
        "orders":orders
    }
    return render(request,'food/orders.html',content)

def search(request):
     if request.method == "POST":
        search=request.POST.get('search')
        foods=Food.objects.filter(name__icontains=search)
        print(foods)
        
        types=Type.objects.all()
        categories=Category.objects.all().order_by('id')

        ratings={}
        for food in foods:
            print(food.id)
            feedbacks=Feedback.objects.filter(food=food)
            sum=0
            flen=len(feedbacks)
            food.noRating=flen
            for f in feedbacks:
                sum+=f.rating
            if flen!=0:
                # print(sum/flen)
                food.rating=sum/flen
                ratings[food.id]=sum/flen
                print(food.rating)
            else:
                food.rating=0
                ratings[food]=0
          
            context={
               "foods":foods,
               "categories":categories,
               "types":types,
            }
            return render(request,'food/foods.html',context)
     
def add_feedback(request):
    if request.method == "POST":
        user = request.user
        food_id=request.POST.get("food_id")
        food=Food.objects.get(id=food_id)
        rating = request.POST.get("rating")
        comment=request.POST.get("comment")
        feedback=None
        try:
            feedback=Feedback.objects.get(user=user,food=food)
        except:
            print("Comment Not available")
        if feedback is None:
            feedback=Feedback()
            feedback.user=user
            feedback.food=food
        feedback.rating=rating
        feedback.comment=comment
        feedback.save()
        return redirect("orders")
