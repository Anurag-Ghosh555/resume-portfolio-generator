# Resume → Portfolio Website Generator

Transform your PDF resume into a stunning portfolio website in seconds! This Flask-based application uses AI to extract information from your resume and generates a beautiful, responsive portfolio website ready for deployment.

## 🌟 Features

- **PDF Resume Upload**: Upload your resume in PDF format
- **AI-Powered Extraction**: Automatically extract contact info, skills, experience, and projects
- **GPT Enhancement**: Improve content quality with OpenAI's GPT
- **Modern Design**: Bootstrap-powered responsive design
- **GitHub Pages Ready**: Download and deploy to GitHub Pages instantly
- **Mobile Responsive**: Looks great on all devices
- **SEO Optimized**: Built with search engines in mind

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- OpenAI API key (optional, for enhanced content generation)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-portfolio-generator.git
   cd resume-portfolio-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional)**
   ```bash
   # Create a .env file in the project root
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
resume-portfolio-generator/
│
├── app.py                      # Main Flask application
├── templates/
│   ├── index.html             # Upload page
│   ├── result.html            # Success page
│   └── portfolio_template.html # Portfolio template
├── static/
│   └── css/
│       └── style.css          # Custom styles
├── uploads/                   # Temporary file storage
├── generated_portfolios/      # Generated portfolio files
├── utils/
│   ├── pdf_parser.py         # PDF text extraction
│   └── html_generator.py     # HTML generation
├── requirements.txt           # Project dependencies
├── README.md                 # This file
└── .gitignore               # Git ignore rules
```

## 🔧 Usage

### Basic Usage

1. **Upload Resume**: Visit the homepage and upload your PDF resume
2. **Generate Portfolio**: Click "Generate Portfolio" and wait for processing
3. **Preview**: View your generated portfolio in the browser
4. **Download**: Download the HTML file for deployment

### Advanced Usage

#### With OpenAI API Key

Set your OpenAI API key in a `.env` file to enable:
- Enhanced content generation
- Professional summary improvement
- Better skill categorization
- Achievement highlighting

#### Customization

The generated portfolio includes:
- Professional header with contact information
- About section with enhanced summary
- Skills section with categorized technologies
- Experience section with job descriptions
- Projects section with descriptions
- Contact information
- Modern, responsive design

## 🚀 Deployment

### GitHub Pages

1. **Create a new repository** named `your-username.github.io`
2. **Upload the generated HTML file** and rename it to `index.html`
3. **Enable GitHub Pages** in repository settings
4. **Your site will be live** at `https://your-username.github.io`

### Other Hosting Options

- **Netlify**: Drag and drop the HTML file
- **Vercel**: Connect your GitHub repository
- **Firebase Hosting**: Deploy using Firebase CLI

## 🛠️ Technical Details

### PDF Processing

- Uses `pdfplumber` for accurate text extraction
- Fallback to `PyPDF2` for compatibility
- Intelligent parsing of resume sections

### AI Enhancement

- OpenAI GPT-3.5 for content improvement
- Professional summary generation
- Skill categorization
- Achievement extraction

### Frontend

- Bootstrap 5 for responsive design
- Font Awesome icons
- Smooth scrolling navigation
- Modern CSS animations

## 🎨 Customization

### Styling

Edit the CSS in the generated HTML file to:
- Change color schemes
- Modify fonts and typography
- Adjust layout and spacing
- Add custom animations

### Content

Modify the generated HTML to:
- Add project links and images
- Include social media profiles
- Add custom sections
- Update contact information

## 🔒 Security

- File upload validation
- Secure filename handling
- Temporary file cleanup
- Input sanitization

## 📊 Performance

- Optimized HTML generation
- Minimal external dependencies
- Fast loading times
- SEO-friendly structure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

**PDF not parsing correctly**
- Ensure your PDF has selectable text
- Try a different PDF format
- Check if the PDF is password-protected

**OpenAI API errors**
- Verify your API key is correct
- Check your API quota and billing
- The app works without the API key (with basic features)

**Upload failures**
- Check file size (max 16MB)
- Ensure file is a valid PDF
- Try uploading again

### Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs in the console
3. Create an issue on GitHub
4. Join our community discussions

## 🚧 Roadmap

- [ ] Multiple resume formats (DOCX, TXT)
- [ ] More design templates
- [ ] Custom domain integration
- [ ] Portfolio analytics
- [ ] Team collaboration features
- [ ] API for programmatic access

## 📞 Contact

- **GitHub**: [Your GitHub Profile](https://github.com/Anurag-Ghosh555)
- **Email**: your.ghoshanurag238@gmail.com.com

---

Made by Anurag Ghosh