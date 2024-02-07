import functools
import os
import time
import typing
from abc import ABC, ABCMeta
import logging
from typing import List, Optional, Union

from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.print_page_options import PrintOptions
from selenium.webdriver.common.timeouts import Timeouts
from selenium.webdriver.common.virtual_authenticator import VirtualAuthenticatorOptions, required_virtual_authenticator, \
    Credential
from selenium.webdriver.common.window import WindowTypes
from selenium.webdriver.remote.file_detector import FileDetector
from selenium.webdriver.remote.shadowroot import ShadowRoot
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from nrobo.cli.tools import nprint
from nrobo.cli import STYLE

from selenium.webdriver.remote.webelement import WebElement
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory import PageFactory
from selenium.webdriver.support import expected_conditions
from nrobo.util.common import Common
from selenium.webdriver.common.keys import Keys


class WAITS:
    """Supported wait types in nrobo.
    These names are used as key in nrobo-config.yaml."""
    SLEEP = "sleep"
    WAIT = "static_wait"
    TIMEOUT = "timeout"
    ELE_WAIT = "ele_wait"


@functools.lru_cache(maxsize=None)
def read_nrobo_configs():
    return Common.read_yaml(f"nrobo{os.sep}framework{os.sep}nrobo-config.yaml")


class WebdriverWrapperNrobo(WebDriver):
    """
    Customized wrapper in nrobo of selenium-webdriver commands with enhanced functionality.

    This class is not instantiable.

    Doc: https://www.selenium.dev/selenium/docs/api/py/#
    """

    # Webdriver class variable
    driver = None
    # Logger class variable
    logger = None

    def __init__(self, driver: Union[None, WebDriver], logger: logging.Logger):
        """
        Constructor - NroboSeleniumWrapper

        :param driver: reference to selenium webdriver
        :param logger: reference to logger instance
        """
        # super().__init__()
        self.driver = driver
        self.logger = logger
        self.nconfig = read_nrobo_configs()

    """
    Following are selenium webdriver wrapper methods and properties
    """

    @property
    def name(self) -> str:
        """Returns the name of the underlying browser for this instance.

        :Usage:
            ::

                name = <obj>.name
        """
        return self.driver.name

    def get(self, url: str):
        """selenium webdriver wrapper method: get"""
        url = str(url).replace('\\', "\\\\")  # perform replacements
        nprint(f"Go to url <{url}>", logger=self.logger)
        self.driver.get(url)

    def execute(self, driver_command: str, params: dict = None) -> dict:
        """selenium webdriver wrapper method: execute"""
        nprint(f"Executing script...")
        return self.driver.execute(driver_command, dict)

    @property
    def title(self) -> str:
        """Returns the title of the current page.

        :Usage:
            ::

                title = <obj>.title
        """
        return self.driver.title

    @property
    def current_url(self) -> str:
        """Gets the URL of the current page.

        :Usage:
            ::

                <obj>.current_url
        """
        return self.driver.current_url

    @property
    def page_source(self) -> str:
        """Gets the source of the current page.

        :Usage:
            ::

               <obj>.page_source
        """
        return self.driver.page_source

    def close(self) -> None:
        """selenium webdriver wrapper method: close

        Closes the current window.

        :Usage:
            ::

                driver.close()
        return self.driver.close()
        """

    def quit(self) -> None:
        """Quits the driver and closes every associated window.

        :Usage:
            ::

                driver.quit()
        """
        self.driver.quit()

    @property
    def current_window_handle(self) -> str:
        """Returns the handle of the current window.

        :Usage:
            ::

                <obj>.current_window_handle
        """
        return self.driver.current_window_handle

    @property
    def window_handles(self) -> List[str]:
        """Returns the handles of all windows within the current session.

        :Usage:
            ::

                <obj>.window_handles
        """
        return self.driver.window_handles

    def maximize_window(self) -> None:
        """Maximizes the current window that webdriver is using."""
        self.driver.maximize_window()

    def fullscreen_window(self) -> None:
        """Invokes the window manager-specific 'full screen' operation."""
        self.driver.fullscreen_window()

    def minimize_window(self) -> None:
        """Invokes the window manager-specific 'minimize' operation."""
        self.driver.minimize_window()

    def print_page(self, print_options: Optional[PrintOptions] = None) -> str:
        """Takes PDF of the current page.

        The driver makes a best effort to return a PDF based on the
        provided parameters.
        """
        return self.driver.print_page(print_options)

    def switch_to_active_element(self) -> WebElement:
        """Returns the element with focus, or BODY if nothing has focus."""
        return self.driver.switch_to.active_element

    def switch_to_alert(self) -> Alert:
        """Switches focus to an alert on the page."""
        return self.driver.switch_to.alert

    def switch_to_default_content(self) -> None:
        """Switch focus to the default frame."""
        return self.driver.switch_to.default_content()

    def frame(self, frame_reference: Union[str, int, WebElement]) -> None:
        """Switches focus to the specified frame, by index, name, or webelement.

        :Args:
         - frame_reference: The name of the window to switch to, an integer representing the index,
                            or a webelement that is an (i)frame to switch to.

        :Usage:
            ::

                switch_to_frame('frame_name')
                switch_to_frame(1)
                switch_to_frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
        """
        return self.driver.switch_to.frame(frame_reference)

    def switch_to_new_window(self, type_hint: Optional[str] = None) -> None:
        """Switches to a new top-level browsing context.

        The type hint can be one of "tab" or "window". If not specified the
        browser will automatically select it.

        :Usage:
            ::

                switch_to_new_window('tab')
        """
        self.driver.switch_to.new_window(type_hint)

    def switch_to_parent_frame(self) -> None:
        """Switches focus to the parent context. If the current context is the
        top level browsing context, the context remains unchanged.

        :Usage:
            ::

                switch_to_parent_frame()
        """
        self.switch_to.parent_frame()

    def switch_to_window(self, window_name: str) -> None:
        """Switches focus to the specified window.

        :Args:
         - window_name: The name or window handle of the window to switch to.

        :Usage:
            ::

                switch_to_window('main')
        """
        self.switch_to.window(window_name)

    # Navigation
    def back(self) -> None:
        """Goes one step backward in the browser history.

        :Usage:
            ::

                back()
        """
        self.driver.back()

    def forward(self) -> None:
        """Goes one step forward in the browser history.

        :Usage:
            ::

                forward()
        """
        self.driver.forward()

    def refresh(self) -> None:
        """Refreshes the current page.

        :Usage:
            ::

                refresh()
        """
        self.driver.refresh()

    # Options
    def get_cookies(self) -> List[dict]:
        """Returns a set of dictionaries, corresponding to cookies visible in
        the current session.

        :Usage:
            ::

                get_cookies()
        """
        return self.driver.get_cookies()

    def get_cookie(self, name) -> typing.Optional[typing.Dict]:
        """Get a single cookie by name. Returns the cookie if found, None if
        not.

        :Usage:
            ::

                get_cookie('my_cookie')
        """
        return self.driver.get_cookie(name)

    def delete_cookie(self, name) -> None:
        """Deletes a single cookie with the given name.

        :Usage:
            ::

                delete_cookie('my_cookie')
        """
        self.driver.delete_cookie(name)

    def delete_all_cookies(self) -> None:
        """Delete all cookies in the scope of the session.

        :Usage:
            ::

                delete_all_cookies()
        """
        self.driver.delete_all_cookies()

    def add_cookie(self, cookie_dict) -> None:
        """Adds a cookie to your current session.

        :Args:
         - cookie_dict: A dictionary object, with required keys - "name" and "value";
            optional keys - "path", "domain", "secure", "httpOnly", "expiry", "sameSite"

        :Usage:
            ::

                add_cookie({'name' : 'foo', 'value' : 'bar'})
                add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/'})
                add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/', 'secure' : True})
                add_cookie({'name' : 'foo', 'value' : 'bar', 'sameSite' : 'Strict'})
        """
        self.driver.add_cookie(cookie_dict)

    # Timeouts
    def implicitly_wait(self, time_to_wait: float) -> None:
        """Sets a sticky timeout to implicitly wait for an element to be found,
        or a command to complete. This method only needs to be called one time
        per session. To set the timeout for calls to execute_async_script, see
        set_script_timeout.

        :Args:
         - time_to_wait: Amount of time to wait (in seconds)

        :Usage:
            ::

                implicitly_wait(30)
        """
        self.driver.implicitly_wait(time_to_wait)

    def set_script_timeout(self, time_to_wait: float) -> None:
        """Set the amount of time that the script should wait during an
        execute_async_script call before throwing an error.

        :Args:
         - time_to_wait: The amount of time to wait (in seconds)

        :Usage:
            ::

                set_script_timeout(30)
        """
        self.driver.set_script_timeout(time_to_wait)

    def set_page_load_timeout(self, time_to_wait: float) -> None:
        """Set the amount of time to wait for a page load to complete before
        throwing an error.

        :Args:
         - time_to_wait: The amount of time to wait

        :Usage:
            ::

                set_page_load_timeout(30)
        """
        self.driver.set_page_load_timeout(time_to_wait)

    @property
    def timeouts(self) -> Timeouts:
        """Get all the timeouts that have been set on the current session.

        :Usage:
            ::

                <obj>.timeouts
        :rtype: Timeout
        """
        return self.driver.timeouts

    @timeouts.setter
    def timeouts(self, timeouts) -> None:
        """Set all timeouts for the session. This will override any previously
        set timeouts.

        :Usage:
            ::
                my_timeouts = Timeouts()
                my_timeouts.implicit_wait = 10
                <obj>.timeouts = my_timeouts
        """
        self.driver.timeouts = timeouts

    def find_element(self, by=By.ID, value: Optional[str] = None) -> WebElement:
        """Find an element given a By strategy and locator.

        :Usage:
            ::

                element = find_element(By.ID, 'foo')

        :rtype: WebElement
        """

        WebDriverWait(self.driver, self.nconfig[WAITS.ELE_WAIT]) \
            .until(expected_conditions.presence_of_element_located([by, value]))
        return self.driver.find_element(by, value)

    def find_elements(self, by=By.ID, value: Optional[str] = None) -> List[WebElement]:
        """Find elements given a By strategy and locator.

        :Usage:
            ::

                elements = find_elements(By.CLASS_NAME, 'foo')

        :rtype: list of WebElement
        """
        WebDriverWait(self.driver, self.nconfig[WAITS.ELE_WAIT]) \
            .until(expected_conditions.presence_of_element_located([by, value]))
        return self.driver.find_elements(by, value)

    @property
    def capabilities(self) -> dict:
        """Returns the drivers current capabilities being used."""
        return self.driver.capabilities

    def get_screenshot_as_file(self, filename) -> bool:
        """Saves a screenshot of the current window to a PNG image file.
        Returns False if there is any IOError, else returns True. Use full
        paths in your filename.

        :Args:
         - filename: The full path you wish to save your screenshot to. This
           should end with a `.png` extension.

        :Usage:
            ::

                get_screenshot_as_file('/Screenshots/foo.png')
        """
        return self.driver.get_screenshot_as_file(filename)

    def save_screenshot(self, filename) -> bool:
        """Saves a screenshot of the current window to a PNG image file.
        Returns False if there is any IOError, else returns True. Use full
        paths in your filename.

        :Args:
         - filename: The full path you wish to save your screenshot to. This
           should end with a `.png` extension.

        :Usage:
            ::

                save_screenshot('/Screenshots/foo.png')
        """
        return self.driver.save_screenshot(filename)

    def get_screenshot_as_png(self) -> bytes:
        """Gets the screenshot of the current window as a binary data.

        :Usage:
            ::

                get_screenshot_as_png()
        """
        return self.driver.get_screenshot_as_png()

    def get_screenshot_as_base64(self) -> str:
        """Gets the screenshot of the current window as a base64 encoded string
        which is useful in embedded images in HTML.

        :Usage:
            ::

                get_screenshot_as_base64()
        """
        return self.driver.get_screenshot_as_base64()

    def set_window_size(self, width, height, windowHandle: str = "current") -> None:
        """Sets the width and height of the current window. (window.resizeTo)

        :Args:
         - width: the width in pixels to set the window to
         - height: the height in pixels to set the window to

        :Usage:
            ::

                set_window_size(800,600)
        """
        self.driver.set_window_size(width, height, windowHandle)

    def get_window_size(self, windowHandle: str = "current") -> dict:
        """Gets the width and height of the current window.

        :Usage:
            ::

                get_window_size()
        """
        return self.driver.set_window_size(windowHandle)

    def set_window_position(self, x, y, windowHandle: str = "current") -> dict:
        """Sets the x,y position of the current window. (window.moveTo)

        :Args:
         - x: the x-coordinate in pixels to set the window position
         - y: the y-coordinate in pixels to set the window position

        :Usage:
            ::

                set_window_position(0,0)
        """
        return self.driver.set_window_position(x, y, windowHandle)

    def get_window_position(self, windowHandle="current") -> dict:
        """Gets the x,y position of the current window.

        :Usage:
            ::

                get_window_position()
        """
        return self.driver.get_window_position(windowHandle)

    def get_window_rect(self) -> dict:
        """Gets the x, y coordinates of the window as well as height and width
        of the current window.

        :Usage:
            ::

               get_window_rect()
        """
        return self.driver.get_window_rect()

    def set_window_rect(self, x=None, y=None, width=None, height=None) -> dict:
        """Sets the x, y coordinates of the window as well as height and width
        of the current window. This method is only supported for W3C compatible
        browsers; other browsers should use `set_window_position` and
        `set_window_size`.

        :Usage:
            ::

                set_window_rect(x=10, y=10)
                set_window_rect(width=100, height=200)
                set_window_rect(x=10, y=10, width=100, height=200)
        """
        return self.driver.set_window_rect(x, y, width, height)

    @property
    def file_detector(self) -> FileDetector:
        return self.driver.file_detector

    @file_detector.setter
    def file_detector(self, detector) -> None:
        """Set the file detector to be used when sending keyboard input. By
        default, this is set to a file detector that does nothing.

        see FileDetector
        see LocalFileDetector
        see UselessFileDetector

        :Args:
         - detector: The detector to use. Must not be None.
        """
        self.driver.file_detector = detector

    @property
    def orientation(self):
        """Gets the current orientation of the device.

        :Usage:
            ::

                orientation = <obj>.orientation
        """
        return self.driver.orientation

    @orientation.setter
    def orientation(self, value) -> None:
        """Sets the current orientation of the device.

        :Args:
         - value: orientation to set it to.

        :Usage:
            ::

                <obj>.orientation = 'landscape'
        """
        self.driver.orientation = value

    @property
    def log_types(self):
        """Gets a list of the available log types. This only works with w3c
        compliant browsers.

        :Usage:
            ::

                log_types
        """
        return self.driver.log_types

    def get_log(self, log_type):
        """Gets the log for a given log type.

        :Args:
         - log_type: type of log that which will be returned

        :Usage:
            ::

                get_log('browser')
                get_log('driver')
                get_log('client')
                get_log('server')
        """
        return self.driver.get_log(log_type)

    """
    Research needed to wrap this method!

    @asynccontextmanager
    async def bidi_connection(self):
    """

    # Virtual Authenticator Methods
    def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions) -> None:
        """Adds a virtual authenticator with the given options."""
        self.driver.add_virtual_authenticator(options)

    @property
    def virtual_authenticator_id(self) -> str:
        """Returns the id of the virtual authenticator."""
        return self.driver.virtual_authenticator_id

    @required_virtual_authenticator
    def remove_virtual_authenticator(self) -> None:
        """Removes a previously added virtual authenticator.

        The authenticator is no longer valid after removal, so no
        methods may be called.
        """
        return self.driver.remove_virtual_authenticator

    @required_virtual_authenticator
    def add_credential(self, credential: Credential) -> None:
        """Injects a credential into the authenticator."""
        self.driver.add_credential(credential)

    @required_virtual_authenticator
    def get_credentials(self) -> List[Credential]:
        """Returns the list of credentials owned by the authenticator."""
        return self.driver.get_credentials()

    @required_virtual_authenticator
    def remove_credential(self, credential_id: Union[str, bytearray]) -> None:
        """Removes a credential from the authenticator."""
        return self.driver.remove_credential()

    @required_virtual_authenticator
    def remove_all_credentials(self) -> None:
        """Removes all credentials from the authenticator."""
        return self.driver.remove_all_credentials()

    @required_virtual_authenticator
    def set_user_verified(self, verified: bool) -> None:
        """Sets whether the authenticator will simulate success or fail on user
        verification.

        verified: True if the authenticator will pass user verification, False otherwise.
        """
        return self.driver.set_user_verified(bool)

    def get_downloadable_files(self) -> dict:
        """Retrieves the downloadable files as a map of file names and their
        corresponding URLs."""
        return self.driver.get_downloadable_files()

    def download_file(self, file_name: str, target_directory: str) -> None:
        """Downloads a file with the specified file name to the target
        directory.

        file_name: The name of the file to download.
        target_directory: The path to the directory to save the downloaded file.
        """
        return self.driver.download_file(file_name, target_directory)

    def delete_downloadable_files(self) -> None:
        """Deletes all downloadable files."""
        return self.driver.delete_downloadable_files()


