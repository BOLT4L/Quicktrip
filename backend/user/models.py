from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin ,BaseUserManager




class branch(models.Model):
    class b_type(models.TextChoices):
        MAIN = 'm',('main')
        BRANCH = 'b',('branch')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    type = models.CharField(max_length=15,default=b_type.BRANCH,choices=b_type.choices)
    
    def __str__(self):
        return f'{self.name}'

class accountmanagerBase(BaseUserManager):
    def create_user(self, phone_number=None, password=None, **extra_fields):
        user = self.model(phone_number = phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, password, **extra_fields)
    
    
class user(AbstractBaseUser,PermissionsMixin):
    class type(models.TextChoices):
        ADMIN = 'a' , ('admin')
        SUB_ADMIN = 's',('sub_admin')
        USER = 'u',('user')
        DRIVER = 'd',('driver')
    
    user_type = models.CharField(max_length=12 , choices=type.choices, default=type.USER)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone_number = models.BigIntegerField(null=False,default=0,unique=True)
    password = models.CharField(null=False,max_length=10)
    branch = models.ForeignKey(branch,on_delete=models.SET_NULL,null=True)
    objects = accountmanagerBase()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['password']  
    

    def __str__(self):
        return f'{self.phone_number}'

class credentials(models.Model):
    
    class credit_type(models.TextChoices):
            DRIVING_LICENSE = 'd',('driving_license')
            PASSPORT = 'p',('passport')
            INSTITUTE_ID = 'i',('institute_id')
            GOVERMENT_ID = 'g',('goverment id')
            OTHER = 'o',('other')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100) 
    user = models.ForeignKey(user, on_delete= models.CASCADE, related_name='credentials')
    type = models.CharField(max_length=12,choices=credit_type.choices , default=credit_type.OTHER)
    did = models.CharField(max_length=100, unique=True)
    doc = models.FileField(upload_to="driuser/uploads")


    