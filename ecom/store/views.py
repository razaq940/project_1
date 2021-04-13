import random
import string


from .models import Item, OrderItem, Order, Address
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from .forms import CheckoutForm



def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid



class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"



class Search(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"
    def get_queryset(self):
                
                queryset = super(Search, self).get_queryset()
                search = self.request.GET.get("search")
                return queryset.filter(title__contains=search)
    
class SF(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"
    def get_queryset(self):
                queryset = super(SF, self).get_queryset()
                return queryset.filter(category='SF')

class S(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"
    def get_queryset(self):
                queryset = super(S, self).get_queryset()
                return queryset.filter(category='S')

class SO(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"
    def get_queryset(self):
                queryset = super(SO, self).get_queryset()
                return queryset.filter(category='SO')



        

    

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

   
class StatusOrderedView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            ordered_list = Order.objects.filter(user=self.request.user, ordered=True, received=False)
            context = {
                'object': ordered_list
            }
            return render(self.request, 'ordered.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("store:home")
            
    def post(self, request, *args, **kwargs):
        try:


            id = request.POST.get("id")
            print(id)
            order = Order.objects.get(user=self.request.user, pk=id, is_paid=True)
            order.received = True
            order.save()
            messages.success(self.request, "Done")
            return redirect("store:StatusOrderedView")

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active ordered")
            return redirect("/")


        

    


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("store:home")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("store:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("store:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("store:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("store:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("store:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("store:product", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("store:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("store:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("store:product", slug=slug)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
                
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("store:checkout")
        
        
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST , self.request.FILES or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                print(form.cleaned_data)

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('store:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('store:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                
                proof_of_payment = form.cleaned_data.get('proof_of_payment')
                if proof_of_payment is not None:
                    order.proof_of_payment = proof_of_payment
                    order.save()
                    order_items = order.items.all()
                    order_items.update(ordered=True)
                    for item in order_items:

                        item.save()
            
                    order.ordered = True
                    order.ref_code = create_ref_code()
                    order.save()
                    messages.success(self.request, "Your order was successful!")
                    return redirect("/")

                else:
                    messages.info(
                        self.request, "Please fill in the required shipping address fields")
                    return redirect('store:checkout')



               
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("store:order-summary")



