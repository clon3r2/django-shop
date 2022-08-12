from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from apps.core.models import User
from .models import Address, Customer
from django.contrib.auth import views as auth_views
import sweetify
from apps.order.models import Order
from apps.order.cart import Cart
from apps.customer.models import Customer
from django.views.generic import UpdateView, CreateView, DeleteView
from django import http


# Create your views here.


class UserRegisterView(View):
    """
        View for User Registration
    """
    template_name = 'customer/register.html'
    form = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        """
            checks if user is already logged in or not
        """
        if request.user.is_authenticated:  # a user is already logged in
            return redirect('product:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """
            sends register template to customer
        """
        form = UserRegistrationForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
            gets Registration form data and validates
        """
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = User.objects.create_user(phone=cd['phone'], email=cd['email'], password=cd['password1'])
            Customer.objects.create(user=new_user, gender=cd['gender'])
            sweetify.toast(request, "you registered successfully", icon="success", timer=5000)
            return redirect('product:home')
        else:  # user sends wrong data in register form
            sweetify.toast(request, "some entries are invalid, try again", icon="error", timer=5000)
            return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    """
        View for User login
    """
    template_name = 'customer/login.html'
    form = UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
            checks if user is already logged in or not
        """
        if request.user.is_authenticated:
            return redirect('product:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """
            sends login template to customer
        """
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        """
            gets Login form data and validates
        """
        form = self.form(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(request, username=clean_data['phone'], password=clean_data['password1'])
            if user is not None:  # user exists and passed of authentication
                login(request, user)
                customer, created = Customer.objects.get_or_create(user=request.user)
                open_order, created = Order.objects.get_or_create(customer=customer, is_active=True)
                self.cart.session_merge_order(open_order)
                sweetify.toast(request, "you logged in successfully.", icon="success", timer=1500)
                return redirect('product:home')
            else:
                sweetify.toast(request, "username or password is not correct", icon="error", timer=1500)

        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    """
        View for User Logout
    """

    def get(self, request):
        logout(request)
        sweetify.toast(request, "You've been logged out successfully.", icon="success", timer=1500)
        return redirect('product:home')


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'customer/password_reset_form.html'
    success_url = reverse_lazy('customer:password_reset_done')
    email_template_name = 'customer/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'customer/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'customer/password_reset_confirm.html'
    success_url = reverse_lazy('customer:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'customer/password_reset_complete.html'


class PanelView(View):

    def get(self, request):
        recent_orders = Order.objects.filter(customer=request.user.customer, is_active=False)
        addresses = Address.objects.filter(customer=request.user.customer)
        return render(request, 'customer/panel.html', {'recent_orders': recent_orders, 'addresses': addresses})


class UserAddressView(UpdateView):
    template_name = 'customer/address_edit.html'
    model = Address
    fields = ['city', 'postal_code', 'address']
    success_url = reverse_lazy('customer:panel')


class UserAddressCreateView(CreateView):
    template_name = 'customer/address_create.html'
    model = Address
    fields = ['city', 'postal_code', 'address']
    success_url = reverse_lazy('customer:panel')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer = self.request.user.customer
        self.object.save()

        return http.HttpResponseRedirect(self.get_success_url())


class UserAddressDeleteView(DeleteView):
    model = Address
    success_url = reverse_lazy('customer:panel')


class UserProfileEditView(UpdateView):
    template_name = 'customer/profile_edit.html'
    model = User
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('customer:panel')


class UserProfileImageEditView(UpdateView):
    template_name = 'customer/profile_pic_edit.html'
    model = Customer
    fields = ['image']
    success_url = reverse_lazy('customer:panel')


class UserProfileView(View):
    def get(self, request):
        return render(request, 'customer/profile.html')
