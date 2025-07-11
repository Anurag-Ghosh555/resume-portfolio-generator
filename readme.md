# Resume → Portfolio Website Generator

Transform your PDF resume into a stunning portfolio website in seconds! This Flask-based application extracts information from your resume and generates a beautiful, responsive portfolio website ready for deployment.

## 🌟 Features

- **PDF Resume Upload**: Upload your resume in PDF format
- **Modern Design**: Bootstrap-powered responsive design
- **GitHub Pages Ready**: Download and deploy to GitHub Pages instantly
- **Mobile Responsive**: Looks great on all devices
- **SEO Optimized**: Built with search engines in mind

## 🚀 Quick Start

### Prerequisites

- Python 3.7+

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


4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
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


1. **Upload Resume**: Visit the homepage and upload your PDF resume
2. **Generate Portfolio**: Click "Generate Portfolio" and wait for processing
3. **Preview**: View your generated portfolio in the browser
4. **Download**: Download the HTML file for deployment


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


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


## 🐛 Troubleshooting

### Common Issues

**PDF not parsing correctly**
- Ensure your PDF has selectable text
- Try a different PDF format
- Check if the PDF is password-protected


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

- **GitHub**:https://github.com/Anurag-Ghosh555
- **Email**: ghoshanurag238@gmail.com

---

Made by Anurag Ghosh