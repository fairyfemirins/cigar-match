"""
CigarMatch: AI-Powered Personalized Cigar Subscription Service
"""
import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cigarmatch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock AI Recommendation Engine (Rule-Based MVP)
def mock_recommend_cigars(preferences):
    """Mock recommendation engine based on user preferences."""
    cigar_db = {
        'mild': ['Montecristo White', 'Romeo y Julieta Reserva Real', 'H. Upmann Half Corona'],
        'medium': ['Partagas Serie D No. 4', 'Bolivar Petit Coronas', 'Cohiba Robusto'],
        'strong': ['Cohiba Behike', 'Trinidad Fundadores', 'El Rey del Mundo Choix Supreme'],
        'connecticut': ['Montecristo White', 'H. Upmann Half Corona'],
        'habano': ['Partagas Serie D No. 4', 'Bolivar Petit Coronas'],
        'maduro': ['Cohiba Robusto', 'Trinidad Fundadores'],
        'ecuador': ['Montecristo White', 'Romeo y Julieta Reserva Real'],
        'nicaragua': ['Partagas Serie D No. 4', 'Cohiba Behike'],
        'dominican': ['H. Upmann Half Corona', 'El Rey del Mundo Choix Supreme'],
        'budget': ['Montecristo White', 'H. Upmann Half Corona', 'Bolivar Petit Coronas'],
        'premium': ['Cohiba Behike', 'Trinidad Fundadores', 'El Rey del Mundo Choix Supreme']
    }
    
    strength = preferences.get('strength', 'medium')
    wrapper = preferences.get('wrapper', 'habano')
    origin = preferences.get('origin', 'nicaragua')
    price = preferences.get('price', 'budget')
    
    # Simple rule-based recommendation
    recommendations = set()
    for key in [strength, wrapper, origin, price]:
        recommendations.update(cigar_db.get(key, []))
    
    return list(recommendations)[:3]

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')  # user, admin

class Cigar(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    strength = db.Column(db.String(20), nullable=False)  # mild, medium, strong
    wrapper = db.Column(db.String(20), nullable=False)  # connecticut, habano, maduro
    origin = db.Column(db.String(50), nullable=False)  # ecuador, nicaragua, dominican
    price_range = db.Column(db.String(20), nullable=False)  # budget, premium
    description = db.Column(db.Text)

class UserPreference(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    strength = db.Column(db.String(20))
    wrapper = db.Column(db.String(20))
    origin = db.Column(db.String(50))
    price = db.Column(db.String(20))
    frequency = db.Column(db.String(20))  # monthly, quarterly
    user = db.relationship('User', backref=db.backref('preferences', lazy=True))

class Subscription(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    cigar_ids = db.Column(db.String(500))  # Comma-separated list of cigar IDs
    frequency = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    user = db.relationship('User', backref=db.backref('subscriptions', lazy=True))

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PreferenceForm(FlaskForm):
    strength = SelectField('Strength', choices=[
        ('mild', 'Mild'), ('medium', 'Medium'), ('strong', 'Strong')
    ], validators=[DataRequired()])
    wrapper = SelectField('Wrapper', choices=[
        ('connecticut', 'Connecticut'), ('habano', 'Habano'), ('maduro', 'Maduro')
    ], validators=[DataRequired()])
    origin = SelectField('Origin', choices=[
        ('ecuador', 'Ecuador'), ('nicaragua', 'Nicaragua'), ('dominican', 'Dominican Republic')
    ], validators=[DataRequired()])
    price = SelectField('Price Range', choices=[
        ('budget', 'Budget ($50-$100)'), ('premium', 'Premium ($100-$300)')
    ], validators=[DataRequired()])
    frequency = SelectField('Frequency', choices=[
        ('monthly', 'Monthly'), ('quarterly', 'Quarterly')
    ], validators=[DataRequired()])
    submit = SubmitField('Save Preferences')

# Flask-Login User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    preferences = UserPreference.query.filter_by(user_id=current_user.id).first()
    recommendations = []
    if preferences:
        recommendations = mock_recommend_cigars({
            'strength': preferences.strength,
            'wrapper': preferences.wrapper,
            'origin': preferences.origin,
            'price': preferences.price
        })
    return render_template('dashboard.html', preferences=preferences, recommendations=recommendations)

@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    form = PreferenceForm()
    preferences = UserPreference.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        if preferences:
            preferences.strength = form.strength.data
            preferences.wrapper = form.wrapper.data
            preferences.origin = form.origin.data
            preferences.price = form.price.data
            preferences.frequency = form.frequency.data
        else:
            preferences = UserPreference(
                user_id=current_user.id,
                strength=form.strength.data,
                wrapper=form.wrapper.data,
                origin=form.origin.data,
                price=form.price.data,
                frequency=form.frequency.data
            )
            db.session.add(preferences)
        db.session.commit()
        flash('Preferences saved!', 'success')
        return redirect(url_for('dashboard'))
    if preferences:
        form.strength.data = preferences.strength
        form.wrapper.data = preferences.wrapper
        form.origin.data = preferences.origin
        form.price.data = preferences.price
        form.frequency.data = preferences.frequency
    return render_template('preferences.html', form=form)

@app.route('/subscribe')
@login_required
def subscribe():
    preferences = UserPreference.query.filter_by(user_id=current_user.id).first()
    if not preferences:
        flash('Please set your preferences first.', 'warning')
        return redirect(url_for('preferences'))
    
    recommendations = mock_recommend_cigars({
        'strength': preferences.strength,
        'wrapper': preferences.wrapper,
        'origin': preferences.origin,
        'price': preferences.price
    })
    
    # Get cigar IDs from names (mock)
    cigar_ids = []
    for name in recommendations:
        cigar = Cigar.query.filter_by(name=name).first()
        if cigar:
            cigar_ids.append(cigar.id)
    
    # Create or update subscription
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    if subscription:
        subscription.cigar_ids = ','.join(cigar_ids)
        subscription.frequency = preferences.frequency
        subscription.active = True
    else:
        subscription = Subscription(
            user_id=current_user.id,
            cigar_ids=','.join(cigar_ids),
            frequency=preferences.frequency
        )
        db.session.add(subscription)
    db.session.commit()
    
    flash(f'Subscription activated! You will receive {preferences.frequency} shipments.', 'success')
    return redirect(url_for('dashboard'))

# Admin Routes
@app.route('/admin/cigars')
@login_required
def admin_cigars():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    cigars = Cigar.query.all()
    return render_template('admin_cigars.html', cigars=cigars)

# Initialize Database
with app.app_context():
    db.create_all()
    # Add admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            id=str(uuid.uuid4()),
            username='admin',
            email='admin@cigarmatch.com',
            password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
    # Add sample cigars if not exists
    if not Cigar.query.first():
        sample_cigars = [
            Cigar(name='Montecristo White', brand='Montecristo', strength='mild', wrapper='connecticut', origin='ecuador', price_range='budget', description='Smooth and creamy with notes of cedar and nuts.'),
            Cigar(name='Partagas Serie D No. 4', brand='Partagas', strength='medium', wrapper='habano', origin='nicaragua', price_range='budget', description='Rich and full-bodied with spice and leather notes.'),
            Cigar(name='Cohiba Behike', brand='Cohiba', strength='strong', wrapper='maduro', origin='dominican', price_range='premium', description='Complex and powerful with cocoa, coffee, and pepper notes.')
        ]
        db.session.bulk_save_objects(sample_cigars)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)