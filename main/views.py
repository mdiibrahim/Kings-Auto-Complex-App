from decimal import Decimal
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Sum, Max, Q, F
from datetime import datetime, date, timedelta
from .models import Item, Car, Service, Sale, Dues, Stuff, Salary, Cost, Stock, Jobcard, CustomerRequest, Diagnosis, IssueDemand, IssueDemandEngineer
from .forms import SaleForm
from django.contrib import messages
from django.core.paginator import Paginator
from . import globals
from django.utils.dateparse import parse_date
current_month = datetime.now().month
current_year = datetime.now().year


def index(response):
    globals.is_logged_in = False
    return render(response, "main/base.html", {})


def home(response):
    if globals.is_logged_in:
        return render(response, "main/home.html", {})
    return redirect("index")


def check_login(request):
    username = "admin"
    password = "123456"

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        if username_input == username and password_input == password:
            globals.is_logged_in = True
            return redirect('sale')
        else:
            messages.error(request, 'Invalid username or password.')

    # Redirect to the login page if verification fails
    return redirect("index")
# # Service


def service(response):
    if globals.is_logged_in:
        return render(response, "main/create-service.html", {})
    else:
        return redirect("index")


def create_service(request):
    if globals.is_logged_in:
        if request.method == 'POST':
            service_name = request.POST.get('service_name')
            # service_cost = request.POST.get('service_cost')
            service_charge = request.POST.get('service_charge')

            service = Service(service_name=service_name,
                              service_charge=service_charge)
            service.save()

            # # Insert a new record into the Stock model with qty=0
            # stock = Stock(service=service, qty=0)
            # stock.save()

        return redirect('service_list')

    return redirect("index")


def service_list(request):
    if globals.is_logged_in:
        services = Service.objects.all()
        return render(request, 'main/service_list.html', {'services': services})

    return redirect("index")


def edit_service(request, service_id):
    if globals.is_logged_in:
        service = get_object_or_404(Service, service_id=service_id)

        return render(request, 'main/edit-service.html', {'service': service})

    return redirect("index")


def update_service(request, service_id):
    if globals.is_logged_in:
        service = get_object_or_404(Service, service_id=service_id)

        if request.method == 'POST':
            service_name = request.POST.get('service_name')
            # service_cost = request.POST.get('service_cost')
            service_charge = request.POST.get('service_charge')

            service.service_name = service_name
            # service.service_cost = service_cost
            service.service_charge = service_charge
            service.save()

            return redirect('service_list')

        return render(request, 'edit_service.html', {'service': service})

    return redirect("index")


def delete_service(request, service_id):
    if globals.is_logged_in:
        service = get_object_or_404(Service, service_id=service_id)

        service.delete()

        return redirect('service_list')

    return redirect("index")


def item(response):
    if globals.is_logged_in:
        return render(response, "main/create-item.html", {})
    else:
        return redirect("index")


def create_item(request):
    if globals.is_logged_in:
        if request.method == 'POST':
            item_name = request.POST.get('service_name')
            item_cost = request.POST.get('service_cost')
            item_charge = request.POST.get('service_charge')

            item = Item(item_name=item_name,
                        item_cost=item_cost,
                        item_charge=item_charge)
            item.save()

            # Insert a new record into the Stock model with qty=0
            stock = Stock(item=item, qty=0)
            stock.save()

        return redirect('item_list')

    return redirect("index")


def item_list(request):
    if globals.is_logged_in:
        items = Item.objects.all()
        return render(request, 'main/item_list.html', {'items': items})

    return redirect("index")


def edit_item(request, item_id):
    if globals.is_logged_in:
        item = get_object_or_404(Item, item_id=item_id)

        return render(request, 'main/edit-item.html', {'item': item})

    return redirect("index")


def update_item(request, item_id):
    if globals.is_logged_in:
        item = get_object_or_404(Item, item_id=item_id)

        if request.method == 'POST':
            item_name = request.POST.get('item_name')
            item_cost = request.POST.get('item_cost')
            item_charge = request.POST.get('item_charge')

            item.item_name = item_name
            item.item_cost = item_cost
            item.item_charge = item_charge
            item.save()

            return redirect('item_list')

        return render(request, 'edit_item.html', {'item': item})

    return redirect("index")


def delete_item(request, item_id):
    if globals.is_logged_in:
        item = get_object_or_404(Item, item_id=item_id)

        item.delete()

        return redirect('item_list')

    return redirect("index")

# # Car


def car(response):
    return render(response, "main/create-car.html", {})


def create_car(request):
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        car_color = request.POST.get('car_color')

        car = Car(car_name=car_name,
                  car_color=car_color)
        car.save()

    return redirect('car_list')


def car_list(request):
    cars = Car.objects.all()
    return render(request, 'main/car_list.html', {'cars': cars})


def edit_car(request, car_id):
    car = get_object_or_404(Car, car_id=car_id)

    return render(request, 'main/edit-car.html', {'car': car})


def update_car(request, car_id):
    car = get_object_or_404(Car, car_id=car_id)

    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        car_color = request.POST.get('car_color')

        car.car_name = car_name
        car.car_color = car_color
        car.save()

        return redirect('car_list')

    return render(request, 'edit_car.html', {'car': car})


def delete_car(request, car_id):
    car = get_object_or_404(Car, car_id=car_id)

    car.delete()

    return redirect('car_list')


# # Stuff
def stuff(response):
    if globals.is_logged_in:
        return render(response, "main/create-stuff.html", {})

    return redirect("index")


def create_stuff(request):
    if globals.is_logged_in:
        if request.method == 'POST':
            stuff_name = request.POST.get('stuff_name')
            join_date = request.POST.get('join_date')
            stuff_father = request.POST.get('stuff_father')
            stuff_nid = request.POST.get('stuff_nid')
            stuff_address = request.POST.get('stuff_address')
            stuff_mobile = request.POST.get('stuff_mobile')
            stuff_salary = request.POST.get('stuff_salary')
            duty_days = request.POST.get('duty_days')

            stuff = Stuff(stuff_name=stuff_name,
                          join_date=join_date,
                          stuff_father=stuff_father,
                          stuff_nid=stuff_nid,
                          stuff_address=stuff_address,
                          stuff_mobile=stuff_mobile,
                          stuff_salary=stuff_salary, duty_days=duty_days)
            stuff.save()

        return redirect('stuff_list')

    return redirect("index")


