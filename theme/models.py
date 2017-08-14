from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField(null=True, blank=True)
    join_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    def __str__(self):
        return self.name


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class UserExtend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_extend')
    company = models.ManyToManyField(Company, related_name='user_extend')

    def __str__(self):
        return self.user.username


class Salary(models.Model):
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='salary')
    user_extend = models.ForeignKey(UserExtend, on_delete=models.CASCADE, related_name='salary', null=True)
    title = models.CharField(max_length=50)
    monthly_pay = models.PositiveIntegerField()
    related_expr = models.PositiveSmallIntegerField()
    education = models.CharField(max_length=10)
    school = models.CharField(max_length=50, null=True, blank=True)
    major = models.CharField(max_length=50, null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    other = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.email + " " + str(self.monthly_pay)


class SalaryForm(ModelForm):
    class Meta:
        model = Salary
        fields = ['title', 'monthly_pay', 'related_expr', 'education', 'school', 'major', 'other']