class WebElementWrapperNrobo(WebdriverWrapperNrobo):
    """NRobo webelement wrapper class"""

    def __init__(self, driver: Union[None, WebDriver], logger: logging.Logger):
        """
        Constructor - NroboSeleniumWrapper

        :param driver: reference to selenium webdriver
        :param logger: reference to logger instance
        """
        super().__init__(driver, logger)
        # self.driver = driver
        # self.logger = logger

    def tag_name(self, by=By.ID, value: Optional[str] = None) -> str:
        """This element's ``tagName`` property."""
        return super().find_element(by, value).tag_name

    def text(self, by=By.ID, value: Optional[str] = None) -> str:
        """The text of the element."""
        return self.find_element(by, value).text

    def click(self, by=By.ID, value: Optional[str] = None) -> None:
        """Clicks the element."""
        self.find_element(by, value).click()

    def element_to_be_clickable(self, by=By.ID, value: Optional[str] = None) -> None:
        """
        wait for <wait> seconds mentioned in nrobo-config.yaml till the element is clickble.

        :param by:
        :param value:
        :return:
        """
        WebDriverWait(self.driver, self.nconfig[WAITS.WAIT]).until(
            expected_conditions.element_to_be_clickable([by, value]))
        self.click(by, value)

    def submit(self, by=By.ID, value: Optional[str] = None):
        """Submits a form."""
        self.find_element(by, value).submit()

    def clear(self, by=By.ID, value: Optional[str] = None) -> None:
        """Clears the text if it's a text entry element."""
        self.find_element(by, value).clear()

    def get_property(self, name, by=By.ID, value: Optional[str] = None) -> str | bool | WebElement | dict:
        """Gets the given property of the element.

        :Args:
            - name - Name of the property to retrieve.

        :Usage:
            ::

                text_length = target_element.get_property("text_length")
        """
        return self.find_element(by, value).get_property(name)

    def get_dom_attribute(self, name, by=By.ID, value: Optional[str] = None) -> str:
        """Gets the given attribute of the element. Unlike
        :func:`~selenium.webdriver.remote.BaseWebElement.get_attribute`, this
        method only returns attributes declared in the element's HTML markup.

        :Args:
            - name - Name of the attribute to retrieve.

        :Usage:
            ::

                text_length = target_element.get_dom_attribute("class")
        """
        return self.find_element(by, value).get_dom_attribute(name)

    def get_attribute(self, name, by=By.ID, value: Optional[str] = None) -> str | None:
        """Gets the given attribute or property of the element.

        This method will first try to return the value of a property with the
        given name. If a property with that name doesn't exist, it returns the
        value of the attribute with the same name. If there's no attribute with
        that name, ``None`` is returned.

        Values which are considered truthy, that is equals "true" or "false",
        are returned as booleans.  All other non-``None`` values are returned
        as strings.  For attributes or properties which do not exist, ``None``
        is returned.

        To obtain the exact value of the attribute or property,
        use :func:`~selenium.webdriver.remote.BaseWebElement.get_dom_attribute` or
        :func:`~selenium.webdriver.remote.BaseWebElement.get_property` methods respectively.

        :Args:
            - name - Name of the attribute/property to retrieve.

        Example::

            # Check if the "active" CSS class is applied to an element.
            is_active = "active" in target_element.get_attribute("class")
        """
        return self.find_element(by, value).get_attribute(name)

    def is_selected(self, by=By.ID, value: Optional[str] = None) -> bool:
        """Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
        """
        return self.find_element(by, value).is_selected()

    def is_enabled(self, by=By.ID, value: Optional[str] = None) -> bool:
        """Returns whether the element is enabled."""
        return self.find_element(by, value).is_enabled()

    def send_keys(self, by=By.ID, value: Optional[str] = None, *text) -> None:
        """Simulates typing into the element.

        :Args:
            - text - A string for typing, or setting form fields.  For setting
              file inputs, this could be a local file path.

        Use this to send simple key events or to fill out form fields::

            form_textfield = driver.find_element(By.NAME, 'username')
            form_textfield.send_keys("admin")

        This can also be used to set file inputs.

        ::

            file_input = driver.find_element(By.NAME, 'profilePic')
            file_input.send_keys("path/to/profilepic.gif")
            # Generally it's better to wrap the file path in one of the methods
            # in os.path to return the actual path to support cross OS testing.
            # file_input.send_keys(os.path.abspath("path/to/profilepic.gif"))
        """
        self.find_element(by, value).send_keys(text)

    def shadow_root(self, by=By.ID, value: Optional[str] = None) -> ShadowRoot:
        """Returns a shadow root of the element if there is one or an error.
        Only works from Chromium 96, Firefox 96, and Safari 16.4 onwards.

        :Returns:
          - ShadowRoot object or
          - NoSuchShadowRoot - if no shadow root was attached to element
        """
        return self.find_element(by, value).shadow_root

    # RenderedWebElement Items
    def is_displayed(self, by=By.ID, value: Optional[str] = None) -> bool:
        """Whether the element is visible to a user."""
        return self.find_element(by, value).is_displayed

    def location_once_scrolled_into_view(self, by=By.ID, value: Optional[str] = None) -> dict:
        """THIS PROPERTY MAY CHANGE WITHOUT WARNING. Use this to discover where
        on the screen an element is so that we can click it. This method should
        cause the element to be scrolled into view.

        Returns the top lefthand corner location on the screen, or zero
        coordinates if the element is not visible.
        """
        return self.find_element(by, value).location_once_scrolled_into_view

    def size(self, by=By.ID, value: Optional[str] = None) -> dict:
        """The size of the element."""
        return self.find_element(by, value).size

    def value_of_css_property(self, property_name, by=By.ID, value: Optional[str] = None) -> str:
        """The value of a CSS property."""
        return self.find_element(by, value).value_of_css_property(property_name)

    def location(self, by=By.ID, value: Optional[str] = None) -> dict:
        """The location of the element in the renderable canvas."""
        return self.find_element(by, value).location

    def rect(self, by=By.ID, value: Optional[str] = None) -> dict:
        """A dictionary with the size and location of the element."""
        return self.find_element(by, value).rect

    def aria_role(self, by=By.ID, value: Optional[str] = None) -> str:
        """Returns the ARIA role of the current web element."""
        return self.find_element(by, value).aria_role

    def accessible_name(self, by=By.ID, value: Optional[str] = None) -> str:
        """Returns the ARIA Level of the current webelement."""
        return self.find_element(by, value).accessible_name

    def screenshot_as_base64(self, by=By.ID, value: Optional[str] = None) -> str:
        """Gets the screenshot of the current element as a base64 encoded
        string.

        :Usage:
            ::

                img_b64 = element.screenshot_as_base64
        """
        return self.find_element(by, value).screenshot_as_base64

    def screenshot_as_png(self, by=By.ID, value: Optional[str] = None) -> bytes:
        """Gets the screenshot of the current element as a binary data.

        :Usage:
            ::

                element_png = element.screenshot_as_png
        """
        return self.find_element(by, value).screenshot_as_png

    def screenshot(self, filename, by=By.ID, value: Optional[str] = None) -> bool:
        """Saves a screenshot of the current element to a PNG image file.
        Returns False if there is any IOError, else returns True. Use full
        paths in your filename.

        :Args:
         - filename: The full path you wish to save your screenshot to. This
           should end with a `.png` extension.

        :Usage:
            ::

                element.screenshot('/Screenshots/foo.png')
        """
        return self.find_element(by, value).screenshot(filename)

    def parent(self, by=By.ID, value: Optional[str] = None):
        """Internal reference to the WebDriver instance this element was found
        from."""
        return self.find_element(by, value).parent

    def id(self, by=By.ID, value: Optional[str] = None) -> str:
        """Internal ID used by selenium.

        This is mainly for internal use. Simple use cases such as checking if 2
        webelements refer to the same element, can be done using ``==``::

            if element1 == element2:
                print("These 2 are equal")
        """
        return self.find_element(by, value).id


