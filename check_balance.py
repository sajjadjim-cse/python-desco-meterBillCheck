import requests
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def fetch_data():
    ACCOUNT_NO = os.environ["ACCOUNT_NO"]
    URL = "https://prepaid.desco.org.bd/api/tkdes/customer/getBalance"
    params = {'accountNo': ACCOUNT_NO}

    try:
        res = requests.get(url=URL, params=params, verify=False)
        data = res.json()
        inner_data = data.get("data")
        if inner_data is not None:
            balance = inner_data.get("balance")
            currentMonthConsumption = inner_data.get("currentMonthConsumption")
            readingTime = inner_data.get("readingTime")
            return balance, currentMonthConsumption , readingTime
        else:
            return None
    except Exception as err:
        print(f"Could not fetch, {err}")
        return None


def telegram_notify(balance, currentMonthConsumption , readingTime):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False, "Telegram not configured (TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID)"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, json={
                          "chat_id": chat_id, "text": f"⚡️⚡️⚡️Desco Current Bill⚡️⚡️⚡️\n💁‍♂️S.M. SAJJAD HOSSAIN JIM \n⏦Account Number : {os.environ['ACCOUNT_NO']}\nUsed Balance this Month :{currentMonthConsumption}\nThe current desco balance is {balance}\nReading Time: {readingTime}"}, timeout=20)
        if r.ok:
            return True, "Telegram sent"
        return False, f"Telegram failed: HTTP {r.status_code} {r.text}"
    except Exception as e:
        return False, f"Telegram failed: {e}"


def send_notification(balance, currentMonthConsumption, readingTime):
    res = telegram_notify(balance, currentMonthConsumption, readingTime)
    print(res)


def main():
    # balance = fetch_data()
    balance, currentMonthConsumption, readingTime = fetch_data()
    if balance is not None:
        send_notification(balance, currentMonthConsumption, readingTime)


if __name__ == "__main__":
    main()