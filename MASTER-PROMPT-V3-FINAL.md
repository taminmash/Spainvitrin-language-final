# پرامپت اصلی پروژه ویترین اسپانیایی — نسخه ۳ 🇪🇸

این پرامپت رو توی چت جدید claude.ai بفرست.

---

## معرفی پروژه

**ویترین اسپانیایی** — آموزش زبان اسپانیایی به فارسی‌زبانان از طریق ویدیوهای روزانه در تلگرام.
هر درس = کارت گرافیکی + صدای اسپانیایی → ویدیو MP4 → ارسال به تلگرام.

---

## مشخصات فنی

### ریپوی GitHub
- همه سطوح توی یه ریپو: **github.com/taminmash/vitrin-spanish**

### کانال‌ها و گروه‌ها
- گروه آرشیو (مقصد اول): ID `-1003969948606`
- کانال حیاط خلوت (فوروارد از آرشیو): `t.me/hayatkhalvatspain` — ID `-1003854428039`
- بات: `@VitrinSpainBot`

### نحوه ارسال (مهم)
۱. همه ی ویدئوها به ترتیب هر سطح با قابلیت کامنت گذاری زیر پست ابتدا به گروه آرشیو (`-1003969948606`) ارسال میشه
۲. بعد از آرشیو، همون یک پست مربوطه طبق برنامه ریزی و زمانبندی هر روز ساعت 8 مادرید بصورت پست با قابلیت کامنت گذاری زیر پست به کانال حیاط خلوت فوروارد میشه
```python
# ارسال به آرشیو
msg = await bot.send_video(chat_id=-1003969948606, video=video)
# فوروارد به کانال اصلی
await bot.forward_message(
    chat_id=-1003854428039,
    from_chat_id=-1003969948606,
    message_id=msg.message_id
)
```

### زمانبندی
- هر روز ساعت ۸ صبح مادرید
- تابستان (UTC+2): `cron: '0 6 * * *'`
- زمستان (UTC+1): `cron: '0 7 * * *'`
- هر بار فقط **۱ درس**

---

## برنامه درسی (بر اساس Nuevo Prisma)

### ساختار هر سطح
```
۱۲ واحد — هر واحد یه موضوع — هر واحد به تعداد لازم درس برای آموزش
ترتیب روزانه:
  روز ۱: واژه 📚
  روز ۲: فعل 🔤
  روز ۳: مکالمه 🗣️
  روز ۴: واژه 📚
  روز ۵: گرامر 📝
  روز ۶: مکالمه 🗣️
  روز ۷: واژه 📚
  روز ۸: فعل 🔤
  روز ۹: مکالمه 🗣️
  روز ۱۰: مرور 🔄
```

### سطوح و رنگ‌ها
| سطح | موضوع | رنگ | کد رنگ |
|-----|-------|-----|---------|
| A1 | مبتدی | 🔴 قرمز | `#c0392b` |
| A2 | پایه | 🟠 نارنجی تیره | `#d35400` |
| B1 | متوسط | 🟢 سبز تیره | `#1e8449` |
| B2 | فوق متوسط | 🔵 آبی تیره | `#1a5276` |
| C1 | پیشرفته | 🟣 بنفش تیره | `#6c3483` |
| C2 | مسلط | ⚫ طلایی/مشکی | `#7d6608` |

### گرادیان هر سطح
```
A1: linear-gradient(155deg, #c0392b 0%, #96281B 35%, #1a1a2e 100%)
A2: linear-gradient(155deg, #d35400 0%, #a04000 35%, #1a1a2e 100%)
B1: linear-gradient(155deg, #1e8449 0%, #145a32 35%, #0a1a0f 100%)
B2: linear-gradient(155deg, #1a5276 0%, #0e3460 35%, #0a0f1a 100%)
C1: linear-gradient(155deg, #6c3483 0%, #4a235a 35%, #1a0a2e 100%)
C2: linear-gradient(155deg, #7d6608 0%, #5a4a05 35%, #1a1500 100%)
```

### واحدهای A1
1. Saludos y presentaciones — سلام و معرفی
2. Datos personales — اطلاعات شخصی
3. La familia — خانواده
4. El tiempo libre — اوقات فراغت
5. La casa — خانه
6. La ciudad — شهر
7. La comida — غذا
8. La ropa y las compras — لباس و خرید
9. La salud — سلامت
10. Los viajes — سفر
11. El trabajo — کار
12. Repaso general — مرور کلی

---

## طراحی کارت (تایید شده — هرگز تغییر نده)

### مشخصات فنی
```
سایز body: 900×1200 پیکسل
سایز card داخلی: 820×1120
پس‌زمینه body: #1a0f0a
border-radius: 48px
shadow کارت: 0 20px 60px rgba(0,0,0,0.6)
بدون پین گوشه
```

### محتوای کارت (از بالا به پایین)
```
نوار رنگی بالا: 7px — رنگ سطح
بالا چپ: badge سطح (A1 — واحد ۱) + شماره درس (درس ۸) — بدون "از ۱۲۰"
بالا راست: پرچم 🇪🇸
کنار کلمه: badge نوع درس (📚/🔤/🗣️/📝/🔄)
کلمه اسپانیایی: Playfair Display Bold — چپ‌چین — بزرگ
ترجمه انگلیسی: Inter — چپ‌چین — کم‌رنگ (28-30px)
تلفظ فارسی: Vazirmatn — راست‌چین — زرد
معنی فارسی: Vazirmatn Bold — راست‌چین
باکس نکته: background تیره — border کم‌رنگ — border-radius: 28px
  - نکته گرامری به فارسی
  - کاربرد با 🎯
  - توضیح انگلیسی (کم‌رنگ، چپ‌چین)
```

