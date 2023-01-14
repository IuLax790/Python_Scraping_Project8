import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import booking.constants as const
from booking.booking_filtration import BookingFiltration

class Booking(webdriver.Chrome):
    def __init__(self,\
                 driver_path=r"C:\SeleniumDrivers",\
                 teardown=False):
        self.teardown = teardown
        self.driver_path = driver_path
        os.environ['PATH']+=self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',
                                        ['enable-logging'])
        super(Booking,self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self,currency=None):
        currency_element = self.find_element(By.XPATH, '//div[@class="ea1163d21f bc6c5feac2 e8e856c3e0"]').get_attribute()
        selected_currency_element = currency_element.find_elements(By.XPATH,f'div[@class="e6e585da6={currency}"]')
        selected_currency_element.click()
    def select_place_to_go(self,place_to_go):
        search_field = self.find_element(By.ID,'ss')
        search_field.clear()
        search_field.send_keys(place_to_go)
        first_result = self.find_element(By.CSS_SELECTOR,'li[data-i="0"]')
        first_result.click()
    def select_dates(self,check_in_date,check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR,f'td[data-date="{check_in_date}"]')
        check_in_element.click()
        check_out_date = self.find_element(By.CSS_SELECTOR,f'td[data-date="{check_out_date}"]')
        check_out_date.click()
    def select_adults(self,count):
        selection_element  =self.find_element(By.ID,'xp__guests__toggle')
        selection_element.click()
        while True:
            decrease_adults_elements = self.find_element(By.CSS_SELECTOR,'button[aria-label="Decrease number of Adults"]')
            decrease_adults_elements.click()
            #if the value of adults reaches 1, we should exit while loop
            adults_value_element = self.find_element(By.ID,'group_adults')
            adults_value = adults_value_element.get_attribute('value'
            )
            #should give back the adults count
            if int(adults_value) ==1:
                break
            increase_button_element = self.find_element(By.CSS_SELECTOR,
                'button[aria-label="Increase number of Adults"]')
            for _ in range(count-1):
                increase_button_element.click()
    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR,
                                'button[type="submit"]')
        search_button.click()
    def apply_filtrations(self):
        filtraion = BookingFiltration(driver=self)
        filtraion.apply_star_rating(3,4,5)
        filtraion.sort_price_lowest_first()

