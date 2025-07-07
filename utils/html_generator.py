from utils.pdf_parser import parse_resume_data
import openai
import os
from typing import Dict, Any

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_portfolio_html(resume_text: str) -> str:
    """Generate a complete portfolio HTML from resume text"""
    
    # Parse resume data
    resume_data = parse_resume_data(resume_text)
    
    # Enhance data with GPT if API key is available
    if openai.api_key:
        try:
            enhanced_data = enhance_with_gpt(resume_data, resume_text)
            resume_data.update(enhanced_data)
        except Exception as e:
            print(f"GPT enhancement failed: {e}")
    
    # Generate HTML
    html_content = create_portfolio_html(resume_data)
    return html_content

def enhance_with_gpt(resume_data: Dict[str, Any], resume_text: str) -> Dict[str, Any]:
    """Use GPT to enhance and improve resume data"""
    
    prompt = f"""
    Analyze this resume and improve the content for a professional portfolio website:

    Resume Text:
    {resume_text[:2000]}  # Limit text to avoid token limits

    Current parsed data:
    Name: {resume_data.get('name', 'N/A')}
    Email: {resume_data.get('email', 'N/A')}
    Phone: {resume_data.get('phone', 'N/A')}
    Summary: {resume_data.get('summary', 'N/A')}

    Please provide:
    1. An improved professional summary (2-3 sentences)
    2. A catchy tagline for the portfolio
    3. 3-5 key achievements or highlights
    4. Improved skill categorization

    Return as JSON format:
    {{
        "improved_summary": "...",
        "tagline": "...",
        "achievements": ["...", "...", "..."],
        "skill_categories": {{
            "Technical": ["...", "..."],
            "Tools": ["...", "..."],
            "Soft Skills": ["...", "..."]
        }}
    }}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.7
    )
    
    import json
    enhanced_data = json.loads(response.choices[0].message.content)
    return enhanced_data

def create_portfolio_html(data: Dict[str, Any]) -> str:
    """Create the complete portfolio HTML"""
    
    name = data.get('name', 'Your Name')
    email = data.get('email', '')
    phone = data.get('phone', '')
    summary = data.get('improved_summary', data.get('summary', ''))
    tagline = data.get('tagline', 'Professional Developer & Problem Solver')
    achievements = data.get('achievements', [])
    skills = data.get('skills', [])
    skill_categories = data.get('skill_categories', {})
    experience = data.get('experience', [])
    education = data.get('education', [])
    projects = data.get('projects', [])
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Portfolio</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
        }}
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 0;
            text-align: center;
        }}
        .section-title {{
            color: #333;
            margin-bottom: 30px;
            font-weight: 600;
        }}
        .skill-badge {{
            background: #667eea;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            margin: 5px;
            display: inline-block;
            font-size: 0.9em;
        }}
        .experience-card, .project-card {{
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .contact-info {{
            background: #333;
            color: white;
            padding: 50px 0;
        }}
        .navbar {{
            background: rgba(255,255,255,0.95) !important;
            backdrop-filter: blur(10px);
        }}
        .navbar.scrolled {{
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .achievement-item {{
            background: #e8f4f8;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .btn-primary {{
            background: #667eea;
            border-color: #667eea;
        }}
        .btn-primary:hover {{
            background: #5a6fd8;
            border-color: #5a6fd8;
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light fixed-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="#home">{name}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="#skills">Skills</a></li>
                    <li class="nav-item"><a class="nav-link" href="#experience">Experience</a></li>
                    <li class="nav-item"><a class="nav-link" href="#projects">Projects</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero-section">
        <div class="container">
            <h1 class="display-4 fw-bold">{name}</h1>
            <p class="lead mb-4">{tagline}</p>
            <div class="d-flex justify-content-center gap-3">
                <a href="#contact" class="btn btn-primary btn-lg">Get In Touch</a>
                <a href="#projects" class="btn btn-outline-light btn-lg">View Work</a>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-5">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 mx-auto">
                    <h2 class="section-title text-center">About Me</h2>
                    <p class="lead text-center">{summary}</p>
                    
                    {generate_achievements_html(achievements)}
                </div>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center">Skills & Technologies</h2>
            <div class="row">
                {generate_skills_html(skills, skill_categories)}
            </div>
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="py-5">
        <div class="container">
            <h2 class="section-title text-center">Professional Experience</h2>
            {generate_experience_html(experience)}
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center">Featured Projects</h2>
            <div class="row">
                {generate_projects_html(projects)}
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact-info">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 mx-auto text-center">
                    <h2 class="mb-4">Let's Get In Touch</h2>
                    <p class="lead mb-4">Ready to start your next project? Let's connect and discuss how we can work together.</p>
                    <div class="d-flex justify-content-center gap-4 flex-wrap">
                        {f'<a href="mailto:{email}" class="btn btn-outline-light"><i class="fas fa-envelope"></i> {email}</a>' if email else ''}
                        {f'<a href="tel:{phone}" class="btn btn-outline-light"><i class="fas fa-phone"></i> {phone}</a>' if phone else ''}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="py-4 bg-dark text-white text-center">
        <div class="container">
            <p>&copy; 2024 {name}. All rights reserved.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});

        // Navbar scroll effect
        window.addEventListener('scroll', function() {{
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {{
                navbar.classList.add('scrolled');
            }} else {{
                navbar.classList.remove('scrolled');
            }}
        }});
    </script>
</body>
</html>
"""
    
    return html