class WaitImplementationsNrobo(WebElementWrapperNrobo):
    """
    Nrobo implementation of wait methods
    """

    def __init__(self, driver: Union[None, WebDriver], logger: logging.Logger):
        """
        Constructor - NroboSeleniumWrapper

        :param driver: reference to selenium webdriver
        :param logger: reference to logger instance
        """
        super().__init__(driver, logger)
        # self.driver = driver
        # self.logger = logger

    def wait_for_page_to_be_loaded(self):
        """Waits for give timeout time for page to completely load.
        timeout time is configurable in nrobo-config.yaml"""

        nprint("Wait for page load...", style=STYLE.HLOrange)
        try:
            # Webdriver implementation of page load timeout
            super().set_page_load_timeout(self.nconfig[WAITS.TIMEOUT])

            # Custom page load timeout
            WebDriverWait(self.driver, self.nconfig[WAITS.TIMEOUT]).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete')
        except TimeoutException as te:
            nprint(f"Exception: {te}", STYLE.HLRed)
        except AttributeError as ae:
            nprint(f"Exception: {ae}", STYLE.HLRed)
        nprint("End of Wait for page load...", style=STYLE.PURPLE4)

    def wait_for_a_while(time_in_sec):
        """
        Pause for <time_in_sec>

        :param time_in_sec:
        :return:
        """
        time.sleep(time_in_sec)

    def wait_for_element_to_be_invisible(self, locator: WebElement | tuple[str, str]):
        """wait till <element> disappears from the UI"""

        nprint("wait for element invisible", style=STYLE.HLOrange)

        # wait a little
        self.wait_for_a_while(self.nconfig[WAITS.WAIT])

        # wait until the locator becomes invisible
        WebDriverWait(self.driver, self.nconfig[WAITS.WAIT]).until(
            expected_conditions.invisibility_of_element_located(locator))

        self.wait_for_a_while(self.nconfig[WAITS.WAIT])

        nprint("end of wait for element invisible", style=STYLE.PURPLE4)

    def wait_for_element_to_be_clickable(self, timeout=None):
        """
        wait till element is visible and clickable.

        :param timeout:
        :return:
        """
        super().element_to_be_clickable(timeout)


