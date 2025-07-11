import PyPDF2
import pdfplumber
import re
from typing import Dict, List, Any, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self):
        self.common_skills = {
            'python', 'javascript', 'java', 'c++', 'c#', 'react', 'angular', 'vue',
            'html', 'css', 'sql', 'mongodb', 'postgresql', 'mysql', 'aws', 'azure',
            'docker', 'kubernetes', 'git', 'django', 'flask', 'nodejs', 'express',
            'machine learning', 'data science', 'tensorflow', 'pytorch', 'pandas',
            'numpy', 'scikit-learn', 'typescript', 'php', 'ruby', 'go', 'rust',
            'spring', 'hibernate', 'redux', 'graphql', 'rest api', 'microservices',
            'agile', 'scrum', 'jenkins', 'ci/cd', 'linux', 'unix', 'bash'
        }
        
        self.section_keywords = {
            'experience': ['experience', 'work experience', 'employment', 'professional experience', 'work history'],
            'education': ['education', 'academic background', 'qualifications', 'degrees', 'academic'],
            'skills': ['skills', 'technical skills', 'technologies', 'competencies', 'expertise'],
            'projects': ['projects', 'portfolio', 'personal projects', 'key projects'],
            'summary': ['summary', 'objective', 'profile', 'about me', 'professional summary'],
            'certifications': ['certifications', 'certificates', 'credentials'],
            'achievements': ['achievements', 'accomplishments', 'awards', 'honors']
        }

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF with improved error handling"""
        try:
            # Try pdfplumber first (better for formatted documents)
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                        else:
                            logger.warning(f"No text extracted from page {page_num + 1}")
                    except Exception as e:
                        logger.error(f"Error extracting text from page {page_num + 1}: {str(e)}")
                        continue
                
                if text.strip():
                    return self.clean_text(text)
                    
        except Exception as e:
            logger.error(f"pdfplumber failed: {str(e)}")
        
        # Fallback to PyPDF2
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception as e:
                        logger.error(f"Error extracting text from page {page_num + 1} with PyPDF2: {str(e)}")
                        continue
                
                if text.strip():
                    return self.clean_text(text)
                    
        except Exception as e:
            logger.error(f"PyPDF2 also failed: {str(e)}")
            
        raise Exception("Could not extract text from PDF using any method")

    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common OCR/extraction errors
        text = text.replace('•', '•')  # Fix bullet points
        text = text.replace('–', '-')  # Fix dashes
        text = text.replace('"', '"').replace('"', '"')  # Fix quotes
        
        # Remove page numbers and headers/footers
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip likely page numbers
            if re.match(r'^\d+$', line):
                continue
            # Skip very short lines that are likely artifacts
            if len(line) > 2:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

    def parse_resume_data(self, text: str) -> Dict[str, Any]:
        """Parse resume text and extract structured data with improved logic"""
        resume_data = {
            'name': self.extract_name(text),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'summary': self.extract_summary(text),
            'experience': self.extract_experience(text),
            'education': self.extract_education(text),
            'skills': self.extract_skills(text),
            'projects': self.extract_projects(text),
            'certifications': self.extract_certifications(text)
        }
        
        # Post-process to ensure data quality
        resume_data = self.post_process_data(resume_data)
        return resume_data

    def extract_name(self, text: str) -> str:
        """Extract name with improved logic"""
        lines = text.split('\n')
        
        # Look for name patterns in first 10 lines
        for line in lines[:10]:
            line = line.strip()
            if not line:
                continue
                
            # Skip lines with contact info
            if any(keyword in line.lower() for keyword in ['email', 'phone', 'address', '@', 'linkedin', 'github']):
                continue
                
            # Skip lines with common resume headers
            if any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum vitae']):
                continue
                
            words = line.split()
            
            # Check if line looks like a name (2-4 words, mostly alphabetic)
            if 2 <= len(words) <= 4:
                # Check if words are mostly alphabetic (allow some punctuation)
                if all(re.match(r'^[A-Za-z\.\s\-\']+$', word) for word in words):
                    # Check if it's likely a name (proper case or all caps)
                    if any(word[0].isupper() for word in words if word):
                        return line
        
        return "Your Name"

    def extract_email(self, text: str) -> str:
        """Extract email with improved regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        emails = re.findall(email_pattern, text, re.IGNORECASE)
        
        # Filter out common false positives
        valid_emails = [email for email in emails if not any(word in email.lower() for word in ['example', 'test', 'sample'])]
        
        return valid_emails[0] if valid_emails else ""

    def extract_phone(self, text: str) -> str:
        """Extract phone number with comprehensive patterns"""
        phone_patterns = [
            r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
            r'(\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',       # International
            r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',                          # (123) 456-7890
            r'\d{3}-\d{3}-\d{4}',                                       # 123-456-7890
            r'\d{10}',                                                  # 1234567890
            r'\+\d{1,3}\s?\d{1,4}\s?\d{1,4}\s?\d{1,9}'                # International formats
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                phone = matches[0]
                if isinstance(phone, tuple):
                    phone = ''.join(phone)
                # Clean up the phone number
                phone = re.sub(r'\s+', ' ', phone.strip())
                return phone
        
        return ""

    def find_section_boundaries(self, text: str) -> Dict[str, Tuple[int, int]]:
        """Find section boundaries with improved logic"""
        lines = text.split('\n')
        sections = {}
        current_section = None
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Check for section headers
            for section_name, keywords in self.section_keywords.items():
                for keyword in keywords:
                    if keyword in line_lower and len(line_lower) < 50:  # Likely a header
                        # Mark end of previous section
                        if current_section and current_section not in sections:
                            sections[current_section] = (sections.get(current_section, (0, 0))[0], i)
                        
                        # Start new section
                        current_section = section_name
                        sections[section_name] = (i, len(lines))
                        break
                if current_section == section_name:
                    break
        
        return sections

    def extract_section_content(self, text: str, section_name: str) -> str:
        """Extract content from a specific section"""
        sections = self.find_section_boundaries(text)
        
        if section_name not in sections:
            return ""
        
        start_line, end_line = sections[section_name]
        lines = text.split('\n')
        
        # Get content, skipping the header line
        content_lines = lines[start_line + 1:end_line]
        
        # Remove empty lines and clean up
        content_lines = [line.strip() for line in content_lines if line.strip()]
        
        return '\n'.join(content_lines)

    def extract_summary(self, text: str) -> str:
        """Extract professional summary with improved logic"""
        section_content = self.extract_section_content(text, 'summary')
        
        if section_content:
            # Take first paragraph or first few sentences
            sentences = re.split(r'[.!?]+', section_content)
            summary_sentences = []
            
            for sentence in sentences[:3]:  # Limit to first 3 sentences
                sentence = sentence.strip()
                if len(sentence) > 10:  # Ignore very short fragments
                    summary_sentences.append(sentence)
            
            if summary_sentences:
                return '. '.join(summary_sentences) + '.'
        
        return ""

    def extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience with improved parsing"""
        section_content = self.extract_section_content(text, 'experience')
        
        if not section_content:
            return []
        
        experiences = []
        lines = section_content.split('\n')
        current_exp = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for job title/company pattern
            if self.is_job_title_line(line):
                if current_exp:
                    experiences.append(current_exp)
                
                # Parse job title and company
                title, company = self.parse_job_title_company(line)
                current_exp = {
                    'title': title,
                    'company': company,
                    'duration': '',
                    'description': ''
                }
            
            # Check for date pattern
            elif self.is_date_line(line):
                if current_exp:
                    current_exp['duration'] = line
            
            # Otherwise, it's likely description
            else:
                if current_exp:
                    if current_exp['description']:
                        current_exp['description'] += ' ' + line
                    else:
                        current_exp['description'] = line
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences[:5]  # Limit to 5 experiences

    def is_job_title_line(self, line: str) -> bool:
        """Check if line contains job title/company info"""
        # Look for patterns that suggest job title
        patterns = [
            r'[A-Z][a-z]+ [A-Z][a-z]+',  # Title Case
            r'at [A-Z]',                  # "at Company"
            r'[A-Z][a-z]+, [A-Z]',      # "Title, Company"
            r'[A-Z][a-z]+ - [A-Z]',     # "Title - Company"
        ]
        
        return any(re.search(pattern, line) for pattern in patterns)

    def is_date_line(self, line: str) -> bool:
        """Check if line contains date information"""
        date_patterns = [
            r'\d{4}[-/]\d{4}',           # 2020-2023
            r'\d{1,2}/\d{4}',            # 01/2020
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)',  # Month names
            r'Present|Current|Now',       # Current position indicators
        ]
        
        return any(re.search(pattern, line, re.IGNORECASE) for pattern in date_patterns)

    def parse_job_title_company(self, line: str) -> Tuple[str, str]:
        """Parse job title and company from a line"""
        # Common separators
        separators = [' at ', ' - ', ', ', ' | ', ' @ ']
        
        for sep in separators:
            if sep in line:
                parts = line.split(sep, 1)
                if len(parts) == 2:
                    return parts[0].strip(), parts[1].strip()
        
        # If no separator found, return the whole line as title
        return line.strip(), ""

    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education with improved parsing"""
        section_content = self.extract_section_content(text, 'education')
        
        if not section_content:
            return []
        
        educations = []
        lines = section_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for degree keywords
            degree_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'associate', 'diploma', 'certificate']
            
            if any(keyword in line.lower() for keyword in degree_keywords):
                # Try to parse degree and institution
                degree, institution, year = self.parse_education_line(line)
                
                educations.append({
                    'degree': degree,
                    'institution': institution,
                    'year': year
                })
        
        return educations

    def parse_education_line(self, line: str) -> Tuple[str, str, str]:
        """Parse education line to extract degree, institution, and year"""
        # Extract year
        year_match = re.search(r'\b(19|20)\d{2}\b', line)
        year = year_match.group(0) if year_match else ""
        
        # Remove year from line for further processing
        line_without_year = re.sub(r'\b(19|20)\d{2}\b', '', line).strip()
        
        # Look for institution indicators
        institution_indicators = ['university', 'college', 'institute', 'school']
        
        for indicator in institution_indicators:
            if indicator in line_without_year.lower():
                parts = line_without_year.lower().split(indicator)
                if len(parts) >= 2:
                    degree = parts[0].strip()
                    institution = (parts[1].strip() + ' ' + indicator).strip()
                    return degree, institution, year
        
        # If no institution found, return the whole line as degree
        return line_without_year, "", year

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills with improved detection"""
        section_content = self.extract_section_content(text, 'skills')
        
        # Also search in the entire text for skills
        search_text = (section_content + '\n' + text).lower()
        
        found_skills = set()
        
        # Check for predefined skills
        for skill in self.common_skills:
            if skill.lower() in search_text:
                found_skills.add(skill.title())
        
        # Extract comma-separated skills from skills section
        if section_content:
            lines = section_content.split('\n')
            for line in lines:
                if ',' in line:
                    skills_in_line = [skill.strip() for skill in line.split(',')]
                    for skill in skills_in_line:
                        if len(skill) > 1 and len(skill) < 30:  # Reasonable skill length
                            found_skills.add(skill.title())
        
        return list(found_skills)[:15]  # Limit to 15 skills

    def extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Extract projects with improved parsing"""
        section_content = self.extract_section_content(text, 'projects')
        
        if not section_content:
            return []
        
        projects = []
        lines = section_content.split('\n')
        current_project = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line looks like a project title
            if self.is_project_title_line(line):
                if current_project:
                    projects.append(current_project)
                
                current_project = {
                    'name': line,
                    'description': '',
                    'technologies': ''
                }
            else:
                if current_project:
                    if current_project['description']:
                        current_project['description'] += ' ' + line
                    else:
                        current_project['description'] = line
        
        if current_project:
            projects.append(current_project)
        
        return projects[:5]  # Limit to 5 projects

    def is_project_title_line(self, line: str) -> bool:
        """Check if line is likely a project title"""
        # Project titles are usually short and may contain tech keywords
        if len(line) > 100:  # Too long to be a title
            return False
        
        # Look for title-like patterns
        if any(char.isupper() for char in line[:10]):  # Starts with uppercase
            return True
        
        # Look for tech project indicators
        tech_indicators = ['app', 'system', 'platform', 'website', 'tool', 'api', 'dashboard']
        if any(indicator in line.lower() for indicator in tech_indicators):
            return True
        
        return False

    def extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        section_content = self.extract_section_content(text, 'certifications')
        
        if not section_content:
            return []
        
        certifications = []
        lines = section_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 5:  # Reasonable cert name length
                certifications.append(line)
        
        return certifications[:10]  # Limit to 10 certifications

    def post_process_data(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Post-process extracted data to ensure quality"""
        # Clean up descriptions
        for exp in resume_data.get('experience', []):
            if exp.get('description'):
                exp['description'] = self.clean_description(exp['description'])
        
        for proj in resume_data.get('projects', []):
            if proj.get('description'):
                proj['description'] = self.clean_description(proj['description'])
        
        # Remove empty entries
        resume_data['experience'] = [exp for exp in resume_data.get('experience', []) if exp.get('title')]
        resume_data['education'] = [edu for edu in resume_data.get('education', []) if edu.get('degree')]
        resume_data['projects'] = [proj for proj in resume_data.get('projects', []) if proj.get('name')]
        
        return resume_data

    def clean_description(self, description: str) -> str:
        """Clean up description text"""
        # Remove excessive whitespace
        description = re.sub(r'\s+', ' ', description.strip())
        
        # Ensure it ends with a period
        if description and not description.endswith('.'):
            description += '.'
        
        return description

# Backward compatibility functions for existing code
def extract_text_from_pdf(file_path: str) -> str:
    """Backward compatibility function"""
    parser = ResumeParser()
    return parser.extract_text_from_pdf(file_path)

def parse_resume_data(text: str) -> Dict[str, Any]:
    """Backward compatibility function"""
    parser = ResumeParser()
    return parser.parse_resume_data(text)

# Individual extraction functions for backward compatibility
def extract_name(text: str) -> str:
    parser = ResumeParser()
    return parser.extract_name(text)

def extract_email(text: str) -> str:
    parser = ResumeParser()
    return parser.extract_email(text)

def extract_phone(text: str) -> str:
    parser = ResumeParser()
    return parser.extract_phone(text)

def extract_summary(text: str) -> str:
    parser = ResumeParser()
    return parser.extract_summary(text)

def extract_experience(text: str) -> List[Dict[str, str]]:
    parser = ResumeParser()
    return parser.extract_experience(text)

def extract_education(text: str) -> List[Dict[str, str]]:
    parser = ResumeParser()
    return parser.extract_education(text)

def extract_skills(text: str) -> List[str]:
    parser = ResumeParser()
    return parser.extract_skills(text)

def extract_projects(text: str) -> List[Dict[str, str]]:
    parser = ResumeParser()
    return parser.extract_projects(text)

# Usage example
def main():
    parser = ResumeParser()
    
    try:
        # Extract text from PDF
        text = parser.extract_text_from_pdf('resume.pdf')
        print("Text extracted successfully!")
        
        # Parse resume data
        resume_data = parser.parse_resume_data(text)
        
        # Print parsed data
        print("\n=== PARSED RESUME DATA ===")
        for key, value in resume_data.items():
            print(f"\n{key.upper()}:")
            if isinstance(value, list):
                for item in value:
                    print(f"  {item}")
            else:
                print(f"  {value}")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()