from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Reservation
from customers.models import Customer
from tables.models import Table
import json
from datetime import datetime

def reservation_create(request):
    if request.method == "GET":
        customers = Customer.objects.all()
        tables = Table.objects.filter(is_available=True)
        return render(request, "reservations/reservation_create.html", {
            "customers": customers,
            "tables": tables,
        })
    elif request.method == "POST":
        if request.content_type == "application/json":
            data = json.loads(request.body)
            customer = get_object_or_404(Customer, id=data["customer_id"])
            table = get_object_or_404(Table, id=data["table_id"])
            date = data["date"]
        else:
            customer_id = request.POST.get("customer_id")
            table_id = request.POST.get("table_id")
            date_str = request.POST.get("date")
            customer = get_object_or_404(Customer, id=customer_id)
            table = get_object_or_404(Table, id=table_id)
            date = datetime.strptime(date_str, "%Y-%m-%d").date()

        if Reservation.objects.filter(table=table, date=date, status="confirmed").exists():
            if request.content_type == "application/json":
                return JsonResponse({"error": "Table already reserved"}, status=400)
            else:
                return render(request, "reservations/reservation_create.html", {
                    "error": "Table already reserved",
                    "customers": Customer.objects.all(),
                    "tables": Table.objects.all(),
                })
        
        if Reservation.objects.filter(customer=customer, date=date).exists():
            if request.content_type == "application/json":
                return JsonResponse({"error": "Customer already has a reservation"}, status=400)
            else:
                return render(request, "reservations/reservation_create.html", {
                    "error": "Customer already has a reservation",
                    "customers": Customer.objects.all(),
                    "tables": Table.objects.all(),
                })

        reservation = Reservation.objects.create(customer=customer, table=table, date=date)
        if request.content_type == "application/json":
            return JsonResponse({"id": reservation.id})
        else:
            return redirect("reservation_detail", id=reservation.id)
        
        
def reservation_detail(request, id):
    """GET /reservations/{id}/ - Get details of a specific reservation"""
    reservation = get_object_or_404(Reservation, id=id)
    return render(request, "reservations/reservation_detail.html", {"reservation": reservation})

# Add other missing views if not already implemented
def user_reservations(request, user_id):
    """GET /reservations/user/{user_id}/ - List all reservations for a user"""
    reservations = Reservation.objects.filter(customer_id=user_id)
    return render(request, "reservations/user_reservations.html", {"reservations": reservations})

def reservation_update(request, id):
    """POST /reservations/{id}/ - Update reservation status"""
    reservation = get_object_or_404(Reservation, id=id)
    if request.method == "POST":
        data = json.loads(request.body)
        reservation.status = data["status"]
        reservation.save()
        return JsonResponse({"id": reservation.id, "status": reservation.status})
    return HttpResponse(status=405)  # Method not allowed for GET

def reservation_delete(request, id):
    """DELETE /reservations/{id}/ - Delete a reservation"""
    reservation = get_object_or_404(Reservation, id=id)
    if request.method == "DELETE":
        reservation.delete()
        return HttpResponse(status=204)  # No content
    return HttpResponse(status=405)  # Method not allowed for GET