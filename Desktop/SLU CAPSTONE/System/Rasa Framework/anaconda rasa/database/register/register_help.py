import os
from typing import Dict, Optional


class RegisterHelp:
    """Centralized sign-up help content and registration page lookup helpers."""

    _REGISTER_PAGE_FALLBACK = "http://localhost:3000/register"

    _RESPONSES: Dict[str, str] = {
        "registration_steps": (
            "Here is how to register an account:\n"
            "1. Open the registration or sign-up page.\n"
            "2. Choose your registration method.\n"
            "3. You can continue with Google or register using a username, email, and password.\n"
            "4. Review the information you entered.\n"
            "5. Submit the sign-up form.\n"
            "6. Complete email or phone verification if the website asks for it.\n"
            "7. After verification, sign in to your new account."
        ),
        "registration_methods": (
            "There are two ways to register on the website:\n"
            "1. Continue with Google or Gmail for faster sign-up.\n"
            "2. Register manually using a username, email address, and password.\n\n"
            "If you want to use your Gmail account, choose the Google sign-up option. If you prefer a regular website account, use the username and password registration form."
        ),
        "required_information": (
            "Registration usually requires basic account details such as your name, email address, username, and a password.\n\n"
            "If you sign up with Google or Gmail, some details may be filled in automatically. Some sign-up forms may also ask for a phone number or other profile information, depending on how the website is set up."
        ),
        "eligibility_requirements": (
            "Eligibility to register depends on the website's sign-up policy.\n\n"
            "In most cases, anyone allowed by the church or website system can create an account. If sign-up is restricted to members, verified users, or invited users, please follow the instructions provided on the registration page or contact support for confirmation."
        ),
        "email_verification": (
            "After sign-up, the website may send a verification email so you can confirm your account.\n\n"
            "Open the verification email and click the provided link or enter the code if one is required. If you do not receive the message, check your spam or junk folder and make sure you used the correct email address."
        ),
        "duplicate_email": (
            "If the website says your email already exists, it usually means an account has already been created with that email address.\n\n"
            "Try signing in instead, or use the Forgot Password option if you cannot access the account. If you believe this is an error, contact support for assistance."
        ),
        "password_requirements": (
            "During sign-up, your password needs to meet the website's password rules.\n\n"
            "A strong password usually includes uppercase and lowercase letters, numbers, and special characters, and should be long enough to satisfy the minimum length requirement."
        ),
        "failed_registration": (
            "If your registration did not finish successfully, try these steps:\n"
            "1. Review the form for missing or incorrect details.\n"
            "2. Make sure your email address is valid.\n"
            "3. Check that your password meets the required rules.\n"
            "4. Refresh the page and try again.\n"
            "5. If the form still fails, contact support or use the Contact page."
        ),
        "verify_email_or_phone": (
            "To verify your account, follow the verification instructions sent to your email address or phone number.\n\n"
            "If the website uses email verification, click the link in the message. If it uses phone verification, enter the code sent to your mobile number."
        ),
        "resend_verification": (
            "If you did not receive the verification email or code, use the resend verification option on the sign-up or verification screen.\n\n"
            "Also check your spam or junk folder, confirm your email address or phone number is correct, and wait a few minutes in case delivery is delayed."
        ),
    }

    @staticmethod
    def get_help(topic: str) -> Optional[str]:
        return RegisterHelp._RESPONSES.get(topic)

    @staticmethod
    def get_register_page_url(db) -> str:
        try:
            response = (
                db.client.table("website_pages")
                .select("path, url")
                .or_("path.eq./register,path.eq./signup,slug.ilike.%register%,slug.ilike.%sign-up%,slug.ilike.%signup%,title.ilike.%register%,title.ilike.%sign up%")
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
            print(f"[ERROR] Could not fetch registration page URL: {e}")
        return RegisterHelp._REGISTER_PAGE_FALLBACK
