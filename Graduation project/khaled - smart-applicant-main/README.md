# Smart Applicant 📄✨
### AI Resume & Job Description Matcher | نظام مطابقة السيرة الذاتية مع متطلبات الوظائف بالذكاء الاصطناعي
> **Graduation Project / مشروع تخرج متكامل**  
> Built with Python (Flask), Scikit-Learn (TF-IDF & Cosine Similarity), pdfplumber, SQLite (SQLAlchemy), Tailwind CSS, and Vanilla JavaScript.

---

## 📌 Project Overview (نظرة عامة على المشروع)

**Smart Applicant** is a full-stack AI-driven web application designed to help job seekers and recruitment teams evaluate the compatibility between candidate resumes (in PDF format) and target job descriptions.

By leveraging **Natural Language Processing (NLP)** and **Vector Space Modeling**, the system extracts textual content from resumes, tokenizes and computes numerical weight vectors using **TF-IDF (Term Frequency-Inverse Document Frequency)**, and calculates the exact directional correlation via **Cosine Similarity**. 

The application produces:
1. **Accurate Match Score (0 - 100%)** with color-coded ATS compatibility ratings.
2. **Matched Keywords**: Crucial qualifications and technical skills found in both the resume and the job posting.
3. **Missing Keywords Gap Analysis**: High-weight job requirements absent from the resume, prioritized by their TF-IDF significance.
4. **Targeted AI Optimization Advice**: Concrete suggestions to improve the resume's ATS ranking.
5. **Persistent History**: All scans are automatically recorded in an embedded SQLite database.
6. **Print / Export Ready**: One-click printable executive report for review or presentation.

---

## 🧠 Scientific & Mathematical Foundation (الأساس الرياضي والعلمي لمناقشة التخرج)

During the academic graduation defense, this section demonstrates the theoretical rigor behind the matching engine:

### 1. TF-IDF (Term Frequency - Inverse Document Frequency)
TF-IDF quantifies the importance of a term $t$ within a document $d$ relative to a collection of documents $D$:

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

Where:
- **Term Frequency (TF)**:
  $$\text{TF}(t, d) = \frac{f_{t, d}}{\sum_{t' \in d} f_{t', d}}$$
- **Inverse Document Frequency (IDF)**:
  $$\text{IDF}(t, D) = \ln\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$

*Intuition*: Common stop words ("the", "and", "is") yield near-zero IDF weights, whereas domain-specific technical terms ("Python", "SQLAlchemy", "Tailwind", "Machine Learning") receive high weights.

### 2. Cosine Similarity (حساب التشابه الجيبي في الفضاء المتجهي)
Rather than comparing raw keyword frequencies (which would unfairly bias long resumes over concise ones), Cosine Similarity computes the cosine of the angle between the two normalized feature vectors in $N$-dimensional space:

$$\text{Cosine Similarity}(\mathbf{A}, \mathbf{B}) = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\|_2 \|\mathbf{B}\|_2} = \frac{\sum_{i=1}^n A_i B_i}{\sqrt{\sum_{i=1}^n A_i^2} \sqrt{\sum_{i=1}^n B_i^2}}$$

- **1.0 (100%)**: Perfect alignment; the resume covers the identical vocabulary distribution as the job description.
- **0.0 (0%)**: Orthogonal vectors; zero shared technical keywords.

---

## 🏗️ System Architecture (معمارية النظام)

```
                       +-----------------------------------+
                       |        Client Web Browser         |
                       | (HTML5, Tailwind CSS, Vanilla JS) |
                       +-----------------------------------+
                                    |         ^
          1. Upload PDF + Job Desc  |         |  4. Dynamic Results & History
                                    v         |
                       +-----------------------------------+
                       |         Flask REST API            |
                       |             (app.py)              |
                       +-----------------------------------+
                             |                      |
                 2. Extract  |                      |  3. NLP Analysis
                             v                      v
           +--------------------+         +-------------------------------+
           |     pdfplumber     |         |         scikit-learn          |
           |  (Text Extraction) |         | - TfidfVectorizer(ngram=(1,2))|
           +--------------------+         | - cosine_similarity           |
                                          +-------------------------------+
                                                    |
                                                    v
                                       +--------------------------+
                                       | SQLite DB via SQLAlchemy |
                                       |   - users table          |
                                       |   - analysis_history     |
                                       +--------------------------+
```

---

## 📁 Project Structure (هيكل ملفات المشروع)

```bash
smart-applicant/
├── app.py                      # Flask Application, SQLite Models, NLP pipeline & Endpoints
├── requirements.txt            # Python dependencies (Flask, scikit-learn, pdfplumber, etc.)
├── run.bat                     # 1-Click Windows execution script
├── generate_sample_resume.py   # Script to generate sample PDF resume
├── sample_resume.pdf           # Sample resume for instant testing and demonstration
├── .gitignore                  # Git ignore rules for clean repository
├── README.md                   # Complete academic and operational documentation
├── templates/
│   └── index.html              # Main dashboard interface with Tailwind CSS & Modals
├── static/
│   ├── css/
│   │   └── style.css           # Custom micro-animations, scrollbars, and print layout
│   └── js/
│       └── main.js             # Drag-and-drop, asynchronous Fetch calls, dynamic charts
├── instance/
│   └── smart_applicant.db      # SQLite database (auto-generated)
└── uploads/                    # Temporary secure upload directory
```

---

## 🚀 Quick Start Guide (طريقة التشغيل السريعة)

### Option A: 1-Click Runner on Windows (الطريقة الأسهل)
Simply double click:
```bash
run.bat
```
The script will automatically detect Python, install dependencies, and launch the web server.

### Option B: Manual Setup (التشغيل اليدوي خطوة بخطوة)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/khaledmohamedabdullatif55-source/smart-applicant.git
   cd smart-applicant
   ```

2. **Create and Activate Virtual Environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   # Or on Command Prompt:
   # .\.venv\Scripts\activate.bat
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate the Sample Resume** (if not already created):
   ```bash
   python generate_sample_resume.py
   ```

5. **Start the Web Application**:
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to:
   👉 **http://127.0.0.1:5000**

---

## 🔌 REST API Endpoints (واجهات برمجة التطبيقات)

| Method | Endpoint | Description | Payload |
|---|---|---|---|
| `GET` | `/` | Renders the web application dashboard | None |
| `POST` | `/api/analyze` | Processes PDF resume and Job Description, returns score & keywords | `multipart/form-data`: `resume` (PDF file), `job_description` (text) |
| `GET` | `/api/history` | Fetches recent analysis records from SQLite | None |
| `DELETE` | `/api/history/<id>` | Deletes an analysis record by ID | None |
| `GET` | `/api/sample-job/<type>` | Returns preset job descriptions (`fullstack`, `datascientist`, `frontend`) | URL parameter |

---

## 🧪 Testing & Demonstration Guide (دليل العرض للجنة التحكيم)

1. Open **http://127.0.0.1:5000**.
2. **Drag & Drop** the provided `sample_resume.pdf` into the upload zone.
3. Click one of the **Quick Presets** (e.g., **Full-Stack Dev** or **Data Scientist**).
4. Click **"Analyze Resume & Calculate Match"**.
5. Observe the smooth circular score animation, green matched pills, red missing pills, and tailored recommendations.
6. Click **"Print / Save PDF"** to demonstrate the formatted report layout.
7. Click **"History"** in the top navigation bar to show the SQLite database persistence.
8. Click **"Algorithm (عن الخوارزمية)"** to explain the mathematical foundation to your professors.

---

**Developed for Graduation Project.**
