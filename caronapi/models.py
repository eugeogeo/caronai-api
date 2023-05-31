from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, nome, ra, password=None):
        if not email:
            raise ValueError('O email deve ser fornecido')
        if not nome:
            raise ValueError('O nome deve ser fornecido')
        if not ra:
            raise ValueError('O RA deve ser fornecido')

        user = self.model(
            email=self.normalize_email(email),
            nome=nome,
            ra=ra,
        )

        user.set_password(password)  # Define a senha corretamente
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    ra = models.CharField(max_length=20, unique=True, verbose_name='RA')

    objects = UserManager()

    USERNAME_FIELD = 'ra'
    REQUIRED_FIELDS = ['email', 'nome']

    def __str__(self):
        return self.ra

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Ride(models.Model):
    driver_name = models.CharField(max_length=255)
    driver_ra = models.CharField(max_length=20, verbose_name='RA')
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    start_time = models.TimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    

class RideHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    role = models.CharField(choices=[('driver', 'Driver'), ('passenger', 'Passenger')], max_length=10)