def stuff_list(request):
    if globals.is_logged_in:
        stuffs = Stuff.objects.all()
        return render(request, 'main/stuff_list.html', {'stuffs': stuffs})

    return redirect("index")


def edit_stuff(request, stuff_id):
    if globals.is_logged_in:
        stuff = get_object_or_404(Stuff, stuff_id=stuff_id)

        return render(request, 'main/edit-stuff.html', {'stuff': stuff})

    return redirect("index")


def update_stuff(request, stuff_id):
    if globals.is_logged_in:
        stuff = get_object_or_404(Stuff, stuff_id=stuff_id)

        if request.method == 'POST':
            stuff_name = request.POST.get('stuff_name')
            join_date = request.POST.get('join_date')
            stuff_father = request.POST.get('stuff_father')
            stuff_nid = request.POST.get('stuff_nid')
            stuff_address = request.POST.get('stuff_address')
            stuff_mobile = request.POST.get('stuff_mobile')
            stuff_salary = request.POST.get('stuff_salary')
            duty_days = request.POST.get('duty_days')

            stuff.stuff_name = stuff_name
            stuff.join_date = join_date
            stuff.stuff_father = stuff_father
            stuff.stuff_nid = stuff_nid
            stuff.stuff_address = stuff_address
            stuff.stuff_mobile = stuff_mobile
            stuff.stuff_salary = stuff_salary
            stuff.duty_days = duty_days
            stuff.save()

            return redirect('stuff_list')

        return render(request, 'edit_stuff.html', {'stuff': stuff})

    return redirect("index")


def delete_stuff(request, stuff_id):
    if globals.is_logged_in:
        stuff = get_object_or_404(Stuff, stuff_id=stuff_id)

        stuff.delete()

        return redirect('stuff_list')

    return redirect("index")


# Sale
def sale(response):
    if globals.is_logged_in:
        services = Service.objects.all()
        stuffs = Stuff.objects.all()

        current_memo_id = 1
        last_memo_id = Sale.objects.aggregate(Max('memo_id'))['memo_id__max']
        if last_memo_id:
            current_memo_id = int(last_memo_id) + 1

        return render(response, "main/sale.html", {'services': services, 'stuffs': stuffs, 'current_memo_id': current_memo_id})

    return redirect("index")


def create_sale(request):
    if globals.is_logged_in:
        if request.method == 'POST':
            sale_date = request.POST.get('sale_date')

            # Check if it is the first row
            is_first_row = Sale.objects.count() == 0

            # Set the memo_id accordingly
            if is_first_row:
                memo_id = 1
            else:
                last_memo_id = Sale.objects.aggregate(Max('memo_id'))[
                    'memo_id__max']
                memo_id = last_memo_id + 1

            sale_rows = []
            total_due_amount = 0  # Initialize total due amount

            for key, value in request.POST.items():
                if key.startswith('stuff') and value:
                    unique_id = key.split('stuff')[1]

                    # Move stuff_id inside the loop
                    stuff_id = int(value)
                    customer_name = request.POST.get(
                        f'customer-name{unique_id}')
                    car_name = request.POST.get(f'car-name{unique_id}')
                    color = request.POST.get(f'color{unique_id}')
                    car_reg = request.POST.get(f'car-registration{unique_id}')
                    service_id = int(request.POST.get(f'service{unique_id}'))
                    total = float(request.POST.get(f'total{unique_id}'))
                    paid_total = float(request.POST.get(
                        f'paid-total{unique_id}'))
                    due_amount = total - paid_total
                    total_due_amount += due_amount
                    payment_status = request.POST.get(
                        f'payment-status{unique_id}')

                    sale_row = {
                        'stuff_id': stuff_id,
                        'customer_name': customer_name,
                        'car_name': car_name,
                        'color': color,
                        'car_reg': car_reg,
                        'service_id': service_id,
                        'total': total,
                        'paid_total': paid_total,
                        'due_amount': due_amount,
                        'payment_status': payment_status,
                    }
                    sale_rows.append(sale_row)

            # Create Sale objects from the captured data
            for sale_row in sale_rows:
                sale = Sale(
                    sale_date=sale_date,
                    memo_id=memo_id,
                    stuff_id=sale_row['stuff_id'],
                    customer_name=sale_row['customer_name'],
                    car_name=sale_row['car_name'],
                    color=sale_row['color'],
                    car_reg=sale_row['car_reg'],
                    service_id=sale_row['service_id'],
                    sale_total=sale_row['paid_total'],
                    # Set payment status here
                    payment_status=sale_row['payment_status']
                )
                sale.save()

                if sale_row['payment_status'] == 'unpaid':
                    dues = Dues(
                        memo_id=sale,
                        due_date=sale_date,
                        due_total=sale_row['due_amount'],
                        due_received=0
                    )
                    dues.save()

            # Update the total due amount in the last Dues entry for the memo_id
            last_due = Dues.objects.filter(
                memo_id=memo_id).order_by('-due_id').first()
            if last_due:
                last_due.due_total = total_due_amount
                last_due.save()

        return redirect('sales_list')

    return redirect("index")


def sales_list(request):
    if globals.is_logged_in:
        enc = 'today'
        current_date = date.today()
        sales = Sale.objects.select_related(
            'service', 'stuff').filter(sale_date=current_date).order_by('-memo_id')

        paginator = Paginator(sales, 20)  # Display 10 rows per page
        page_number = request.GET.get('page')
        new_sales = paginator.get_page(page_number)

        return render(request, 'main/sales-list.html', {'sales': new_sales, 'enc': enc, 'paginator': paginator})

    return redirect("index")


