
from django.conf import settings
from django.db import models


from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    company_name = models.CharField(max_length=115, null=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    zip = models.CharField(max_length=45)
    fax = models.CharField(max_length=45, null=True, blank=True)
    cell = models.CharField(max_length=45, null=True, blank=True)
    our_source = models.CharField(max_length=200, null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{str(self.username)} + {str(self.email)}"


class UserCredsSaver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=115)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="profile")
    is_verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=500)
    can_add = models.PositiveBigIntegerField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)
 
    # is_month = models.BooleanField(default=False)
    # is_year = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    # is_yearly = models.BooleanField(default=False)
    pro_start_date = models.DateField(null=True, blank=True)
    strip_costumer_token = models.CharField(
        max_length=200,  null=True, blank=True)
    strip_subscription_token = models.CharField(
        max_length=200,  null=True, blank=True)

    def __str__(self):
        return self.user.username




class Property(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="properties")
    property_name = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=100, null=True, blank=True)
    borough = models.CharField(max_length=200)
    block = models.CharField(max_length=100, null=True, blank=True)
    lott = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    house = models.CharField(max_length=100, null=True, blank=True)
    bin_number = models.CharField(max_length=200, null=True, blank=True)
   

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.user.username



class AdditionalContact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="contacts", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f" {self.name}:  {self.property.house}, {self.property.street}"







class Complaints(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="complaints", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="complaints")
    complaint_number = models.CharField(max_length=600)
    complaint_adress = models.CharField(max_length=600)
    complaint_date = models.CharField(max_length=600)
    complaint_category = models.CharField(max_length=600)
    complaint_details = models.CharField(max_length=600)
    complaint_inspection_date = models.CharField(
        max_length=255, blank=True, null=True)
    complaint_deposition = models.CharField(
        max_length=255, blank=True, null=True)
    complaint_link = models.CharField(max_length=600)
    complaint_status = models.CharField(max_length=600)

    def __str__(self):
        return self.complaint_number


class Voilation(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="voilations", null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="voilations")
    voilation_number = models.CharField(max_length=600, blank=True, null=True)
    voilation_type = models.CharField(max_length=600, blank=True, null=True)
    voilation_filedate = models.CharField(
        max_length=600, blank=True, null=True)
    voilation_dismissaldate = models.CharField(
        max_length=600, blank=True, null=True)
    voilation_Bageno = models.CharField(max_length=600, blank=True, null=True)
    v_link = models.CharField(max_length=1000, blank=True, null=True)


    def __str__(self):
        return self.voilation_number


class Price(models.Model):
    name = models.CharField(max_length=100)
    price_per_month = models.IntegerField(null=True)
    number_of_properties = models.IntegerField(null=True)
    is_yearly = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, blank=True)
    descripion = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.name}  +  {self.email}"

# class Borough(models.Model):
#     user = models.ForeignKey(User, on_delete=CASCADE)
#     name = models.CharField(max_length=100, blank=True, null=True, default="Borough")

#     def __str__(self):
#         return self.name

# class Street(models.Model):
#     borough = models.ForeignKey(Borough, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100, blank=True, null=True, default="Street Name")

#     def __str__(self):
#         return self.name


# class House(models.Model):
#     borough = models.ForeignKey(Borough, on_delete=models.CASCADE)
#     street = models.ForeignKey(Street, on_delete=models.CASCADE)
#     number = models.IntegerField()

#     def __str__(self):
#         return self.number
