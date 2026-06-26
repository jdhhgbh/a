import requests
from bs4 import BeautifulSoup
import random
import string
import sys

def generate_random_string(length=6):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def main():
    url = "https://protoiptv.com/2026-iptvtrial-free-pro/"
    ajax_url = "https://protoiptv.com/wp-admin/admin-ajax.php"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "Referer": url,
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://protoiptv.com"
    }
    
    session = requests.Session()
    
    try:
        print("1. جاري دخول الموقع وجلب التوكن الحقيقي...")
        response = session.get(url, headers={"User-Agent": headers["User-Agent"]})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        nonce = ""
        nonce_tag = soup.find("input", attrs={"name": "wpforms[nonce]"})
        if nonce_tag:
            nonce = nonce_tag.get("value", "")
        
        random_part = generate_random_string(6)
        email = f"zwri+{random_part}@outlook.sa"
        name = f"Ismail_{generate_random_string(4)}"
        
        # بناء الحقول المطابقة تماماً لطلب الـ AJAX مع تفعيل قنوات الـ Adult
        form_data = {
            "wpforms[id]": "541",
            "wpforms[author]": "1",
            "wpforms[fields][1]": name,
            "wpforms[fields][34]": "Saudi Arabia",
            "wpforms[fields][2]": email,
            "wpforms[fields][5]": "Android Box",
            "wpforms[fields][8]": "Iptv Smarters Pro",
            "wpforms[fields][14]": "All Playlist",
            "wpforms[fields][24]": "Yes",  # تم التعديل إلى Yes لفتح قنوات الـ Adult 😉
            "wpforms[fields][23]": "Trial Request with adult channels",
            "wpforms[fields][39]": "",  # مصيدة البوتات تترك فارغة تماماً
            "action": "wpforms_submit",
            "page_id": "1342",
            "wpforms[nonce]": nonce
        }
        
        print(f"-> جاري إرسال الطلب للإيميل: {email}")
        post_response = session.post(ajax_url, data=form_data, headers=headers)
        
        print(f"-> رد السيرفر: {post_response.text}")
        
        if "success" in post_response.text.lower():
            print("\n✅ تم التسجيل بنجاح ملوّز وتفعيل الباقة الكاملة! شيك على بريدك الآن.")
        else:
            print("\n⚠️ تم الإرسال ولكن تحقق من رد السيرفر أعلاه.")
            
    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")

if __name__ == "__main__":
    main()
