import PyPDF2
import pdfplumber
import re
from typing import Dict, List, Any

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using pdfplumber (more reliable than PyPDF2)"""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        # Fallback to PyPDF2
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e2:
            raise Exception(f"Could not extract text from PDF: {str(e2)}")

def parse_resume_data(text: str) -> Dict[str, Any]:
    """Parse resume text and extract structured data"""
    resume_data = {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'summary': extract_summary(text),
        'experience': extract_experience(text),
        'education': extract_education(text),
        'skills': extract_skills(text),
        'projects': extract_projects(text)
    }
    return resume_data

def extract_name(text: str) -> str:
    """Extract name from resume text"""
    lines = text.split('\n')
    # Usually name is in the first few lines
    for line in lines[:5]:
        line = line.strip()
        if line and not any(keyword in line.lower() for keyword in ['email', 'phone', 'address', '@']):
            # Check if line looks like a name (2-4 words, proper case)
            words = line.split()
            if 2 <= len(words) <= 4 and all(word.replace('.', '').isalpha() for word in words):
                return line
    return "Your Name"

def extract_email(text: str) -> str:
    """Extract email from resume text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else ""

def extract_phone(text: str) -> str:
    """Extract phone number from resume text"""
    phone_patterns = [
        r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'(\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}'
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            return phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
    return ""

def extract_summary(text: str) -> str:
    """Extract professional summary/objective"""
    summary_keywords = ['summary', 'objective', 'profile', 'about']
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in summary_keywords):
            # Get next few lines as summary
            summary_lines = []
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip() and not any(section in lines[j].lower() for section in ['experience', 'education', 'skills']):
                    summary_lines.append(lines[j].strip())
                else:
                    break
            if summary_lines:
                return ' '.join(summary_lines)
    return ""

def extract_experience(text: str) -> List[Dict[str, str]]:
    """Extract work experience"""
    experience_section = extract_section(text, ['experience', 'work', 'employment'])
    if not experience_section:
        return []
    
    experiences = []
    lines = experience_section.split('\n')
    current_exp = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line looks like a job title/company
        if any(char.isupper() for char in line) and len(line.split()) >= 2:
            if current_exp:
                experiences.append(current_exp)
            current_exp = {
                'title': line,
                'company': '',
                'duration': '',
                'description': ''
            }
        elif current_exp:
            current_exp['description'] += line + ' '
    
    if current_exp:
        experiences.append(current_exp)
    
    return experiences[:3]  # Limit to 3 experiences

def extract_education(text: str) -> List[Dict[str, str]]:
    """Extract education information"""
    education_section = extract_section(text, ['education', 'qualification', 'degree'])
    if not education_section:
        return []
    
    educations = []
    lines = education_section.split('\n')
    
    for line in lines:
        line = line.strip()
        if line and any(keyword in line.lower() for keyword in ['bachelor', 'master', 'degree', 'university', 'college']):
            educations.append({
                'degree': line,
                'institution': '',
                'year': ''
            })
    
    return educations

def extract_skills(text: str) -> List[str]:
    """Extract skills"""
    skills_section = extract_section(text, ['skills', 'technologies', 'technical'])
    if not skills_section:
        return []
    
    # Common skill keywords
    skill_keywords = [
        'python', 'javascript', 'java', 'c++', 'react', 'angular', 'vue',
        'html', 'css', 'sql', 'mongodb', 'postgresql', 'aws', 'azure',
        'docker', 'kubernetes', 'git', 'django', 'flask', 'nodejs',
        'machine learning', 'data science', 'tensorflow', 'pytorch'
    ]
    
    skills = []
    text_lower = skills_section.lower()
    
    for keyword in skill_keywords:
        if keyword in text_lower:
            skills.append(keyword.title())
    
    # Also extract comma-separated skills
    lines = skills_section.split('\n')
    for line in lines:
        if ',' in line:
            line_skills = [skill.strip() for skill in line.split(',')]
            skills.extend(line_skills)
    
    return list(set(skills))[:10]  # Limit to 10 skills

def extract_projects(text: str) -> List[Dict[str, str]]:
    """Extract projects"""
    projects_section = extract_section(text, ['projects', 'portfolio'])
    if not projects_section:
        return []
    
    projects = []
    lines = projects_section.split('\n')
    current_project = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if any(char.isupper() for char in line) and len(line.split()) >= 2:
            if current_project:
                projects.append(current_project)
            current_project = {
                'name': line,
                'description': '',
                'technologies': ''
            }
        elif current_project:
            current_project['description'] += line + ' '
    
    if current_project:
        projects.append(current_project)
    
    return projects[:3]  # Limit to 3 projects

def extract_section(text: str, section_keywords: List[str]) -> str:
    """Extract a specific section from resume text"""
    lines = text.split('\n')
    section_start = -1
    
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in section_keywords):
            section_start = i
            break
    
    if section_start == -1:
        return ""
    
    # Find section end (next major section or end of text)
    section_end = len(lines)
    major_sections = ['experience', 'education', 'skills', 'projects', 'summary', 'objective']
    
    for i in range(section_start + 1, len(lines)):
        line_lower = lines[i].lower()
        if any(section in line_lower for section in major_sections):
            section_end = i
            break
    
    return '\n'.join(lines[section_start:section_end])