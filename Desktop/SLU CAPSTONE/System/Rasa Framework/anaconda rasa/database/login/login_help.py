import os
from typing import Dict, Optional


class LoginHelp:
    """Centralized login-help content and page lookup helpers."""

    _LOGIN_PAGE_FALLBACK = "http://localhost:3000/login"

    _RESPONSES: Dict[str, str] = {
        "steps": (
            "Here is how you can log in:\n"
            "1. Open the login page.\n"
            "2. Choose your preferred login method.\n"
            "3. You can either continue with Google or sign in using your username or email and password.\n"
            "4. If you see separate member and admin access, choose the correct portal first.\n"
            "5. Complete two-factor verification if a code is required.\n"
            "6. If you forgot your password, use the Forgot Password option before trying again too many times."
        ),
        "login_methods": (
            "There are two ways to log in on the website:\n"
            "1. Continue with Google or Gmail login.\n"
            "2. Sign in using your username or email and password.\n\n"
            "If your account was created with Google, use the Google sign-in option. If your account was created with regular credentials, use your username or email and password."
        ),
        "account_types": (
            "Member login is for regular church members who need access to their personal account features.\n\n"
            "Admin login is for authorized church staff or administrators who manage website content, records, or internal tools.\n\n"
            "If you are unsure which one to use, start with the member login unless the church explicitly gave you admin credentials."
        ),
        "invalid_credentials": (
            "If the website says your credentials are invalid, try these steps:\n"
            "1. Make sure you entered the correct email or username.\n"
            "2. Re-type your password carefully and check Caps Lock.\n"
            "3. Make sure you are using the correct login method. If you normally use Google, choose the Google sign-in button instead of typing a password.\n"
            "4. Try the Forgot Password option if you are not sure about the password.\n"
            "5. If the problem continues, contact the church admin for account checking."
        ),
        "session_timeout": (
            "You may be asked to sign in again when your session expires after inactivity or for security protection.\n\n"
            "This helps keep your account safe, especially on shared or public devices. If this happens often, make sure your browser is not clearing cookies automatically and check whether a Remember Me option is available."
        ),
        "lockout": (
            "If your account was locked after too many failed login attempts, wait a few minutes before trying again.\n\n"
            "Use the password reset option if you think the password is wrong. If the account stays locked, please contact the church administrator so they can help unlock or verify your account."
        ),
        "browser_issues": (
            "If the login page is not loading or the sign-in button is not working, try these steps:\n"
            "1. Refresh the page.\n"
            "2. Open the site in an incognito or private window.\n"
            "3. Clear your browser cache and cookies.\n"
            "4. Disable browser extensions that may block scripts.\n"
            "5. Try a different browser or device.\n"
            "6. Make sure your internet connection is stable."
        ),
        "two_factor": (
            "Two-factor authentication adds an extra security step after you enter your password.\n\n"
            "You may receive a verification code by emaiL. Enter that code on the login screen to finish signing in. If the code does not arrive, wait a moment, request a new one, and make sure your device time is correct if you use an authenticator app."
        ),
        "remember_me": (
            "If you want to stay signed in, look for a Remember Me or Keep Me Signed In option on the login page.\n\n"
            "Use that option only on a private device you trust. Even with it enabled, the website may still sign you out after security updates, browser cookie clearing, or session expiration."
        ),
    }

    @staticmethod
    def get_login_help(topic: str) -> Optional[str]:
        return LoginHelp._RESPONSES.get(topic)

    @staticmethod
    def get_login_page_url(db) -> str:
        try:
            response = (
                db.client.table("website_pages")
                .select("path, url")
                .or_("path.eq./login,slug.ilike.%login%,title.ilike.%login%")
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
            print(f"[ERROR] Could not fetch login page URL: {e}")
        return LoginHelp._LOGIN_PAGE_FALLBACK
