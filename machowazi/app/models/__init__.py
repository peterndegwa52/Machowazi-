from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db, login_manager
import hashlib


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email_hash = db.Column(db.String(128), unique=True, nullable=False)  # hashed for privacy
    display_token = db.Column(db.String(32), unique=True, nullable=False)  # random anonymous ID
    password_hash = db.Column(db.String(256), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    salaries = db.relationship('Salary', backref='contributor', lazy='dynamic')
    interviews = db.relationship('Interview', backref='author', lazy='dynamic')
    votes = db.relationship('ReviewVote', backref='voter', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def hash_email(email):
        return hashlib.sha256(email.lower().strip().encode()).hexdigest()

    @staticmethod
    def generate_token():
        import secrets
        return secrets.token_hex(16)

    def __repr__(self):
        return f'<User {self.display_token}>'


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    logo_initials = db.Column(db.String(5), nullable=False)
    logo_color = db.Column(db.String(100), default='linear-gradient(135deg,#0A1628,#152240)')
    industry = db.Column(db.String(80), default='Banking & Finance')
    headquarters = db.Column(db.String(120), default='Nairobi, Kenya')
    founded = db.Column(db.Integer)
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    size = db.Column(db.String(50))  # e.g. "1000-5000 employees"
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship('Review', backref='company', lazy='dynamic', cascade='all, delete-orphan')
    salaries = db.relationship('Salary', backref='company', lazy='dynamic', cascade='all, delete-orphan')
    interviews = db.relationship('Interview', backref='company', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def avg_rating(self):
        reviews = Review.query.filter_by(company_id=self.id, is_approved=True).all()
        if not reviews:
            return 0
        return round(sum(r.overall_rating for r in reviews) / len(reviews), 1)

    @property
    def review_count(self):
        return Review.query.filter_by(company_id=self.id, is_approved=True).count()

    @property
    def salary_count(self):
        return Salary.query.filter_by(company_id=self.id, is_approved=True).count()

    @property
    def transparency_score(self):
        reviews = Review.query.filter_by(company_id=self.id, is_approved=True).all()
        if not reviews:
            return 0
        scores = []
        for r in reviews:
            avg = (r.culture_rating + r.management_rating + r.worklife_rating +
                   r.pay_rating + r.growth_rating) / 5
            scores.append(avg)
        return round((sum(scores) / len(scores)) / 5 * 100) if scores else 0

    @property
    def recommend_pct(self):
        reviews = Review.query.filter_by(company_id=self.id, is_approved=True).all()
        if not reviews:
            return 0
        recommended = sum(1 for r in reviews if r.would_recommend)
        return round(recommended / len(reviews) * 100)

    def __repr__(self):
        return f'<Company {self.name}>'


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    job_title = db.Column(db.String(120), nullable=False)
    employment_status = db.Column(db.String(20), nullable=False)  # current / former
    years_at_company = db.Column(db.Float)
    location = db.Column(db.String(80), default='Nairobi')

    # Ratings 1-5
    overall_rating = db.Column(db.Float, nullable=False)
    culture_rating = db.Column(db.Float, nullable=False)
    management_rating = db.Column(db.Float, nullable=False)
    worklife_rating = db.Column(db.Float, nullable=False)
    pay_rating = db.Column(db.Float, nullable=False)
    growth_rating = db.Column(db.Float, nullable=False)

    # Content
    headline = db.Column(db.String(200), nullable=False)
    pros = db.Column(db.Text, nullable=False)
    cons = db.Column(db.Text, nullable=False)
    advice_to_management = db.Column(db.Text)
    would_recommend = db.Column(db.Boolean, default=True)
    ceo_approval = db.Column(db.Boolean)

    # Moderation
    is_approved = db.Column(db.Boolean, default=False)
    is_flagged = db.Column(db.Boolean, default=False)
    flag_reason = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    votes = db.relationship('ReviewVote', backref='review', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def helpful_count(self):
        return ReviewVote.query.filter_by(review_id=self.id, is_helpful=True).count()

    @property
    def not_helpful_count(self):
        return ReviewVote.query.filter_by(review_id=self.id, is_helpful=False).count()

    @property
    def star_display(self):
        full = int(self.overall_rating)
        return '★' * full + '☆' * (5 - full)

    def __repr__(self):
        return f'<Review {self.id} for {self.company_id}>'


class ReviewVote(db.Model):
    __tablename__ = 'review_votes'

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_helpful = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('review_id', 'user_id', name='unique_vote'),)


class Salary(db.Model):
    __tablename__ = 'salaries'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    job_title = db.Column(db.String(120), nullable=False)
    job_level = db.Column(db.String(50))  # Junior / Mid / Senior / Manager / Director
    department = db.Column(db.String(80))
    monthly_gross = db.Column(db.Integer, nullable=False)  # KES
    monthly_net = db.Column(db.Integer)
    allowances = db.Column(db.Integer, default=0)
    bonus_annual = db.Column(db.Integer, default=0)
    employment_type = db.Column(db.String(30), default='Full-time')
    years_experience = db.Column(db.Float)
    location = db.Column(db.String(80), default='Nairobi')

    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Salary {self.job_title} at {self.company_id}>'


class Interview(db.Model):
    __tablename__ = 'interviews'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    job_title = db.Column(db.String(120), nullable=False)
    experience = db.Column(db.String(20), nullable=False)  # positive / negative / neutral
    got_offer = db.Column(db.String(20))  # yes / no / waiting
    how_applied = db.Column(db.String(50))  # online / referral / headhunter / walk-in
    difficulty = db.Column(db.Integer)  # 1-5
    process_description = db.Column(db.Text, nullable=False)
    questions_asked = db.Column(db.Text)
    tips = db.Column(db.Text)
    duration_weeks = db.Column(db.Integer)
    num_rounds = db.Column(db.Integer)

    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Interview {self.job_title} at {self.company_id}>'


class EmailVerification(db.Model):
    __tablename__ = 'email_verifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
