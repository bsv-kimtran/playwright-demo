from playwright.sync_api import Page, expect

ADMIN_LOGIN_URL = "https://admin.odakyu.bravesoft.vn/login"
ACCOUNT_MANAGEMENT_URL = "https://admin.odakyu.bravesoft.vn/account-management"


class AccountManagementPage:
    def __init__(self, page: Page):
        self.page = page

        # --- Main page ---
        self.new_account_btn = page.locator("button.common-submit-btn.primary")

        # --- Modal (opens after clicking 新規追加) ---
        self.modal = page.locator(".modify-account-modal-content")
        self.modal_title = page.locator(".header-modal")

        # Form inputs inside modal
        self.account_name_input = page.locator("input[name='userName']")
        self.email_input = page.locator(".modal-content input[name='email']")
        self.password_input = page.locator("input[name='password'].inputPassword")

        # Permission multiselect
        self.permission_multiselect = self.modal.locator(".multiselect").first
        self.permission_caret = self.modal.locator(".multiselect-caret").first
        self.permission_options = self.modal.locator(".multiselect-options").first
        self.permission_selected_label = self.modal.locator(".multiselect .multiselect-single-label").first

        # チケット組成時のポイント付与パラメータの変更権限 (appears after selecting テナント管理者)
        self.ticket_permission_label = page.locator(".label-title").filter(has_text="チケット組成時のポイント付与パラメータの変更権限")
        self.radio_yu = page.locator("#authority1")         # 有
        self.radio_mu = page.locator("#authority2")         # 無
        self.label_yu = page.locator("label[for='authority1']")
        self.label_mu = page.locator("label[for='authority2']")

        # Modal action buttons
        self.cancel_btn = self.modal.get_by_text("キャンセル")
        self.save_btn = self.modal.locator("button.common-submit-btn.primary")

    def navigate(self):
        self.page.goto(ACCOUNT_MANAGEMENT_URL)
        self.page.wait_for_load_state("networkidle")

    def open_new_account_modal(self):
        self.new_account_btn.click()
        self.page.wait_for_timeout(800)

    def select_permission(self, option_text: str):
        self.permission_multiselect.click()
        self.page.wait_for_timeout(500)
        self.modal.get_by_text(option_text, exact=True).click()
        self.page.wait_for_timeout(500)

    def is_permission_initial_blank(self) -> bool:
        label = self.permission_selected_label
        return not label.is_visible() or label.inner_text().strip() == ""
