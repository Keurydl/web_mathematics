# Web Calculator

An advanced calculator web application developed with Django and Streamlit that offers various mathematical and scientific functionalities.

## Key Features

- **Modern Web Interface**: Developed with Django for a fluid user experience.
- **Advanced Scientific Calculator**: Includes modules for:
- Differential and Integral Calculus
- Physics
- Topology
- Advanced Mathematics
- Statistics
- **Calculation History**: Saves the last 10 calculations performed.
- **Keyboard Input**: Supports direct keyboard input.
- **Responsive Design**: Adapts to different screen sizes.

## System Requirements

- Python 3.10 or higher
- pip (Python package manager)
- Virtual Environment (recommended)

## Installation

1. **Clone the repository**
```bash
git clone [REPOSITORY_URL]
cd WebCalculator
```

2. **Create and activate a virtual environment**
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Apply migrations**
```bash
python manage.py migrate
```

5. **Run the development server**
```bash
python manage.py runserver
```

6. **Access the application**
Open your browser and go to: http://127.0.0.1:8000/

## Project Structure

```
CalculadoraWeb/
├── calculos/ # Main application
│ ├── migrations/ # Database migrations
│ ├── static/ # Static files (CSS, JS, images)
│ │ └── calculos/
│ │ └── sections/ # JS scripts for each section
│ ├── templates/ # HTML templates
│ │ └── calculos/
│ │ └── sections/ # Templates for each section
│ ├── admin.py # Django admin configuration
│ ├── apps.py # Application configuration
│ ├── streamlit_app.py # Streamlit calculator application
│ └── views.py # Application views
├── config/ # Django project configuration
├── manage.py # Django management script
└── requirements.txt # Project dependencies
```

## Technologies Used

- **Backend**:
- Django 4.2.7
- Python 3.10+
- Streamlit 1.45.1

- **Frontend**:
- HTML5
- CSS3
- JavaScript
- Bootstrap (optional, depending on implementation)

- **Database**:
- SQLite (default in development)

## Technical Features

- **Template System**: Uses Django template inheritance to maintain a consistent design.
- **Class-Based Views**: For cleaner, more maintainable code.
- **Error Handling**: Captures syntax errors and division by zero.
- **Operation History**: Temporary storage of recent calculations.

## Contribution

Contributions are welcome. Please follow these steps:

1. Fork the project.
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Contact

[Your Name] - [keurydd@outlook.com]

Project Link: []()
