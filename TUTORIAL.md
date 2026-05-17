# CigarMatch - Reproducible Setup Guide

## Prerequisites
- Python 3.8+
- pip
- A modern web browser (Chrome, Firefox, Edge)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/fairyfemirins/cigar-match.git
cd cigar-match
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install flask flask-sqlalchemy flask-login flask-wtf markdown2 weasyprint
```

### 4. Run the Server
```bash
python app.py
```

### 5. Access the App
Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### 1. Register & Log In
1. Click **Register** to create an account.
2. Log in with your credentials.

### 2. Set Your Preferences
1. Navigate to **Preferences**.
2. Select your preferred **strength, wrapper, origin, price range, and frequency**.
3. Click **Save Preferences**.

### 3. Get Recommendations
1. Go to **Dashboard** to see your personalized cigar recommendations.
2. Click **Subscribe Now** to activate your subscription.

### 4. Admin Dashboard
1. Log in as `admin` (password: `admin123`).
2. Navigate to **Admin Panel** to manage cigar inventory.

## Troubleshooting

### 1. Port Already in Use
If port `5000` is already in use, change the port in `app.py`:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

### 2. Templates Not Found
Ensure the `templates/` directory exists and contains all HTML files. If missing, recreate it:
```bash
mkdir -p templates
mv *.html templates/
```

### 3. Database Errors
If the database fails to initialize:
1. Delete the existing database:
   ```bash
   rm cigarmatch.db
   ```
2. Restart the server to recreate the database:
   ```bash
   python app.py
   ```

## License
MIT