class ActionChainsNrobo(WebElementWrapperNrobo):
    def __init__(self, driver: Union[None, WebDriver], logger: logging.Logger):
        """
        Constructor - NroboSeleniumWrapper

        :param driver: reference to selenium webdriver
        :param logger: reference to logger instance
        """
        super().__init__(driver, logger)
        # self.driver = driver
        # self.logger = logger
        self._action_chain = ActionChains(self.driver)

    def action_chain(self):
        """Return ActionChains object"""
        return ActionChains(self._action_chain)


class AlertNrobo(ActionChainsNrobo):
    def __init__(self, driver: Union[None, WebDriver], logger: logging.Logger):
        """
        Constructor - NroboSeleniumWrapper

        :param driver: reference to selenium webdriver
        :param logger: reference to logger instance
        """
        super().__init__(driver, logger)
        # self.driver = driver
        # self.logger = logger

    def accept_alert(self) -> None:
        """accept alert"""
        self.switch_to_alert().accept()

    def dismiss_alert(self) -> None:
        """dismiss alert"""
        self.switch_to_alert().dismiss()

    def send_keys_to_alert(self, keysToSend: str) -> None:
        """Send Keys to the Alert.

        :Args:
         - keysToSend: The text to be sent to Alert.
        """
        self.switch_to_alert().send_keys(keysToSend)

    def send_keys_and_accept_alert(self, keysToSend: str) -> None:
        """Send Keys to the Alert and accept it.

        :Args:
         - keysToSend: The text to be sent to Alert.
        """
        self.send_keys_to_alert(keysToSend)
        self.accept_alert()

    def get_alert_text(self) -> None:
        """Get alert text"""
        return self.switch_to_alert().text


