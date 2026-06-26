import random
import string
import os
import sys
import imaplib
import email
import re
import time
from playwright.sync_api import sync_playwright

def generate_random_string(length=6):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def get_iptv_credentials(mail_user, mail_pass):
    print("3. جاري الاتصال بالبريد الإلكتروني لسحب بيانات الاشتراك...")
    time.sleep(30) # انتظار 30 ثانية لضمان وصول الرسالة
    
    try:
        # الاتصال بسيرفر Outlook IMAP
        mail = imaplib.IMAP4_SSL("outlook.office365.com")
        mail.login(mail_user, mail_pass)
        mail.select("inbox")
        
        # البحث عن الرسائل القادمة من PROTOIPTV
        status, messages = mail.search(None, '(FROM "PROTOIPTV")')
        if status != "OK" or not messages[0]:
            print("⚠️ لم يتم العثور على رسالة التفعيل بعد.")
            return None
            
        latest_message_id = messages[0].split()[-1]
        status, data = mail.fetch(latest_message_id, "(RFC822)")
        
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
            
        # استخراج البيانات باستخدام RegEx
        username_match = re.search(r"Username:\s*([^\s\n]+)", body)
        password_match = re.search(r"Password:\s*([^\s\n]+)", body)
        host_match = re.search(r"Host:\s*([^\s\n]+)", body)
        
        if username_match and password_match:
            user = username_match.group(1).strip()
            password = password_match.group(1).strip()
            host = host_match.group(1).strip() if host_match else "http://protoiptv.com:8000"
            
            # بناء رابط M3U الذكي
            m3u_url = f"{host}/get.php?username={user}&password={password}&output=ts"
            print(f"✅ تم استخراج البيانات بنجاح لليوزر: {user}")
            return m3u_url
            
    except Exception as e:
        print(f"❌ خطأ أثناء قراءة البريد: {str(e)}")
    return None

def upload_to_mytv(m3u_url, tv_id):
    print(f"4. جاري الدخول إلى mytv.best لرفع الرابط للتلفزيون...")
    upload_url = "https://mytv.best/upload-channels/"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(upload_url, wait_until="load")
            page.wait_for_timeout(3000)
            
            # تعبئة كود التلفزيون ورابط الـ M3U بناءً على حقول الموقع
            page.locator('input[name="device_key"], #device_key').fill(tv_id)
            page.locator('input[name="playlist_url"], #playlist_url').fill(m3u_url)
            
            # الضغط على زر الحفظ أو الرفع
            submit_btn = page.locator('button[type="submit"], .submit-btn')
            submit_btn.first.click()
            page.wait_for_timeout(5000)
            
            print("🚀 ملوّز! تم تحديث القنوات على تلفزيونك تلقائياً بنجاح.")
        except Exception as e:
            print(f"❌ خطأ أثناء الرفع للموقع: {str(e)}")
        finally:
            browser.close()

def main():
    # جلب البيانات الحساسة من بيئة تشغيل جيت هاب الآمنة
    mail_user = os.getenv("MAIL_USER", "Zwri@outlook.sa")
    mail_pass = os.getenv("MAIL_PASS", "@Dddd1992")
    tv_id = "d2ae-801d-d2f7-94d5-9398"
    
    url = "https://protoiptv.com/2026-iptvtrial-free-pro/"
    random_part = generate_random_string(6)
    email_address = f"zwri+{random_part}@outlook.sa"
    name = f"Ismail_{generate_random_string(4)}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(4000) 
            
            print(f"1. التسجيل الآلي بالإيميل: {email_address}")
            page.locator('[name="wpforms[fields][1]"]').fill(name)
            page.locator('[name="wpforms[fields][2]"]').fill(email_address)
            
            country_field = page.locator('[name="wpforms[fields][34]"]')
            if country_field.count() > 0:
                country_field.select_option(label="Saudi Arabia")
            
            page.locator('[name="wpforms[fields][14]"][value="All Playlist"]').check()
            page.locator('[name="wpforms[fields][24]"][value="Yes"]').check()
            page.locator('[name="wpforms[fields][23]"]').fill("Please send the complete package.")
            
            print("2. إرسال طلب تفعيل الحساب...")
            submit_btn = page.locator('button[type="submit"], .wpforms-submit')
            submit_btn.first.click()
            page.wait_for_timeout(5000)
            
        except Exception as e:
            print(f"❌ خطأ أثناء التسجيل: {str(e)}")
        finally:
            browser.close()
            
    # الانتقال لخطوة قراءة الإيميل والرفع
    m3u_link = get_iptv_credentials(mail_user, mail_pass)
    if m3u_link:
        創造_to_mytv(m3u_link, tv_id)

if __name__ == "__main__":
    main()
