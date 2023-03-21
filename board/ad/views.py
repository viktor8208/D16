from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from .models import Ad, UserResponse
from .forms import AdForm, UserResponseForm, UserResponseUpdateForm
from django.core.mail import send_mail
from .filters import ResponseFilter


class AdList(ListView):
    model = Ad
    ordering = '-id'
    template_name = 'adlist.html'
    context_object_name = 'ads'
    paginate_by = 10


class AdDetail(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        us_r = UserResponse.objects.filter(ad=self.kwargs['pk'])
        context['us_r'] = us_r
        return context


class AdUserList(ListView):
    model = Ad
    template_name = 'adlistD.html'
    context_object_name = 'ad_user'
    paginate_by = 4

    def get_queryset(self):
        queryset = Ad.objects.filter(author=self.request.user).order_by("-id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        us_r = UserResponse.objects.all()#(ad=self.kwargs['pk'])
        context['us_r'] = us_r
        return context


class AdUserCreate(LoginRequiredMixin, CreateView):
    form_class = AdForm
    model = Ad
    template_name = 'adcreate.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdUserUpdate(LoginRequiredMixin, UpdateView):
    form_class = AdForm
    model = Ad
    template_name = 'adcreate.html'


class AdUserDelete(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'delete.html'
    success_url = reverse_lazy('ad_user_list')


class UserResponseCreate(LoginRequiredMixin, CreateView):
    form_class = UserResponseForm
    model = UserResponse
    template_name = 'ur_create.html'
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.author = User.objects.get(id=self.request.user.pk)
        form.instance.ad = Ad.objects.get(id=self.kwargs.get('pk'))
        return super().form_valid(form)


class UserResponseList(LoginRequiredMixin, ListView):
    model = UserResponse
    template_name = 'urlist.html'
    context_object_name = 'ur_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ur = UserResponse.objects.filter(ad=Ad.objects.get(id=self.kwargs.get('pk')))
        context['user_ur'] = user_ur
        return context


class UserResponseUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserResponseUpdateForm
    model = UserResponse
    template_name = 'ur_update.html'
    success_url = reverse_lazy('ad_user_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = True
        self.object.save()
        return super().form_valid(form)


class UserResponseDelete(LoginRequiredMixin, DeleteView):
    model = UserResponse
    template_name = 'ur_delete.html'
    success_url = reverse_lazy('ad_user_list')
