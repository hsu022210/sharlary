from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.utils import translation
from .models import *
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
import requests
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordChangeView
# Create your views here.


def index(request):
    ctx = {}
    search_args = ""
    ggl_map_zoom_value = 12
    ggl_map_center_lat_lng_arr = None
    user_object = None
    saved_companies = None
    all_companies_qs = Company.objects.all()

    options_city = all_companies_qs.values_list("city", flat=True).distinct()
    options_category = all_companies_qs.values_list("category", flat=True).distinct()

    ctx['options_city'] = options_city
    ctx['options_category'] = options_category

    if request.user.is_authenticated():
        user_object = get_object_or_404(User, id=request.user.id)
        try:
            user_extend_object = user_object.user_extend
            saved_companies = user_extend_object.company.all()
        except UserExtend.DoesNotExist:
            pass

    ctx['saved_companies'] = saved_companies

    query_redirect_type = request.GET.get("redirect_type")

    if query_redirect_type == "login":
        ctx['first_login'] = True
    elif query_redirect_type == "logout":
        ctx['logout'] = True
    elif query_redirect_type == "register":
        ctx['register'] = True
    elif query_redirect_type == "user_update":
        ctx['user_update'] = True
    elif query_redirect_type == "password_change":
        ctx['password_change'] = True

    if query_redirect_type == "user_saved_list" and request.user.is_authenticated():
        ctx['user_saved_list'] = True
        companies = saved_companies.order_by('-update_time')
    else:
        companies = all_companies_qs.order_by('-update_time')

    if request.method == "POST":
        if request.POST["keyword"]:
            keyword = request.POST['keyword']
            keywords_list = keyword.split()
            companies = Company.objects.none()

            if "user_saved_list" in ctx:
                for k in keywords_list:
                    result = saved_companies.filter(name__icontains=k)
                    companies = companies | result
                    search_args = search_args + " " + k
            else:
                for k in keywords_list:
                    # result = Restaurant.objects.filter(Q(city__icontains=k) | Q(name__icontains=k))
                    result = Company.objects.filter(name__icontains=k)
                    companies = companies | result
                    search_args = search_args + " " + k

        req_post_city = request.POST["city"]
        req_post_category = request.POST["category"]

        if req_post_city != "城市" and req_post_city != "City":
            city = request.POST["city"]
            companies = companies.filter(city__icontains=city)
            search_args = search_args + " " + city
            # ggl_map_center_lat_lng_arr = [float(companies[0].latitude), float(companies[0].longitude)]

        if req_post_category != "產業" and req_post_category != "Type":
            category = request.POST["category"]
            companies = companies.filter(category__icontains=category)
            # result = Restaurant.objects.filter(category__icontains=category)
            # companies = companies | result
            search_args = search_args + " " + category
        ctx['search_args'] = search_args
    else:
        search_query_city = request.GET.get("search_query_city")
        search_query_category = request.GET.get("search_query_category")
        if search_query_city:
            companies = companies.filter(city__icontains=search_query_city)
            # ggl_map_center_lat_lng_arr = [float(companies[0].latitude), float(companies[0].longitude)]
            ctx['search_args'] = search_query_city

        if search_query_category:
            companies = companies.filter(category__icontains=search_query_category)
            ctx['search_args'] = search_query_category

    ctx['companies'] = companies

    tmp_rst_dict = companies.values('name', 'latitude', 'longitude', 'pk')
    tmp_rst_dict = json.dumps(list(tmp_rst_dict), cls=DjangoJSONEncoder)
    ctx['restaurants_locations_dict'] = tmp_rst_dict

    if companies:
        ggl_map_center_lat_lng_arr = [float(companies[0].latitude), float(companies[0].longitude)]

    ctx['ggl_map_center_lat_lng_arr'] = ggl_map_center_lat_lng_arr
    ctx['ggl_map_zoom_value'] = ggl_map_zoom_value
    return render(request, 'index.html', ctx)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/?redirect_type=logout')


def set_lang(request):
    user_language = request.GET.get("type")
    request_path = request.GET.get("next")
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return redirect(request_path)


def company_info(request, company_id):
    ctx = {}
    ctx['r'] = get_object_or_404(Company, pk=company_id)

    if request.user.is_authenticated():
        try:
            if get_object_or_404(User, id=request.user.id).user_extend.company.filter(id=company_id):
                ctx['user_saved'] = True
        except UserExtend.DoesNotExist:
            pass
    return render(request, 'company_info.html', ctx)


@login_required
@require_POST
def user_save_company(request):
    ctx = {}
    if request.method == 'POST':
        action = request.POST["action"]
        company_id = request.POST["company_id"]

        company_object = get_object_or_404(Company, id=company_id)
        user_object = get_object_or_404(User, id=request.user.id)
        user_extend_object = user_object.user_extend

        if action == "save":
            user_extend_object.company.add(company_object)
        else:
            user_extend_object.company.remove(company_object)
    return JsonResponse(json.dumps(ctx), safe=False)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            user.email = user.username
            user.first_name = request.POST["first_name"].capitalize()
            user.last_name = request.POST["last_name"].capitalize()
            user.save()
            user_extend_object = UserExtend(user=user)
            if Salary.objects.get(email=user.email):
                user_extend_object.salary = Salary.objects.get(email=user.email)
            user_extend_object.save()

            send_mail(
                '{0} ，歡迎加入Sharlary！'.format(user.first_name),
                'Hi {0}！快快分享薪資一起讓就業環境變得更好！\n\n\n The Eaggie Team'.format(user.first_name),
                'hsu022210@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return redirect(reverse_lazy('index') + '?redirect_type=register')
    else:
        form = UserCreationForm()
    ctx = {'form': form}
    return render(request, 'registration/register.html', ctx)


@login_required
def user_saved_list(request):
    return redirect(reverse_lazy('index') + '?redirect_type=user_saved_list')


@login_required
def user_update(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
        return redirect(reverse_lazy('index') + '?redirect_type=user_update')
    else:
        form = ProfileForm(instance=request.user)
    ctx = {'form': form}
    return render(request, 'registration/user_update.html', ctx)


def add_company(request):
    ctx = {}
    if request.method == "POST":
        name = request.POST["name"]
        website = request.POST["website"]
        country = request.POST["country"]
        city = request.POST["city"]
        street = request.POST["street"]
        category = request.POST["category"]

        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'sensor': 'false', 'address': country + city + street}
        response = requests.get(url, params=params)
        results = response.json()['results']
        location = results[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']

        c = Company(name=name, website=website, country=country, city=city, street=street, category=category, latitude=latitude, longitude=longitude)
        c.save()
        ctx['saved'] = True
    return render(request, 'add_company.html', ctx)


class MyPasswordChangeView(PasswordChangeView):
    template_name = "registration/user_password_change.html"

    def get_success_url(self):
        return reverse_lazy('index') + "?redirect_type=password_change"

    def get_context_data(self, **kwargs):
        ctx = super(MyPasswordChangeView, self).get_context_data(**kwargs)
        return ctx
