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
from django.db.models import Q
from sharlary import settings
# Create your views here.


def index(request):
    ctx = {}
    search_args = ""
    ggl_map_zoom_value = 12
    ggl_map_center_lat_lng_arr = None
    user_object = None
    saved_companies = None
    all_companies_qs = Company.objects.all()

    ctx['GOOGLE_API_KEY'] = settings.GOOGLE_API_KEY

    # options_city = all_companies_qs.values_list("city", flat=True).distinct()
    # options_category = all_companies_qs.values_list("category", flat=True).distinct()
    #
    # ctx['options_city'] = options_city
    # ctx['options_category'] = options_category

    ctx['options_city'] = ["台北市", "新北市", "基隆市", "宜蘭縣", "桃園市", "新竹市", "新竹縣", "苗栗縣",
                           "台中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "台南市", "高雄市",
                           "屏東縣", "花蓮縣", "臺東縣", "澎湖縣"]

    ctx['options_category'] = ["資訊業", "航空業", "電子業", "光電業", "製造業", "法律業", "醫療業", "服務業",
                               "金融業", "不動產業", "保險業", "餐飲業", "飯店業", "營造業", "傳產業",
                               "工程業", "運輸業", "倉儲業", "批發業", "貿易業", "設計業", "顧問業", "演藝業",
                               "體育業", "自由業", "政府機關", "其他"]

    if request.user.is_authenticated():
        user_object = get_object_or_404(User, id=request.user.id)
        user_extend_object = user_object.user_extend
        saved_companies = user_extend_object.company.all()

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
                    for company in saved_companies:
                        if len(company.salary.all().filter(title__icontains=k)) > 0:
                            qs = saved_companies.filter(id=company.id)
                            result = result | qs
                    companies = companies | result
                    search_args = search_args + " " + k
            else:
                for k in keywords_list:
                    # result = Company.objects.filter(Q(city__icontains=k) | Q(name__icontains=k))
                    result = Company.objects.filter(name__icontains=k)
                    for company in all_companies_qs:
                        if len(company.salary.all().filter(title__icontains=k)) > 0:
                            qs = all_companies_qs.filter(id=company.id)
                            result = result | qs
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
    ctx['local_tz'] = "Asia/Taipei"
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
    ctx['GGL_API_KEY'] = settings.GOOGLE_API_KEY
    ctx['r'] = get_object_or_404(Company, pk=company_id)

    if request.user.is_authenticated():
        if get_object_or_404(User, id=request.user.id).user_extend.company.filter(id=company_id):
            ctx['user_saved'] = True
    ctx['local_tz'] = "Asia/Taipei"
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
            # user.last_name = request.POST["last_name"].capitalize()
            user.save()
            user_extend_object = UserExtend.objects.create(user=user)
            Salary.objects.filter(email=user.email).update(user_extend=user_extend_object)

            subject = '{0} ，歡迎加入Sharlary！'.format(user.first_name)
            from_email = settings.DEFAULT_FROM_EMAIL
            text_content = 'Hi {0}！快快分享薪資一起讓就業環境變得更好！\n\n\n The Sharlary Team'.format(user.first_name)

            send_mail(
                subject,
                text_content,
                from_email,
                [user.email],
                fail_silently=False
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
            user.user_extend.salary.all().update(email=user.email)
            user.save()
        return redirect(reverse_lazy('index') + '?redirect_type=user_update')
    else:
        form = ProfileForm(instance=request.user)
    ctx = {'form': form}
    return render(request, 'registration/user_update.html', ctx)


def add_company(request):
    ctx = {}

    ctx['city_option'] = ["台北市", "新北市", "基隆市", "宜蘭縣", "桃園市", "新竹市", "新竹縣", "苗栗縣",
                          "台中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "台南市", "高雄市",
                          "屏東縣", "花蓮縣", "臺東縣", "澎湖縣"]
    ctx['category_option'] = ["資訊業", "航空業", "電子業", "光電業", "製造業", "法律業", "醫療業", "服務業",
                              "金融業", "不動產業", "保險業", "餐飲業", "飯店業", "營造業", "傳產業",
                              "工程業", "運輸業", "倉儲業", "批發業", "貿易業", "設計業", "顧問業", "演藝業",
                              "體育業", "自由業", "政府機關", "其他"]

    ctx['GOOGLE_RECAPTCHA_SITE_KEY'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
    if request.method == "POST":
        result = recaptcha_validation(request)

        if result['success']:
            name = request.POST["name"]
            try:
                tmp = Company.objects.get(name=name)
            except Company.DoesNotExist:
                tmp = None
            if tmp:
                return redirect('company_info', company_id=tmp.id)
            website = request.POST["website"]
            country = request.POST["country"]
            city = request.POST["city"]
            street = request.POST["street"]
            category = request.POST["category"]

            params = {'sensor': 'false', 'address': country + city + street}
            response = requests.get(settings.GOOGLE_GEOCODE_URL, params=params)
            results = response.json()['results']
            if len(results) == 1:
                location = results[0]['geometry']['location']
                latitude = location['lat']
                longitude = location['lng']

                c = Company.objects.create(name=name, website=website, country=country, city=city, street=street,
                                           category=category,
                                           latitude=latitude, longitude=longitude)
                ctx['saved'] = True
                ctx['company_id'] = c.id
            else:
                ctx['address_error'] = True
                ctx['error_msg'] = "請輸入詳細且正確的地址"
        else:
            ctx['recaptcha_error'] = True
            ctx['error_msg'] = "Google reCAPTCHA 認證失敗"
    return render(request, 'add_company.html', ctx)


class MyPasswordChangeView(PasswordChangeView):
    template_name = "registration/user_password_change.html"

    def get_success_url(self):
        return reverse_lazy('index') + "?redirect_type=password_change"

    def get_context_data(self, **kwargs):
        ctx = super(MyPasswordChangeView, self).get_context_data(**kwargs)
        return ctx


def share_salary(request, company_id):
    ctx = {}
    company = get_object_or_404(Company, id=company_id)
    ctx['GOOGLE_RECAPTCHA_SITE_KEY'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
    if request.method == "POST":

        result = recaptcha_validation(request)

        if result['success']:
            if request.user.is_authenticated():
                email = request.user.email
            else:
                email = request.POST["email"]
            title = request.POST["title"]
            monthly_pay = request.POST["monthly_pay"]
            related_expr = request.POST["related_expr"]
            education = request.POST["education"]
            school = request.POST["school"]
            major = request.POST["major"]
            other = request.POST["other"]

            s = Salary.objects.create(email=email, company=company, title=title, monthly_pay=monthly_pay, related_expr=related_expr,
                       education=education, school=school, major=major, other=other)
            company.update_time = s.update_time
            company.save()
            if request.user.is_authenticated():
                user_object = get_object_or_404(User, id=request.user.id)
                user_extend_object = user_object.user_extend
                user_extend_object.salary.add(s)
                user_extend_object.save()

            ctx['saved'] = True
        else:
            ctx['recaptcha_error'] = True
            ctx['error_msg'] = "Google reCAPTCHA 認證失敗"

    ctx['company'] = company
    ctx['education_options'] = ["國小", "國中", "高中", "高職", "公立大學", "私立大學", "海外大學",
                                "公立碩士", "私立碩士", "海外碩士", "公立博士", "私立博士", "海外博士"]
    return render(request, 'share_salary.html', ctx)


def search_company(request):
    ctx = {}
    company_names = Company.objects.values_list("name", flat=True).distinct()
    company_names = json.dumps(list(company_names), cls=DjangoJSONEncoder, ensure_ascii=False)
    ctx['company_names'] = company_names

    if request.method == "POST":
        query_company_name = request.POST["company_name"]
        companies = Company.objects.filter(name__icontains=query_company_name)
        ctx['query_company_name'] = query_company_name
        ctx['companies'] = companies
    return render(request, 'search_company.html', ctx)


@login_required()
def user_salary(request):
    ctx = {}
    user_object = get_object_or_404(User, id=request.user.id)
    salaries = user_object.user_extend.salary.all().order_by('-update_time')
    ctx['salaries'] = salaries
    return render(request, 'user_salary.html', ctx)


@login_required()
def user_salary_update(request, salary_id):
    ctx = {}
    user_object = get_object_or_404(User, id=request.user.id)
    salary_object = user_object.user_extend.salary.get(id=salary_id)
    ctx['salary'] = salary_object

    ctx['education_options'] = ["國小", "國中", "高中", "高職", "公立大學", "私立大學", "海外大學",
                                "公立碩士", "私立碩士", "海外碩士", "公立博士", "私立博士", "海外博士"]

    if request.method == 'POST':
        form = SalaryForm(data=request.POST, instance=salary_object)
        if form.is_valid():
            salary = form.save()
            salary.company.update_time = salary.update_time
            salary.company.save()
            ctx['saved'] = True
    else:
        form = SalaryForm(instance=salary_object)
    ctx['form'] = form
    return render(request, 'user_salary_update.html', ctx)


def recaptcha_validation(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post(settings.GOOGLE_RECAPTCHA_URL, data=data)
    result = r.json()
    return result


@login_required()
@require_POST
def comment_save(request, salary_id):
    salary_object = get_object_or_404(Salary, id=salary_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save()
        comment.salary = salary_object
        comment.user_extend = request.user.user_extend
        comment.save()
    return redirect('company_info', company_id=salary_object.company.id)


def company_update(request, company_id):
    ctx = {}
    ctx['GOOGLE_RECAPTCHA_SITE_KEY'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
    company_object = get_object_or_404(Company, id=company_id)
    ctx['company'] = company_object
    ctx['city_option'] = ["台北市", "新北市", "基隆市", "宜蘭縣", "桃園市", "新竹市", "新竹縣", "苗栗縣",
                          "台中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "台南市", "高雄市",
                          "屏東縣", "花蓮縣", "臺東縣", "澎湖縣"]
    ctx['category_option'] = ["資訊業", "航空業", "電子業", "光電業", "製造業", "法律業", "醫療業", "服務業",
                              "金融業", "不動產業", "保險業", "餐飲業", "飯店業", "營造業", "傳產業",
                              "工程業", "運輸業", "倉儲業", "批發業", "貿易業", "設計業", "顧問業", "演藝業",
                              "體育業", "自由業", "政府機關", "其他"]

    form = CompanyForm(instance=company_object)

    if request.method == 'POST':
        result = recaptcha_validation(request)

        if result['success']:
            country = request.POST["country"]
            city = request.POST["city"]
            street = request.POST["street"]

            params = {'sensor': 'false', 'address': country + city + street}
            response = requests.get(settings.GOOGLE_GEOCODE_URL, params=params)
            results = response.json()['results']

            if len(results) == 1:
                location = results[0]['geometry']['location']
                latitude = location['lat']
                longitude = location['lng']

                form = CompanyForm(data=request.POST, instance=company_object)
                if form.is_valid():
                    company = form.save()

                    company.latitude = latitude
                    company.longitude = longitude
                    company.save()
                    ctx['saved'] = True
                    ctx['company_id'] = company_id
            else:
                ctx['address_error'] = True
                ctx['error_msg'] = "請輸入詳細且正確的地址"

        else:
            ctx['recaptcha_error'] = True
            ctx['error_msg'] = "Google reCAPTCHA 認證失敗"

    ctx['form'] = form
    return render(request, 'company_update.html', ctx)
