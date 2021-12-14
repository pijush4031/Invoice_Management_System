from django.shortcuts import redirect, render, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import UserDetail
from .models import Customer, Invoice
from datetime import date
from xhtml2pdf import pisa
from django.http import HttpResponse

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        data={}
        data["customers"]=list(Customer.objects.all().values_list("id","email"))
        data["name"]=UserDetail.objects.get(user=request.user.id).name
        data["invoices"]=Invoice.objects.all()
        return render(request,"dashboard.html",data)
        
class AccountView(LoginRequiredMixin, View):
    def get(self, request):
        if request.GET.get("type"):
            invoice=request.GET.get("invoice_number")
            record=Invoice.objects.get(invoice_number=invoice)
            record.delete()
            return redirect("home:dashboard")
        data={}
        obj=Invoice.objects.get(invoice_number=request.GET.get('invoice_number'))
        cus=Customer.objects.get(id=obj.customer.id)
        data["customer"]=cus
        data["invoice"]=obj
        return render(request,"details.html",data)
        
    def post(self, request):

        if request.POST.get("type")=="put":
            return self.edit(request)
        
        customer = request.POST.get("customer")
        applicable_taxes = request.POST.get("applicable_taxes","")
        gst_number = request.POST.get("gst_number","")
        try:
            id=Invoice.objects.latest('id')
            id=id.id
        except:
            id=0
        invoice_number=f"TW/{date.today().year}/{date.today().month}/{id+1}"

        Invoice.objects.create(
            customer=Customer.objects.get(id=customer),
            invoice_number=invoice_number,
            applicable_taxes=applicable_taxes,
            gst_number=gst_number
        )
        return redirect("home:dashboard")

    def edit(self, request):
        
        invoice_number=request.POST.get("invoice_number")
        applicable_taxes = request.POST.get("applicable_taxes")
        gst_number = request.POST.get("gst_number")
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        country = request.POST.get('country')
        
        obj = Invoice.objects.get(
            invoice_number=invoice_number
        )

        cus = Customer.objects.get(
            id=obj.customer.id
        )

        if applicable_taxes:
            obj.applicable_taxes=applicable_taxes
        if gst_number:
            obj.gst_number=gst_number
        if name:
            cus.name=name
        if email:
            cus.email=email
        if address:
            cus.address=address
        if country:
            cus.country=country
        
        obj.save()
        cus.save()
        return redirect(reverse("home:account")+f"?invoice_number={invoice_number}")


def pdfGenerator(request):
    ivn=request.GET.get("invoice_number")                                  
    obj=Invoice.objects.get(invoice_number=ivn)
    response = HttpResponse(content_type='application/pdf') 
    response['Content-Disposition'] = f'attachment; filename="{obj.invoice_number}.pdf"'
    html = f"""
    <html>
    <h1 style='font-size:40px; text-align:center;'>TW COMPANY</h1> 
    <h1>Invoice Number = {obj.invoice_number}</h1><br/>
    <h1>Name = {obj.customer.name}</h1><br/>
    <h1>Email = {obj.customer.email}</h1><br/>
    <h1>Address = {obj.customer.address}</h1><br/>
    <h1>Country = {obj.customer.country}</h1><br/>
    <h1>Applicable Tax = {obj.applicable_taxes}</h1><br/>
    <h1>GST Number = {obj.gst_number}</h1><br/>
    </html>
    """
    pisa_status = pisa.CreatePDF(
      html, dest=response)
    return response
