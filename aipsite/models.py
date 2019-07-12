from django.db import models
from Crypto.Util import number
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

# Create your models here.
def get_semaster():
    now = timezone.now()
    if now.month in (9,10,11,12,1,2):
        # Fall semaster
        return '{}-{}-1'.format(now.year, now.year+1)
    else:
        return '{}-{}-2'.format(now.year-1, now.year)

class TeachingClass(models.Model):
    classno = models.CharField(max_length=10, unique=True)
    school = models.CharField('学院', max_length=10, blank=True)

    def __str__(self):
        return self.classno

class PublicKey(models.Model):

    a = models.CharField(max_length=500, blank=True)
    b = models.CharField(max_length=500, blank=True)
    c = models.CharField(max_length=500, blank=True)
    n = models.CharField(max_length=500, blank=True)
    g = models.CharField(max_length=500, blank=True)
    h = models.CharField(max_length=500, blank=True)
    p = models.CharField(max_length=500, blank=True)

    le = 2050
    ls = 8196
    ln = 4096

    teaching_class = models.ForeignKey(TeachingClass, models.CASCADE)
    semaster = models.CharField("学期", max_length=20)

    def get_int(self, name):
        if isinstance(name, (list, tuple)):
            ret = []
            for i in name:
                if i in ('a', 'b', 'c', 'n', 'g', 'h', 'p'):
                    ret.append(int(self.__getattribute__(i)))
            return ret
        if name in ('a', 'b', 'c', 'n', 'g', 'h', 'p'):
            return int(self.__getattribute__(name))
        else:
            return None

    def init_key(self):
        p = number.getStrongPrime(2048)
        q = number.getStrongPrime(2048)
        n = p*q
        randlis = [random.randrange(0, 1<<1024) for _ in range(4)]
        rand2lis = list(map(lambda x: pow(x, 2, n) ,randlis))
        h = rand2lis[3]
        r = random.randrange(100)
        g = pow(h, r, n)
        self.n = str(n)
        self.a = str(rand2lis[0])
        self.b = str(rand2lis[1])
        self.c = str(rand2lis[2])
        self.h = str(rand2lis[3])
        self.p = str(p)
        self.g = str(g)

    @classmethod
    def create(cls, teaching_class, semaster=None):
        if not semaster:
            semaster = get_semaster()
        obj = cls(
            teaching_class = teaching_class,
            semaster = semaster
        )
        obj.init_key()
        return obj

    def __str__(self):
        return '{}_{}'.format(self.teaching_class, self.semaster)

    def renew(self):
        if get_semaster() == self.semaster:
            return None
        return self.create(self.teaching_class)

class AipUser(AbstractUser):
    teaching_class = models.ForeignKey(
        TeachingClass, on_delete=models.SET_NULL, 
        blank=True, null=True
    )
    is_signed = models.BooleanField(default=False)