def generate_achievements_html(achievements):
    """Generate HTML for achievements section"""
    if not achievements:
        return ""
    
    html = """
    <div class="mt-4">
        <h4 class="text-center mb-3">Key Achievements</h4>
    """
    
    for achievement in achievements:
        html += f"""
        <div class="achievement-item">
            <i class="fas fa-trophy text-warning me-2"></i>
            {achievement}
        </div>
        """
    
    html += "</div>"
    return html

def generate_skills_html(skills, skill_categories):
    """Generate HTML for skills section"""
    if skill_categories:
        html = ""
        for category, category_skills in skill_categories.items():
            html += f"""
            <div class="col-md-4 mb-4">
                <h5 class="text-center mb-3">{category}</h5>
                <div class="text-center">
            """
            for skill in category_skills:
                html += f'<span class="skill-badge">{skill}</span>'
            html += """
                </div>
            </div>
            """
        return html
    else:
        html = '<div class="col-12 text-center">'
        for skill in skills:
            html += f'<span class="skill-badge">{skill}</span>'
        html += '</div>'
        return html

def generate_experience_html(experience):
    """Generate HTML for experience section"""
    if not experience:
        return '<p class="text-center text-muted">Experience information will be extracted from your resume.</p>'
    
    html = ""
    for exp in experience:
        html += f"""
        <div class="experience-card">
            <h4>{exp.get('title', 'Position Title')}</h4>
            <h6 class="text-muted">{exp.get('company', 'Company Name')} | {exp.get('duration', 'Duration')}</h6>
            <p>{exp.get('description', 'Job description and responsibilities.')}</p>
        </div>
        """
    return html

def generate_projects_html(projects):
    """Generate HTML for projects section"""
    if not projects:
        return '''
        <div class="col-12">
            <div class="project-card text-center">
                <h4>Sample Project</h4>
                <p>Your projects will be automatically extracted from your resume and displayed here with descriptions and technologies used.</p>
            </div>
        </div>
        '''
    
    html = ""
    for project in projects:
        html += f"""
        <div class="col-md-6 mb-4">
            <div class="project-card">
                <h4>{project.get('name', 'Project Name')}</h4>
                <p>{project.get('description', 'Project description.')}</p>
                <div class="mt-3">
                    <small class="text-muted">Technologies: {project.get('technologies', 'Various technologies')}</small>
                </div>
            </div>
        </div>
        """
    return html