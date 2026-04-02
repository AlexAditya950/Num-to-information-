# 📱 Number Info Bot

Ek powerful **Phone Number Information** tool jo **Telegram Bot** aur **Web Dashboard** dono ke saath kaam karta hai.

Number daalne par yeh deta hai:
- Valid hai ya nahi
- Country + City/Region
- Telecom Provider / Carrier (Jio, Airtel, Vodafone etc.)
- Timezone
- Formatted Number

### Features
- Telegram Bot Support (inline aur private chat dono)
- Beautiful Web Interface
- REST API endpoint bhi available
- Easy config via environment variables
- Free Heroku deployment ready

---

### Configuration (Environment Variables)

Deploy karne se pehle yeh variables set karna **zaruri** hai:

| Variable              | Description                              | Example / Required                  |
|-----------------------|------------------------------------------|-------------------------------------|
| `BOT_TOKEN`           | Telegram Bot Token (BotFather se)       | `7123456789:AAFxxxxxxxxxxxxxxxx`   |
| `API_ID`              | Telegram API ID (my.telegram.org)       | `12345678`                         |
| `API_HASH`            | Telegram API Hash                        | `0123456789abcdef0123456789abcdef` |
| `OWNER_ID`            | Aapka Telegram User ID (Owner)          | `987654321`                        |
| `PORT`                | Heroku ke liye (auto set hota hai)      | `5000` (default)                   |

**Note:**  
- Agar sirf **Web Dashboard** chahiye toh `BOT_TOKEN`, `API_ID`, `API_HASH`, `OWNER_ID` ko empty chhod sakte ho.  
- Bot fully use karne ke liye upar wale saare variables daalna padega.

---

### Local Setup & Testing

```bash
git clone <your-repo>
cd number-info-app

# Virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Environment variables set karo
export BOT_TOKEN=your_bot_token
export API_ID=your_api_id
export API_HASH=your_api_hash
export OWNER_ID=your_owner_id

python app.py