def sales_list_previous(request):
    if globals.is_logged_in:
        current_date = date.today()
        enc = 'previous'

        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            request.session['start_date'] = start_date
            request.session['end_date'] = end_date
        else:
            start_date = request.session.get(
                'start_date', current_date.replace(day=1).strftime('%Y-%m-%d'))
            end_date = request.session.get(
                'end_date', current_date.strftime('%Y-%m-%d'))

        sales = Sale.objects.select_related('service', 'stuff') \
            .filter(sale_date__range=[start_date, end_date]) \
            .order_by('-memo_id')

        total_amount = sales.aggregate(total=Sum('sale_total'))['total']

        paginator = Paginator(sales, 20)  # Display 20 rows per page
        page_number = request.GET.get('page')
        new_sales = paginator.get_page(page_number)

        return render(request, 'main/sales-list-previous.html', {
            'sales': new_sales,
            'start_date': start_date,
            'end_date': end_date,
            'enc': enc,
            'total_amount': total_amount
        })

    return redirect("index")


def sales_list_month(request):
    if globals.is_logged_in:
        current_date = date.today()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            request.session['start_date'] = start_date_str
            request.session['end_date'] = end_date_str
        else:
            start_date_str = request.session.get(
                'start_date', current_date.replace(day=1).strftime('%Y-%m-%d'))
            end_date_str = request.session.get(
                'end_date', current_date.strftime('%Y-%m-%d'))

        # Convert to date objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Calculate monthly sale_total grouped by service and sale_date
        sales = Sale.objects.select_related('service', 'stuff') \
            .filter(sale_date__range=(start_date, end_date)) \
            .values('service__service_name', 'sale_date') \
            .annotate(monthly_sale_total=Sum('sale_total'))

        # Group the sales data by service
        sales_by_service = {}
        grand_total = 0  # Initialize the grand total
        for sale in sales:
            service_name = sale['service__service_name']
            sale_date = sale['sale_date']
            sale_total = sale['monthly_sale_total']
            if service_name not in sales_by_service:
                sales_by_service[service_name] = []
            sales_by_service[service_name].append((sale_date, sale_total))
            grand_total += sale_total  # Add the sale_total to the grand total

        paginated_sales = []
        for service_name, service_sales in sales_by_service.items():
            # Display 20 rows per page
            paginator = Paginator(service_sales, 20)
            page_number = request.GET.get('page')
            service_sales_page = paginator.get_page(page_number)

            # Calculate service-wise total
            service_total = sum(sale_total for _, sale_total in service_sales)
            paginated_sales.append(
                (service_name, service_sales_page, service_total))

        month = start_date.strftime('%B')

        # Pass start and end dates back to the template
        return render(request, 'main/sales-list-month.html', {
            'sales': paginated_sales,
            'month': month,
            'grand_total': grand_total,
            'start_date': start_date_str,
            'end_date': end_date_str
        })

    return redirect("index")


def sales_list_all(request):
    if globals.is_logged_in:
        enc = 'all'
        sales = Sale.objects.select_related(
            'service', 'stuff').all().order_by('-memo_id')

        # Get the search parameters from the request
        mobile_number = request.GET.get('mobile')
        registration_number = request.GET.get('registration')

        # Apply search filters if search parameters are provided
        if mobile_number:
            sales = sales.filter(customer_name__icontains=mobile_number)
        if registration_number:
            sales = sales.filter(car_reg__icontains=registration_number)

        paginator = Paginator(sales, 20)  # Display 20 rows per page
        page_number = request.GET.get('page')
        new_sales = paginator.get_page(page_number)

        return render(request, 'main/sales-list.html', {'sales': new_sales, 'enc': enc, 'paginator': paginator})

    return redirect("index")


def dues_list(request):
    if globals.is_logged_in:
        query = request.GET.get('q')
        if query:
            dues = Dues.objects.select_related('memo_id').filter(
                Q(memo_id__customer_name__icontains=query) |
                Q(memo_id__car_name__icontains=query),
                due_total__gt=F('due_received')
            )
        else:
            dues = Dues.objects.select_related('memo_id').filter(
                due_total__gt=F('due_received')
            )
        return render(request, 'main/dues-list.html', {'dues': dues, 'query': query})

    return redirect("index")


def dues_list_pending(request):
    if globals.is_logged_in:
        dues = Dues.objects.select_related('memo_id').filter(
            due_total__gt=0, due_received__lt=F('due_total'))
        return render(request, 'main/dues-list.html', {'dues': dues})

    return redirect("index")


def update_due(request, due_id):
    if globals.is_logged_in:
        if request.method == 'POST':
            receive_str = 'receive-' + str(due_id)
            received = float(request.POST.get(receive_str))

            due = get_object_or_404(Dues, due_id=due_id)
            total_received = float(due.due_received)

            total_received += received
            due.due_received = total_received
            due.due_received_date = date.today()  # Update the received date
            due.save()

        return redirect("dues_list")

    return redirect("index")


def delete_sale(request, sale_id):
    if globals.is_logged_in:
        sale = get_object_or_404(Sale, sale_id=sale_id)

        sale.delete()

        # return redirect('sales_list')
        # Reload the current page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return redirect("index")




def edit_sale(request):
    pass


# Salary
def salary(response):
    if globals.is_logged_in:
        salaries = Salary.objects.all()
        stuffs = Stuff.objects.all()

        return render(response, "main/salary.html", {'salaries': salaries, 'stuffs': stuffs})

    return redirect("index")


def salary_view(response):
    if globals.is_logged_in:
        salaries = Salary.objects.all()
        stuffs = Stuff.objects.all()

        return render(response, "main/salary-view.html", {'salaries': salaries, 'stuffs': stuffs})

    return redirect("index")

# Define get_date_range function (as above)
def get_date_range(start_date_str, end_date_str):
    """Parse start and end date strings and return date objects."""
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        # Handle invalid date format
        start_date = end_date = date.today()
    return start_date, end_date


def salary_report(request, stuff_id):
    if globals.is_logged_in:
        stuff = get_object_or_404(Stuff, pk=stuff_id)
        total_salary = stuff.stuff_salary

        # Get date range from query parameters or default to current month
        start_date_str = request.GET.get(
            'start_date', date.today().replace(day=15).strftime('%Y-%m-%d'))
        end_date_str = request.GET.get('end_date', (date.today(
        ) + relativedelta(months=1, day=14)).strftime('%Y-%m-%d'))

        start_date, end_date = get_date_range(start_date_str, end_date_str)

        # Query for salaries within the date range
        salaries = Salary.objects.filter(
            stuff=stuff,
            salary_date__range=(start_date, end_date)
        )

        # Calculate received salary and remaining salary
        received = salaries.aggregate(Sum("total"))["total__sum"] or 0
        remaining = total_salary - received

        # Prepare data for the template
        salary_data = {
            'stuff': stuff.stuff_name,
            'total': total_salary,
            'received': received,
            'remaining': remaining,
            'status': received >= total_salary,
            'start_date': start_date,
            'end_date': end_date,
            'stuff_id': stuff_id
        }

        return render(request, 'main/salary-report.html', salary_data)

    return redirect("index")