### پایین چپ
```
📲 t.me/vitrinspain
🌿 t.me/hayatkhalvatspain
🤖 @VitrinSpainBot
```

### پایین راست (از بالا به پایین)
```
🔊 (font-size: 52px)
Design by: Tamin .M
💬 @taminmashoori
✉️ tamin.mashoori@gmail.com
```

### کارت فعل
```
مصدر فعل بزرگ بالا
جدول صرف ۶ تایی (grid 2 ستونه):
  yo | hablo | حرف میزنم
  tú | hablas | حرف میزنی
  él/ella | habla | حرف میزنه
  nosotros | hablamos | حرف میزنیم
  vosotros | habláis | حرف میزنید
  ellos | hablan | حرف میزنن
نکته + کاربرد + انگلیسی
```

### کارت مکالمه
```
جمله اصلی بالا
حباب‌های چت:
  👨 اسپانیایی
     فارسی (زرد کم‌رنگ)
     English (خیلی کم‌رنگ)
  👩 اسپانیایی
     فارسی
     English
```

---

## فرمت هر درس در فایل Python

```python
{
    "lesson": "درس ۱",
    "unit": "واحد ۱",
    "type": "واژه",  # واژه / فعل / مکالمه / گرامر / مرور
    "word": "¡Hola!",
    "translation_en": "Hello! / Hi!",
    "pronunciation": "اُلا",
    "meaning": "یعنی: سلام! 👋",
    "tip": "کلمات مرتبط:\n<b>Buenos días</b> = صبح بخیر\n\n🎯 کاربرد: برای سلام کردن استفاده میشه",
    "audio_word": "Hola. Buenos días. Buenas tardes"
    # فقط اسپانیایی در audio_word — نه فارسی نه انگلیسی
}
```

---

## قانون صدا (audio_word) — حیاتی

**فقط متن اسپانیایی** در audio_word میاد:
```python
# کارت واژه:
"audio_word": "Hola. Buenos días. Buenas tardes"  ✅
"audio_word": "Hola یعنی سلام"  ❌

# کارت فعل — مصدر + صرف + مثال:
"audio_word": "hablar. yo hablo, tú hablas, él habla, nosotros hablamos, ellos hablan. Hablas español"

# کارت مکالمه — همه سوال‌ها و جواب‌ها:
"audio_word": "Cómo te llamas. Me llamo Sara. Mucho gusto. Igualmente"
```

---

## قوانین فنی

1. **async_playwright** — نه sync
2. **FFmpeg** در workflow قبل از Python نصب بشه
3. مسیر ffmpeg: `shutil.which("ffmpeg") or "ffmpeg"`
4. **BOT_TOKEN** از `os.environ.get("BOT_TOKEN")`
5. **Workflow permissions**: Read and write ✅
6. فایل yml فقط داخل `.github/workflows/`
7. هیچوقت از **Railway** — فقط GitHub Actions
8. Archive workflow از **actions/cache@v3** برای apt

---

## تلفظ فارسی دقیق

```
H ساکته:      hola = اُلا
LL = ی:       llama = یاما
J = خ:        jarabe = خاراβه
V = ب نرم:    vino = بینُ
C/Z قبل e/i:  cinco = ثینکُ
G قبل e/i:    general = خِنِرال
QU = ک:       quiero = کیِرُ
Ñ = نی:       año = آنیُ
CH = چ:       mucho = موچُ
GU قبل e/i:   guerra = گِرا
```

---

## نمونه workflow ارسال روزانه

```yaml
name: Spanish A1

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

jobs:
  send:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
          playwright install-deps chromium
      - name: Install FFmpeg
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg
      - name: Verify FFmpeg
        run: ffmpeg -version
      - name: Run scheduler
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
        run: python spanish_a1_scheduler.py
      - name: Save progress
        run: |
          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add spanish_a1_day.json
          git commit -m "Update A1 day" || echo "No changes"
          git push
```

## نمونه workflow آرشیو (با cache)

```yaml
name: Archive A1

on:
  workflow_dispatch:
    inputs:
      start_lesson:
        required: true
        default: '0'
      end_lesson:
        required: true
        default: '10'

jobs:
  archive:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Cache apt packages
        uses: actions/cache@v3
        with:
          path: /var/cache/apt/archives
          key: apt-ffmpeg-${{ runner.os }}
      - name: Install FFmpeg
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
          playwright install-deps chromium
      - name: Run archive batch
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          START_LESSON: ${{ github.event.inputs.start_lesson }}
          END_LESSON: ${{ github.event.inputs.end_lesson }}
        run: python archive_a1_lessons.py
```

---

---

## نحوه ارتباط با من

- هر دستور در **یک خط جداگانه**
- منتظر تایید بمون قبل از مرحله بعد
- پاسخ **کوتاه و مستقیم**
- من در کدنویسی و GitHub **مبتدی** هستم
- همه پاسخ‌ها به **فارسی**

