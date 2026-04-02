import os
from typing import Dict, Optional


class ForgotPasswordHelp:
    """Centralized forgot-password content and reset page lookup helpers."""

    _RESET_PAGE_FALLBACK = "http://localhost:3000/login"

    _RESPONSES: Dict[str, str] = {
        "reset_steps": (
            "Here is how to reset your password:\n"
            "1. Open the login page.\n"
            "2. Click the Forgot Password or Reset Password option.\n"
            "3. Enter the email address connected to your account.\n"
            "4. Submit the request.\n"
            "5. Check your email for the password reset link.\n"
            "6. Open the link and create a new password.\n"
            "7. Return to the login page and sign in with your new password."
        ),
        "reset_page": (
            "You can start the password reset process from the login page. "
            "Look for the Forgot Password or Reset Password option there."
        ),
        "reset_email_sent": (
            "If you requested a password reset, a reset email should be sent to your inbox shortly.\n\n"
            "Please check your inbox carefully, and also make sure you are checking the same email address linked to your account."
        ),
        "check_spam": (
            "If you do not see the reset email, please try these checks:\n"
            "1. Look in your spam, junk, promotions, or updates folders.\n"
            "2. Confirm that you entered the correct email address.\n"
            "3. Wait a few minutes in case the email is delayed.\n"
            "4. Request another reset email if needed."
        ),
        "expired_link": (
            "If your password reset link has expired or no longer works, request a new reset link from the login page.\n\n"
            "Use only the most recent reset email, because older links may stop working after a new request is made."
        ),
        "password_requirements": (
            "When creating a new password, make sure it follows the website's password rules.\n\n"
            "A strong password usually includes a mix of uppercase and lowercase letters, numbers, and special characters, and should be long enough to meet the minimum length requirement. If the site rejects your new password, try a stronger one and avoid reusing your old password."
        ),
        "recover_username_or_email": (
            "If you forgot your username or the email address registered on your account, try searching your inbox for past messages from the website or church system.\n\n"
            "Check for welcome emails, account notifications, or password reset emails that may show which email address you used. If you still cannot find it, please contact support so they can help verify your account."
        ),
        "no_access_to_email_or_phone": (
            "If you no longer have access to your registered email address or phone number, you may need manual account recovery.\n\n"
            "Please contact support or send a message through the Contact page and explain that your email or phone number has changed. Be ready to provide account details they can use to verify your identity."
        ),
        "support_escalation": (
            "If self-service password reset is still not working, please contact church support or the website administrator for manual account recovery.\n\n"
            "Let them know whether the reset email did not arrive, the link expired, or the new password was not accepted so they can help more quickly."
        ),
    }

    @staticmethod
    def get_help(topic: str) -> Optional[str]:
        return ForgotPasswordHelp._RESPONSES.get(topic)

    @staticmethod
    def get_reset_page_url(db) -> str:
        try:
            response = (
                db.client.table("website_pages")
                .select("path, url")
                .or_("path.eq./login,path.eq./forgot-password,slug.ilike.%login%,slug.ilike.%password%,title.ilike.%login%,title.ilike.%password%")
                .limit(1)
                .execute()
            )
            if response.data:
                page = response.data[0]
                if page.get("url"):
                    return page["url"]
                if page.get("path"):
                    base_url = os.getenv("SITE_BASE_URL", "http://localhost:3000")
                    return f"{base_url}{page['path']}"
        except Exception as e:
            print(f"[ERROR] Could not fetch forgot-password page URL: {e}")
        return ForgotPasswordHelp._RESET_PAGE_FALLBACK
