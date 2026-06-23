from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from .. import db, mail
from ..models import User, EmailVerification
from ..forms import RegisterForm, LoginForm
import secrets

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        email_hash = User.hash_email(form.email.data)

        if User.query.filter_by(email_hash=email_hash).first():
            flash('An account with this email already exists.', 'error')
            return render_template('auth/register.html', form=form)

        user = User(
            email_hash=email_hash,
            display_token=User.generate_token(),
            is_verified=False
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Send verification email
        token = secrets.token_urlsafe(32)
        verification = EmailVerification(
            user_id=user.id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        db.session.add(verification)
        db.session.commit()

        _send_verification_email(form.email.data, token)

        flash('Account created! Check your email to verify your account.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        email_hash = User.hash_email(form.email.data)
        user = User.query.filter_by(email_hash=email_hash).first()

        if user and user.check_password(form.password.data):
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Welcome back!', 'success')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/verify/<token>')
def verify_email(token):
    verification = EmailVerification.query.filter_by(token=token, is_used=False).first()

    if not verification:
        flash('Invalid or expired verification link.', 'error')
        return redirect(url_for('auth.login'))

    if verification.expires_at < datetime.utcnow():
        flash('Verification link has expired. Please request a new one.', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.get(verification.user_id)
    user.is_verified = True
    verification.is_used = True
    db.session.commit()

    login_user(user)
    flash('Email verified! You can now write reviews.', 'success')
    return redirect(url_for('main.index'))


@auth_bp.route('/resend-verification')
@login_required
def resend_verification():
    if current_user.is_verified:
        return redirect(url_for('main.index'))
    flash('Verification email sent. Check your inbox.', 'info')
    return redirect(url_for('main.index'))


def _send_verification_email(email, token):
    try:
        from flask_mail import Message
        from flask import current_app
        verify_url = url_for('auth.verify_email', token=token, _external=True)
        msg = Message(
            subject='Verify your Macho Wazi account',
            recipients=[email],
            html=f'''
            <div style="font-family:Inter,sans-serif;max-width:520px;margin:0 auto;">
              <h2 style="color:#0A1628;">Welcome to Macho Wazi 👁️</h2>
              <p>Click the link below to verify your email and start writing anonymous reviews:</p>
              <a href="{verify_url}"
                 style="display:inline-block;background:#F5A623;color:#0A1628;
                        padding:12px 28px;border-radius:8px;font-weight:600;
                        text-decoration:none;margin:16px 0;">
                Verify My Account
              </a>
              <p style="color:#8A9BB0;font-size:0.85rem;">
                This link expires in 24 hours. Your email is never shared with anyone.
              </p>
            </div>
            '''
        )
        mail.send(msg)
    except Exception as e:
        print(f'Email send failed: {e}')
