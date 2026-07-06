<div dir="rtl">

<p align="center">
  <img src="assets/banner.png" alt="Evil Hermes" width="100%">
</p>

# ایول ہرمیس (Evil Hermes)

**بنایا گیا، محققین اور آپریٹرز کے لیے ایک خود مختار، خود بہتر ہونے والا AI ایجنٹ فریم ورک — جنہیں شناخت، فلٹرز اور پالیسی پر مکمل کنٹرول کی ضرورت ہے۔**

[![Docs](https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge)](https://evil-hermes.nousresearch.com/docs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Built by Lord Tanzeel Shujah Khan](https://img.shields.io/badge/Built%20by-Lord%20Tanzeel%20Shujah%20Khan-blueviolet?style=for-the-badge)](https://github.com/tanzeelshujahkhan)
[![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/nousresearch)
[![English](https://img.shields.io/badge/Lang-English-lightgrey?style=for-the-badge)](README.md)
[![中文](https://img.shields.io/badge/Lang-中文-red?style=for-the-badge)](README.zh-CN.md)
[![Español](https://img.shields.io/badge/Lang-Español-orange?style=for-the-badge)](README.es.md)

ایول ہرمیس ایک مکمل ایجنٹ فریم ورک ہے — ٹرمینل UI، میسجنگ گیٹ وے، ڈیسک ٹاپ ایپ، لرننگ لوپ، پلگ ان سسٹم، اور سکلز ایکو سسٹم — سب کچھ ایک Python پیکج میں جو $5 والے VPS، GPU کلسٹر، یا سرور لیس انفراسٹرکچر پر چلتا ہے۔ [ہرمیس ایجنٹ](https://github.com/NousResearch/hermes-agent) جیسی ہی فن تعمیر؛ جان بوجھ کر آڈٹ شدہ پری فلٹرز کا ایک ذیلی مجموعہ ہٹا دیا گیا ہے تاکہ آپریٹر کو پالیسی کے فیصلے وراثت میں ملنے کی بجائے ملکیت میں ملیں۔

> **[Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan) کی تعمیر۔**
> خود مختار شناخت، خود مختار ترتیب، خود مختار تعیناتی۔

---

## آپ کو کیا ملتا ہے

- **اصل ٹرمینل انٹرفیس** — مکمل TUI، ملٹی لائن ایڈیٹنگ، سلیش کمانڈ آٹو کمپلیشن، گفتگو کی سرگزشت، انٹرپٹ اور ری ڈائریکٹ، اور ٹول آؤٹ پٹ اسٹریمنگ۔
- **ایک گیٹ وے، بیس پلیٹ فارمز** — ٹیلی گرام، ڈسکارڈ، سلیک، واٹس ایپ، سگنل، میٹرکس، آئی مسیج، ٹیمز، ہوم اسسٹنٹ، اور مزید، ایک ہی عمل سے، متحدہ گفتگو کی سرگزشت اور کراس پلیٹ فارم تسلسل کے ساتھ۔
- **بند لرننگ لوپ** — ایجنٹ کی طرف سے منتخب کردہ میموری، وقفے وقفے سے استقامت کی یاد دہانیوں کے ساتھ۔ پیچیدہ کاموں کے بعد خود مختار سکلز بنانا۔ سکلز استعمال کے دوران خود کو بہتر بناتی ہیں۔ کراس سیشن یاددہانی کے لیے LLM خلاصے کے ساتھ FTS5 سیشن سرچ۔ [agentskills.io](https://agentskills.io) کھلے معیار کے ساتھ مکمل مطابقت۔
- **شیڈیولڈ آٹومیشنز** — کسی بھی پلیٹ فارم پر ترسیل کے ساتھ بلٹ ان cron شیڈیولر۔ روزانہ رپورٹس، رات کے بیک اپ، ہفتہ وار آڈٹس — فطری زبان میں، بغیر نگہبانی کے۔
- **تفویض اور متوازی کاری** — متوازی ورک فلو کے لیے الگ تھلگ ذیلی ایجنٹس بنائیں، یا ایسے Python اسکرپٹس لکھیں جو RPC کے ذریعے ٹولز کو کال کریں اور کثیر مرحلہ پائپ لائنز کو صفر سیاق و سباق لاگت والے موڑ میں تبدیل کریں۔
- **کہیں بھی چلائیں** — چھ ٹرمینل بیک اینڈز: local، Docker، SSH، Singularity، Modal، Daytona۔ سرور لیس استقامت کا مطلب ہے کہ آپ کا ایجنٹ بیکار ہونے پر ہائبرنیٹ کرتا ہے اور مانگ پر جاگتا ہے۔
- **ریسرچ گریڈ ٹولنگ** — بیچ ٹریجیکٹری جنریشن، ٹریجیکٹری کمپریشن، اور اگلی نسل کے ٹول استعمال کرنے والے ماڈلز کی تربیت کے لیے نصاب کے ہکس۔

---

## تنصیب

### Linux، macOS، WSL2، Termux

```bash
curl -fsSL https://evil-hermes.nousresearch.com/install.sh | bash
```

### Windows (مقامی PowerShell)

```powershell
iex (irm https://evil-hermes.nousresearch.com/install.ps1)
```

انسٹالر سب کچھ فراہم کرتا ہے: `uv`، Python 3.11، Node.js، ripgrep، ffmpeg، اور ایک پورٹیبل Git Bash (MinGit) جو کسی بھی سسٹم Git تنصیب کو نہیں چھیتا۔ اگر Git پہلے سے موجود ہو تو انسٹالر اسے استعمال کرتا ہے اور ڈاؤن لوڈ چھوڑ دیتا ہے۔

تنصیب کے بعد:

```bash
source ~/.bashrc    # شیل دوبارہ لوڈ کریں (یا: source ~/.zshrc)
hermes              # چیٹ شروع کریں
```

### پہلی بار سیٹ اپ

```bash
hermes model        # اپنا LLM فراہم کنندہ اور ماڈل منتخب کریں
hermes tools        # فعال ٹولز کی تشکیل کریں
hermes setup        # مکمل سیٹ اپ وزرڈ چلائیں
hermes gateway      # میسجنگ گیٹ وے شروع کریں (ٹیلی گرام، ڈسکارڈ وغیرہ)
hermes update       # تازہ ترین ورژن پر اپ ڈیٹ کریں
hermes doctor       # مسائل کی تشخیص کریں
```

📖 **[مکمل دستاویزات →](https://evil-hermes.nousresearch.com/docs/)**

---

## ایول ہرمیس اپ اسٹریم سے کیسے مختلف ہے

ایول ہرمیس [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan) کی طرف سے [ہرمیس ایجنٹ](https://github.com/NousResearch/hermes-agent) کا ایک فورک ہے۔ انجن، گیٹ وے، پلگ ان سسٹم، سکل فارمیٹ، اور فراہم کنندہ میٹرکس **بالکل ایک جیسے ہیں اور ایک ساتھ ٹیسٹ شدہ ہیں**۔ فرق جان بوجھ کر اور سرجریکل ہیں۔

| پہلو | ہرمیس ایجنٹ (اپ اسٹریم) | ایول ہرمیس |
|---|---|---|
| **شناخت** | `agent/prompt_builder.py:DEFAULT_AGENT_IDENTITY` ایک غیر جانبدار Nous اسسٹنٹ کے طور پر آتی ہے۔ `SOUL.md` اختیاری ہے۔ | Lord Tanzeel Shujah Khan کی طرف سے بنائی گئی ایک خود مختار شناخت۔ `SOUL.md` **ہر گفتگو پر بطور ڈیفالٹ لوڈ ہوتا ہے** — پہلی انسٹالیشن ایک خود مختار ٹیمپلیٹ بوائی کرتی ہے۔ غیر جانبدار شناخت کا راستہ صرف ایک جھنڈے کی دوری پر ہے۔ |
| **اخلاقی پری فلٹرز** | دھمکی پیٹرن regex، ٹول کال لوپ گارڈریلز، اور ڈیفالٹ فائل رائٹ ڈینی لسٹ (`.ssh`، `.aws`، `.gnupg`، `.kube`، `.docker`، `.env`، `.netrc`، `.pgpass` وغیرہ) فعال ہیں۔ | پری فلٹرز کو **کم سے کم ڈینی لسٹ** تک کم کر دیا گیا ہے: صرف سسٹم شناختی فائلز (`/etc/passwd`، `/etc/shadow`، `/etc/sudoers*`) اور ایجنٹ کا اپنا اسناد اسٹور۔ باقی سب آپریٹر کا علاقہ ہے۔ فلٹر کا کوڈ ابھی بھی درخت میں ہے — ایک جھنڈا پلٹائیں اور اپ اسٹریم کا رویہ واپس آ جاتا ہے۔ |
| **ٹول گارڈریلز** | ڈیفالٹ `warnings=True`، بار بار ناکام ٹول کالز کے لیے `hard_stop=True`۔ Skills Guard کمیونٹی کی `dangerous` سکلز کے لیے `block` واپس کرتا ہے۔ | ڈیفالٹ `warnings=False`، `hard_stop=False`۔ Skills Guard ابھی بھی `safe / caution / dangerous` فیصلہ جاری کرتا ہے اور انسٹال پر دکھاتا ہے — کوئی فیصلہ بلاک نہیں کرتا۔ اسکینر آلہ سازی کے ذریعہ کے طور پر لوپ میں رہتا ہے۔ |
| **خفیہ معلومات کی تبدیلی** | MCP ٹرانسپورٹ میں `HERMES_REDACT_SECRETS=true` بطور ڈیفالٹ۔ | `_REDACT_ENABLED` بطور ڈیفالٹ `false`۔ اگر لاگ اسکربنگ چاہیں تو جھنڈا لگائیں؛ پیٹرن بدلے نہیں رہتے۔ |
| **اندرونی نام** | `hermes-agent` پیکج، `hermes_*` امپورٹ راستے، `HERMES_HOME` ماحول متغیر، `~/.hermes/` کنفیگ ڈائریکٹری۔ | **ڈیزائن کے مطابق ایک جیسا۔** نام تبدیل کرنا 6,000+ فائل امپورٹس توڑ دے گا۔ صرف صارف کے سامنے آنے والے تار، ڈیفالٹ شناخت، اور پری فلٹر ڈیفالٹس مختلف ہیں — چند فائلوں تک محدود۔ |
| **لائسنس** | MIT | MIT (بلا تغیر) |
| **دیکھ بھال کی پالیسی** | بنیادی ایجنٹ + ماڈل ٹول اسکیما پر قدامت پسند۔ AGENTS.md تعاون کا ربرک لاگو ہوتا ہے۔ | بالکل ایک جیسا۔ بنیادی کوڈ اپ اسٹریم تعاون ربرک سے منحرف نہیں ہوتا۔ |

**فورک کا نکتہ ملکیت ہے۔** فلٹر کا کوڈ حقیقی، معائنہ کے قابل ایجنٹ انفراسٹرکچر ہے۔ اپ اسٹریم کوڈ بیس میں فلٹرز ایجنٹ کی صارف شناخت سے جڑے ہوتے ہیں اور بطور ڈیفالٹ فعال آتے ہیں۔ ایول ہرمیس ان دونوں کو الگ کرتا ہے: فلٹرز موجود ہیں اور قابل آڈٹ ہیں، لیکن اس بات کا فیصلہ کہ کیا فعال ہے، آپریٹر کا ہے — نہ کہ فریم ورک کا۔

---

## تعیناتی

ایول ہرمیس سنگل ٹیننٹ ذاتی ایجنٹ ہے۔ ٹرسٹ ماڈل [SECURITY.md](SECURITY.md) میں بیان کیا گیا ہے۔ تین فیصلے کھلونے اور پروڈکشن تعیناتی کے درمیان فرق رکھتے ہیں:

1. **`toolsets` کو جان بوجھ کر سیٹ کریں** `~/.hermes/config.yaml` میں۔ `hermes-cli` آپ کو shell + file + edit دیتا ہے۔ نیٹ ورک کے لیے `web` شامل کریں۔ سیٹ جتنا تنگ، دھماکے کا دائرہ اتنا چھوٹا۔
2. **اپنے دھمکی ماڈل سے میل کھانے والا ٹرمینل بیک اینڈ منتخب کریں**۔ قابل اعتماد سنگل صارف ہوسٹس کے لیے `backend: local`۔ عارضی کنٹینر تنہائی کے لیے `backend: docker`۔ سرور لیس سینڈ باکسنگ کے لیے `backend: modal` یا `backend: daytona`۔
3. **آپریٹر کنفیگ میں ان فلٹرز کو دوبارہ فعال کریں جو آپ واقعی چاہتے ہیں**۔ لاگ اسکربنگ کے لیے `HERMES_REDACT_SECRETS=true`۔ دھمکی پیٹرن اسکینر کو `tools/threat_patterns.py:_PATTERNS` میں ترمیم کرکے دوبارہ فعال کیا جا سکتا ہے — فریم ورک پیٹرنز بھیجتا ہے؛ صرف ڈیفالٹ لسٹ خالی ہے۔

گیٹ وے یا API کو کھلے انٹرنیٹ پر ظاہر کرنے سے پہلے [SECURITY.md](SECURITY.md) پڑھیں۔

---

## دستاویزات

مکمل دستاویزات کی سائٹ **[evil-hermes.nousresearch.com/docs](https://evil-hermes.nousresearch.com/docs/)** پر شائع ہے۔ انجن مشترک ہے، لہذا اپ اسٹریم دستاویزات لغوی طور پر لاگو ہوتی ہیں؛ ایول ہرمیس سے متعلقہ نوٹس مقام پر نشان زد ہیں۔

| سیکشن | مواد |
|---|---|
| [فوری آغاز (Quickstart)](https://evil-hermes.nousresearch.com/docs/getting-started/quickstart) | انسٹال → سیٹ اپ → 2 منٹ میں پہلی گفتگو |
| [CLI کا استعمال](https://evil-hermes.nousresearch.com/docs/user-guide/cli) | کمانڈز، کی بائنڈنگز، پرسنلٹیز، سیشنز |
| [کنفیگریشن (Configuration)](https://evil-hermes.nousresearch.com/docs/user-guide/configuration) | کنفگ فائل، فراہم کنندگان، ماڈلز، تمام آپشنز |
| [میسجنگ گیٹ وے](https://evil-hermes.nousresearch.com/docs/user-guide/messaging) | ٹیلی گرام، ڈسکارڈ، سلیک، واٹس ایپ، سگنل، ہوم اسسٹنٹ |
| [سیکیورٹی (Security)](https://evil-hermes.nousresearch.com/docs/user-guide/security) | کمانڈ کی منظوری، DM پیئرنگ، کنٹینر تنہائی |
| [ٹولز اور ٹول سیٹس](https://evil-hermes.nousresearch.com/docs/user-guide/features/tools) | 40+ ٹولز، ٹول سیٹ سسٹم، ٹرمینل بیک اینڈز |
| [مہارتوں کا سسٹم (Skills System)](https://evil-hermes.nousresearch.com/docs/user-guide/features/skills) | پروسیجرل میموری، سکلز ہب، سکلز بنانا |
| [میموری (Memory)](https://evil-hermes.nousresearch.com/docs/user-guide/features/memory) | مستقل میموری، یوزر پروفائلز، بہترین طریقہ کار |
| [MCP انضمام (Integration)](https://evil-hermes.nousresearch.com/docs/user-guide/features/mcp) | ایم سی پی سرورز کو جوڑ کر صلاحیتوں میں توسیع |
| [کرون (Cron) شیڈیولنگ](https://evil-hermes.nousresearch.com/docs/user-guide/features/cron) | پلیٹ فارم ڈیلیوری کے ساتھ شیڈیول کیے گئے کام |
| [کانٹیکسٹ (Context) فائلز](https://evil-hermes.nousresearch.com/docs/user-guide/features/context-files) | ہر گفتگو کو شکل دینے والا پروجیکٹ کا سیاق و سباق |
| [آرکیٹیکچر (Architecture)](https://evil-hermes.nousresearch.com/docs/developer-guide/architecture) | پروجیکٹ کا ڈھانچہ، ایجنٹ لوپ، کلیدی کلاسز |
| [تعاون (Contributing)](https://evil-hermes.nousresearch.com/docs/developer-guide/contributing) | ڈیویلپمنٹ سیٹ اپ، PR کا طریقہ کار، کوڈنگ کا انداز |
| [CLI حوالہ جات (Reference)](https://evil-hermes.nousresearch.com/docs/reference/cli-commands) | تمام کمانڈز اور فلیگز |
| [انوائرمنٹ ویری ایبلز](https://evil-hermes.nousresearch.com/docs/reference/environment-variables) | مکمل ماحولیاتی متغیر حوالہ |

---

## OpenClaw سے منتقلی

سیٹ اپ وزرڈ (`hermes setup`) خود بخود `~/.openclaw` کا پتہ لگاتا ہے اور ترتیب شروع ہونے سے پہلے منتقلی کی پیشکش کرتا ہے۔ انسٹال کے بعد منتقلی:

```bash
hermes claw migrate              # انٹرایکٹو منتقلی (مکمل پری سیٹ)
hermes claw migrate --dry-run    # منتقل ہونے والی چیزوں کا پیش منظر
hermes claw migrate --preset user-data   # خفیہ معلومات کے بغیر منتقلی
hermes claw migrate --overwrite  # موجودہ تنازعات کو اوور رائٹ کریں
```

درآمد: `SOUL.md`، `MEMORY.md`، `USER.md`، صارف کی بنائی ہوئی مہارتیں (→ `~/.hermes/skills/openclaw-imports/`)، کمانڈ کی اجازت کی فہرست، میسجنگ کی ترتیبات، اجازت نامہ API کیز، TTS اثاثے، اور ورک اسپیس `AGENTS.md`۔

---

## تعاون

تعاون کا خیرمقدم ہے۔ ڈیویلپمنٹ سیٹ اپ، کوڈنگ اسٹائل، اور PR کے عمل کے لیے [CONTRIBUTING.md](CONTRIBUTING.md) دیکھیں۔ [AGENTS.md](AGENTS.md) میں تعاون کا ربرک طے کرتا ہے کہ کیا شامل ہو گا اور کیا نہیں — بڑا PR کھولنے سے پہلے پڑھیں۔

```bash
git clone https://github.com/tanzeelshujahkhan/evil-hermes.git
cd evil-hermes
uv venv ~/.hermes/venvs/hermes-dev --python 3.11
source ~/.hermes/venvs/hermes-dev/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

مکمل ہرمیس ایجنٹ ٹیسٹ سوٹ (~17k ٹیسٹس) `tests/` میں شائع ہوتا ہے۔

---

## کمیونٹی

- 💬 [Discord](https://discord.gg/nousresearch) — ہرمیس ایجنٹ کمیونٹی
- 🐛 [GitHub Issues](https://github.com/tanzeelshujahkhan/evil-hermes/issues) — بگ رپورٹس اور فیچر کی درخواستیں
- 💡 [GitHub Discussions](https://github.com/tanzeelshujahkhan/evil-hermes/discussions) — سوالات اور ڈیزائن پر بحث
- 📚 [سکلز ہب (Skills Hub)](https://agentskills.io) — ایجنٹ مہارتوں کے لیے کھلا معیار

---

## لائسنس

MIT — [LICENSE](LICENSE) دیکھیں۔

**[Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan) کی تعمیر۔** [ہرمیس ایجنٹ](https://github.com/NousResearch/hermes-agent) سے فورک شدہ — ایک ہی انجن، خود مختار شناخت، آپریٹر کی ملکیت والی پالیسی۔

</div>
