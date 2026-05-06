"""
新規アカウント追加 自動テスト
対象URL: https://admin.odakyu.bravesoft.vn/account-management
"""
import re
from playwright.sync_api import Page, expect
from pages.account_management_page import AccountManagementPage, ACCOUNT_MANAGEMENT_URL


# ============================================================
# 新規アカウント追加-1〜2: 画面タイトル・URL
# ============================================================
class TestPageInfo:

    def test_account_1_modal_title(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-1: 「新規アカウント追加」の画面タイトルが表示されること"""
        expect(account_management_page.modal_title).to_be_visible()
        expect(account_management_page.modal_title).to_contain_text("新規アカウント追加")

    def test_account_2_url_contains_account_management(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-2: URLに /account-management が含まれること"""
        expect(account_management_page.page).to_have_url(re.compile(r"/account-management"))


# ============================================================
# 新規アカウント追加-3〜4: アカウント名
# ============================================================
class TestAccountNameField:

    def test_account_3_account_name_label(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-3: 「アカウント名 * （255文字以内）」ラベルが表示されること"""
        label = account_management_page.modal.locator(".label-title").filter(has_text="アカウント名")
        expect(label).to_be_visible()
        expect(label).to_contain_text("アカウント名")
        expect(label).to_contain_text("255文字以内")

    def test_account_4_account_name_input(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-4: アカウント名ボックスに文字入力できること"""
        account_management_page.account_name_input.fill("テストアカウント")
        expect(account_management_page.account_name_input).to_have_value("テストアカウント")


# ============================================================
# 新規アカウント追加-5〜6: メールアドレス
# ============================================================
class TestEmailField:

    def test_account_5_email_label(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-5: 「メールアドレス」ラベルが表示されること"""
        label = account_management_page.modal.locator(".label-title").filter(has_text="メールアドレス")
        expect(label).to_be_visible()
        expect(label).to_contain_text("メールアドレス")

    def test_account_6_email_input(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-6: 正しいメールアドレスを入力すると表示されること"""
        account_management_page.email_input.fill("trucly@bravesoft-vn.com.vn")
        expect(account_management_page.email_input).to_have_value("trucly@bravesoft-vn.com.vn")


# ============================================================
# 新規アカウント追加-7〜9: パスワード
# ============================================================
class TestPasswordField:

    def test_account_7_password_label(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-7: 「パスワード *（半角英数字 8文字以上32文字以内）」ラベルが表示されること"""
        label = account_management_page.modal.locator(".label-title").filter(has_text="パスワード")
        expect(label).to_be_visible()
        expect(label).to_contain_text("パスワード")
        expect(label).to_contain_text("8文字以上32文字以内")

    def test_account_8_password_placeholder(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-8: パスワードフィールドに placeholder「**********」が表示されること"""
        expect(account_management_page.password_input).to_have_attribute("placeholder", "**********")

    def test_account_9_password_masked_input(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-9: パスワード入力できること・マスク表示されること"""
        expect(account_management_page.password_input).to_have_attribute("type", "password")
        account_management_page.password_input.fill("Password1!")
        expect(account_management_page.password_input).to_have_attribute("type", "password")


# ============================================================
# 新規アカウント追加-10〜13: 権限セレクトボックス
# ============================================================
class TestPermissionSelect:

    def test_account_10_permission_select_display(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-10: 権限セレクトボックス・プルダウンアイコン・初期表示空白が表示されること"""
        expect(account_management_page.permission_multiselect).to_be_visible()
        expect(account_management_page.permission_caret).to_be_visible()
        assert account_management_page.is_permission_initial_blank(), \
            "権限の初期表示が空白ではありません"

    def test_account_11_select_master_admin(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-11: マスター管理者を選択すると表示されること"""
        account_management_page.select_permission("マスター管理者")
        expect(account_management_page.permission_multiselect).to_contain_text("マスター管理者")

    def test_account_12_select_tenant_admin(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-12: テナント管理者を選択すると表示されること"""
        account_management_page.select_permission("テナント管理者")
        expect(account_management_page.permission_multiselect).to_contain_text("テナント管理者")

    def test_account_13_cannot_select_both_permissions(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-13: マスター管理者とテナント管理者を同時選択できないこと"""
        # First clear any existing selection by closing modal and reopening
        account_management_page.cancel_btn.click()
        account_management_page.page.wait_for_timeout(500)
        account_management_page.open_new_account_modal()
        
        account_management_page.select_permission("マスター管理者")
        account_management_page.select_permission("テナント管理者")
        # single-select: 選択済みラベルにはテナント管理者のみ表示される
        selected = account_management_page.permission_selected_label
        expect(selected).to_contain_text("テナント管理者")
        expect(selected).not_to_contain_text("マスター管理者")


# ============================================================
# 新規アカウント追加-14〜17: チケット組成時のポイント付与パラメータの変更権限
# ※ テナント管理者選択後に表示される
# ============================================================
class TestTicketPermission:

    def test_account_14_ticket_permission_label_display(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-14: 「チケット組成時のポイント付与パラメータの変更権限」ラベルと有/無が表示されること"""
        account_management_page.select_permission("テナント管理者")
        expect(account_management_page.ticket_permission_label).to_be_visible()
        expect(account_management_page.label_yu).to_be_visible()
        expect(account_management_page.label_yu).to_contain_text("有")
        expect(account_management_page.label_mu).to_be_visible()
        expect(account_management_page.label_mu).to_contain_text("無")

    def test_account_15_select_yu(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-15: 「有」を選択すると選択済みになること"""
        account_management_page.select_permission("テナント管理者")
        account_management_page.label_yu.click()
        expect(account_management_page.radio_yu).to_be_checked()

    def test_account_16_select_mu(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-16: 「無」を選択すると選択済みになること"""
        account_management_page.select_permission("テナント管理者")
        account_management_page.label_mu.click()
        expect(account_management_page.radio_mu).to_be_checked()

    def test_account_17_cannot_select_both_yu_mu(self, account_management_page: AccountManagementPage):
        """新規アカウント追加-17: 「有」と「無」を同時選択できないこと (radio button)"""
        account_management_page.select_permission("テナント管理者")
        account_management_page.label_yu.click()
        account_management_page.label_mu.click()
        # radio button: 最後の選択のみ有効
        expect(account_management_page.radio_mu).to_be_checked()
        expect(account_management_page.radio_yu).not_to_be_checked()