class ByNrobo(AlertNrobo):
    """
    Doc: https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.by.html#module-selenium.webdriver.common.by
    """

    def __init__(self, driver: Union[None, WebDriver], logger: logging.Logger):
        """
        Constructor

        :param driver: reference to selenium webdriver
        :param logger: reference to logger instance
        """
        super().__init__(driver, logger)
        # self.driver = driver
        # self.logger = logger


class DesiredCapabilitiesNrobo(ByNrobo):
    """
        Doc: https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.desired_capabilities.html#module-selenium.webdriver.common.desired_capabilities
        """

    def __init__(self, driver: Union[None, WebDriver], logger: logging.Logger):
        """
        Constructor

        :param driver: reference to selenium webdriver
        :param logger: reference to logger instance
        """
        super().__init__(driver, logger)
        # self.driver = driver
        # self.logger = logger


class SelectNrobo(DesiredCapabilitiesNrobo):
    def __init__(self, driver: Union[None, WebDriver], logger: logging.Logger):
        """
        Constructor

        :param driver: reference to selenium webdriver
        :param logger: reference to logger instance
        """
        super().__init__(driver, logger)
        # self.driver = driver
        # self.logger = logger

    def select(self, by=By.ID, value: Optional[str] = None) -> Select:
        """
        Get SELECT element

        :param by:
        :param value:
        :return:
        """
        return Select(self.find_element(by, value))


class NRobo(SelectNrobo):
    """NRobo class"""

    def __init__(self, driver: Union[None, WebDriver], logger: logging.Logger):
        """
        Constructor - NroboSeleniumWrapper

        :param driver: reference to selenium webdriver
        :param logger: reference to logger instance
        """
        super().__init__(driver, logger)
        # self.driver = driver
        # self.logger = logger

        # objects from common classes
        self.keys = Keys()
        self.by = By()
        self.print_options = PrintOptions()
        self.window_types = WindowTypes()

        # wait for page load
        # self.wait_for_page_to_be_loaded()
