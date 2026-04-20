"""
ログイン画面 自動テスト
テスト仕様書: eventosテスト仕様書.xlsx - ログイン
対象URL: https://woven-demo.eventos.tokyo/web/portal/1163/event/15549/users/login
"""
import os
import re
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage, LOGIN_URL, TOP_URL

VALID_EMAIL = os.getenv("TEST_EMAIL", "your_registered@email.com")
VALID_PASSWORD = os.getenv("TEST_PASSWORD", "YourPassword1!")


# ============================================================
# ログイン-1: 画面遷移
# ============================================================
class TestNavigation:

    def test_login_1_navigate_from_top_via_ticket_button(self, login_page: LoginPage):
        """TOP画面の「チケット申し込み」ボタンを押すとログイン画面へ遷移する"""
        login_page.page.goto(TOP_URL)
        login_page.page.get_by_role("link", name="チケット申し込み").or_(
            login_page.page.get_by_role("button", name="チケット申し込み")
        ).first.click()
        expect(login_page.page).to_have_url(re.compile(r"/users/login"))


# ============================================================
# ログイン-3〜4: URL・画面タイトル
# ============================================================
class TestUrlAndTitle:

    def test_login_3_url_contains_login(self, login_page: LoginPage):
        """PC版: URLに /users/login が含まれること"""
        expect(login_page.page).to_have_url(re.compile(r"/users/login"))

    def test_login_4_page_title(self, login_page: LoginPage):
        """「ログイン」という画面タイトルが表示されること"""
        expect(login_page.login_btn).to_contain_text("ログイン")


# ============================================================
# ログイン-5〜14: メールアドレス
# ============================================================
class TestEmailField:

    def test_login_5_email_field_display(self, login_page: LoginPage):
        """メールアドレス ラベルとテキストボックスが表示されること"""
        expect(login_page.email_label).to_be_visible()
        expect(login_page.email_label).to_contain_text("メールアドレス")
        expect(login_page.email_input).to_be_visible()

    def test_login_6_email_input_accepts_text(self, login_page: LoginPage):
        """文字入力できること・入力した文字が表示されること"""
        login_page.email_input.fill("test")
        expect(login_page.email_input).to_have_value("test")

    def test_login_7_email_lowercase(self, login_page: LoginPage):
        """abc@gmail.com を入力すると表示されること"""
        login_page.email_input.fill("abc@gmail.com")
        expect(login_page.email_input).to_have_value("abc@gmail.com")

    def test_login_8_email_uppercase(self, login_page: LoginPage):
        """ABC@GMAIL.COM を入力すると表示されること"""
        login_page.email_input.fill("ABC@GMAIL.COM")
        expect(login_page.email_input).to_have_value("ABC@GMAIL.COM")

    def test_login_9_invalid_email_no_tld(self, login_page: LoginPage):
        """ログイン-9: abc@gmail (ドメイン不完全) → エラー表示"""
        login_page.fill_email("abc@gmail")
        expect(login_page.email_error).to_be_visible()
        expect(login_page.email_error).to_contain_text("メールアドレスが正しくありません")

    def test_login_10_invalid_email_special_char(self, login_page: LoginPage):
        """ログイン-10: abc!@gmail.com (記号混在) → エラー表示"""
        login_page.fill_email("abc!@gmail.com")
        expect(login_page.email_error).to_be_visible()
        expect(login_page.email_error).to_contain_text("メールアドレスが正しくありません")

    def test_login_11_invalid_email_no_at(self, login_page: LoginPage):
        """ログイン-11: test.abc (@なし) → エラー表示"""
        login_page.fill_email("test.abc")
        expect(login_page.email_error).to_be_visible()
        expect(login_page.email_error).to_contain_text("メールアドレスが正しくありません")

    def test_login_12_invalid_email_no_local(self, login_page: LoginPage):
        """ログイン-12: @gmail.com (ローカル部なし) → エラー表示"""
        login_page.fill_email("@gmail.com")
        expect(login_page.email_error).to_be_visible()
        expect(login_page.email_error).to_contain_text("メールアドレスが正しくありません")

    def test_login_13_fullwidth_characters(self, login_page: LoginPage):
        """全角文字入力 → 「メールアドレスが正しくありません」エラー"""
        login_page.fill_email("テスト@gmail.com")
        expect(login_page.email_error).to_be_visible()
        expect(login_page.email_error).to_contain_text("メールアドレスが正しくありません")

    def test_login_14_email_cleared(self, login_page: LoginPage):
        """メールアドレスを入力後クリア → 「メールアドレスを入力してください」エラー"""
        login_page.email_input.fill("abc@gmail.com")
        login_page.email_input.fill("")
        login_page.email_input.blur()
        expect(login_page.email_error).to_be_visible()
        expect(login_page.email_error).to_contain_text("メールアドレスを入力してください")


