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
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "Referer": url
    }
    
    session = requests.Session()
    
    try:
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        
        if not form:
            print("لم يتم العثور على الفورم!")
            sys.exit(1)
            
        random_part = generate_random_string(6)
        email = f"zwri+{random_part}@outlook.sa"
        name = f"Ismail_{generate_random_string(4)}"
        
        # تعبئة الحقول بناءً على أرقام WPForms الصحيحة للموقع
        form_data = {
            "wpforms[fields][1]": name,                  # Name
            "wpforms[fields][34]": "Saudi Arabia",       # Country
            "wpforms[fields][2]": email,                 # Email
            "wpforms[fields][5]": "Android Box",          # Device Type
            "wpforms[fields][8]": "Iptv Smarters Pro",   # IPTV Application
            "wpforms[fields][14]": "All Playlist",       # Channels Selection
            "wpforms[fields][24]": "No",                 # Adult Channels
            "wpforms[fields][23]": "Please send the trial", # Note
            "wpforms[fields][39]": "Free Trial Request"   # Single Line Text
        }
        
        # جلب الحقول المخفية التلقائية من الفورم (الـ ID والـ Tokens)
        print("--- جاري تجميع الحقول المخفية ---")
        for input_tag in form.find_all('input'):
            name_attr = input_tag.get('name')
            if name_attr and name_attr not in form_data:
                # التحقق من الراديو أو الـ Checkbox الافتراضي
                if input_tag.get('type') in ['radio', 'checkbox']:
                    if input_tag.has_attr('checked'):
                        form_data[name_attr] = input_tag.get('value', '')
                else:
                    form_data[name_attr] = input_tag.get('value', '')
        
        # طباعة الحقول للتأكد قبل الإرسال
        for k, v in form_data.items():
            print(f"{k}: {v}")

        action = form.get('action', url)
        if not action.startswith('http'):
            action = "https://protoiptv.com" + action if action.startswith('/') else url
                
        print("\nجاري إرسال الطلب الصحيح والمكتمل إلى السيرفر...")
        post_response = session.post(action, data=form_data, headers=headers)
        
        print(f"رمز استجابة الموقع (Status Code): {post_response.status_code}")
        
        if "wpforms-confirmation" in post_response.text or "Thank you" in post_response.text or post_response.status_code == 200:
            print("\n✅ تم إرسال جميع الحقول بنجاح ملوّز! شيك على إيميلك الآن.")
        else:
            print("\n❌ تم الإرسال ولكن قد يكون هناك نقص في التوثيق.")
            
    except Exception as e:
        print(f"حدث خطأ أثناء التنفيذ: {str(e)}")

if __name__ == "__main__":
    main()
