from django.test import TestCase, Client
from .models import PublicKey, AipUser
import gmpy2
import random
import json
from .utils import cl_sign

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


class CLSignInterfaceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AipUser.objects.create_user('spencer')
        cls.pubkey = PublicKey.create('233')
        cls.pubkey.save()
        cls.user.classno = cls.pubkey
        cls.user.save()
        return super().setUpTestData()
    
    def test_hello_world(self):
        client = Client()
        client.force_login(self.user)
        response = client.get('/')
        self.assertContains(response, 'hello, world')

    def test_sign(self):
        client = Client()
        client.force_login(self.user)
        uk = random.randrange(1<<4096)
        r = random.randrange(1<<32)
        r1, r2 = [random.randrange(1<<32) for _ in range(2)]
        a, b, c, n, g, h = self.pubkey.get_int(('a','b','c','n','g','h'))
        C = pow(a,uk,n) * pow(b, r, n) % n
        y = pow(a, r1, n) * pow(b, r2, n) % n
        x = C * g * h % 731499577
        z1 = r1 + x * uk
        z2 = r2 + x * r
        param = {
            'x': str(x),
            'y': str(y),
            'z1': str(z1),
            'z2': str(z2),
            'C': str(C)
        }
        response = client.post(
            '/api/v1/sign', 
            json.dumps(param),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        s = r + int(response.json()['r_'])
        e = int(response.json()['e'])
        v = int(response.json()['v'])
        left = pow(v, e, n)
        right = pow(a, uk, n) * pow(b, s, n) * c % n
        self.assertEqual(left, right)

