import re
import os
from typing import Dict, Any, List
import json

def parse_resume_data(resume_text: str) -> Dict[str, Any]:
    """Enhanced resume parsing with better section detection"""
    
    # Clean and normalize the text
    text = re.sub(r'\s+', ' ', resume_text.strip())
    text = re.sub(r'\n+', '\n', text)
    
    # Initialize data structure
    data = {
        'name': '',
        'email': '',
        'phone': '',
        'summary': '',
        'skills': [],
        'experience': [],
        'education': [],
        'projects': []
    }
    
    # Extract contact information
    data['name'] = extract_name(text)
    data['email'] = extract_email(text)
    data['phone'] = extract_phone(text)
    
    # Split text into sections
    sections = split_into_sections(text)
    
    # Parse each section
    for section_name, section_content in sections.items():
        if section_name in ['summary', 'objective', 'profile']:
            data['summary'] = clean_text(section_content)
        elif section_name in ['skills', 'technical skills', 'core competencies']:
            data['skills'] = extract_skills(section_content)
        elif section_name in ['experience', 'work experience', 'professional experience']:
            data['experience'] = extract_experience(section_content)
        elif section_name in ['education', 'academic background']:
            data['education'] = extract_education(section_content)
        elif section_name in ['projects', 'key projects', 'notable projects']:
            data['projects'] = extract_projects(section_content)
    
    return data

def extract_name(text: str) -> str:
    """Extract name from resume text"""
    lines = text.split('\n')
    
    # Look for name in first few lines
    for i, line in enumerate(lines[:5]):
        line = line.strip()
        if line and not re.search(r'@|phone|tel|\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', line.lower()):
            # Skip lines that look like headers or contact info
            if not re.search(r'resume|curriculum|cv|contact|address', line.lower()):
                # Check if it looks like a name (2-4 words, mostly letters)
                words = line.split()
                if 2 <= len(words) <= 4 and all(re.match(r'^[A-Za-z]+$', word) for word in words):
                    return line
    
    return "Your Name"

