"""
Generate a realistic sample PDF resume for testing Smart Applicant.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf(output_filename="sample_resume.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1e3a8a')
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569')
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=10,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # Header
    story.append(Paragraph("Ahmed Hassan", title_style))
    story.append(Paragraph("Full-Stack Software Engineer & Machine Learning Enthusiast | Cairo, Egypt<br/>Email: ahmed.hassan@example.com | GitHub: github.com/ahmed-hassan | LinkedIn: linkedin.com/in/ahmed-hassan", subtitle_style))
    story.append(Spacer(1, 12))

    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
    story.append(Paragraph(
        "Passionate Full-Stack Developer with 3+ years of experience building modern web applications, scalable RESTful APIs, and NLP data pipelines. Proficient in Python, Flask, SQLite, PostgreSQL, and SQLAlchemy ORM. Experienced with modern frontend technologies including HTML5, Tailwind CSS, and JavaScript. Dedicated to clean code architecture, automated testing, and agile development.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", section_style))
    skills_data = [
        [Paragraph("<b>Programming Languages:</b>", body_style), Paragraph("Python, JavaScript (ES6+), SQL, HTML5, CSS3", body_style)],
        [Paragraph("<b>Frameworks & Libraries:</b>", body_style), Paragraph("Flask, SQLAlchemy, Scikit-Learn, Pandas, NumPy, Tailwind CSS", body_style)],
        [Paragraph("<b>Databases:</b>", body_style), Paragraph("SQLite, PostgreSQL, MySQL", body_style)],
        [Paragraph("<b>Developer Tools:</b>", body_style), Paragraph("Git, GitHub, Docker, Postman, Linux, VS Code", body_style)],
        [Paragraph("<b>Machine Learning / NLP:</b>", body_style), Paragraph("TF-IDF Vectorization, Cosine Similarity, Text Mining, pdfplumber", body_style)]
    ]
    t = Table(skills_data, colWidths=[150, 380])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # Experience
    story.append(Paragraph("WORK EXPERIENCE", section_style))
    story.append(Paragraph("<b>Software Engineer</b> | TechCorp Solutions (2023 - Present)", body_style))
    story.append(Paragraph("• Engineered RESTful APIs using Python and Flask with SQLite and PostgreSQL databases.<br/>• Integrated TF-IDF vectorization and Cosine Similarity algorithms to automate text classification.<br/>• Built responsive frontend interfaces using Tailwind CSS and modern JavaScript Fetch API.<br/>• Optimized SQL queries and reduced database response latency by 25%.", body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Junior Web Developer</b> | Innovate Agency (2021 - 2023)", body_style))
    story.append(Paragraph("• Developed dynamic web applications with Python, HTML5, and CSS3.<br/>• Implemented user authentication and role-based access control.<br/>• Collaborated with cross-functional teams in an Agile/Scrum environment using Git.", body_style))
    story.append(Spacer(1, 8))

    # Education
    story.append(Paragraph("EDUCATION", section_style))
    story.append(Paragraph("<b>B.Sc. in Computer Science & Information Systems</b> (2020 - 2024)<br/>Graduation Project: AI Resume & Job Description Matcher (Grade: Excellent)", body_style))

    doc.build(story)
    print(f"Sample resume generated: {output_filename}")

if __name__ == '__main__':
    generate_pdf()
