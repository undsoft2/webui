# coding=utf-8
"""High Availability (tn-bhyve01) feature tests."""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from function import (
    wait_on_element,
    is_element_present,
    wait_on_element_disappear
)
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)


@scenario('features/NAS-T954.feature', 'Edit User enable Password')
def test_edit_user_enable_password(driver):
    """Edit User enable Password."""


@given(parsers.parse('The browser is open navigate to "{nas_url}"'))
def the_browser_is_open_navigate_to_nas_url(driver, nas_url):
    """The browser is open navigate to "{nas_user}"."""
    if nas_url not in driver.current_url:
        driver.get(f"http://{nas_url}/ui/sessions/signin")
        time.sleep(3)


@when(parsers.parse('If login page appear enter "{user}" and "{password}"'))
def if_login_page_appear_enter_root_and_password(driver, user, password):
    """If login page appear enter "{user}" and "{password}"."""
    if not is_element_present(driver, '//mat-list-item[@ix-auto="option__Dashboard"]'):
        assert wait_on_element(driver, 0.5, 5, '//input[@data-placeholder="Username"]')
        driver.find_element_by_xpath('//input[@data-placeholder="Username"]').clear()
        driver.find_element_by_xpath('//input[@data-placeholder="Username"]').send_keys(user)
        driver.find_element_by_xpath('//input[@data-placeholder="Password"]').clear()
        driver.find_element_by_xpath('//input[@data-placeholder="Password"]').send_keys(password)
        assert wait_on_element(driver, 0.5, 30, '//button[@name="signin_button"]')
        driver.find_element_by_xpath('//button[@name="signin_button"]').click()
    else:
        driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Dashboard"]').click()


@then('You should see the dashboard')
def you_should_see_the_dashboard(driver):
    """You should see the dashboard."""
    assert wait_on_element(driver, 0.5, 7, '//h1[contains(.,"Dashboard")]')
    assert wait_on_element(driver, 0.5, 7, '//span[contains(.,"System Information")]')


@then('Click on the Credentials item in the left side menu')
def click_on_the_credentials_item_in_the_left_side_menu(driver):
    """Click on the Credentials item in the left side menu."""
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Credentials"]').click()


@then('The Credentials menu should expand to the right')
def the_credentials_menu_should_expand_to_the_right(driver):
    """The Credentials menu should expand to the right."""
    assert wait_on_element(driver, 1, 7, '//mat-list-item[@ix-auto="option__Local Users"]')


@then('Click on Local Users')
def click_on_localusers(driver):
    """Click on Local Users."""
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Local Users"]').click()


@then('The Users page should open')
def the_users_page_should_open(driver):
    """The Users page should open."""
    assert wait_on_element(driver, 1, 7, '//div[contains(.,"Users")]')


@then('On the right side of the table, click the expand arrow for one of the users')
def on_the_right_side_of_the_table_click_the_expand_arrow_for_one_of_the_users(driver):
    """On the right side of the table, click the expand arrow for one of the users."""
    assert wait_on_element(driver, 0.5, 7, '//tr[@ix-auto="expander__ericbsd"]/td')
    driver.find_element_by_xpath('//tr[@ix-auto="expander__ericbsd"]/td').click()


@then('The User Field should expand down to list further details')
def the_user_field_should_expand_down_to_list_further_details(driver):
    """The User Field should expand down to list further details."""
    assert wait_on_element(driver, 0.5, 7, '//button[@ix-auto="button__EDIT_ericbsd"]')


@then('Click the Edit button that appears')
def click_the_edit_button_that_appears(driver):
    """Click the Edit button that appears."""
    driver.find_element_by_xpath('//button[@ix-auto="button__EDIT_ericbsd"]').click()


@then('The User Edit Page should open')
def the_user_edit_page_should_open(driver):
    """The User Edit Page should open."""
    assert wait_on_element(driver, 0.5, 7, '//h3[contains(.,"Edit User")]')


@then('Change "Disable Password" to No and click save')
def change_disable_password_to_no_and_click_save(driver):
    """Change "Disable Password" to No and click save."""
    driver.find_element_by_xpath('//mat-select[@ix-auto="select__Disable Password"]').click()
    assert wait_on_element(driver, 0.5, 30, '//mat-option[@ix-auto="option__Disable Password_No"]')
    driver.find_element_by_xpath('//mat-option[@ix-auto="option__Disable Password_No"]').click()


@then('Change should be saved')
def change_should_be_saved(driver):
    """Change should be saved."""
    assert wait_on_element(driver, 0.5, 30, '//button[@ix-auto="button__SAVE"]')
    driver.find_element_by_xpath('//button[@ix-auto="button__SAVE"]').click()
    assert wait_on_element_disappear(driver, 1, 30, '//h6[contains(.,"Please wait")]')
    assert wait_on_element(driver, 0.5, 30, '//div[contains(.,"Users")]')


@then('Open the user drop down to verify the user Disable Password is false')
def open_the_user_drop_down_to_verify_the_user_disable_password_is_false(driver):
    """Open the user drop down to verify the user Disable Password is false."""
    driver.find_element_by_xpath('//tr[@ix-auto="expander__ericbsd"]/td').click()
    assert wait_on_element(driver, 0.5, 30, '//button[@ix-auto="button__EDIT_ericbsd"]')
    driver.find_element_by_xpath('//h4[contains(.,"Password Disabled:")]')


@then('Updated value should be visible')
def updated_value_should_be_visible(driver):
    """Updated value should be visible."""
    element_text = driver.find_element_by_xpath('//h4[contains(.,"Password Disabled:")]/../div/p').text
    assert element_text == 'false'


@then('Try login with ssh')
def try_login_with_ssh(driver):
    """Try login with ssh."""
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__System Settings"]').click()
    assert wait_on_element(driver, 0.5, 7, '//mat-list-item[@ix-auto="option__Shell"]')
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Shell"]').click()
    assert wait_on_element(driver, 4, 7, '//span[@class="reverse-video terminal-cursor"]')
    actions = ActionChains(driver)
    actions.send_keys('ssh ericbsd@127.0.0.1', Keys.ENTER)
    actions.perform()
    assert wait_on_element(driver, 0.5, 3, '//span[contains(.,"(yes/no)?")]')
    if is_element_present(driver, '//span[contains(.,"(yes/no)?")]'):
        actions = ActionChains(driver)
        actions.send_keys('yes', Keys.ENTER)
        actions.perform()
    assert wait_on_element(driver, 0.5, 3, '//span[contains(.,"password:")]')
    actions = ActionChains(driver)
    actions.send_keys('testing', Keys.ENTER)
    actions.perform()


@then('User should be able to login')
def user_should_be_able_to_login(driver):
    """User should be able to login."""
    assert wait_on_element(driver, 1, 5, '//span[contains(.,"Permission") and contains(.,"denied,")]')
    assert not is_element_present(driver, '//span[contains(.,"Permission") and contains(.,"denied,")]')