def extract_email(text: str) -> str:
    """Extract email from resume text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else ""

def extract_phone(text: str) -> str:
    """Extract phone number from resume text"""
    phone_patterns = [
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',
        r'\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
    ]
    
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    
    return ""

def split_into_sections(text: str) -> Dict[str, str]:
    """Split resume text into logical sections"""
    sections = {}
    
    # Common section headers
    section_patterns = {
        'summary': r'(?i)(summary|objective|profile|about)\s*:?\s*\n',
        'skills': r'(?i)(skills|technical skills|core competencies|technologies)\s*:?\s*\n',
        'experience': r'(?i)(experience|work experience|professional experience|employment)\s*:?\s*\n',
        'education': r'(?i)(education|academic background|qualifications)\s*:?\s*\n',
        'projects': r'(?i)(projects|key projects|notable projects)\s*:?\s*\n'
    }
    
    # Find section boundaries
    section_positions = {}
    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, text)
        if match:
            section_positions[section_name] = match.end()
    
    # Extract content between sections
    sorted_sections = sorted(section_positions.items(), key=lambda x: x[1])
    
    for i, (section_name, start_pos) in enumerate(sorted_sections):
        if i + 1 < len(sorted_sections):
            end_pos = sorted_sections[i + 1][1]
            content = text[start_pos:end_pos].strip()
        else:
            content = text[start_pos:].strip()
        
        sections[section_name] = content
    
    return sections

def extract_skills(text: str) -> List[str]:
    """Extract skills from skills section"""
    skills = []
    
    # Remove common separators and split
    text = re.sub(r'[•\-\*]', ',', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Split by common delimiters
    potential_skills = re.split(r'[,;\n\|]', text)
    
    for skill in potential_skills:
        skill = skill.strip()
        if skill and len(skill) > 2 and len(skill) < 50:
            # Filter out non-skill text
            if not re.search(r'(?i)(years?|experience|proficient|skilled)', skill):
                skills.append(skill)
    
    return skills[:15]  # Limit to top 15 skills

def extract_experience(text: str) -> List[Dict[str, str]]:
    """Extract work experience from experience section"""
    experience = []
    
    # Split by job entries (look for patterns like dates or company names)
    job_blocks = re.split(r'\n(?=\S)', text)
    
    for block in job_blocks:
        if len(block.strip()) > 20:  # Minimum length for a job entry
            job_data = parse_job_block(block)
            if job_data:
                experience.append(job_data)
    
    return experience

def parse_job_block(block: str) -> Dict[str, str]:
    """Parse a single job block"""
    lines = [line.strip() for line in block.split('\n') if line.strip()]
    
    if len(lines) < 2:
        return None
    
    # Try to identify title, company, and duration
    title = lines[0]
    company = ""
    duration = ""
    description = ""
    
    # Look for date patterns
    date_pattern = r'\d{4}[-\s]?\d{4}|\d{1,2}/\d{4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}'
    
    for i, line in enumerate(lines[1:], 1):
        if re.search(date_pattern, line) and not duration:
            duration = line
        elif not company and i == 1:
            company = line
        else:
            if description:
                description += " " + line
            else:
                description = line
    
    return {
        'title': clean_text(title),
        'company': clean_text(company),
        'duration': clean_text(duration),
        'description': clean_text(description)
    }

def extract_education(text: str) -> List[Dict[str, str]]:
    """Extract education information"""
    education = []
    
    # Split by education entries
    edu_blocks = re.split(r'\n(?=\S)', text)
    
    for block in edu_blocks:
        if len(block.strip()) > 10:
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            if lines:
                education.append({
                    'degree': clean_text(lines[0]),
                    'institution': clean_text(lines[1] if len(lines) > 1 else ""),
                    'year': extract_year(block)
                })
    
    return education

def extract_projects(text: str) -> List[Dict[str, str]]:
    """Extract project information"""
    projects = []
    
    # Split by project entries
    project_blocks = re.split(r'\n(?=\S)', text)
    
    for block in project_blocks:
        if len(block.strip()) > 15:
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            if lines:
                name = lines[0]
                description = " ".join(lines[1:]) if len(lines) > 1 else ""
                
                projects.append({
                    'name': clean_text(name),
                    'description': clean_text(description),
                    'technologies': extract_technologies(block)
                })
    
    return projects

def extract_year(text: str) -> str:
    """Extract year from text"""
    year_pattern = r'\b(19|20)\d{2}\b'
    matches = re.findall(year_pattern, text)
    return matches[-1] if matches else ""

def extract_technologies(text: str) -> str:
    """Extract technologies from project description"""
    # Look for common technology patterns
    tech_patterns = [
        r'(?i)technologies?:?\s*([^\n]+)',
        r'(?i)tools?:?\s*([^\n]+)',
        r'(?i)built with:?\s*([^\n]+)'
    ]
    
    for pattern in tech_patterns:
        match = re.search(pattern, text)
        if match:
            return clean_text(match.group(1))
    
    return "Various technologies"

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove bullet points and special characters
    text = re.sub(r'^[•\-\*\s]+', '', text)
    text = re.sub(r'[•\-\*]+', ' ', text)
    
    return text.strip()

def generate_portfolio_html(resume_text: str) -> str:
    """Generate a complete portfolio HTML from resume text"""
    
    # Parse resume data
    resume_data = parse_resume_data(resume_text)
    
    # Generate HTML
    html_content = create_portfolio_html(resume_data)
    return html_content

def create_portfolio_html(data: Dict[str, Any]) -> str:
    """Create the complete portfolio HTML with proper formatting"""
    
    name = data.get('name', 'Your Name')
    email = data.get('email', '')
    phone = data.get('phone', '')
    summary = data.get('summary', 'Professional summary will be generated from your resume.')
    tagline = 'Professional Developer & Problem Solver'
    skills = data.get('skills', [])
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
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 120px 0;
            text-align: center;
            min-height: 100vh;
            display: flex;
            align-items: center;
        }}
        .section-title {{
            color: #333;
            margin-bottom: 40px;
            font-weight: 600;
            text-align: center;
        }}
        .skill-badge {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            margin: 8px 5px;
            display: inline-block;
            font-size: 0.9em;
            font-weight: 500;
            transition: transform 0.3s ease;
        }}
        .skill-badge:hover {{
            transform: translateY(-2px);
        }}
        .experience-card, .project-card, .education-card {{
            border: none;
            border-left: 4px solid #667eea;
            padding: 30px;
            margin-bottom: 30px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .experience-card:hover, .project-card:hover, .education-card:hover {{
            transform: translateY(-5px);
        }}
        .contact-info {{
            background: linear-gradient(135deg, #333 0%, #555 100%);
            color: white;
            padding: 80px 0;
        }}
        .navbar {{
            background: rgba(255,255,255,0.95) !important;
            backdrop-filter: blur(10px);
            padding: 1rem 0;
        }}
        .navbar.scrolled {{
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }}
        .btn-primary {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .btn-primary:hover {{
            background: linear-gradient(45deg, #5a6fd8, #6a42a0);
            transform: translateY(-2px);
        }}
        .btn-outline-light {{
            border: 2px solid white;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .btn-outline-light:hover {{
            transform: translateY(-2px);
        }}
        .section {{
            padding: 80px 0;
        }}
        .bg-light {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
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
                    <li class="nav-item"><a class="nav-link" href="#education">Education</a></li>
                    <li class="nav-item"><a class="nav-link" href="#projects">Projects</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero-section">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 mx-auto">
                    <h1 class="display-3 fw-bold mb-4">{name}</h1>
                    <p class="lead mb-5">{tagline}</p>
                    <div class="d-flex justify-content-center gap-3 flex-wrap">
                        <a href="#contact" class="btn btn-primary btn-lg">Get In Touch</a>
                        <a href="#projects" class="btn btn-outline-light btn-lg">View Work</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="section">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 mx-auto">
                    <h2 class="section-title">About Me</h2>
                    <p class="lead text-center mb-5">{summary}</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="section bg-light">
        <div class="container">
            <h2 class="section-title">Skills & Technologies</h2>
            <div class="row">
                {generate_skills_html(skills)}
            </div>
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="section">
        <div class="container">
            <h2 class="section-title">Professional Experience</h2>
            <div class="row">
                <div class="col-lg-10 mx-auto">
                    {generate_experience_html(experience)}
                </div>
            </div>
        </div>
    </section>

    <!-- Education Section -->
    <section id="education" class="section bg-light">
        <div class="container">
            <h2 class="section-title">Education</h2>
            <div class="row">
                <div class="col-lg-10 mx-auto">
                    {generate_education_html(education)}
                </div>
            </div>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="section">
        <div class="container">
            <h2 class="section-title">Featured Projects</h2>
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
                    <p class="lead mb-5">Ready to start your next project? Let's connect and discuss how we can work together.</p>
                    <div class="d-flex justify-content-center gap-4 flex-wrap">
                        {f'<a href="mailto:{email}" class="btn btn-outline-light btn-lg"><i class="fas fa-envelope me-2"></i>{email}</a>' if email else ''}
                        {f'<a href="tel:{phone}" class="btn btn-outline-light btn-lg"><i class="fas fa-phone me-2"></i>{phone}</a>' if phone else ''}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="py-4 bg-dark text-white text-center">
        <div class="container">
            <p class="mb-0">&copy; 2024 {name}. All rights reserved.</p>
        </div>
    </footer>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
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

        // Add fade-in animation on scroll
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver(function(entries) {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);

        // Observe all cards
        document.querySelectorAll('.experience-card, .project-card, .education-card').forEach(card => {{
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        }});
    </script>
</body>
</html>
"""
    
    return html