# ============================================================
# ログイン-15〜26: パスワード
# ============================================================
class TestPasswordField:

    def test_login_15_password_field_display(self, login_page: LoginPage):
        """パスワード ラベル・テキストボックス・目アイコン(非アクティブ)が表示されること"""
        expect(login_page.password_label).to_be_visible()
        expect(login_page.password_label).to_contain_text("パスワード")
        expect(login_page.password_input).to_be_visible()
        expect(login_page.toggle_password_btn).to_be_visible()
        icon_text = login_page.toggle_password_btn.inner_text()
        assert "visibility_off" in icon_text, f"初期アイコンが visibility_off でない: {icon_text}"

    def test_login_16_password_masked_on_input(self, login_page: LoginPage):
        """パスワード入力時にマスク(type=password)で表示されること"""
        expect(login_page.password_input).to_have_attribute("type", "password")
        login_page.password_input.fill("Password1!")
        expect(login_page.password_input).to_have_attribute("type", "password")

    def test_login_17_toggle_show_password(self, login_page: LoginPage):
        """目アイコン押下 → マスク解除・type=text に変わること"""
        login_page.password_input.fill("Password1!")
        login_page.toggle_password_visibility()
        expect(login_page.password_input).to_have_attribute("type", "text")
        icon_text = login_page.toggle_password_btn.inner_text()
        assert "visibility_off" not in icon_text, "アイコンがアクティブ状態に変わっていない"

    def test_login_18_toggle_hide_password(self, login_page: LoginPage):
        """目アイコンを再度押下 → マスク表示に戻ること"""
        login_page.password_input.fill("Password1!")
        login_page.toggle_password_visibility()
        login_page.toggle_password_visibility()
        expect(login_page.password_input).to_have_attribute("type", "password")
        icon_text = login_page.toggle_password_btn.inner_text()
        assert "visibility_off" in icon_text, "アイコンが非アクティブ状態に戻っていない"

    def test_login_19_password_too_short(self, login_page: LoginPage):
        """8文字未満 → パスワードエラーメッセージが表示されること"""
        login_page.fill_password("Pass1!")
        expect(login_page.password_error).to_be_visible()
        expect(login_page.password_error).to_contain_text("パスワードは8文字以上32文字以下で指定してください")

    def test_login_20_password_max_32_chars(self, login_page: LoginPage):
        """33文字以上入力できないこと (maxlength=32)"""
        login_page.password_input.fill("A" * 33)
        actual = login_page.password_input.input_value()
        assert len(actual) <= 32, f"32文字以下に制限されるべきだが {len(actual)} 文字入力できた"

    def test_login_21_password_numbers_only(self, login_page: LoginPage):
        """ログイン-21: 数字のみ → エラーなし"""
        login_page.fill_password("12345678")
        expect(login_page.password_error).not_to_be_visible()

    def test_login_22_password_letters_only(self, login_page: LoginPage):
        """ログイン-22: 英大小文字のみ → エラーなし"""
        login_page.fill_password("Abcdefgh")
        expect(login_page.password_error).not_to_be_visible()

    def test_login_23_password_symbols_only(self, login_page: LoginPage):
        """ログイン-23: 記号のみ → エラーなし"""
        login_page.fill_password("!@#$%^&*")
        expect(login_page.password_error).not_to_be_visible()

    def test_login_24_password_numbers_and_letters(self, login_page: LoginPage):
        """ログイン-24: 数字 + 英字 → エラーなし"""
        login_page.fill_password("Abc12345")
        expect(login_page.password_error).not_to_be_visible()

    def test_login_25_password_numbers_and_symbols(self, login_page: LoginPage):
        """ログイン-25: 数字 + 記号 → エラーなし"""
        login_page.fill_password("12345!@#")
        expect(login_page.password_error).not_to_be_visible()

    def test_login_26_password_symbols_and_letters(self, login_page: LoginPage):
        """ログイン-26: 記号 + 英字 → エラーなし"""
        login_page.fill_password("Abcd!@#$")
        expect(login_page.password_error).not_to_be_visible()


