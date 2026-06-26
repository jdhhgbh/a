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
        # تشغيل متصفح خفي كأنه جهاز حقيقي
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
            viewport={"width": 390, "height": 844},
            is_mobile=True
        )
        page = context.new_page()
        
        try:
            # دخول الموقع والانتظار لين يحمل بالكامل ويشغل الـ JS
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(3000) # انتظار 3 ثواني إضافية لضمان توليد توكن الحماية
            
            print("1. جاري تعبئة الحقول داخل المتصفح...")
            
            # تعبئة الحقول الأساسية بناءً على المعرفات الرقمية لـ WPForms
            page.fill('input[name="wpforms[fields][1]"]', name) # الاسم
            page.fill('input[name="wpforms[fields][34]"]', "Saudi Arabia") # الدولة
            page.fill('input[name="wpforms[fields][2]"]', email) # الإيميل
            
            # اختيار نوع الجهاز وتطبيق الـ IPTV من القوائم المنسدلة
            page.select_option('select[name="wpforms[fields][5]"]', label="Android Box")
            page.select_option('select[name="wpforms[fields][8]"]', label="Iptv Smarters Pro")
            
            # اختيار نوع القنوات (All Playlist) والـ Adult (Yes) عبر أزرار الراديو
            page.check('input[name="wpforms[fields][14]"][value="All Playlist"]')
            page.check('input[name="wpforms[fields][24]"][value="Yes"]') # تفعيل الـ Adult 😉
            
            # تعبئة الحقل 15 الإجباري (اختيار باقات فرعية إن وجدت، نحدد أول خيار)
            checkbox_15 = page.locator('input[name^="wpforms[fields][15]"]').first
            if checkbox_15.count() > 0:
                checkbox_15.check()
                print("-> تم تفعيل الحقل الإجباري رقم 15")
                
            page.fill('textarea[name="wpforms[fields][23]"]', "Please send me the full playlist with adult channels.") # الملاحظة
            
            print("2. جاري إرسال الفورم ومحاكاة الضغط البشري...")
            # الضغط على زر الإرسال
            page.click('button[type="submit"]')
            
            # الانتظار 5 ثواني حتى تظهر رسالة النجاح في الصفحة
            page.wait_for_timeout(5000)
            
            # طباعة محتوى الصفحة أو التأكيد لمعرفة النتيجة
            content = page.content()
            if "wpforms-confirmation" in content or "thank" in content.lower() or "successfully" in content.lower():
                print("\n✅ كفوووو تم اختراق الحماية والتسجيل بنجاح ملوّز عن طريق المتصفح! شيك إيميلك الحين.")
            else:
                print("\n⚠️ تم ضغط الزر، لكن يرجى مراجعة حالة الصفحة للتأكد.")
                
        except Exception as e:
            print(f"❌ حدث خطأ أثناء محاكاة المتصفح: {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