# Modify the getSalaryInfo function


def getSalaryInfo(request, stuff_id):
    if globals.is_logged_in:
        stuff = get_object_or_404(Stuff, stuff_id=stuff_id)
        total_salary = stuff.stuff_salary

        start_date = request.GET.get('start_date', date.today())
        end_date = request.GET.get('end_date', date.today())

        # Convert dates to proper format
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            # Handle invalid date format
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        # Query for salaries within the date range
        salaries = Salary.objects.filter(
            stuff=stuff,
            salary_date__range=(start_date, end_date)
        )

        # Calculate received salary and remaining salary
        received = salaries.aggregate(Sum("total"))["total__sum"] or 0
        remaining = total_salary - received

        # Prepare data for the JSON response
        salary_data = {
            'stuff': stuff.stuff_name,
            'total': total_salary,
            'received': received,
            'remaining': remaining,
            'status': received >= total_salary,
            'start_date': start_date,
            'end_date': end_date
        }

        # Return data as a JSON response
        return JsonResponse(salary_data)

    return redirect("index")


def salaries_list(request):
    if globals.is_logged_in:
        query = request.GET.get('q')  # Get the search query from the request
        if query:
            salaries = Salary.objects.select_related('stuff').filter(
                stuff__stuff_name__icontains=query)  # Filter by name
        else:
            # Show all salaries if no query is present
            salaries = Salary.objects.select_related('stuff').all()

        return render(request, 'main/salary-list.html', {'salaries': salaries, 'query': query})

    return redirect("index")


def create_salary(request):
    if globals.is_logged_in:
        if request.method == 'POST':
            salary_date_str = request.POST.get('salary_date')
            stuff_id = int(request.POST.get('stuff'))
            total = Decimal(request.POST.get('pay_amt'))  # Convert to Decimal

            # Convert salary_date_str to a date object
            try:
                salary_date = datetime.strptime(
                    salary_date_str, '%Y-%m-%d').date()
            except ValueError:
                # Handle the error if salary_date is not valid
                return redirect('salary')  # Or render an error page

            # Retrieve the Stuff instance based on the stuff_id
            stuff = get_object_or_404(Stuff, pk=stuff_id)
            # Ensure stuff_salary is Decimal
            stuff_salary = Decimal(stuff.stuff_salary)

            current_month = datetime.now().month
            current_year = datetime.now().year

            if total >= stuff_salary:
                paid_status = True
            else:
                # Sum the total received salary in the current month/year
                salaries = Salary.objects.filter(
                    stuff=stuff, salary_date__month=current_month, salary_date__year=current_year
                )
                received = salaries.aggregate(Sum("total"))[
                    "total__sum"] or Decimal('0.00')
                # Convert received to Decimal before adding
                received = Decimal(received) + total

                # Set paid status based on the total received amount
                paid_status = received >= stuff_salary

            # Create and save the Salary object
            salary = Salary(salary_date=salary_date, stuff=stuff,
                            total=total, paid_status=paid_status)
            salary.save()

        return redirect('salary_list')

    return redirect("index")


def edit_salary(request, salary_id):
    if globals.is_logged_in:
        salary = get_object_or_404(
            Salary.objects.select_related('stuff'), salary_id=salary_id)

        return render(request, 'main/edit-salary.html', {'salary': salary})

    return redirect("index")


def delete_salary(request, salary_id):
    if globals.is_logged_in:
        salary = get_object_or_404(Salary, salary_id=salary_id)

        salary.delete()

        return redirect('salary_list')

    return redirect("index")


def update_salary(request, salary_id):
    if globals.is_logged_in:
        salary = get_object_or_404(Salary, salary_id=salary_id)

        if request.method == 'POST':
            salary_date = request.POST.get('salary_date')
            stuff_id = request.POST.get('stuff')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Convert the incoming new_tt value to Decimal
            new_total = Decimal(request.POST.get('new_tt'))

            stuff = get_object_or_404(Stuff, pk=stuff_id)

            # Make sure stuff_salary is treated as Decimal
            stuff_salary = Decimal(stuff.stuff_salary)

            # Calculate the total amount received in the specified date range
            salaries_in_range = Salary.objects.filter(
                stuff=stuff,
                salary_date__range=[start_date, end_date]
            )

            # Sum the total salary within the range and handle the case where no result is found
            received = salaries_in_range.aggregate(
                Sum("total"))["total__sum"] or Decimal('0.00')

            # Ensure all values are Decimal for consistency
            new_advance = received + new_total  # Both should be Decimal
            new_remaining = stuff_salary - new_advance  # Both are Decimal

            # Set the paid status based on the new_advance and stuff_salary
            if new_advance >= stuff_salary:
                salary.paid_status = True
            else:
                salary.paid_status = False

            salary.salary_date = salary_date
            salary.total = new_total
            salary.save()

            return redirect('salary_list')

        return render(request, 'main/edit-salary.html', {'salary': salary})

    return redirect("index")


# cost
def cost(response):
    if globals.is_logged_in:
        services = Service.objects.all()
        stuffs = Stuff.objects.all()

        return render(response, "main/cost.html", {'services': services, 'stuffs': stuffs})

    return redirect("index")


def create_cost(request):
    if globals.is_logged_in:
        if request.method == 'POST':
            cost_date = request.POST.get('cost_date')

            cost_rows = []

            for key, value in request.POST.items():
                if key.startswith('cost_name'):
                    unique_id = key.split('cost_name')[1]
                    cost_name = value if value else None
                    total = float(request.POST.get(
                        'total{}'.format(unique_id)))

                    cost_row = {
                        'cost_name': cost_name,
                        'total': total
                    }
                    cost_rows.append(cost_row)

            # Create cost objects from the captured data
            for cost_row in cost_rows:
                cost = Cost(
                    cost_date=cost_date,
                    cost_name=cost_row['cost_name'],
                    cost_amount=cost_row['total']
                )
                cost.save()

        return redirect('costs_list_day')

    return redirect("index")