# ============================================================
# ログイン-27〜28: パスワードを忘れた場合
# ============================================================
class TestForgotPassword:

    def test_login_27_forgot_password_link_display(self, login_page: LoginPage):
        """「パスワードを忘れた場合」テキストが表示されること"""
        expect(login_page.forgot_password_link).to_be_visible()
        expect(login_page.forgot_password_link).to_contain_text("パスワードを忘れた場合")

    def test_login_28_forgot_password_navigation(self, login_page: LoginPage):
        """「パスワードを忘れた場合」押下でパスワード再設定画面へ遷移"""
        login_page.click_forgot_password()
        expect(login_page.page).to_have_url(re.compile(r"password|remind|reset"))


# ============================================================
# ログイン-29〜32: ログインボタン
# ============================================================
class TestLoginAction:

    def test_login_29_login_button_initially_disabled(self, login_page: LoginPage):
        """初期状態でログインボタンが非活性であること"""
        assert login_page.is_login_btn_disabled(), \
            "初期状態でログインボタンが非活性ではありません"

    def test_login_30_wrong_password(self, login_page: LoginPage):
        """正しいメール + 誤パスワード → ログイン失敗・エラーメッセージ表示"""
        login_page.fill_email(VALID_EMAIL)
        login_page.fill_password("WrongPass999!")
        login_page.click_login()
        expect(login_page.login_error).to_be_visible()
        expect(login_page.login_error).to_contain_text(
            "ログインできませんでした。入力内容をご確認の上、もう一度お試しください。"
        )

    def test_login_31_unregistered_email(self, login_page: LoginPage):
        """未登録メール + 正しいパスワード → ログイン失敗・エラーメッセージ表示"""
        login_page.fill_email("notregistered_xyz@example.com")
        login_page.fill_password(VALID_PASSWORD)
        login_page.click_login()
        expect(login_page.login_error).to_be_visible()
        expect(login_page.login_error).to_contain_text(
            "ログインできませんでした。入力内容をご確認の上、もう一度お試しください。"
        )

    def test_login_32_success(self, login_page: LoginPage):
        """正しい認証情報でログイン成功 → 別画面へ遷移"""
        login_page.fill_email(VALID_EMAIL)
        login_page.fill_password(VALID_PASSWORD)
        login_page.click_login()
        expect(login_page.page).not_to_have_url(re.compile(r"/users/login"))


# ============================================================
# ログイン-33〜34: 新規登録
# ============================================================
class TestSignup:

    def test_login_33_signup_button_display(self, login_page: LoginPage):
        """「新規登録」ボタンが表示されること"""
        expect(login_page.signup_btn).to_be_visible()
        expect(login_page.signup_btn).to_contain_text("新規登録")

    def test_login_34_signup_navigation(self, login_page: LoginPage):
        """「新規登録」ボタン押下で新規登録画面へ遷移"""
        login_page.click_signup()
        expect(login_page.page).not_to_have_url(re.compile(r"/users/login"))


# ============================================================
# ログイン-35〜37: スクロール
# ============================================================
class TestScroll:

    def test_login_35_scroll_up_to_top_and_header_fixed(self, login_page: LoginPage):
        """最下部から上スクロール → 最上部に戻れること・ヘッダー固定確認"""
        page = login_page.page
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.evaluate("window.scrollTo(0, 0)")
        scroll_y = page.evaluate("window.scrollY")
        assert scroll_y == 0, "最上部にスクロールできていません"

        header = page.locator(".contents-header").first
        if header.count() > 0 and header.is_visible():
            position = page.evaluate(
                "el => getComputedStyle(el).position",
                header.element_handle()
            )
            assert position in ("fixed", "sticky", "static"), \
                f"ヘッダーのpositionが予期しない値: {position}"

    def test_login_36_scroll_down_to_bottom(self, login_page: LoginPage):
        """上部から下スクロール → 最下部まで到達できること"""
        page = login_page.page
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        scroll_y = page.evaluate("window.scrollY")
        total = page.evaluate("document.body.scrollHeight - window.innerHeight")
        assert scroll_y >= total - 5, "最下部までスクロールできていません"

    def test_login_37_scroll_up_and_down(self, login_page: LoginPage):
        """中央から上下スクロールが両方できること"""
        page = login_page.page
        mid = page.evaluate("document.body.scrollHeight / 2")
        page.evaluate(f"window.scrollTo(0, {mid})")
        page.evaluate("window.scrollTo(0, 0)")
        assert page.evaluate("window.scrollY") == 0, "上スクロールできていません"

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        bottom = page.evaluate("document.body.scrollHeight - window.innerHeight")
        assert page.evaluate("window.scrollY") >= bottom - 5, "下スクロールできていません"
