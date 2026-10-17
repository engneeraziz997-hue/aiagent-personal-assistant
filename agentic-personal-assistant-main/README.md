# المساعد الشخصي الذكي (Agentic Personal Assistant)

تطبيق متكامل لاسترجاع المعلومات المعززة بالذكاء الاصطناعي (RAG) يتيح للمستخدمين رفع ملفات PDF والتفاعل معها من خلال محادثة ذكية مع مساعد يعتمد على نماذج الذكاء الاصطناعي.

## 🚀 المميزات الرئيسية

- **رفع الوثائق (PDF)**: رفع ومعالجة ملفات PDF وتخزينها في قاعدة بيانات متجهة.
- **المحادثة الذكية**: وكيل ذكي يقرر متى يبحث في قاعدة المعرفة.
- **ذاكرة المحادثة**: يحتفظ بسياق المحادثة عبر الأسئلة المتعددة.
- **واجهة مستخدم عصرية**: واجهة شبيهة بـ ChatGPT مع إمكانية رفع الملفات.
- **إمكانية المراقبة**: متكامل مع LangSmith و LangChain Python للمراقبة والتتبع.

---

## 🏗️ هيكلية المشروع التقنية

### الباك إند (Python / FastAPI)
- **السيرفر**: FastAPI يعمل على Uvicorn مع دعم CORS ورفع الملفات.
- **الوكيل الذكي (Agent)**: LangChain / LangGraph مع نموذج OpenAI GPT-4o.
- **قاعدة البيانات المتجهة**: Pinecone لتخزين الوثائق والبحث بالتشابه.
- **نموذج التضمين (Embeddings)**: نموذج Pinecone `llama-text-embed-v2`.
- **المراقبة**: LangSmith للتتبع والمراقبة.

### الفرونت إند (React / Vite)
- **إطار العمل**: React مع Vite للتطوير السريع.
- **التصميم**: واجهة داكنة مستوحاة من ChatGPT.
- **رفع الملفات**: رفع ملفات PDF مع تقديم تغذية راجعة فورية.
- **واجهة المحادثة**: رسائل فورية مع مؤشرات الكتابة.

---

## 📋 المتطلبات الأساسية

- **Python** (الإصدار 3.9 أو أعلى) - للباك إند.
- **Node.js** (الإصدار 18 أو أعلى) - للفرونت إند.
- حساب فعّال على **Pinecone** مع إنشاء Index.
- مفتاح API خاص بـ **OpenAI**.

---

## 🛠️ خطوات الإعداد والتثبيت

### 1. الانتقال إلى مجلد المشروع
```bash
cd agentic-personal-assistant-maim
```

### 2. إعداد الباك إند (Python)
```bash
cd server
pip install -r requirements.txt
```

### 3. ضبط متغيرات البيئة
أنشئ ملف `.env` داخل مجلد `server/` وأضف مفاتيحك:
```env
# نموذج الذكاء الاصطناعي
OPENAI_API_KEY=your_openai_api_key

# قاعدة البيانات المتجهة (Pinecone)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=your_pinecone_index_name

# LangSmith للمراقبة (اختياري)
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT="Agentic Personal Assistant"
```

### 4. إعداد الفرونت إند (React)
```bash
cd ../client
npm install
```

---

## 🚀 تشغيل التطبيق

### 1. تشغيل الباك إند (Python FastAPI)
```bash
cd server
python main.py
```
سيعمل السيرفر على `http://localhost:3001`

### 2. تشغيل الفرونت إند (React)
```bash
cd client
npm run dev
```
سيعمل تطبيق الواجهة على `http://localhost:5173`

---

## 📁 هيكل الملفات والمجلدات

```
agentic-personal-assistant-maim/
├── server/                    # الباك إند بلغة Python
│   ├── main.py               # سيرفر FastAPI والمسارات (/api/chat, /api/ingest)
│   ├── agent.py              # منطق الوكيل الذكي وإدارة الذاكرة
│   ├── tools.py              # أداة البحث في قاعدة معرفة Pinecone
│   ├── ingest.py             # خط أنابيب معالجة وتضمين ملفات PDF
│   ├── requirements.txt      # مكتبات Python المطلوبة
│   └── .env.example          # نموذج متغيرات البيئة
├── client/                    # الفرونت إند بـ React
│   ├── src/
│   │   ├── App.jsx           # المكوّن الرئيسي للتطبيق
│   │   ├── App.css           # تنسيقات الواجهة على طراز ChatGPT
│   │   └── main.jsx          # نقطة الدخول لـ React
│   └── package.json          # اعتماديات الفرونت إند
└── README.md                  # ملف التوثيق
```

---

## 🔄 آلية عمل النظام

### رفع الوثائق (PDF Ingestion)
1. يقوم المستخدم برفع ملف PDF عبر واجهة React.
2. يستقبل FastAPI الملف على المسار `/api/ingest` ويمرره لـ `ingest.py`.
3. يُقرأ نص الـ PDF باستخدام `PyPDFLoader` ويُقسَّم إلى أجزاء بحجم 1000 حرف مع تداخل 200 حرف.
4. تُحوَّل الأجزاء إلى تضمينات (Embeddings) بنموذج `llama-text-embed-v2` وتُخزَّن في Pinecone.

### آلية المحادثة الذكية
1. يُرسل المستخدم سؤاله عبر المسار `/api/chat`.
2. يعالج `agent.py` الرسالة باستخدام `gpt-4o`.
3. إذا لزم الأمر، يُشغِّل الوكيل أداة `search_knowledge_base` في `tools.py`.
4. تُسترجع الأجزاء ذات الصلة من Pinecone وتُقدَّم للنموذج كسياق.
5. يُرجع الوكيل إجابة دقيقة منسقة بـ Markdown.

---

## 🐛 استكشاف الأخطاء وحلها

### 1. خطأ: رفض الاتصال (Connection Refused)
- تأكد من أن الباك إند يعمل على البورت `3001`.
- تحقق من عدم وجود تعارض في المنافذ.

### 2. متغيرات البيئة غير موجودة
- تأكد من وجود ملف `.env` داخل مجلد `server/`.
- تحقق من أن جميع مفاتيح API مُدرجة وصحيحة.

### 3. أخطاء Pinecone
- تحقق من وجود الـ Index في Pinecone.
- تأكد من صحة مفاتيح الـ API وصلاحياتها.
- تأكد من أن نموذج التضمين هو نفسه عند الرفع والاسترجاع.

---

## 📚 التقنيات المستخدمة

| الجزء | التقنية |
| :--- | :--- |
| **الباك إند** | Python, FastAPI, Uvicorn, python-multipart |
| **الفرونت إند** | React, Vite |
| **الذكاء الاصطناعي** | LangChain, LangGraph, OpenAI GPT-4o |
| **قاعدة البيانات** | Pinecone Vector Store |
| **معالجة الـ PDF** | PyPDF, RecursiveCharacterTextSplitter |
| **المراقبة** | LangSmith |

---

## 📄 الرخصة

هذا المشروع مرخص بموجب رخصة MIT.
