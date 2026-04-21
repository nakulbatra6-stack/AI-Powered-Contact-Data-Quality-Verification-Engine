from utils.file_handler import load_file, save_file
from services.email_validator import validate_email
from services.phone_validator import validate_phone
from services.scoring import overall_score
from services.cleaner import clean_data

INPUT_FILE = "data/sample.xlsx"
OUTPUT_FILE = "output/result.xlsx"

def process():
    df = load_file(INPUT_FILE)
    df = clean_data(df)

    email_scores = []
    email_reasons = []

    phone_scores = []
    phone_reasons = []

    overall_scores = []

    for _, row in df.iterrows():
        email = row.get("Email", "")
        phone = row.get("Phone", "")

        e_score, e_reason = validate_email(email)
        p_score, p_reason = validate_phone(phone)

        total = overall_score(e_score, p_score)

        email_scores.append(e_score)
        email_reasons.append(e_reason)

        phone_scores.append(p_score)
        phone_reasons.append(p_reason)

        overall_scores.append(total)

    df["Email Score"] = email_scores
    df["Email Issues"] = email_reasons

    df["Phone Score"] = phone_scores
    df["Phone Issues"] = phone_reasons

    df["Overall Score"] = overall_scores

    save_file(df, OUTPUT_FILE)
    print("✅ Processing complete. Check output/result.xlsx")

if __name__ == "__main__":
    process()
    print("✅ All done.")