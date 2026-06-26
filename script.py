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
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        try:
            # دخول الموقع والانتظار حتى يستقر الاتصال
            page.goto(url, wait_until="load")
            page.wait_for_timeout(4000) 
            
            print("1. جاري تعبئة الحقول الأساسية...")
            
            # استخدامselectors مرنة للوصول للحقول مباشرة بأسماء الحقول التابعة لـ WPForms
            page.locator('[name="wpforms[fields][1]"]').fill(name) # الاسم
            page.locator('[name="wpforms[fields][2]"]').fill(email) # الإيميل
            
            # تعبئة حقل الدولة بمرونة (سواء كان اختيار أو كتابة)
            country_field = page.locator('[name="wpforms[fields][34]"]')
            if country_field.count() > 0:
                tag_name = country_field.evaluate("el => el.tagName.toLowerCase()")
                if tag_name == "select":
                    country_field.select_option(label="Saudi Arabia")
                else:
                    country_field.fill("Saudi Arabia")
            
            # اختيار الأجهزة والتطبيقات
            page.locator('[name="wpforms[fields][5]"]').select_option(label="Android Box")
            page.locator('[name="wpforms[fields][8]"]').select_option(label="Iptv Smarters Pro")
            
            # خيارات القنوات والـ Adult (نعم بالتأكيد 😉)
            page.locator('[name="wpforms[fields][14]"][value="All Playlist"]').check()
            page.locator('[name="wpforms[fields][24]"][value="Yes"]').check()
            
            # حقل 15 الإجباري تفعيله إذا كان متواجداً
            checkbox_15 = page.locator('[name^="wpforms[fields][15]"]').first
            if checkbox_15.count() > 0:
                checkbox_15.check()
            
            # الملاحظة
            page.locator('[name="wpforms[fields][23]"]').fill("Please send the complete package.")
            
            print("2. جاري إرسال الفورم ومحاكاة الضغط الحقيقي...")
            # البحث عن زر السمت والضغط عليه
            submit_btn = page.locator('button[type="submit"], .wpforms-submit')
            submit_btn.first.click()
            
            # انتظار النتيجة لمدة 6 ثواني
            page.wait_for_timeout(6000)
            
            content = page.content()
            if "wpforms-confirmation" in content or "thank" in content.lower() or "successfully" in content.lower():
                print("\n✅ ملوّز الملوّز! تم تجاوز التايم أوت والحماية بالكامل، تفقد بريدك الآن.")
            else:
                print("\n⚠️ تم الضغط على الزر، شيك على البريد تحسباً لنجاح الإرسال بالخلفية.")
                
        except Exception as e:
            print(f"❌ حدث خطأ أثناء تنفيذ المتصفح: {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
