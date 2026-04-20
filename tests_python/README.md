# ログイン画面 Playwright Python テスト

## セットアップ

```bash
pip install pytest playwright pytest-playwright
playwright install chromium
```

## 環境変数

| 変数 | 説明 | デフォルト |
|---|---|---|
| `BASE_URL` | テスト対象URL | `https://eventos.example.com` |
| `TEST_EMAIL` | 有効なテストメールアドレス | `test@example.com` |
| `TEST_PASSWORD` | 有効なテストパスワード | `Password123!` |

## 実行方法

```bash
cd tests_python

# 全テスト実行
BASE_URL=https://your-app.com TEST_EMAIL=your@email.com TEST_PASSWORD=YourPass! pytest

# 特定クラスのみ
pytest test_login.py::TestEmailField -v

# 特定テストID
pytest test_login.py::TestEmailField::test_login_9_to_12_invalid_email_format -v
```

## テストケース対応表

| テストID | クラス | メソッド |
|---|---|---|
| ログイン-1 | TestNavigation | test_login_1_navigate_from_top_via_ticket_button |
| ログイン-3 | TestUrlAndTitle | test_login_3_url_contains_login |
| ログイン-4 | TestUrlAndTitle | test_login_4_page_title |
| ログイン-5 | TestEmailField | test_login_5_email_field_display |
| ログイン-6 | TestEmailField | test_login_6_email_input_accepts_text |
| ログイン-7 | TestEmailField | test_login_7_email_lowercase |
| ログイン-8 | TestEmailField | test_login_8_email_uppercase |
| ログイン-9〜12 | TestEmailField | test_login_9_to_12_invalid_email_format |
| ログイン-13 | TestEmailField | test_login_13_fullwidth_characters |
| ログイン-14 | TestEmailField | test_login_14_email_cleared |
| ログイン-15 | TestPasswordField | test_login_15_password_field_display |
| ログイン-16 | TestPasswordField | test_login_16_password_masked_on_input |
| ログイン-17 | TestPasswordField | test_login_17_toggle_show_password |
| ログイン-18 | TestPasswordField | test_login_18_toggle_hide_password |
| ログイン-19 | TestPasswordField | test_login_19_password_too_short |
| ログイン-20 | TestPasswordField | test_login_20_password_max_32_chars |
| ログイン-21〜26 | TestPasswordField | test_login_21_to_26_password_valid_patterns |
| ログイン-27 | TestForgotPassword | test_login_27_forgot_password_link_display |
| ログイン-28 | TestForgotPassword | test_login_28_forgot_password_navigation |
| ログイン-29 | TestLoginAction | test_login_29_login_button_initially_disabled |
| ログイン-30 | TestLoginAction | test_login_30_wrong_password |
| ログイン-31 | TestLoginAction | test_login_31_unregistered_email |
| ログイン-32 | TestLoginAction | test_login_32_success |
| ログイン-33 | TestSignup | test_login_33_signup_button_display |
| ログイン-34 | TestSignup | test_login_34_signup_navigation |
| ログイン-35 | TestScroll | test_login_35_scroll_up_to_top_and_header_fixed |
| ログイン-36 | TestScroll | test_login_36_scroll_down_to_bottom |
| ログイン-37 | TestScroll | test_login_37_scroll_up_and_down |

> ※ ログイン-2 (デザイン確認) は目視確認のため自動化対象外
