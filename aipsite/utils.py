import gmpy2
import random
from .models import PublicKey
from Crypto.Util import number
from django.utils import timezone
from hashlib import sha256

def cl_sign(pubkey, **kwargs):
    n = pubkey.get_int('n')
    a = pubkey.get_int('a')
    b = pubkey.get_int('b')
    c = pubkey.get_int('c')
    g = pubkey.get_int('g')
    h = pubkey.get_int('h')
    p = pubkey.get_int('p')
    param_list = ('x', 'C', 'z1', 'z2', 'y')
    param = dict()
    for i in param_list:
        try:
            param[i] = int(kwargs[i])
        except:
            return None
    if param['x'] != int(sha256(str(g * h * param['C']).encode()).hexdigest(), 16) % 731499577:
        return False
    if pow(a, param['z1'], n) * pow(b, param['z2'], n) * \
        gmpy2.invert(param['y'], n) % n != pow(param['C'], param['x'], n):
        return False
    r_ = random.randrange(1<<PublicKey.ls)
    e = number.getPrime(PublicKey.le)
    q = n // p
    d = gmpy2.invert(e, (p-1)*(q-1))
    v = pow(param['C'] * c * pow(b, r_, n), d, n)
    return r_, e, v