def generate_skills_html(skills):
    """Generate HTML for skills section with proper spacing"""
    html = '<div class="col-12 text-center">'
    for skill in skills:
        html += f'<span class="skill-badge">{skill}</span>'
    html += '</div>'
    return html

def generate_experience_html(experience):
    """Generate HTML for experience section with proper formatting"""
    if not experience:
        return '''
        <div class="experience-card text-center">
            <h4>Experience Section</h4>
            <p class="text-muted">Your work experience will be automatically extracted from your resume and displayed here with proper formatting.</p>
        </div>
        '''
    
    html = ""
    for exp in experience:
        title = exp.get('title', 'Position Title')
        company = exp.get('company', 'Company Name')
        duration = exp.get('duration', 'Duration')
        description = exp.get('description', 'Job description and responsibilities will be displayed here.')
        
        html += f"""
        <div class="experience-card">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                    <h4 class="mb-1">{title}</h4>
                    <h6 class="text-muted mb-0">{company}</h6>
                </div>
                <span class="badge bg-primary">{duration}</span>
            </div>
            <p class="mb-0">{description}</p>
        </div>
        """
    return html

def generate_education_html(education):
    """Generate HTML for education section"""
    if not education:
        return '''
        <div class="education-card text-center">
            <h4>Education Section</h4>
            <p class="text-muted">Your educational background will be automatically extracted from your resume and displayed here.</p>
        </div>
        '''
    
    html = ""
    for edu in education:
        degree = edu.get('degree', 'Degree')
        institution = edu.get('institution', 'Institution')
        year = edu.get('year', 'Year')
        
        html += f"""
        <div class="education-card">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h4 class="mb-1">{degree}</h4>
                    <h6 class="text-muted mb-0">{institution}</h6>
                </div>
                <span class="badge bg-secondary">{year}</span>
            </div>
        </div>
        """
    return html

