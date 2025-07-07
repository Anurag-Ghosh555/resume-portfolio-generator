from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
import uuid
from utils.pdf_parser import extract_text_from_pdf
from utils.html_generator import generate_portfolio_html

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PORTFOLIO_FOLDER'] = 'generated_portfolios'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload and portfolio directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PORTFOLIO_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['resume']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        filename = secure_filename(file.filename)
        filename = f"{unique_id}_{filename}"
        
        # Save uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Extract text from PDF
            resume_text = extract_text_from_pdf(file_path)
            
            # Generate portfolio HTML
            portfolio_html = generate_portfolio_html(resume_text)
            
            # Save portfolio
            portfolio_filename = f"portfolio_{unique_id}.html"
            portfolio_path = os.path.join(app.config['PORTFOLIO_FOLDER'], portfolio_filename)
            
            with open(portfolio_path, 'w', encoding='utf-8') as f:
                f.write(portfolio_html)
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return render_template('result.html', 
                                 portfolio_filename=portfolio_filename,
                                 unique_id=unique_id)
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('index'))
    
    flash('Please upload a valid PDF file')
    return redirect(url_for('index'))

@app.route('/portfolio/<filename>')
def view_portfolio(filename):
    return send_from_directory(app.config['PORTFOLIO_FOLDER'], filename)

@app.route('/download/<filename>')
def download_portfolio(filename):
    return send_from_directory(app.config['PORTFOLIO_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)