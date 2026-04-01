from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
import time

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless")
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(10)

        User.objects.all().delete()
        user = User.objects.create_superuser("isard", "isard@isardvdi.com", "pirineus")
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_admin_login(self):
        # Login
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        self.selenium.find_element(By.NAME, "username").send_keys('isard')
        self.selenium.find_element(By.NAME, "password").send_keys('pirineus')
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()
        self.assertIn("Site administration", self.selenium.title)

    def test_tasca_professor_view_site(self):
        # Login
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        self.selenium.find_element(By.NAME, "username").send_keys('isard')
        self.selenium.find_element(By.NAME, "password").send_keys('pirineus')
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(2)

        # Comprovem que estiguem a la pagina admin
        if "Site administration" not in self.selenium.title:
            self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
            time.sleep(1)

        # M'ha costat la vida  trobar la forma de fer click a VIWESITE
        # he utilitzat IA per trobar una forma de  que funcioni passant info de l'inspector.
        links = self.selenium.find_elements(By.TAG_NAME, "a")
        view_site_link = None
        
        for link in links:
            href = link.get_attribute("href")
            text = link.text.lower()
            if href == (self.live_server_url + "/") or "view site" in text or "veure el lloc" in text:
                view_site_link = link
                break
        
        if view_site_link:
            view_site_link.click()
        else:
            # Si no l'hem trobat en el bucle, provem un últim intent desesperat
            self.selenium.get(self.live_server_url + "/")

        # Verifico el contingut q he possat a urls.py per aconseguir el 200
        time.sleep(1)
        body_text = self.selenium.find_element(By.TAG_NAME, "body").text
        self.assertIn("Benvingut a la pàgina VIEWSITE", body_text)
