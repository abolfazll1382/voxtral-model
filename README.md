# مستندات فنی سیستم تبدیل گفتار فارسی به متن با Voxtral

## معرفی کلی

این پروژه شامل دو سیستم تبدیل گفتار فارسی به متن با استفاده از مدل‌های Voxtral توسعه‌یافته توسط Mistral AI است.

## فایل‌های موجود

### 1. فایل `voxtral_mini.py` - مدل کوچک
- **پارامترها**: 3 میلیارد پارامتر
- **حافظه GPU**: 4-8 گیگابایت
- **کیفیت**: متوسط تا خوب برای فارسی
- **سرعت**: سریع
- **کاربرد**: سیستم‌های با منابع محدود

### 2. فایل `voxtral_small.py` - مدل بزرگ
- **پارامترها**: 24 میلیارد پارامتر  
- **حافظه GPU**: 48+ گیگابایت (حداقل 24 گیگابایت)
- **کیفیت**: حرفه‌ای و بسیار دقیق
- **سرعت**: کندتر اما دقیق‌تر
- **کاربرد**: پروژه‌های حرفه‌ای و تحقیقاتی

## ساختار کد - مدل Mini

### کلاس اصلی: `VoxtralPersianASR`

```python
class VoxtralPersianASR:
    def __init__(self, model_size="mini"):
        # راه‌اندازی اولیه
```

**وظایف کلاس:**
- مدیریت بارگذاری و اجرای مدل
- بهینه‌سازی حافظه برای سخت‌افزارهای ضعیف‌تر
- تشخیص خودکار GPU یا CPU

### متدهای کلیدی

#### 1. متد `__init__` - راه‌اندازی
```python
def __init__(self, model_size="mini"):
    self.model_id = "mistralai/Voxtral-Mini-3B-2507"
    self.processor = None
    self.model = None
    self.device = "cuda" if torch.cuda.is_available() else "cpu"
```

**عملکرد:**
- تعیین شناسه مدل در Hugging Face
- تشخیص دسترسی به GPU یا استفاده از CPU
- مقداردهی اولیه متغیرهای کلاس

#### 2. متد `load_model` - بارگذاری مدل
```python
def load_model(self):
    # بارگذاری پردازشگر
    self.processor = AutoProcessor.from_pretrained(self.model_id)
    
    # بارگذاری مدل با بهینه‌سازی حافظه
    if self.device == "cuda":
        self.model = VoxtralForConditionalGeneration.from_pretrained(
            self.model_id,
            dtype=torch.float16,  # صرفه‌جویی در حافظه
            device_map="auto",
            low_cpu_mem_usage=True,
        )
```

**ویژگی‌های مهم:**
- استفاده از `float16` برای کاهش مصرف VRAM
- بارگذاری تدریجی برای سیستم‌های ضعیف
- تبدیل خودکار به حالت CPU در صورت کمبود حافظه GPU
- نظارت بر مصرف حافظه ویدئو

#### 3. متد `transcribe_persian` - رونویسی فارسی
```python
def transcribe_persian(self, audio_path):
    # بررسی روش‌های موجود رونویسی
    available_methods = [method for method in dir(self.processor) 
                        if 'transcr' in method.lower()]
    
    # آزمایش روش‌های مختلف
    for method_name in transcription_methods:
        if hasattr(self.processor, method_name):
            # تست با کدهای مختلف زبان فارسی
            for lang in ["fa", "persian", "farsi"]:
```

**استراتژی رونویسی:**
1. **تشخیص روش‌های موجود**: بررسی API مدل برای یافتن متد صحیح
2. **آزمایش کدهای زبان**: تست کدهای مختلف فارسی (fa, persian, farsi)
3. **بازگشت به روش‌های جایگزین**: در صورت شکست، استفاده از روش مکالمه‌ای

#### 4. متد `transcribe_chat_mode` - حالت مکالمه‌ای
```python
def transcribe_chat_mode(self, audio_path):
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "audio", "path": audio_path},
                {"type": "text", "text": "لطفا این صدا را رونویسی کنید."},
            ],
        }
    ]
```

**مزایا:**
- استفاده از دستورات فارسی برای بهتر شدن نتایج
- قابلیت ارسال دستورات پیچیده
- سازگاری بهتر با ماهیت مکالمه‌ای مدل

## توابع کمکی

### تابع `convert_to_wav`
```python
def convert_to_wav(input_path, output_path):
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-ar", "16000",      # نرخ نمونه‌برداری 16 کیلوهرتز
        "-ac", "1",          # تبدیل به مونو
        "-c:a", "pcm_s16le", # کدک صوتی
        output_path
    ]
```

**پارامترهای مهم:**
- **16kHz**: نرخ نمونه‌برداری مناسب برای گفتار
- **مونو**: تک کانال برای کاهش حجم
- **PCM 16-bit**: فرمت استاندارد برای پردازش گفتار