def costs_list(request):
    if globals.is_logged_in:
        search_query = request.GET.get('search', '')

        if search_query:
            cost_list = Cost.objects.filter(
                cost_name__icontains=search_query).order_by('-cost_id')
        else:
            cost_list = Cost.objects.all().order_by('-cost_id')

        paginator = Paginator(cost_list, 20)  # Show 20 costs per page

        page_number = request.GET.get('page', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1  # Default to page 1 if the page number is invalid

        costs = paginator.get_page(page_number)

        return render(request, 'main/costs-list.html', {'costs': costs})

    return redirect("index")


def costs_list_day(request):
    if globals.is_logged_in:
        current_date = datetime.now().date()

        cost_list = Cost.objects.filter(
            cost_date=current_date).order_by('-cost_id')
        total_amount = cost_list.aggregate(total=Sum('cost_amount'))['total']

        paginator = Paginator(cost_list, 20)  # Show 10 costs per page

        page_number = request.GET.get('page')
        costs = paginator.get_page(page_number)

        return render(request, 'main/costs-list-day.html', {'costs': costs, 'total_amount': total_amount, 'current_date': current_date})

    return redirect("index")


def costs_list_month(request):
    if globals.is_logged_in:
        current_month = datetime.now().month
        month = datetime.now().strftime('%B')

        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            request.session['start_date'] = start_date
            request.session['end_date'] = end_date
        else:
            start_date = request.session.get(
                'start_date', datetime.now().replace(day=1).strftime('%Y-%m-%d'))
            end_date = request.session.get(
                'end_date', datetime.now().strftime('%Y-%m-%d'))

        cost_list = Cost.objects.filter(
            cost_date__range=[start_date, end_date]).order_by('-cost_id')
        total_amount = cost_list.aggregate(total=Sum('cost_amount'))['total']

        paginator = Paginator(cost_list, 20)  # Show 10 costs per page
        page_number = request.GET.get('page')
        costs = paginator.get_page(page_number)

        return render(request, 'main/costs-list-month.html', {
            'costs': costs,
            'total_amount': total_amount,
            'month': month,
            'start_date': start_date,
            'end_date': end_date
        })

    return redirect("index")


def edit_cost(request, cost_id):
    if globals.is_logged_in:
        cost = get_object_or_404(Cost, cost_id=cost_id)

        return render(request, 'main/edit-cost.html', {'cost': cost})

    return redirect("index")


def update_cost(request, cost_id):
    if globals.is_logged_in:
        cost = get_object_or_404(Cost, cost_id=cost_id)

        if request.method == 'POST':
            cost_name = request.POST.get('cost_name')
            cost_amount = request.POST.get('cost_amount')

            cost.cost_name = cost_name
            cost.cost_amount = cost_amount
            cost.save()

            return redirect('costs_list_day')

    return redirect("index")


def delete_cost(request, cost_id):
    if globals.is_logged_in:
        cost = get_object_or_404(Cost, cost_id=cost_id)

        cost.delete()

        # return redirect('costs_list')
        # Reload the current page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return redirect("index")


def stock(response):
    if globals.is_logged_in:
        items = Item.objects.all()
        return render(response, "main/create-stock.html", {'items': items})

    return redirect("index")


def get_item_qty(request):
    item_id = request.GET.get('item_id')
    if item_id:
        try:
            # item = get_object_or_404(Item, item_id=item_id)
            stock = get_object_or_404(
                Stock.objects.select_related('item'), item_id=item_id)
            return JsonResponse({'qty': stock.qty})
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
    else:
        return JsonResponse({'error': 'Item ID not provided'}, status=400)


def create_stock(request):
    if globals.is_logged_in:
        if request.method == 'POST':
            current_date = datetime.now()
            item_id = request.POST.get('service')
            quantity = request.POST.get('quantity')
            gt = request.POST.get('grand-total')

            try:
                item = get_object_or_404(Item, item_id=item_id)

                try:
                    existing_stock = Stock.objects.get(item=item)
                    existing_quantity = existing_stock.qty

                    # Calculate the new quantity by adding the existing and new quantity
                    new_quantity = existing_quantity + int(quantity)

                    # Update the stock with the new quantity
                    existing_stock.qty = new_quantity
                    existing_stock.save()

                    # cost_name = f'{item.item_name} - {quantity} PC/s'
                    # cost = Cost(cost_date=current_date,
                    #             cost_name=cost_name, cost_amount=float(gt))
                    # cost.save()
                except Stock.DoesNotExist:
                    # Create a new stock entry with the current quantity
                    stock = Stock(item=item, qty=quantity)
                    stock.save()

                    # cost_name = f'{item.item_name} - {quantity} PC/s'
                    # cost = Cost(cost_date=current_date,
                    #             cost_name=cost_name, cost_amount=float(gt))
                    # cost.save()

            except Item.DoesNotExist:
                # Handle the case if the item does not exist
                pass

        return redirect('stock_list')

    return redirect("index")


def sell_item(request):
    if globals.is_logged_in:
        if request.method == 'POST':
            current_date = datetime.now()
            item_id = request.POST.get('service')
            quantity = request.POST.get('quantity-sell')
            gt = request.POST.get('grand-total-sale')

            try:
                item = get_object_or_404(Item, item_id=item_id)

                try:
                    existing_stock = Stock.objects.get(item=item)
                    existing_quantity = existing_stock.qty

                    # Calculate the new quantity by adding the existing and new quantity
                    new_quantity = existing_quantity - int(quantity)

                    # Update the stock with the new quantity
                    existing_stock.qty = new_quantity

                    # charge_name = f'{item.item_name} - {quantity} PC/s'
                    # sale = Sale(sale_date=current_date,
                    #             customer_name=charge_name, sale_total=float(gt))
                    # existing_stock.save()
                    # sale.save()
                except Stock.DoesNotExist:
                    # # Create a new stock entry with the current quantity
                    # stock = Stock(item=item, qty=quantity)
                    # stock.save()

                    # cost_name = f'{item.item_name} - {quantity} PC/s'
                    # cost = Cost(cost_date=current_date,
                    #             cost_name=cost_name, cost_amount=float(gt))
                    # cost.save()
                    pass

            except Item.DoesNotExist:
                # Handle the case if the item does not exist
                pass

        return redirect('stock_list')

    return redirect("index")


def stock_list(request):
    if globals.is_logged_in:
        stocks = Stock.objects.select_related('item').all()
        if not stocks:
            # Handle the case when no stocks are found
            stocks = None

        return render(request, 'main/stock_list.html', {'stocks': stocks})

    return redirect("index")


def edit_stock(request, stock_id):
    if globals.is_logged_in:
        stock = get_object_or_404(Stock, stock_id=stock_id)
        service = stock.service  # Retrieve the service associated with the stock

        return render(request, 'main/edit-stock.html', {'stock': stock, 'service': service})

    return redirect("index")


def update_stock(request, stock_id):
    if globals.is_logged_in:
        stock = get_object_or_404(Stock, stock_id=stock_id)

        if request.method == 'POST':
            quantity = request.POST.get(f'qty{stock_id}')

            # print("QTY", quantity)

            stock.qty = quantity
            stock.save()

            return redirect('stock_list')

    return redirect("index")


def search_stock(request):
    if globals.is_logged_in:
        query = request.GET.get('search_query')
        stocks = []

        if query:
            stocks = Stock.objects.filter(
                Q(service__service_name__icontains=query) | Q(qty__icontains=query))

        return render(request, 'main/stock_list.html', {'stocks': stocks})

    return redirect("index")


def delete_stock(request, stock_id):
    if globals.is_logged_in:
        stock = get_object_or_404(Stock, stock_id=stock_id)

        stock.delete()

        return redirect('stock_list')

    return redirect("index")


def bill(response):
    if globals.is_logged_in:
        return render(response, "main/bill.html", {})

    return redirect("index")


def job_card(response):
    if globals.is_logged_in:
        order_id = 0
        last_order_id = Jobcard.objects.aggregate(
            max_order_id=Max('order_id'))['max_order_id']
        if last_order_id:
            order_id = last_order_id
        return render(response, "main/jobcard.html", {'order_id': order_id+1})

    return redirect("index")


def create_jobcard(request):
    if globals.is_logged_in:
        if request.method == 'POST':
            order_no = int(request.POST.get('order'))
            date = request.POST.get('date1')
            customer_name = request.POST.get('name')
            customer_address = request.POST.get('address')
            phone = request.POST.get('phone')
            chassis_no = request.POST.get('chassisNo')
            vehicle_name = request.POST.get('vehicleName')
            model_year = request.POST.get('modelYear')
            model = request.POST.get('model')
            engine_no = request.POST.get('engineNo')
            vehicle_reg = request.POST.get('vehicleReg')

            # Retrieve engineer name and technician name
            engineer_name = request.POST.get('engineerName')
            technician_name = request.POST.get('technicianname')

            # Retrieve table values
            table_values = []
            for key, value in request.POST.items():
                if key.startswith('slno_') and value:
                    sl_no = value
                    customer_request = request.POST.get(
                        'customerRequest_' + sl_no)
                    category = request.POST.get('category_' + sl_no)
                    labor_charge = request.POST.get('laborCharge_' + sl_no)

                    table_values.append({
                        'sl_no': sl_no,
                        'customer_request': customer_request,
                        'category': category,
                        'labor_charge': labor_charge
                    })

            # Retrieve table values for diagnosis
            diagnosis_table_values = []
            for key, value in request.POST.items():
                if key.startswith('dslno_') and value:
                    sl_no = value
                    diagnosis = request.POST.get('diagnosis_' + sl_no)

                    diagnosis_table_values.append({
                        'sl_no': sl_no,
                        'diagnosis': diagnosis
                    })

            # Retrieve table values for material
            material_table_values = []
            for key, value in request.POST.items():
                if key.startswith('mslno_') and value:
                    sl_no = value
                    mat_des = request.POST.get('mat_des_' + sl_no)
                    mat_qty = request.POST.get('mat_qty_' + sl_no)
                    mat_price = request.POST.get('mat_price_' + sl_no)
                    req_des = request.POST.get('req_des_' + sl_no)
                    req_qty = request.POST.get('req_qty_' + sl_no)
                    mat_sign = request.POST.get('mat_sign_' + sl_no)

                    material_table_values.append({
                        'sl_no': sl_no,
                        'mat_des': mat_des,
                        'mat_qty': mat_qty,
                        'mat_price': mat_price,
                        'req_des': req_des,
                        'req_qty': req_qty,
                        'mat_sign': mat_sign
                    })

            # Perform further operations with the retrieved form values and table values

             # Create a new JobCard instance and save it to the database
            job_card = Jobcard(
                order_id=order_no,
                order_date=date,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_phone=phone,
                chassis=chassis_no,
                vehicle=vehicle_name,
                model_year=model_year,
                model=model,
                engine=engine_no,
                reg=vehicle_reg,
            )
            job_card.save()

            # Insert table values into CustomerRequest table
            for table_value in table_values:
                sl_no = table_value['sl_no']
                customer_request = table_value['customer_request']
                category = table_value['category']
                labor_charge = table_value['labor_charge']

                customer_request_entry = CustomerRequest(
                    sl_no=sl_no,
                    order_id=job_card,
                    request=customer_request,
                    category=category,
                    charge=labor_charge
                )
                customer_request_entry.save()

            # Insert table values into Diagnosis table
            for table_value in diagnosis_table_values:
                sl_no = table_value['sl_no']
                diagnosis = table_value['diagnosis']

                diagnosis_entry = Diagnosis(
                    sl_no=sl_no,
                    order_id=job_card,
                    diagnosis_detail=diagnosis,
                    ref_by=None,  # Set the appropriate value if available
                    diagnosed_by=None,  # Set the appropriate value if available
                    driver_signature=None  # Set the appropriate value if available
                )
                diagnosis_entry.save()

            # Insert table values into IssueDemand table
            for table_value in material_table_values:
                sl_no = table_value['sl_no']
                mat_des = table_value['mat_des']
                mat_qty = table_value['mat_qty']
                mat_price = table_value['mat_price']
                req_des = table_value['req_des']
                req_qty = table_value['req_qty']
                mat_sign = table_value['mat_sign']

                issue_demand_entry = IssueDemand(
                    sl_no=sl_no,
                    order_id=job_card,
                    material_description=mat_des,
                    material_qty=mat_qty,
                    material_price=mat_price,
                    req_description=req_des,
                    req_qty=req_qty,
                    req_sign=mat_sign
                )
                issue_demand_entry.save()

            # Insert engineer and technician names into IssueDemandEngineer table
            issue_demand_engineer_entry = IssueDemandEngineer(
                order_id=job_card,
                engineer=engineer_name,
                technician=technician_name
            )
            issue_demand_engineer_entry.save()

        return redirect("jobcard_list")

    return redirect("index")


def jobcard_list(request):
    if globals.is_logged_in:
        jobcards = Jobcard.objects.all()
        if not jobcards:
            # Handle the case when no jobcards are found
            jobcards = None

        return render(request, 'main/jobcard_list.html', {'jobcards': jobcards})

    return redirect("index")


def view_jobcard(request, order_id):
    if globals.is_logged_in:
        # Retrieve records from Jobcard table
        jobcard_records = Jobcard.objects.filter(order_id=order_id).first()

        # Retrieve records from CustomerRequest table
        customer_records = CustomerRequest.objects.filter(order_id=order_id)

        # Retrieve records from Diagnosis table
        diagnosis_records = Diagnosis.objects.filter(order_id=order_id)

        # Retrieve records from IssueDemand table
        issue_demand_records = IssueDemand.objects.filter(order_id=order_id)

        # Retrieve records from IssueDemandEngineer table
        issue_demand_engineer_records = IssueDemandEngineer.objects.filter(
            order_id=order_id).first()

        return render(request, 'main/jobcard_view.html', {
            'jobcard_records': jobcard_records,
            'customer_records': customer_records,
            'diagnosis_records': diagnosis_records,
            'issue_demand_records': issue_demand_records,
            'issue_demand_engineer_records': issue_demand_engineer_records
        })

    return redirect("index")


def search_jobcard(request):
    if globals.is_logged_in:
        query = request.GET.get('search_query')
        jobcards = []

        if query:
            jobcards = Jobcard.objects.filter(
                Q(order_id__icontains=query) | Q(customer_name__icontains=query))

        return render(request, 'main/jobcard_list.html', {'jobcards': jobcards})

    return redirect("index")


def delete_jobcard(request, order_id):
    if globals.is_logged_in:
        jobcard = get_object_or_404(Jobcard, order_id=order_id)

        jobcard.delete()

        return redirect('jobcard_list')

    return redirect("index")


def monthly_statement(request):
    if globals.is_logged_in:
        if request.method == "POST":
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            request.session['start_date'] = start_date
            request.session['end_date'] = end_date
        else:
            start_date = request.session.get('start_date')
            end_date = request.session.get('end_date')

        if start_date and end_date:
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
        else:
            start_date = date.today().replace(day=1) - relativedelta(months=1)
            end_date = date.today().replace(day=1) - relativedelta(days=1)

        if end_date <= start_date:
            return redirect('monthly_statement')

        sales = Sale.objects.filter(sale_date__range=(start_date, end_date)).values(
            'sale_date').annotate(sale_total=Sum('sale_total'))
        costs = Cost.objects.filter(cost_date__range=(start_date, end_date)).values(
            'cost_date').annotate(cost_total=Sum('cost_amount'))
        salaries = Salary.objects.filter(salary_date__range=(start_date, end_date)).values(
            'salary_date').annotate(salary_total=Sum('total'))
        dues = Dues.objects.filter(due_received_date__range=(start_date, end_date)).values(
            'due_received_date').annotate(due_received_total=Sum('due_received'))

        daily_statement = {}
        grand_sale_total = 0
        grand_cost_total = 0
        grand_salary_total = 0
        grand_due_received_total = 0

        for sale in sales:
            sale_date = sale['sale_date']
            sale_total = sale['sale_total']
            daily_statement[sale_date] = {'sale_total': sale_total}
            grand_sale_total += sale_total

        for cost in costs:
            cost_date = cost['cost_date']
            cost_total = cost['cost_total']
            if cost_date in daily_statement:
                daily_statement[cost_date]['cost_total'] = cost_total
            else:
                daily_statement[cost_date] = {'cost_total': cost_total}
            grand_cost_total += cost_total

        for salary in salaries:
            salary_date = salary['salary_date']
            salary_total = salary['salary_total']
            if salary_date in daily_statement:
                daily_statement[salary_date]['salary_total'] = salary_total
            else:
                daily_statement[salary_date] = {'salary_total': salary_total}
            grand_salary_total += salary_total

        for due in dues:
            due_received_date = due['due_received_date']
            due_received_total = due['due_received_total']
            if due_received_date in daily_statement:
                daily_statement[due_received_date]['due_received_total'] = due_received_total
            else:
                daily_statement[due_received_date] = {
                    'due_received_total': due_received_total}
            grand_due_received_total += due_received_total

        grand_profit = grand_sale_total + grand_due_received_total - \
            grand_cost_total - grand_salary_total

        sorted_statement = sorted(daily_statement.items(), key=lambda x: x[0])

        today_profit = 0
        today_date = date.today()

        upd_total_today = Sale.objects.filter(payment_status='unpaid', sale_date=today_date).aggregate(
            upd_total_today=Sum('sale_total'))['upd_total_today'] or 0
        cash_total_today = Sale.objects.filter(payment_status='cash', sale_date=today_date).aggregate(
            cash_total_today=Sum('sale_total'))['cash_total_today'] or 0

        bkash_total_today = Sale.objects.filter(payment_status='bkash', sale_date=today_date).aggregate(
            bkash_total_today=Sum('sale_total'))['bkash_total_today'] or 0

        card_total_today = Sale.objects.filter(payment_status='card', sale_date=today_date).aggregate(
            card_total_today=Sum('sale_total'))['card_total_today'] or 0

        nagad_total_today = Sale.objects.filter(payment_status='nagad', sale_date=today_date).aggregate(
            nagad_total_today=Sum('sale_total'))['nagad_total_today'] or 0

        if today_date in daily_statement:
            today_sale_total = daily_statement[today_date].get('sale_total', 0)
            today_cost_total = daily_statement[today_date].get('cost_total', 0)
            today_salary_total = daily_statement[today_date].get(
                'salary_total', 0)
            today_due_received_total = daily_statement[today_date].get(
                'due_received_total', 0)
            today_profit = (today_sale_total + today_due_received_total) - \
                (today_cost_total + today_salary_total)

        months_range = [
            end_date - relativedelta(months=month) for month in range(11, -1, -1)]
        monthly_totals = []
        for month_date in months_range:
            month_start_date = month_date.replace(day=1)
            month_end_date = month_start_date + \
                relativedelta(months=1) - relativedelta(days=1)
            monthly_sale_total = Sale.objects.filter(sale_date__range=(month_start_date, month_end_date)).aggregate(
                monthly_sale_total=Sum('sale_total'))['monthly_sale_total'] or 0
            monthly_cost_total = Cost.objects.filter(cost_date__range=(month_start_date, month_end_date)).aggregate(
                monthly_cost_total=Sum('cost_amount'))['monthly_cost_total'] or 0
            monthly_salary_total = Salary.objects.filter(salary_date__range=(month_start_date, month_end_date)).aggregate(
                monthly_salary_total=Sum('total'))['monthly_salary_total'] or 0
            monthly_due_received_total = Dues.objects.filter(due_received_date__range=(month_start_date, month_end_date)).aggregate(
                monthly_due_received_total=Sum('due_received'))['monthly_due_received_total'] or 0
            monthly_profit = monthly_sale_total + monthly_due_received_total - \
                (monthly_cost_total + monthly_salary_total)
            monthly_totals.append({
                'month_date': month_date,
                'month_start_date': month_start_date,
                'month_end_date': month_end_date,
                'sale_total': monthly_sale_total,
                'cost_total': monthly_cost_total,
                'salary_total': monthly_salary_total,
                'due_received_total': monthly_due_received_total,
                'profit': monthly_profit,
            })

        month_order = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        grand_profit_total = 0
        for total in monthly_totals:
            total['month_name'] = total['month_date'].strftime('%B')
            grand_profit_total += float(total['profit'])

        monthly_totals.sort(key=lambda x: month_order.index(x['month_name']))

        context = {
            'statement': sorted_statement,
            'grand_sale_total': grand_sale_total,
            'grand_cost_total': grand_cost_total,
            'grand_salary_total': grand_salary_total,
            'grand_due_received_total': grand_due_received_total,
            'profit': grand_profit,
            'today_profit': today_profit,
            'monthly_totals': monthly_totals,
            'grand_profit_total': grand_profit_total,
            'start_date': start_date,
            'end_date': end_date,
            'upd_total_today': upd_total_today,
            'cash_total_today': cash_total_today,
            'bkash_total_today': bkash_total_today,
            'card_total_today': card_total_today,
            'nagad_total_today': nagad_total_today,
        }
        return render(request, 'main/monthly-statement.html', context)

    return redirect("index")


def calculate_profit(start_date, end_date):
    sales = Sale.objects.filter(sale_date__range=(start_date, end_date)).aggregate(
        total=Sum('sale_total'))['total'] or 0
    costs = Cost.objects.filter(cost_date__range=(start_date, end_date)).aggregate(
        total=Sum('cost_amount'))['total'] or 0
    salaries = Salary.objects.filter(salary_date__range=(
        start_date, end_date)).aggregate(total=Sum('total'))['total'] or 0
    dues = Dues.objects.filter(due_received_date__range=(start_date, end_date)).aggregate(
        total=Sum('due_received'))['total'] or 0
    profit = sales + dues - (costs + salaries)
    return profit


def month_to_month_statement(request):
    month_ranges = [
        ("Jan-Feb", (1, 2)),
        ("Feb-Mar", (2, 3)),
        ("Mar-Apr", (3, 4)),
        ("Apr-May", (4, 5)),
        ("May-Jun", (5, 6)),
        ("Jun-Jul", (6, 7)),
        ("Jul-Aug", (7, 8)),
        ("Aug-Sep", (8, 9)),
        ("Sep-Oct", (9, 10)),
        ("Oct-Nov", (10, 11)),
        ("Nov-Dec", (11, 12)),
        ("Dec-Jan", (12, 1))
    ]

    # Initialize the session storage for date ranges if it doesn't exist
    if 'date_ranges' not in request.session:
        request.session['date_ranges'] = {}

    date_ranges = request.session['date_ranges']

    if request.method == "POST":
        row = request.POST.get('row')
        start_date_str = request.POST.get(f'start_date_{row}')
        end_date_str = request.POST.get(f'end_date_{row}')
        if row and start_date_str and end_date_str:
            date_ranges[row] = {
                'start_date': start_date_str,
                'end_date': end_date_str
            }
            request.session['date_ranges'] = date_ranges

    month_to_month_profits = []
    grand_profit = 0

    for name, (start_month, end_month) in month_ranges:
        name_formatted = name.lower().replace("-", "_")

        # Retrieve the date range from session storage if available
        if name_formatted in date_ranges:
            start_date_str = date_ranges[name_formatted]['start_date']
            end_date_str = date_ranges[name_formatted]['end_date']
            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)
        else:
            # Default start and end dates for the month ranges
            month_start_date = date.today().replace(month=start_month, day=1)
            if start_month == 12:
                month_end_date = (month_start_date +
                                  relativedelta(months=1)).replace(day=1)
            else:
                month_end_date = date.today().replace(month=end_month, day=1)
            start_date = month_start_date
            end_date = month_end_date

        profit = calculate_profit(start_date, end_date)
        grand_profit += profit
        month_to_month_profits.append(
            (name, profit, start_date, end_date, name_formatted))

    context = {
        'month_to_month_profits': month_to_month_profits,
        'grand_profit': grand_profit,
    }
    return render(request, 'main/month-to-month-statement.html', context)


def reports(response):
    if globals.is_logged_in:
        return render(response, "main/report.html", {})

    return redirect("index")
