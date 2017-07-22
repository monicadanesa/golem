import sys
import os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from golem.core import execution_logger as logger


# values used during the execution of a test case
driver = None
driver_name = None
settings = None
project = None
workspace = None
test_data = None
report_directory = None


def get_or_create_webdriver(*args):
    global settings
    global driver

    if not driver:
        driver_selected = get_selected_driver()
        if driver_selected == 'firefox':
            if settings['gecko_driver_path']:
                try:
                    os.environ["webdriver.gecko.driver"] = settings['gecko_driver_path']
                    driver = webdriver.Firefox()
                except:
                    msg = ('Could not start firefox driver using the path \'{}\', '
                           'check the settings file.'.format(settings['gecko_driver_path']))
                    logger.logger.error(msg)
                    raise Exception(msg) from None
            else:
                raise Exception('gecko_driver_path setting is not defined')
        if driver_selected == 'chrome':
            if settings['chrome_driver_path']:
                try:
                    driver = webdriver.Chrome(executable_path=settings['chrome_driver_path'])
                except:
                    msg = ('Could not start chrome driver using the path \'{}\', '
                           'check the settings file.'.format(settings['chrome_driver_path']))
                    logger.logger.error(msg)
                    raise Exception(msg) from None
            else:
                raise Exception('chrome_driver_path setting is not defined')
        # if driver_selected == 'ie':
        #     driver = webdriver.Ie()
        # if driver_selected == 'phantomjs':
        #     if os.name == 'nt':
        #         executable_path = os.path.join(
        #                                     golem.__path__[0],
        #                                     'lib',
        #                                     'phantom',
        #                                     'phantomjs.exe')
        #         driver = webdriver.PhantomJS(
        #                             executable_path=executable_path)
            # else:
            #     print('not implemented yet')
            #     sys.exit()
        # maximize driver window by default (fix)
        driver.maximize_window()

    return driver


def reset_driver_object():
    global driver 
    driver = None


def set_settings(settings_):
    global settings
    settings = settings_


def get_setting(setting):
    if setting in settings:
        return settings[setting]
    else:
        return False


def get_selected_driver():
    global driver_name
    if driver_name:
        driver_selected = driver_name
    else:
        driver_selected = 'chrome'
    return driver_selected