### تابع `main` - کنترلر اصلی
```python
def main():
    INPUT_AUDIO = "voice1.mp3"
    WAV_OUTPUT = "voice1_16k_mono.wav"
    
    # بررسی وجود فایل
    if not os.path.exists(INPUT_AUDIO):
        print("فایل صوتی یافت نشد!")
        return
    
    # تبدیل فرمت
    if not convert_to_wav(INPUT_AUDIO, WAV_OUTPUT):
        return
    
    # اجرای رونویسی
    asr = VoxtralPersianASR()
    result = asr.transcribe_persian(WAV_OUTPUT)
```

## ساختار کد - مدل Small

### تفاوت‌های کلیدی با مدل Mini

#### 1. کلاس `VoxtralSmallPersianASR`
- **حافظه بیشتر**: نیاز به 48+ گیگابایت VRAM
- **دقت بالاتر**: کیفیت حرفه‌ای برای متن‌های پیچیده
- **پردازش دسته‌ای**: قابلیت پردازش چندین فایل به‌طور همزمان

#### 2. متد `batch_transcribe` - پردازش دسته‌ای
```python
def batch_transcribe(self, audio_files):
    results = {}
    for i, audio_file in enumerate(audio_files, 1):
        # پردازش هر فایل
        result = self.transcribe_persian(wav_file)
        results[audio_file] = result
        
        # پاک‌سازی حافظه بین فایل‌ها
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
```

**مزایا:**
- پردازش خودکار چندین فایل
- ذخیره جداگانه نتایج
- مدیریت حافظه بین پردازش‌ها

## مدیریت حافظه و بهینه‌سازی

### برای مدل Mini (GTX 1050 Ti)
```python
# تنظیمات بهینه‌سازی
dtype=torch.float16          # نصف حافظه
low_cpu_mem_usage=True      # بارگذاری تدریجی
offload_folder="./offload"  # انتقال به دیسک

# بررسی مصرف حافظه
if vram_used > 3.5:  # بیش از حد برای GTX 1050 Ti
    self.device = "cpu"  # تبدیل به CPU
```

### برای مدل Small (سیستم‌های قدرتمند)
```python
# تنظیمات حرفه‌ای
dtype=torch.bfloat16        # دقت بالا
device_map="auto"           # توزیع خودکار
offload_state_dict=True     # ذخیره حالت مدل
```

## الگوریتم پردازش صوت

### مراحل تبدیل صوت به متن:

1. **بارگذاری فایل صوتی**
   ```python
   audio, sample_rate = torchaudio.load(audio_path)
   ```

2. **پیش‌پردازش صوتی**
   ```python
   # تبدیل به مونو
   if audio.shape[0] > 1:
       audio = torch.mean(audio, dim=0, keepdim=True)
   
   # تنظیم نرخ نمونه‌برداری
   if sample_rate != 16000:
       resampler = torchaudio.transforms.Resample(sample_rate, 16000)
       audio = resampler(audio)
   ```

3. **پردازش توسط مدل**
   ```python
   inputs = self.processor.apply_chat_template(conversation)
   inputs = inputs.to(self.device, dtype=torch.float16)
   ```

4. **تولید متن**
   ```python
   with torch.no_grad():
       outputs = self.model.generate(
           **inputs,
           max_new_tokens=300,
           do_sample=False,
           temperature=0.0
       )
   ```

5. **رمزگشایی نتیجه**
   ```python
   decoded_outputs = self.processor.batch_decode(
       outputs[:, inputs.input_ids.shape[1]:], 
       skip_special_tokens=True
   )
   ```

## مدیریت خطاها

### خطاهای رایج و راه‌حل‌ها:

#### 1. کمبود حافظه GPU
```python
except torch.cuda.OutOfMemoryError:
    print("کمبود حافظه GPU - تبدیل به حالت CPU")
    self.device = "cpu"
    return self.load_model()
```

#### 2. عدم وجود روش رونویسی
```python
# آزمایش روش‌های مختلف
transcription_methods = [
    'apply_transcrition_request',  # روش رسمی
    'apply_transcription_request', # روش اصلاح‌شده
    'transcribe',                  # روش عمومی
]
```

#### 3. شکست تبدیل صوت
```python
try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"خطا در تبدیل صوت: {e}")
    return False
```

## نکات بهینه‌سازی

### برای بهبود کیفیت رونویسی:
1. **کیفیت صوت**: استفاده از فایل‌های با کیفیت بالا
2. **کاهش نویز**: پاک‌سازی صدای محیط
3. **سرعت گفتار**: سرعت متعادل و واضح
4. **زبان یکنواخت**: اجتناب از تغییر زبان در میانه متن

### برای بهبود کارایی:
1. **مدیریت حافظه**: پاک‌سازی منظم cache
2. **پردازش دسته‌ای**: گروه‌بندی فایل‌های کوچک
3. **تنظیم پارامترها**: کاهش max_new_tokens برای فایل‌های کوتاه

## نتیجه‌گیری

این سیستم امکان تبدیل دقیق گفتار فارسی به متن را با استفاده از مدل‌های پیشرفته Voxtral فراهم می‌کند. انتخاب بین مدل Mini و Small بستگی به نیازهای کیفی و منابع سخت‌افزاری موجود دارد.
