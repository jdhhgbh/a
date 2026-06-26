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
            # دخول الموقع والانتظار حتى استقرار الصفحة
            page.goto(url, wait_until="load")
            page.wait_for_timeout(4000) 
            
            print("1. جاري تعبئة الحقول الأساسية...")
            
            # تعبئة الاسم والإيميل
            page.locator('[name="wpforms[fields][1]"]').fill(name)
            page.locator('[name="wpforms[fields][2]"]').fill(email)
            
            # تعبئة حقل الدولة بمرونة
            country_field = page.locator('[name="wpforms[fields][34]"]')
            if country_field.count() > 0:
                tag_name = country_field.evaluate("el => el.tagName.toLowerCase()")
                if tag_name == "select":
                    country_field.select_option(label="Saudi Arabia")
                else:
                    country_field.fill("Saudi Arabia")
            
            # اختيار VLC / Laptop لتفادي طلب الـ MAC Address الإجباري
            print("-> اختيار نوع الجهاز: VLC Player / Laptop")
            page.locator('[name="wpforms[fields][5]"]').select_option(label="VLC Player / Laptop")
            page.wait_for_timeout(1500) # انتظار ثانية لتحديث الصفحة ديناميكياً
            
            # التعامل مع الحقل 8 بذكاء (سواء تحول لنص أو بقى قائمة)
            field_8 = page.locator('[name="wpforms[fields][8]"]')
            if field_8.count() > 0:
                tag_8 = field_8.evaluate("el => el.tagName.toLowerCase()")
                if tag_8 == "select":
                    field_8.select_option(label="Iptv Smarters Pro")
                else:
                    field_8.fill("IPTV M3U Playlist")
            
            # خيارات القنوات وتفعيل الـ Adult 
            page.locator('[name="wpforms[fields][14]"][value="All Playlist"]').check()
            page.locator('[name="wpforms[fields][24]"][value="Yes"]').check()
            
            # تشييك الحقل 15 الإجباري إن وجد
            checkbox_15 = page.locator('[name^="wpforms[fields][15]"]').first
            if checkbox_15.count() > 0:
                checkbox_15.check()
            
            # الملاحظة
            page.locator('[name="wpforms[fields][23]"]').fill("Please send the complete M3U playlist with adult channels.")
            
            print("2. جاري إرسال الفورم ومحاكاة الضغط البشري الحقيقي...")
            submit_btn = page.locator('button[type="submit"], .wpforms-submit')
            submit_btn.first.click()
            
            # انتظار 8 ثواني للتأكد من إتمام الإرسال وظهور رسالة النجاح
            page.wait_for_timeout(8000)
            
            content = page.content()
            if "wpforms-confirmation" in content or "thank" in content.lower() or "successfully" in content.lower():
                print("\n✅ ملووووز الملووز! تم ترويض الموقع والتسجيل بنجاح، شيك بريدك الحين!")
            else:
                print("\n⚠️ تم ضغط الزر، يرجى مراجعة البريد للتأكد من وصول الرابط.")
                
        except Exception as e:
            print(f"❌ حدث خطأ أثناء التنفيذ: {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
