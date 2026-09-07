"""
Automated unit & integration test for Smart Applicant
"""
import os
import io
import json
from app import app, db, init_db, extract_text_from_pdf, extract_keywords_and_similarity, AnalysisHistory

def run_tests():
    print("[TEST] 1. Testing Database Initialization...")
    init_db()
    with app.app_context():
        count = AnalysisHistory.query.count()
        print(f"      Initial analysis records count: {count}")

    print("[TEST] 2. Testing PDF Text Extraction...")
    sample_pdf_path = os.path.join(os.path.dirname(__file__), 'sample_resume.pdf')
    assert os.path.exists(sample_pdf_path), "sample_resume.pdf does not exist!"
    extracted_text = extract_text_from_pdf(sample_pdf_path)
    assert len(extracted_text) > 100, f"Extracted text too short: {len(extracted_text)}"
    print(f"      Extracted {len(extracted_text)} characters successfully.")
    assert "Ahmed Hassan" in extracted_text
    assert "Flask" in extracted_text

    print("[TEST] 3. Testing NLP & Cosine Similarity Engine...")
    sample_jd = (
        "We are looking for a Senior Full-Stack Python Developer. "
        "Requirements: Python, Flask, SQLAlchemy, SQLite, Scikit-Learn, Tailwind CSS, Docker, and Git."
    )
    result = extract_keywords_and_similarity(extracted_text, sample_jd)
    print(f"      Calculated Match Score: {result['match_score']}%")
    print(f"      Found Keywords ({result['total_found_count']}): {result['found_keywords'][:5]}...")
    print(f"      Missing Keywords ({result['total_missing_count']}): {result['missing_keywords'][:5]}...")
    assert result['match_score'] > 0.0, "Score should be greater than 0"
    assert len(result['found_keywords']) > 0, "Should have found keywords"
    assert len(result['recommendations']) > 0, "Should have generated recommendations"

    print("[TEST] 4. Testing Flask API Client Endpoints...")
    client = app.test_client()

    # Test GET /
    res_index = client.get('/')
    assert res_index.status_code == 200, f"GET / failed with {res_index.status_code}"
    print("      GET / returned 200 OK.")

    # Test POST /api/analyze with sample_resume.pdf
    with open(sample_pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    data = {
        'resume': (io.BytesIO(pdf_bytes), 'sample_resume.pdf', 'application/pdf'),
        'job_description': sample_jd
    }
    res_analyze = client.post('/api/analyze', data=data, content_type='multipart/form-data')
    assert res_analyze.status_code == 200, f"POST /api/analyze failed with {res_analyze.status_code}: {res_analyze.data.decode('utf-8')}"
    analyze_json = res_analyze.get_json()
    assert analyze_json['success'] is True
    print(f"      POST /api/analyze succeeded! Result ID: {analyze_json['id']}, Score: {analyze_json['match_score']}%")

    # Test GET /api/history
    res_history = client.get('/api/history')
    assert res_history.status_code == 200
    history_json = res_history.get_json()
    assert history_json['success'] is True
    assert len(history_json['history']) >= 1
    print(f"      GET /api/history succeeded! Retrieved {len(history_json['history'])} records.")

    print("\n==========================================")
    print("  ALL TESTS PASSED WITH 100% SUCCESS!  ")
    print("==========================================")

if __name__ == '__main__':
    run_tests()
