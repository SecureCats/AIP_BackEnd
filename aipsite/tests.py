from django.test import TestCase, Client
from .models import PublicKey, AipUser, TeachingClass, get_semester
import gmpy2
import random
import json
from .utils import cl_sign
from hashlib import sha256

# Create your tests here.
class CLSignTest(TestCase):

    def test_cl_sign(self):
        teaching_claass = TeachingClass(classno='666')
        pubkey = PublicKey.create(teaching_claass)
        uk = random.randrange(1<<4096)
        r = random.randrange(1<<32)
        r1, r2 = [random.randrange(1<<32) for _ in range(2)]
        a, b, c, n, g, h = pubkey.get_int(('a','b','c','n','g','h'))
        C = pow(a,uk,n) * pow(b, r, n) % n
        y = pow(a, r1, n) * pow(b, r2, n) % n
        x = int(sha256(str(C * g * h).encode()).hexdigest(), 16) % 731499577
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
        cls.teaching_class = TeachingClass(classno='233')
        cls.teaching_class.save()
        cls.user = AipUser.objects.create_user('spencer')
        cls.pubkey = PublicKey.create(cls.teaching_class)
        cls.pubkey.save()
        cls.user.teaching_class = cls.teaching_class
        cls.user.save()
        return super().setUpTestData()
    
    def test_sign(self):
        client = Client()
        client.force_login(self.user)
        uk = random.randrange(1<<4096)
        r = random.randrange(1<<32)
        r1, r2 = [random.randrange(1<<32) for _ in range(2)]
        a, b, c, n, g, h = self.pubkey.get_int(('a','b','c','n','g','h'))
        C = pow(a,uk,n) * pow(b, r, n) % n
        y = pow(a, r1, n) * pow(b, r2, n) % n
        x = int(sha256(str(C * g * h).encode()).hexdigest(), 16) % 731499577
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

    def test_query_pubkey(self):
        client = Client()
        response = client.get('/api/v1/pubkey/'+get_semester()+'/233')
        self.assertEqual(response.status_code, 200)
