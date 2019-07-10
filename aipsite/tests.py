from django.test import TestCase
from .models import PublicKey
import gmpy2
import random
from .crypto_utils import cl_sign

# Create your tests here.
class CLSignTest(TestCase):

    def test_cl_sign(self):
        pubkey = PublicKey.create('666')
        uk = random.randrange(1<<4096)
        r = random.randrange(1<<32)
        r1, r2 = [random.randrange(1<<32) for _ in range(2)]
        a, b, c, n, g, h = pubkey.get_int(('a','b','c','n','g','h'))
        C = pow(a,uk,n) * pow(b, r, n) % n
        y = pow(a, r1, n) * pow(b, r2, n) % n
        x = C * g * h % 731499577
        z1 = r1 + x * uk
        z2 = r2 + x * r
        param = {
            'x': x,
            'y': y,
            'z1': z1,
            'z2': z2,
            'C': C
        }
        ret = cl_sign(pubkey, **param)
        self.assertIsInstance(ret, tuple)
        s = r + ret[0]
        e = ret[1]
        v = ret[2]
        left = pow(v, e, n)
        right = pow(a, uk, n) * pow(b, s, n) * c % n
        self.assertEqual(left, right)