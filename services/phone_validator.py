import phonenumbers

def validate_phone(phone):
    score = 0
    reasons = []

    try:
        parsed = phonenumbers.parse(str(phone), None)

        if phonenumbers.is_valid_number(parsed):
            score += 50
        else:
            reasons.append("Invalid number")

        if phonenumbers.is_possible_number(parsed):
            score += 25

        if parsed.country_code:
            score += 25

    except:
        reasons.append("Parsing failed")

    return score, ", ".join(reasons)