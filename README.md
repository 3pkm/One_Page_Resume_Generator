# OnePageResume

A Django web application that allows users to create, customize, and manage professional one-page resumes with ease.

![OnePageResume Screenshot](resume/assets/Screenshot 2025-02-26 151833.png)

## 🌟 Features

- **Easy Resume Creation**: Build professional one-page resumes without design experience
- **Multiple Templates**: Choose from various professional templates
- **Real-time Preview**: See changes as you make them
- **Export Options**: Download as PDF, DOCX, or HTML
- **User Accounts**: Save and manage multiple resume versions
- **Responsive Design**: Looks great on desktop and mobile devices

<div align="center">
  <img src="resume/assets/Screenshot 2025-02-26 151833.png" alt="Template Gallery" width="400"/>
  <img src="resume/assets/Screenshot 2025-02-26 151708.png.png" alt="Responsive Design" width="400"/>
</div>

## 🔧 Technologies

- Django 4.x
- Python 3.9+
- HTML/CSS/JavaScript
- Bootstrap 5

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

1. Clone the repository
   ```bash
   git clone https://github.com/3pkm/OnePageResume.git
   cd OnePageResume
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (admin)
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000`

## 💻 Usage

1. Register a new account or login
2. Create a new resume using the dashboard
3. Fill in your details in the provided sections
4. Choose a template that fits your style
5. Preview your resume and make adjustments as needed
6. Export your resume in your preferred format

<div align="center">
  <img src="resume/assets/Screenshot 2025-02-26 151708.png" alt="User Dashboard" width="600"/>
</div>

## 🧩 Project Structure

```
OnePageResume/
├── resume/                  # Main application
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, and assets
│   ├── models.py            # Data models
│   ├── views.py             # View functions
│   └── ...
├── onePageResume/           # Project settings
├── templates/               # Global templates
├── static/                  # Global static files
├── media/                   # User-uploaded content
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```
## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Contact

Prakhar Jaiswal - [LinkedIn](https://www.linkedin.com/in/prakhar-jaiswal-772403278/) - jas.prakhar@gmail.com

Project Link: [https://github.com/3pkm/OnePageResume](https://github.com/3pkm/OnePageResume)
