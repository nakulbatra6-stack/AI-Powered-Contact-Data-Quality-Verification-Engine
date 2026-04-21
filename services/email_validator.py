import re

DISPOSABLE_DOMAINS = ["tempmail.com", "10minutemail.com"]

def validate_email(email):
    score = 0
    reasons = []

    # Format check
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, str(email)):
        score += 30
    else:
        reasons.append("Invalid format")

    # Domain check
    if "@" in str(email):
        domain = email.split("@")[1]
        if "." in domain:
            score += 30
        else:
            reasons.append("Invalid domain")

        if domain in DISPOSABLE_DOMAINS:
            reasons.append("Disposable email")
        else:
            score += 20

    return score, ", ".join(reasons)
    