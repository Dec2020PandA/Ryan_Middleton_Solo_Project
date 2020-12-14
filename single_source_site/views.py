from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from single_source_site.models import Category, Product, Order
from django.http import HttpResponse
import requests

# Create your views here.
def index (request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')
    # return render (request, "index.html")

def build_quote(request):
    context={
        'products':Product.objects.all()
    }
    return render(request, "quote_builder.html", context)

def get_accessories(request, product_id):
    context={
        'accessories':Product.objects.get(id=product_id).accessories
    }
    return render(request, "accessory_list.html", context)

def display_cart(request):
    if request.method == "POST":
        # Create a new Order
        new_order = Order.objects.create(
            customer_name = request.POST['name_txt'],
            email = request.POST['email_txt']
        )
        print(new_order.customer_name + " email: " + new_order.email + " created a new order.")
        for key in request.POST:
            if "quantity" in key and int(request.POST[key]) > 0:
                # Add the product to the newly created order and store the quantity
                # parse the product id out of the name of the 'number' element from the form 
                product_in_order_id = key.replace("_quantity", "")
                product_in_order = Product.objects.get(id=int(product_in_order_id))
                # value of the 'number' element is the quantity ordered
                # Update the order quantity of this product for the order
                product_in_order.quantity_in_order = request.POST[key]
                product_in_order.save()
                print("adding " + product_in_order.quantity_in_order + " of product id " + product_in_order_id + " to order# " + str(new_order.id))
                # add the product to the order 
                new_order.products.add(product_in_order)

        context = {
            'order' : new_order
        }       
        return render(request, "cart.html", context)
    return redirect("/quote_page")

def get_order(request, order_id):
    context = {
        'order' : Order.objects.get(id=order_id)
    }
    return render(request, "cart.html", context)

def delete_order_product(request, order_id, product_id):
    # Get references to the order and product
    update_order = Order.objects.get(id=order_id)
    delete_product = Product.objects.get(id=product_id)
    #Remove the product fromt he order
    update_order.products.remove(delete_product)

    #Update any/all of the products in the order with  quantities from the form
    for key in request.POST:
        if "quantity" in key and int(request.POST[key]) > 0:
            # parse the product id out of the name of the 'number' element from the form 
            product_in_order_id = key.replace("_quantity", "")
            product_in_order = Product.objects.get(id=int(product_in_order_id))
            # value of the 'number' element is the quantity ordered
            # Update the order quantity of this product for the order
            product_in_order.quantity_in_order = request.POST[key]
            product_in_order.save()

    return redirect("/get_order/"+ str(order_id))

def send_quote(request, order_id):
    if request.method == "POST":
        send_order = Order.objects.get(id=order_id)
        # First update the order with any edits the user may have made
        for key in request.POST:
            if "quantity" in key and int(request.POST[key]) > 0:
                # parse the product id out of the name of the 'number' element from the form 
                product_in_order_id = key.replace("_quantity", "")
                product_in_order = Product.objects.get(id=int(product_in_order_id))
                # value of the 'number' element is the quantity ordered
                # Update the order quantity of this product for the order
                product_in_order.quantity_in_order = request.POST[key]
                product_in_order.save()

        #Build the html string to put into the email
        email_message = render_to_string('email.html',{'order': send_order})
        send_mail(
            'Order# ' + str(send_order.id),
            'Hi ' + send_order.customer_name + ', \nThank-you for your inquiry. Please see your quote below.',
            '',
            [send_order.email, 'ryantmiddleton@gmail.com'],
            fail_silently=False,
            html_message = email_message
        )
    return render (request, "order_success.html", {'order': send_order})
