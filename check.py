import csv
import requests
import time

CSV_PATH = "slack_user_list.csv"
MAIL_COLUMN_INDEX = 2

def get_mail_list_slack_csv(file_path):
    mail_list = []

    with open(CSV_PATH, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            mail_list.append(row[MAIL_COLUMN_INDEX])

    return mail_list

def is_leaked(mail_address):
    time.sleep(5)

    endpoint = "https://haveibeenpwned.com/api/v2/breachedaccount/%s" % mail_address
    res = requests.get(endpoint)
    if res.status_code == 429:
        time.sleep(5)
        return is_leaked(mail_address)
    else:
        return res.status_code != 404

if __name__ == "__main__":
    mail_list = get_mail_list_slack_csv(CSV_PATH)
    leaked_mail_list = []

    for idx, mail_address in enumerate(mail_list):
        leaked = is_leaked(mail_address)
        print(idx+1, mail_address, "pwned!" if leaked else "no pwnage found!")
        if leaked:
            leaked_mail_list.append(mail_address)
        time.sleep(5)
    print()

    for mail_address in leaked_mail_list:
        print(mail_address)
