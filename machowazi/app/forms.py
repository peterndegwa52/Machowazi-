from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, SelectField,
                     FloatField, IntegerField, BooleanField, SubmitField, HiddenField)
from wtforms.validators import (DataRequired, Email, Length, EqualTo,
                                NumberRange, Optional, ValidationError)


# ── AUTH FORMS ──────────────────────────────────────────────────────────────

class RegisterForm(FlaskForm):
    email = StringField('Work Email', validators=[
        DataRequired(), Email(),
        Length(max=150, message='Email too long')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Create Anonymous Account')

    def validate_email(self, field):
        # Basic check — in production verify it's a work email
        personal_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        domain = field.data.split('@')[-1].lower()
        # Allow all for now, but flag personal emails
        # In production: require work email verification


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Keep me signed in')
    submit = SubmitField('Sign In')


# ── REVIEW FORM ──────────────────────────────────────────────────────────────

class ReviewForm(FlaskForm):
    company_id = HiddenField('Company ID')
    job_title = StringField('Your Job Title', validators=[
        DataRequired(), Length(min=2, max=120)
    ])
    employment_status = SelectField('Employment Status', choices=[
        ('current', 'Current Employee'),
        ('former', 'Former Employee')
    ], validators=[DataRequired()])
    years_at_company = SelectField('Years at Company', choices=[
        ('0.5', 'Less than 1 year'),
        ('1', '1 year'),
        ('2', '2 years'),
        ('3', '3 years'),
        ('4', '4 years'),
        ('5', '5 years'),
        ('7', '6-8 years'),
        ('10', '9+ years'),
    ], validators=[DataRequired()])
    location = SelectField('Location', choices=[
        ('Nairobi', 'Nairobi'),
        ('Mombasa', 'Mombasa'),
        ('Kisumu', 'Kisumu'),
        ('Nakuru', 'Nakuru'),
        ('Eldoret', 'Eldoret'),
        ('Other Kenya', 'Other Kenya'),
    ], default='Nairobi')

    headline = StringField('Review Headline', validators=[
        DataRequired(), Length(min=10, max=200,
        message='Headline should be between 10 and 200 characters')
    ])

    overall_rating = HiddenField('Overall Rating', validators=[DataRequired()])
    culture_rating = HiddenField('Culture Rating', validators=[DataRequired()])
    management_rating = HiddenField('Management Rating', validators=[DataRequired()])
    worklife_rating = HiddenField('Work-Life Rating', validators=[DataRequired()])
    pay_rating = HiddenField('Pay Rating', validators=[DataRequired()])
    growth_rating = HiddenField('Growth Rating', validators=[DataRequired()])

    pros = TextAreaField('Pros', validators=[
        DataRequired(),
        Length(min=30, max=2000, message='Pros must be at least 30 characters')
    ])
    cons = TextAreaField('Cons', validators=[
        DataRequired(),
        Length(min=30, max=2000, message='Cons must be at least 30 characters')
    ])
    advice_to_management = TextAreaField('Advice to Management (Optional)', validators=[
        Optional(), Length(max=1000)
    ])
    would_recommend = BooleanField('I would recommend this company to a friend')
    ceo_approval = BooleanField('I approve of the CEO\'s leadership')
    submit = SubmitField('Submit Anonymously')

    def validate_overall_rating(self, field):
        try:
            val = float(field.data)
            if not (1 <= val <= 5):
                raise ValidationError('Rating must be between 1 and 5')
        except (TypeError, ValueError):
            raise ValidationError('Please select a rating')


# ── SALARY FORM ───────────────────────────────────────────────────────────────

class SalaryForm(FlaskForm):
    company_id = HiddenField('Company ID')
    job_title = StringField('Job Title', validators=[
        DataRequired(), Length(min=2, max=120)
    ])
    job_level = SelectField('Level', choices=[
        ('Junior', 'Junior / Entry Level'),
        ('Mid', 'Mid Level'),
        ('Senior', 'Senior'),
        ('Manager', 'Manager'),
        ('Director', 'Director / Head'),
        ('C-Suite', 'C-Suite / Executive'),
    ], validators=[DataRequired()])
    department = SelectField('Department', choices=[
        ('Retail Banking', 'Retail Banking'),
        ('Corporate Banking', 'Corporate Banking'),
        ('Credit', 'Credit'),
        ('Risk & Compliance', 'Risk & Compliance'),
        ('Technology', 'Technology / IT'),
        ('Digital', 'Digital Banking'),
        ('Finance', 'Finance & Accounting'),
        ('HR', 'Human Resources'),
        ('Marketing', 'Marketing'),
        ('Operations', 'Operations'),
        ('Treasury', 'Treasury'),
        ('Legal', 'Legal & Compliance'),
        ('Other', 'Other'),
    ])
    monthly_gross = IntegerField('Monthly Gross Salary (KES)', validators=[
        DataRequired(),
        NumberRange(min=10000, max=5000000, message='Please enter a valid salary in KES')
    ])
    monthly_net = IntegerField('Monthly Net / Take-Home (KES, optional)', validators=[
        Optional(),
        NumberRange(min=5000, max=4000000)
    ])
    allowances = IntegerField('Monthly Allowances (KES, optional)', validators=[
        Optional(), NumberRange(min=0)
    ])
    bonus_annual = IntegerField('Annual Bonus (KES, optional)', validators=[
        Optional(), NumberRange(min=0)
    ])
    years_experience = SelectField('Total Years of Experience', choices=[
        ('0.5', 'Less than 1 year'),
        ('1', '1 year'),
        ('2', '2 years'),
        ('3', '3 years'),
        ('5', '4-5 years'),
        ('7', '6-8 years'),
        ('10', '9-12 years'),
        ('15', '13+ years'),
    ])
    location = SelectField('Work Location', choices=[
        ('Nairobi', 'Nairobi'),
        ('Mombasa', 'Mombasa'),
        ('Kisumu', 'Kisumu'),
        ('Nakuru', 'Nakuru'),
        ('Eldoret', 'Eldoret'),
        ('Other', 'Other'),
    ])
    submit = SubmitField('Share Salary Anonymously')


# ── INTERVIEW FORM ────────────────────────────────────────────────────────────

class InterviewForm(FlaskForm):
    company_id = HiddenField('Company ID')
    job_title = StringField('Role You Interviewed For', validators=[
        DataRequired(), Length(min=2, max=120)
    ])
    experience = SelectField('Overall Experience', choices=[
        ('positive', '😊 Positive'),
        ('neutral', '😐 Neutral'),
        ('negative', '😞 Negative'),
    ], validators=[DataRequired()])
    got_offer = SelectField('Outcome', choices=[
        ('yes', 'Got the offer'),
        ('no', 'Did not get offer'),
        ('declined', 'Got offer but declined'),
        ('waiting', 'Still waiting'),
    ])
    how_applied = SelectField('How Applied', choices=[
        ('online', 'Applied Online'),
        ('referral', 'Employee Referral'),
        ('headhunter', 'Headhunter / Recruiter'),
        ('walk-in', 'Walk-in / Direct'),
        ('campus', 'Campus Recruitment'),
    ])
    difficulty = SelectField('Interview Difficulty', choices=[
        ('1', '1 - Very Easy'),
        ('2', '2 - Easy'),
        ('3', '3 - Average'),
        ('4', '4 - Difficult'),
        ('5', '5 - Very Difficult'),
    ])
    num_rounds = IntegerField('Number of Interview Rounds', validators=[
        DataRequired(), NumberRange(min=1, max=10)
    ])
    duration_weeks = IntegerField('Total Process Duration (weeks)', validators=[
        Optional(), NumberRange(min=1, max=52)
    ])
    process_description = TextAreaField('Describe the Interview Process', validators=[
        DataRequired(),
        Length(min=50, max=3000, message='Please describe the process in at least 50 characters')
    ])
    questions_asked = TextAreaField('Questions You Were Asked (optional)', validators=[
        Optional(), Length(max=2000)
    ])
    tips = TextAreaField('Tips for Other Candidates (optional)', validators=[
        Optional(), Length(max=1000)
    ])
    submit = SubmitField('Share Experience Anonymously')
