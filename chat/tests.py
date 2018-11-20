from channels.testing import ChannelsLiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait


class ChatTests(ChannelsLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            # NOTE: Requires "chromedriver" binary to be installed in $PATH
            cls.driver = webdriver.Chrome()
        except:
            super().tearDownClass()
            raise
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
        try:
            self._enter_chat_room('room 1')
            
            # NOTE: Background is NOT blue here, showing that static files are NOT being served.
            import pdb; pdb.set_trace()
            
            self._open_new_window()
            self._enter_chat_room('room 1')
            
            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value)
            self._switch_to_window(1)
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value)
        finally:
            self._close_all_new_windows()
    
    def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
        try:
            self._enter_chat_room('room 1')
            
            self._open_new_window()
            self._enter_chat_room('room 2')
            
            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value)
            
            self._switch_to_window(1)
            self._post_message('world')
            WebDriverWait(self.driver, 2).until(lambda _:
                'world' in self._chat_log_value)
            self.assertTrue('hello' not in self._chat_log_value)
        finally:
            self._close_all_new_windows()
    
    # === Utility ===
    
    def _enter_chat_room(self, room_name):
        self.driver.get(self.live_server_url + '/chat/')
        ActionChains(self.driver).send_keys(room_name + '\n').perform()
        WebDriverWait(self.driver, 2).until(lambda _:
            room_name.replace(' ', '%20') in self.driver.current_url)
    
    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self.driver.switch_to_window(self.driver.window_handles[-1])
    
    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[-1])
            self.driver.execute_script('window.close();')
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to_window(self.driver.window_handles[0])
    
    def _switch_to_window(self, window_index):
        self.driver.switch_to_window(self.driver.window_handles[window_index])
    
    def _post_message(self, message):
        ActionChains(self.driver).send_keys(message + '\n').perform()
    
    @property
    def _chat_log_value(self):
        return self.driver.find_element_by_css_selector('#chat-log').get_property('value')


class NonChatTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            # NOTE: Requires "chromedriver" binary to be installed in $PATH
            cls.driver = webdriver.Chrome()
        except:
            super().tearDownClass()
            raise
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
        self._enter_chat_room('room 1')
        
        # NOTE: Background is blue here, showing that static files are being served.
        import pdb; pdb.set_trace()
    
    # === Utility ===
    
    def _enter_chat_room(self, room_name):
        self.driver.get(self.live_server_url + '/chat/')
        ActionChains(self.driver).send_keys(room_name + '\n').perform()
        WebDriverWait(self.driver, 2).until(lambda _:
            room_name.replace(' ', '%20') in self.driver.current_url)
