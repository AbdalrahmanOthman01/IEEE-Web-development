"""
Smart Applicant - AI Resume & Job Description Matcher
=====================================================
Graduation Project: Full-Stack NLP Web Application
Backend: Flask, Flask-SQLAlchemy, SQLite
Text Processing: pdfplumber, scikit-learn (TfidfVectorizer, cosine_similarity)
"""

import os
import re
import json
from datetime import datetime
from typing import Tuple, List, Dict, Any

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# -----------------------------------------------------------------------------
# App Configuration
# -----------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'smart-applicant-secret-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'smart_applicant.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename: str) -> bool:
    """Check if uploaded file has allowed extension (.pdf)."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# -----------------------------------------------------------------------------
# Database Models
# -----------------------------------------------------------------------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    analyses = db.relationship('AnalysisHistory', backref='user', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

class AnalysisHistory(db.Model):
    __tablename__ = 'analysis_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    job_title = db.Column(db.String(255), nullable=False, default="Untitled Position")
    match_score = db.Column(db.Float, nullable=False)
    found_keywords = db.Column(db.Text, nullable=True)    # JSON string
    missing_keywords = db.Column(db.Text, nullable=True)  # JSON string
    recommendations = db.Column(db.Text, nullable=True)   # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'job_title': self.job_title,
            'match_score': round(self.match_score, 1),
            'found_keywords': json.loads(self.found_keywords) if self.found_keywords else [],
            'missing_keywords': json.loads(self.missing_keywords) if self.missing_keywords else [],
            'recommendations': json.loads(self.recommendations) if self.recommendations else [],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

# -----------------------------------------------------------------------------
# NLP & Text Processing Engine
# -----------------------------------------------------------------------------
# Common English stopwords to clean text and prioritize meaningful terms
COMMON_STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
    'any', 'are', 'aren\'t', 'as', 'at', 'be', 'because', 'been', 'before', 'being',
    'below', 'between', 'both', 'but', 'by', 'can', 'can\'t', 'cannot', 'could',
    'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t',
    'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn\'t',
    'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'he\'d', 'he\'ll', 'he\'s',
    'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how',
    'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is',
    'isn\'t', 'it', 'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most',
    'mustn\'t', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once',
    'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over',
    'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should',
    'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their',
    'theirs', 'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they',
    'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through', 'to',
    'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll',
    'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when', 'when\'s',
    'where', 'where\'s', 'which', 'while', 'who', 'who\'s', 'whom', 'why', 'why\'s',
    'with', 'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d', 'you\'ll', 'you\'re',
    'you\'ve', 'your', 'yours', 'yourself', 'yourselves', 'will', 'also', 'etc',
    'including', 'well', 'must', 'able', 'years', 'experience', 'work', 'working',
    'role', 'responsible', 'requirements', 'skills', 'responsibilities', 'team'
}

def extract_text_from_pdf(filepath: str) -> str:
    """Extract all text pages from a PDF file using pdfplumber."""
    extracted_text = []
    try:
        with pdfplumber.open(filepath) as pdf:
            for page_index, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(page_text)
    except Exception as exc:
        raise RuntimeError(f"Failed to extract PDF content: {str(exc)}")

    full_text = "\n".join(extracted_text).strip()
    return full_text

def clean_text(text: str) -> str:
    """Normalize text: lowercase, remove punctuation, reduce extra whitespace."""
    if not text:
        return ""
    # Lowercase
    text = text.lower()
    # Replace newlines, tabs with space
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # Remove unwanted special characters but preserve alphanumeric and hyphens/dots in tech names
    text = re.sub(r'[^a-z0-9+#.\s-]', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_keywords_and_similarity(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Compute Cosine Similarity via TF-IDF vectorization and extract
    matched vs. missing keywords between Resume and Job Description.
    """
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    if not cleaned_resume:
        raise ValueError("The uploaded resume PDF contains no extractable text.")
    if not cleaned_jd:
        raise ValueError("Job description is empty. Please provide the job requirements.")

    # 1. Compute TF-IDF & Cosine Similarity
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=2000,
        sublinear_tf=True
    )
    
    # Fit on both documents
    tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    
    # Cosine similarity between resume (row 0) and job description (row 1)
    sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    raw_similarity = float(sim_matrix[0][0])
    
    # Scale to percentage 0 - 100%
    match_score = round(raw_similarity * 100.0, 1)

    # 2. Keyword Extraction based on TF-IDF in Job Description
    feature_names = np.array(vectorizer.get_feature_names_out())
    jd_tfidf_scores = tfidf_matrix[1].toarray().flatten()

    # Get non-zero features in Job Description sorted by TF-IDF weight descending
    nonzero_indices = np.where(jd_tfidf_scores > 0)[0]
    sorted_indices = nonzero_indices[np.argsort(-jd_tfidf_scores[nonzero_indices])]

    found_keywords = []
    missing_keywords = []

    # Prepare words sets for fast substring/word checking
    resume_tokens = set(re.findall(r'\b[a-z0-9+#.-]+\b', cleaned_resume))

    for idx in sorted_indices:
        term = feature_names[idx]
        # Ignore purely generic single character or common stop words
        if len(term) <= 2 or term in COMMON_STOPWORDS:
            continue

        # Check if term exists in resume tokens or as a substring
        if term in resume_tokens or f" {term} " in f" {cleaned_resume} ":
            if term not in found_keywords:
                found_keywords.append(term)
        else:
            if term not in missing_keywords:
                missing_keywords.append(term)

    # Limit to top most relevant keywords for clear presentation
    top_found = found_keywords[:30]
    top_missing = missing_keywords[:30]

    # 3. Generate Targeted AI Recommendations
    recommendations = generate_recommendations(match_score, top_found, top_missing, cleaned_resume, cleaned_jd)

    # 4. Extract Job Title Candidate (First line or prominent title words)
    job_title = extract_job_title(job_description)

    return {
        'match_score': match_score,
        'job_title': job_title,
        'found_keywords': top_found,
        'missing_keywords': top_missing,
        'total_found_count': len(top_found),
        'total_missing_count': len(top_missing),
        'recommendations': recommendations,
        'resume_word_count': len(cleaned_resume.split()),
        'jd_word_count': len(cleaned_jd.split())
    }

