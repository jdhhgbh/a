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
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "Referer": url
    }
    
    session = requests.Session()
    
    try:
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print(f"فشل في الاتصال بالموقع. رمز الحالة: {response.status_code}")
            sys.exit(1)
            
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        if not form:
            print("لم يتم العثور على نموذج التسجيل في الصفحة.")
            sys.exit(1)
            
        random_part = generate_random_string(6)
        email = f"zwri+{random_part}@outlook.sa"
        name = f"User_{generate_random_string(4)}"
        
        print(f"جاري التسجيل باستخدام الإيميل: {email}")
        
        form_data = {}
        for input_tag in form.find_all(['input', 'select', 'textarea']):
            name_attr = input_tag.get('name')
            if not name_attr:
                continue
                
            value_attr = input_tag.get('value', '')
            
            if 'email' in name_attr.lower() or input_tag.get('type') == 'email':
                form_data[name_attr] = email
            elif 'name' in name_attr.lower():
                form_data[name_attr] = name
            elif 'country' in name_attr.lower():
                form_data[name_attr] = "Saudi Arabia"
            elif 'device' in name_attr.lower() or 'type' in name_attr.lower():
                form_data[name_attr] = "Android Box"
            elif 'application' in name_attr.lower() or 'iptv' in name_attr.lower():
                form_data[name_attr] = "Iptv Smarters Pro"
            elif 'playlist' in name_attr.lower() or 'channel' in name_attr.lower():
                if input_tag.get('type') == 'radio' and 'all' in value_attr.lower():
                    form_data[name_attr] = value_attr
                elif input_tag.get('type') != 'radio':
                    form_data[name_attr] = value_attr
            elif 'adult' in name_attr.lower():
                if input_tag.get('type') == 'radio' and 'no' in value_attr.lower():
                    form_data[name_attr] = value_attr
            else:
                if input_tag.get('type') == 'radio' or input_tag.get('type') == 'checkbox':
                    if input_tag.has_attr('checked'):
                        form_data[name_attr] = value_attr
                else:
                    form_data[name_attr] = value_attr

        action = form.get('action', url)
        if not action.startswith('http'):
            if action.startswith('/'):
                action = "https://protoiptv.com" + action
            else:
                action = url
                
        post_response = session.post(action, data=form_data, headers=headers)
        
        if post_response.status_code == 200:
            print("تم إرسال طلب الفترة التجريبية بنجاح! تفقد بريدك الإلكتروني قريباً.")
        else:
            print(f"تم إرسال الطلب ولكن الموقع رد برمز حالة: {post_response.status_code}")
            
    except Exception as e:
        print(f"حدث خطأ أثناء تنفيذ العملية: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
