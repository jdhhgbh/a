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
            print("لم يتم العثور على الفورم في الصفحة!")
            sys.exit(1)
            
        random_part = generate_random_string(6)
        email = f"zwri+{random_part}@outlook.sa"
        name = f"Ismail_{generate_random_string(4)}"
        
        form_data = {}
        print("--- جاري تجميع الحقول وتعبئتها ---")
        
        # التقاط جميع المدخلات بما فيها المخفية التابعة لـ Forminator
        for input_tag in form.find_all(['input', 'select', 'textarea']):
            name_attr = input_tag.get('name')
            if not name_attr:
                continue
                
            value_attr = input_tag.get('value', '')
            
            # تعبئة الحقول الأساسية بناءً على الأسماء المتوقعة
            if 'email' in name_attr.lower() or input_tag.get('type') == 'email':
                form_data[name_attr] = email
            elif 'name' in name_attr.lower() and 'form_id' not in name_attr.lower():
                form_data[name_attr] = name
            elif 'country' in name_attr.lower():
                form_data[name_attr] = "Saudi Arabia"
            elif 'device' in name_attr.lower() or 'type' in name_attr.lower():
                form_data[name_attr] = "Android Box"
            elif 'application' in name_attr.lower() or 'iptv' in name_attr.lower():
                form_data[name_attr] = "Iptv Smarters Pro"
            elif 'playlist' in name_attr.lower() or 'channel' in name_attr.lower():
                form_data[name_attr] = value_attr if value_attr else "All Playlist"
            elif 'adult' in name_attr.lower():
                form_data[name_attr] = "No"
            else:
                # الحقول المخفية والـ tokens نأخذ قيمتها الافتراضية كما هي من الموقع
                form_data[name_attr] = value_attr
                
            print(f"{name_attr}: {form_data[name_attr]}")

        action = form.get('action', url)
        if not action.startswith('http'):
            action = "https://protoiptv.com" + action if action.startswith('/') else url
                
        print("\nجاري إرسال الطلب إلى السيرفر...")
        post_response = session.post(action, data=form_data, headers=headers)
        
        print(f"رمز استجابة الموقع (Status Code): {post_response.status_code}")
        print("\n--- أول 500 حرف من رد السيرفر النسيجي ---")
        print(post_response.text[:500])
        
    except Exception as e:
        print(f"حدث خطأ أثناء التنفيذ: {str(e)}")

if __name__ == "__main__":
    main()
