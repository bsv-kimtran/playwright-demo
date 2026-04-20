from playwright.sync_api import Page, expect

LOGIN_URL = "https://woven-demo.eventos.tokyo/web/portal/1163/event/15549/users/login"
TOP_URL = "https://woven-demo.eventos.tokyo/web/portal/1163/event/15549"


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        # --- Locators (verified against actual DOM) ---
        self.email_input = page.locator("#mail_address")
        self.password_input = page.locator("#password")
        # Eye icon button to toggle password visibility
        self.toggle_password_btn = page.locator("button[aria-label='append icon']")
        # Clear icon button (×) next to email
        self.clear_email_btn = page.locator("button[aria-label='clear icon']")

        self.login_btn = page.locator("#login_button")
        self.signup_btn = page.locator("#register_button")

        # "パスワードを忘れた場合" is a <span>, not <a>
        self.forgot_password_link = page.locator("span.smart__forget__link")

        # Labels
        self.email_label = page.locator(".login-form__mail__label")
        self.password_label = page.locator(".login-form__password__label")

        # Error messages rendered by Vuetify
        self.email_error = page.locator(".v-input.login-form__mail__text .v-messages__message")
        self.password_error = page.locator(".v-messages__message").nth(1)
        # General login error (wrong credentials)
        self.login_error = page.locator(".v-messages__message, [class*='alert'], [class*='login-error']")

    def navigate(self):
        self.page.goto(LOGIN_URL)

    def fill_email(self, email: str):
        self.email_input.fill(email)
        self.email_input.blur()

    def fill_password(self, password: str):
        self.password_input.fill(password)
        self.password_input.blur()

    def click_login(self):
        self.login_btn.click()

    def click_forgot_password(self):
        self.forgot_password_link.click()

    def click_signup(self):
        self.signup_btn.click()

    def toggle_password_visibility(self):
        self.toggle_password_btn.click()

    def is_login_btn_disabled(self) -> bool:
        # Vuetify uses v-btn--disabled class instead of HTML disabled attr
        return "v-btn--disabled" in (self.login_btn.get_attribute("class") or "")
