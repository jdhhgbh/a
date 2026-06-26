import random
import string
import sys
from playwright.sync_api import sync_playwright

def generate_random_string(length=6):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def main():
    url = "https://protoiptv.com/2026-iptvtrial-free-pro/"
    
    random_part = generate_random_string(6)
    email = f"zwri+{random_part}@outlook.sa"
    name = f"Ismail_{generate_random_string(4)}"
    
    print(f"-> جاري تشغيل المتصفح الخفي للتسجيل بالإيميل: {email}")
    
    with sync_playwright() as p:
        # تشغيل المتصفح الخفي بمحاكاة جهاز كمبيوتر عادي لتفادي مشاكل القوائم
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        try:
            # دخول الموقع والانتظار حتى استقرار الصفحة بالكامل
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(5000) 
            
            print("1. جاري تعبئة الحقول الأساسية...")
            
            # 1. تعبئة الاسم والإيميل
            page.locator('[name="wpforms[fields][1]"]').fill(name)
            page.locator('[name="wpforms[fields][2]"]').fill(email)
            
            # 2. اختيار الدولة من القائمة المنسدلة (Saudi Arabia)
            print("-> جاري تحديد الدولة...")
            country_field = page.locator('[name="wpforms[fields][34]"]')
            country_field.scroll_into_view_if_needed()
            # نحاول نختار بالـ Label أو القيمة المباشرة
            try:
                country_field.select_option(label="Saudi Arabia")
            except:
                country_field.select_option(value="Saudi Arabia")
                
            page.wait_for_timeout(1500)
            
            # ملاحظة: نوع الجهاز (Android Box) والتطبيق (Iptv Smarters Pro) محددين تلقائياً كخيار أول فما نلمسهم لتفادي التعليق
            
            # 3. خيارات القنوات والـ Adult (تفعيل الـ Adult بالتأكيد 😉)
            print("-> جاري تفعيل خيارات القنوات والـ Adult...")
            page.locator('[name="wpforms[fields][14]"][value="All Playlist"]').check()
            page.locator('[name="wpforms[fields][24]"][value="Yes"]').check()
            
            # 4. الملاحظة
            page.locator('[name="wpforms[fields][23]"]').fill("Please send the complete package.")
            
            print("2. جاري إرسال الفورم ومحاكاة الضغط البشري...")
            # البحث عن زر الـ Submit والضغط عليه
            submit_btn = page.locator('button[type="submit"], .wpforms-submit')
            submit_btn.first.click()
            
            # انتظار كافي حتى يتم الإرسال وظهور رسالة النجاح (10 ثواني)
            page.wait_for_timeout(10000)
            
            content = page.content()
            if "wpforms-confirmation" in content or "thank" in content.lower() or "successfully" in content.lower():
                print("\n✅ ملووووز الملووز! تم ترويض الموقع والتسجيل بنجاح، شيك بريدك الحين!")
            else:
                print("\n⚠️ تم ضغط الزر، يرجى مراجعة البريد للتأكد من وصول الرابط الحين بالخلفية.")
                
        except Exception as e:
            print(f"❌ حدث خطأ أثناء التنفيذ: {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
