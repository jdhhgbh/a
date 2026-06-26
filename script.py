import requests
from bs4 import BeautifulSoup
import random
import string
import sys
import json

def generate_random_string(length=6):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def main():
    url = "https://protoiptv.com/2026-iptvtrial-free-pro/"
    # رابط إرسال البيانات المباشر الخاص بإضافة WPForms AJAX
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
        # 1. دخول الصفحة كزائر حقيقي لبدء الجلسة وجلب الكوكيز والـ Tokens
        print("1. جاري جلب ملفات تعريف الارتباط والتوكن من الموقع...")
        response = session.get(url, headers={"User-Agent": headers["User-Agent"]})
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form', id=lambda x: x and x.startswith('wpforms-form-'))
        
        if not form:
            print("❌ لم يتم العثور على فورم WPForms!")
            sys.exit(1)
            
        random_part = generate_random_string(6)
        email = f"zwri+{random_part}@outlook.sa"
        name = f"Ismail_{generate_random_string(4)}"
        
        # 2. بناء الحقول المطابقة تماماً لطلب الـ AJAX الصحيح
        form_data = {
            "wpforms[id]": "541",
            "wpforms[author]": "1",
            "wpforms[fields][1]": name,
            "wpforms[fields][34]": "Saudi Arabia",
            "wpforms[fields][2]": email,
            "wpforms[fields][5]": "Android Box",
            "wpforms[fields][8]": "Iptv Smarters Pro",
            "wpforms[fields][14]": "All Playlist",
            "wpforms[fields][24]": "No",
            "wpforms[fields][23]": "Trial Request",
            "wpforms[fields][39]": "",  # حقل الـ HoneyPot المخفي (يجب أن يترك فارغاً تماماً لخداع الموقع)
            "action": "wpforms_submit", # الأكشن الأساسي لـ WPForms AJAX
            "page_id": "1342"
        }
        
        # جلب التوكن المخفي التلقائي (wpforms[nonce]) إن وجد في الصفحة
        nonce_input = soup.find('input', name=lambda x: x and 'nonce' in x)
        if nonce_input:
            form_data[nonce_input['name']] = nonce_input.get('value', '')
            
        print(f"-> جاري التسجيل بالبريد: {email}")
        
        # 3. إرسال طلب الـ AJAX الفعلي محاكاة لضغطة الـ Submit يدوياً
        print("2. جاري إرسال الطلب عبر بوابة AJAX...")
        post_response = session.post(ajax_url, data=form_data, headers=headers)
        
        print(f"-> رمز الاستجابة: {post_response.status_code}")
        print("--- الرد المباشر من السيرفر ---")
        print(post_response.text)
        
        # التحقق من أن السيرفر أكد استلام الحقول وأرسل النجاح
        if "success" in post_response.text.lower() or '"success":true' in post_response.text.replace(" ", ""):
            print("\n✅ ملووووز الملووز! تم الاختراق بنجاح كأنك أرسلته بيدك، شيك بريدك الآن.")
        else:
            print("\n⚠️ تم الإرسال ولكن رد الموقع غير مؤكد، يرجى فحص الرد أعلاه.")
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء التنفيذ: {str(e)}")

if __name__ == "__main__":
    main()
