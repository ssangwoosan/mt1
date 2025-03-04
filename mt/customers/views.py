from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Customer
import json

def customer_list(request):
    if request.method == "GET":
        customers = Customer.objects.all()
        return render(request, "customers/customer_list.html", {"customers": customers})
    elif request.method == "POST":
        # Handle JSON API request
        if request.content_type == "application/json":
            data = json.loads(request.body)
            customer = Customer.objects.create(name=data["name"], phone=data["phone"])
            return JsonResponse({"id": customer.id, "name": customer.name, "phone": customer.phone})
        # Handle HTML form submission
        else:
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            customer = Customer.objects.create(name=name, phone=phone)
            return redirect("customer_list")
        

def customer_detail(request, id):
    customer = get_object_or_404(Customer, id=id)
    return render(request, "customers/customer_detail.html", {"customer": customer})