def extract_job_title(jd_text: str) -> str:
    """Extract a likely job title from the first lines of the job description."""
    lines = [l.strip() for l in jd_text.splitlines() if l.strip()]
    for line in lines[:3]:
        cleaned = re.sub(r'^(job title|position|role|title)\s*[:\-]\s*', '', line, flags=re.I).strip()
        if 3 <= len(cleaned) <= 60:
            return cleaned.title()
    # Fallback to first line or default
    if lines:
        return lines[0][:40].title()
    return "Target Job Position"

def generate_recommendations(score: float, found: List[str], missing: List[str], resume: str, jd: str) -> List[Dict[str, str]]:
    """Generate structured, actionable advice to boost the candidate's match score."""
    recs = []

    # Category 1: Score Assessment
    if score >= 75.0:
        recs.append({
            'type': 'success',
            'title': 'High Alignment Profile',
            'text': f'Your resume demonstrates strong technical resonance ({score}%). You cover major requirements. Focus on quantifying your impact (e.g., "Increased performance by 35%").'
        })
    elif score >= 50.0:
        recs.append({
            'type': 'warning',
            'title': 'Moderate Match - Action Needed',
            'text': f'Your resume matches {score}% of the target profile. Adding 3-5 prioritized missing keywords in your project bullet points can raise your score into the top tier.'
        })
    else:
        recs.append({
            'type': 'danger',
            'title': 'Significant Keyword Gap',
            'text': f'Your current match score is {score}%. ATS (Applicant Tracking Systems) may filter this resume out. Substantial alignment with the missing required skills is recommended.'
        })

    # Category 2: Missing Keywords Focus
    if missing:
        top_critical = missing[:5]
        recs.append({
            'type': 'info',
            'title': 'High-Priority Missing Keywords',
            'text': f'We recommend adding these critical job keywords to your experience or skills section: {", ".join([f"<strong>{k}</strong>" for k in top_critical])}.'
        })

    # Category 3: Resume Length & Structure Check
    word_count = len(resume.split())
    if word_count < 250:
        recs.append({
            'type': 'warning',
            'title': 'Resume Length is Relatively Short',
            'text': f'Your resume contains approximately {word_count} words. Standard professional resumes usually range between 400 to 700 words to sufficiently detail projects and competencies.'
        })
    elif word_count > 1200:
        recs.append({
            'type': 'warning',
            'title': 'Resume is Overly Lengthy',
            'text': f'Your resume contains {word_count} words. Consider condensing to 1-2 pages focused specifically on the target role.'
        })
    else:
        recs.append({
            'type': 'success',
            'title': 'Optimal Resume Length',
            'text': f'Resume word count ({word_count} words) is within standard 1-2 page executive limits.'
        })

    # Category 4: Action Verbs & Metrics
    action_verbs = ['developed', 'engineered', 'spearheaded', 'optimized', 'implemented', 'designed', 'managed', 'created', 'built', 'led']
    has_verbs = any(verb in resume for verb in action_verbs)
    if not has_verbs:
        recs.append({
            'type': 'info',
            'title': 'Strengthen Bullet Points with Action Verbs',
            'text': 'Enhance your job accomplishments using strong active verbs such as "Engineered", "Optimized", "Spearheaded", and "Deployed".'
        })

    return recs

