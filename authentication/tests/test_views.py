import pdb
from .test_setup import TestSetUp
from ..models import User

class TestView(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 400)

    def test_user_can_register(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, 201)
    
    def test_unverified_user_cannot_login(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 401)
    
    def test_verified_user_can_login(self):
        _res = self.client.post(self.register_url, self.user_data, format="json")
        
        user = User.objects.get(email=_res.data['email'])
        user.is_verified = True
        user.save()

        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)
