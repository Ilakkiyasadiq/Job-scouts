import torch
from transformers import AutoTokenizer, AutoModel
import docx
import PyPDF2
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def extract_text_from_file(file_path):
    """Extract text from PDF or DOCX files"""
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
    else:
        raise ValueError('Unsupported file format')
    return text

def get_bert_embedding(text):
    """Get BERT embeddings for input text"""
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

def extract_skills(text):
    """Extract skills from text using a predefined skill list"""
    # This is a basic implementation - you might want to use a more comprehensive skill database
    common_skills = ['python', 'java', 'javascript', 'react', 'django', 'sql', 'machine learning',
                    'data analysis', 'project management', 'agile', 'scrum', 'git']
    skills = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill in text_lower:
            skills.append(skill)
    return skills

def analyze_resume(resume_text, job_description):
    """Analyze resume against job description"""
    # Get embeddings
    resume_embedding = get_bert_embedding(resume_text)
    job_embedding = get_bert_embedding(job_description)
    
    # Calculate similarity score
    similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
    match_score = float(similarity * 100)
    
    # Extract skills
    resume_skills = set(extract_skills(resume_text))
    required_skills = set(extract_skills(job_description))
    
    matching_skills = list(resume_skills.intersection(required_skills))
    missing_skills = list(required_skills - resume_skills)
    
    # Basic experience analysis (can be improved with more sophisticated NLP)
    experience_match = analyze_experience(resume_text, job_description)
    education_match = analyze_education(resume_text, job_description)
    
    # Generate recommendations
    recommendations = generate_recommendations(matching_skills, missing_skills, experience_match)
    
    return {
        'match_score': match_score,
        'matching_skills': matching_skills,
        'missing_skills': missing_skills,
        'experience_match': experience_match,
        'education_match': education_match,
        'recommendations': recommendations
    }

def analyze_experience(resume_text, job_description):
    """Analyze experience requirements"""
    # Simple pattern matching for years of experience
    resume_years = extract_years_of_experience(resume_text)
    required_years = extract_years_of_experience(job_description)
    
    if required_years == 0:
        return 100.0
    if resume_years >= required_years:
        return 100.0
    return (resume_years / required_years) * 100 if required_years > 0 else 50.0

def analyze_education(resume_text, job_description):
    """Analyze education requirements"""
    education_levels = {
        'phd': 4,
        'master': 3,
        'bachelor': 2,
        'associate': 1
    }
    
    resume_edu = max([education_levels.get(level, 0) 
                     for level in education_levels.keys() 
                     if level in resume_text.lower()])
    required_edu = max([education_levels.get(level, 0) 
                       for level in education_levels.keys() 
                       if level in job_description.lower()])
    
    if resume_edu >= required_edu:
        return 100.0
    return (resume_edu / required_edu) * 100 if required_edu > 0 else 50.0

def extract_years_of_experience(text):
    """Extract years of experience from text"""
    patterns = [
        r'(\d+)\+?\s*years?(?:\s+of)?\s+experience',
        r'experience\s*(?:of|for)?\s*(\d+)\+?\s*years?'
    ]
    
    years = []
    for pattern in patterns:
        matches = re.finditer(pattern, text.lower())
        for match in matches:
            years.append(int(match.group(1)))
    
    return max(years) if years else 0

def generate_recommendations(matching_skills, missing_skills, experience_match):
    """Generate recommendations based on analysis"""
    recommendations = []
    
    if missing_skills:
        recommendations.append(f"Consider acquiring these skills: {', '.join(missing_skills)}")
    
    if experience_match < 70:
        recommendations.append("Gain more relevant experience in the field")
    
    if not matching_skills:
        recommendations.append("Highlight relevant skills that match the job requirements")
    
    if not recommendations:
        recommendations.append("Your profile appears to be a good match for this position")
    
    return recommendations