def generate_projects_html(projects):
    """Generate HTML for projects section with proper spacing"""
    if not projects:
        return '''
        <div class="col-12">
            <div class="project-card text-center">
                <h4>Sample Project</h4>
                <p class="mb-3">Your projects will be automatically extracted from your resume and displayed here with descriptions and technologies used.</p>
                <div class="mt-3">
                    <small class="text-muted">Technologies: React, Node.js, MongoDB</small>
                </div>
            </div>
        </div>
        '''
    
    html = ""
    for project in projects:
        name = project.get('name', 'Project Name')
        description = project.get('description', 'Project description will be displayed here.')
        technologies = project.get('technologies', 'Various technologies')
        
        html += f"""
        <div class="col-lg-6 mb-4">
            <div class="project-card h-100">
                <h4 class="mb-3">{name}</h4>
                <p class="mb-4">{description}</p>
                <div class="mt-auto">
                    <small class="text-muted">
                        <i class="fas fa-tools me-2"></i>
                        <strong>Technologies:</strong> {technologies}
                    </small>
                </div>
            </div>
        </div>
        """
    return html

# Example usage
if __name__ == "__main__":
    # Test with sample resume text
    sample_resume = """
    John Doe
    john.doe@example.com
    (555) 123-4567
    
    SUMMARY
    Experienced software developer with 5+ years in full-stack development and cloud technologies.
    
    SKILLS
    Python, JavaScript, React, Node.js, AWS, Docker, SQL, MongoDB
    
    EXPERIENCE
    Senior Developer
    TechCorp Inc. | 2020 - Present
    Led development of cloud-based applications using React and Node.js. Managed a team of 3 developers.
    
    Software Developer
    StartupXYZ | 2018 - 2020
    Developed web applications using Python and Django. Improved application performance by 40%.
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology | 2018
    
    PROJECTS
    E-commerce Platform
    Built a full-stack e-commerce solution with React, Node.js, and MongoDB. Integrated payment processing and inventory management.
    
    Task Management App
    Developed a collaborative task management application using React and Firebase. Implemented real-time updates and user authentication.
    """
    
    # Generate portfolio
    portfolio_html = generate_portfolio_html(sample_resume)
    
    # Save to file
    with open('portfolio.html', 'w', encoding='utf-8') as f:
        f.write(portfolio_html)
    
    print("Portfolio generated successfully! Check 'portfolio.html' file.")