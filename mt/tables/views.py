from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Table
from reservations.models import Reservation
import json
from datetime import datetime

def table_list(request):
    """GET /tables/ - List all tables"""
    if request.method == "GET":
        tables = Table.objects.all()
        return render(request, "tables/table_list.html", {"tables": tables})

def table_create(request):
    if request.method == "POST":
        if request.content_type == "application/json":
            data = json.loads(request.body)
            table = Table.objects.create(number=data["number"], seats=data["seats"])
            return JsonResponse({"id": table.id, "number": table.number, "seats": table.seats})
        else:
            number = request.POST.get("number")
            seats = request.POST.get("seats")
            table = Table.objects.create(number=number, seats=seats)
            return redirect("table_list")
        

def available_tables(request):
    """GET /tables/available/ - List available tables for a specific date"""
    if request.method == "GET":
        date_str = request.GET.get("date")  # Expecting date in YYYY-MM-DD format
        if not date_str:
            return render(request, "tables/available_tables.html", {"tables": [], "error": "Date parameter required"})
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return render(request, "tables/available_tables.html", {"tables": [], "error": "Invalid date format (use YYYY-MM-DD)"})
        
        # Filter tables that are available and not reserved on the given date with 'confirmed' status
        reserved_tables = Reservation.objects.filter(date=date, status="confirmed").values_list("table_id", flat=True)
        available_tables = Table.objects.filter(is_available=True).exclude(id__in=reserved_tables)
        
        return render(request, "tables/available_tables.html", {"tables": available_tables, "date": date_str})