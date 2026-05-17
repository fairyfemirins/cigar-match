# CigarMatch: AI-Powered Personalized Cigar Subscription

> Discover cigars tailored to your taste with AI-powered recommendations and monthly subscriptions.

![CigarMatch Demo](https://via.placeholder.com/468x240?text=CigarMatch+Demo)

## Features
- **Personalized Recommendations**: AI analyzes your preferences to suggest cigars you'll love.
- **Monthly Subscriptions**: Receive handpicked cigars delivered to your door every month or quarter.
- **Premium Selection**: Access a curated collection of cigars from top brands and regions.
- **Admin Dashboard**: Manage cigar inventory and user subscriptions.

## Installation
```bash
# Clone the repository
 git clone https://github.com/fairyfemirins/cigar-match.git
 cd cigar-match

# Set up a virtual environment (recommended)
 python3 -m venv venv
 source venv/bin/activate  # Linux/Mac
 # OR
 venv\Scripts\activate  # Windows

# Install dependencies
 pip install -r requirements.txt
```

## Usage
```bash
# Run the application
 python app.py
```

Open your browser and navigate to `http://localhost:5000`.

### Admin Access
- **Username**: `admin`
- **Password**: `admin123`

## Technical Architecture
- **Backend**: Python + Flask
- **Frontend**: HTML/CSS/JS + Bootstrap 5
- **Database**: SQLite (file-based, no server required)
- **AI Engine**: Rule-based MVP (expandable to ML)

## License
MIT