# -----------------------------------------------------------------------------
# Web & API Endpoints
# -----------------------------------------------------------------------------
@app.route('/')
def index():
    """Renders the main dashboard interface."""
    return render_template('index.html')

@app.route('/sample_resume.pdf')
def download_sample():
    """Serves the sample resume PDF for instant testing."""
    sample_file = os.path.join(BASE_DIR, 'sample_resume.pdf')
    if not os.path.exists(sample_file):
        return jsonify({'error': 'Sample resume not yet generated.'}), 404
    return send_from_directory(BASE_DIR, 'sample_resume.pdf', as_attachment=True)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    POST /api/analyze
    Payload:
      - resume: PDF file
      - job_description: string
    """
    # 1. Validation
    if 'resume' not in request.files:
        return jsonify({'success': False, 'error': 'No resume file uploaded. Please select a PDF file.'}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No resume file selected.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file format. Only PDF files are supported.'}), 400

    job_description = request.form.get('job_description', '').strip()
    if not job_description:
        return jsonify({'success': False, 'error': 'Job description is required.'}), 400

    saved_path = None
    try:
        # 2. Save file temporarily
        orig_filename = secure_filename(file.filename) or 'resume.pdf'
        timestamp_prefix = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = f"{timestamp_prefix}_{orig_filename}"
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
        file.save(saved_path)

        # 3. Extract text from PDF
        resume_text = extract_text_from_pdf(saved_path)
        if not resume_text.strip():
            return jsonify({
                'success': False,
                'error': 'Could not extract text from this PDF. It may be scanned images. Please upload a searchable text PDF.'
            }), 400

        # 4. Run NLP Analysis
        analysis_result = extract_keywords_and_similarity(resume_text, job_description)

        # 5. Save to SQLite Database
        history_record = AnalysisHistory(
            user_id=1,  # Default demo user
            filename=orig_filename,
            job_title=analysis_result['job_title'],
            match_score=analysis_result['match_score'],
            found_keywords=json.dumps(analysis_result['found_keywords']),
            missing_keywords=json.dumps(analysis_result['missing_keywords']),
            recommendations=json.dumps(analysis_result['recommendations']),
            created_at=datetime.utcnow()
        )
        db.session.add(history_record)
        db.session.commit()

        # 6. Return comprehensive response
        return jsonify({
            'success': True,
            'id': history_record.id,
            'filename': orig_filename,
            'job_title': analysis_result['job_title'],
            'match_score': analysis_result['match_score'],
            'found_keywords': analysis_result['found_keywords'],
            'missing_keywords': analysis_result['missing_keywords'],
            'recommendations': analysis_result['recommendations'],
            'total_found_count': analysis_result['total_found_count'],
            'total_missing_count': analysis_result['total_missing_count'],
            'resume_word_count': analysis_result['resume_word_count'],
            'jd_word_count': analysis_result['jd_word_count'],
            'created_at': history_record.created_at.strftime('%Y-%m-%d %H:%M')
        })

    except Exception as exc:
        db.session.rollback()
        return jsonify({'success': False, 'error': f"Analysis error: {str(exc)}"}), 500

    finally:
        # Clean up temporary uploaded file if desired
        if saved_path and os.path.exists(saved_path):
            try:
                os.remove(saved_path)
            except OSError:
                pass

@app.route('/api/history', methods=['GET'])
def get_history():
    """Retrieve the recent analysis history from SQLite."""
    try:
        records = AnalysisHistory.query.order_by(AnalysisHistory.created_at.desc()).limit(20).all()
        return jsonify({
            'success': True,
            'history': [r.to_dict() for r in records]
        })
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500

@app.route('/api/history/<int:history_id>', methods=['DELETE'])
def delete_history(history_id: int):
    """Delete a specific analysis record."""
    try:
        record = AnalysisHistory.query.get_or_404(history_id)
        db.session.delete(record)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Record deleted successfully.'})
    except Exception as exc:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(exc)}), 500

@app.route('/api/sample-job/<job_type>', methods=['GET'])
def get_sample_job(job_type: str):
    """Provide curated sample job descriptions for quick testing during presentations."""
    samples = {
        'fullstack': (
            "Senior Full-Stack Developer\n"
            "We are seeking an experienced Full-Stack Engineer with proficiency in Python, Flask or Django, "
            "and modern frontend web development (HTML5, Tailwind CSS, JavaScript, React). "
            "Key Requirements:\n"
            "- Strong background in RESTful APIs, SQLite / PostgreSQL, and SQLAlchemy ORM.\n"
            "- Experience in Natural Language Processing (NLP), Scikit-Learn, TF-IDF, and text classification.\n"
            "- Git version control, Docker containerization, CI/CD pipelines, and unit testing.\n"
            "- Excellent problem solving, clean code architecture, and agile software development."
        ),
        'datascientist': (
            "Data Scientist / Machine Learning Engineer\n"
            "Looking for a Data Scientist to build predictive NLP and machine learning models.\n"
            "Requirements:\n"
            "- Proficiency in Python, Pandas, NumPy, Scikit-learn, and PyTorch or TensorFlow.\n"
            "- Expertise in Text Mining, Cosine Similarity, Vectorization, and Sentiment Analysis.\n"
            "- Experience building and deploying Machine Learning REST APIs with Flask or FastAPI.\n"
            "- Strong foundation in statistics, data visualization, and database management."
        ),
        'frontend': (
            "Frontend UI/UX Web Developer\n"
            "Requirements:\n"
            "- Deep knowledge of HTML5, CSS3, Tailwind CSS, Responsive Design, and modern JavaScript (ES6+).\n"
            "- Experience interacting with backend RESTful APIs via Fetch API and Async/Await.\n"
            "- Component design systems, micro-animations, user accessibility (a11y), and performance optimization.\n"
            "- Familiarity with Git, Figma designs to code, and modern frontend tools."
        )
    }
    content = samples.get(job_type.lower())
    if content:
        return jsonify({'success': True, 'content': content})
    return jsonify({'success': False, 'error': 'Sample job not found.'}), 404

# -----------------------------------------------------------------------------
# Database Initialization & CLI Run
# -----------------------------------------------------------------------------
def init_db():
    """Create database tables and insert a default user if not already present."""
    with app.app_context():
        db.create_all()
        # Seed default test user if needed
        if not User.query.filter_by(email="demo@smartapplicant.ai").first():
            demo_user = User(
                email="demo@smartapplicant.ai",
                password_hash="pbkdf2:sha256:dummyhashforgradproject2026"
            )
            db.session.add(demo_user)
            db.session.commit()
            print("[Database] Initialized tables and default user.")

if __name__ == '__main__':
    init_db()
    print("=======================================================")
    print("  Smart Applicant Web Server Running")
    print("  Local:   http://127.0.0.1:5000")
    print("  Network: http://0.0.0.0:5000")
    print("=======================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)
