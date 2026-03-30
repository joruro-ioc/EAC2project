from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User

class MySeleniumTests(StaticLiveServerTestCase):
    # no crearem una BD de test en aquesta ocasió [cite: 39]
    # fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless") # Per a entorns server/GitHub 
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        
        # creem superusuari programàticament [cite: 47-51]
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit() # Tanquem el browser
        super().tearDownClass()

    def test_admin_login(self):
        # Simulem usuari extern que interactua amb l'admin panel [cite: 54-55]
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        
        # Localitzar, escriure i clicar [cite: 55]
        self.selenium.find_element(By.NAME, "username").send_keys('isard')
        self.selenium.find_element(By.NAME, "password").send_keys('pirineus')
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()
        
        # Assert per comprovar que el login és correcte [cite: 56]
        self.assertIn("Site administration", self.selenium.title)

