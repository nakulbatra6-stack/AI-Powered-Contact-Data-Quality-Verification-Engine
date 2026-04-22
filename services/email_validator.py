import re
import dns.resolver
import smtplib

DISPOSABLE_DOMAINS = set([
    "tempmail.com", "10minutemail.com", "mailinator.com",
    "guerrillamail.com", "yopmail.com"
])
TRUSTED_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com"]
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Google DNS


def validate_email(email):
    score = 0
    reasons = []

    email = str(email)

    # -------------------
    # 1. Format Check
    # -------------------
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        score += 20
    else:
        reasons.append("Invalid format")
        return score, ", ".join(reasons)

    # -------------------
    # 2. Extract Domain
    # -------------------
    domain = email.split("@")[1]

    # -------------------
    # 3. Disposable Check
    # -------------------
    if domain in DISPOSABLE_DOMAINS:
        reasons.append("Disposable email")
    else:
        score += 10

    # -------------------
    # 4. MX Record Check
    # -------------------
    if has_mx_record(domain):
        score += 30
    else:
        reasons.append("No MX record")
        return score, ", ".join(reasons)

    # -------------------
    # 5. SMTP Check
    # -------------------
    if domain in TRUSTED_DOMAINS:
        score += 25  # assume valid
    elif smtp_check(email, domain):
        score += 25
    else:
        reasons.append("SMTP validation failed")

    # -------------------
    # 6. Domain Reputation
    # -------------------
    if domain in TRUSTED_DOMAINS:
        score += 15
    else:
        score += 5  # neutral domains

    return score, ", ".join(reasons)

def has_mx_record(domain):
    try:
        answers = resolver.resolve(domain, 'MX')
        return True
    except:
        return False

def smtp_check(email, domain):
    try:
        mx_records = resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange)

        server = smtplib.SMTP(timeout=5)
        server.connect(mx_record)

        server.helo()
        server.mail('test@example.com')
        code, _ = server.rcpt(email)
        server.quit()

        return code == 250
    except:
        return False