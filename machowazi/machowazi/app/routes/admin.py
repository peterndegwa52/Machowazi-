from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, abort)
from flask_login import login_required, current_user
from ..models import Company, Review, Salary, Interview, User
from .. import db
from functools import wraps

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_companies': Company.query.count(),
        'pending_reviews': Review.query.filter_by(is_approved=False, is_flagged=False).count(),
        'approved_reviews': Review.query.filter_by(is_approved=True).count(),
        'flagged_reviews': Review.query.filter_by(is_flagged=True).count(),
        'pending_salaries': Salary.query.filter_by(is_approved=False).count(),
        'pending_interviews': Interview.query.filter_by(is_approved=False).count(),
    }
    recent_reviews = (Review.query
                      .filter_by(is_approved=False, is_flagged=False)
                      .order_by(Review.created_at.desc())
                      .limit(10).all())
    return render_template('admin/dashboard.html', stats=stats,
                           recent_reviews=recent_reviews)


@admin_bp.route('/reviews')
@login_required
@admin_required
def reviews():
    status = request.args.get('status', 'pending')
    if status == 'pending':
        items = Review.query.filter_by(is_approved=False, is_flagged=False).order_by(Review.created_at.desc()).all()
    elif status == 'approved':
        items = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
    else:
        items = Review.query.filter_by(is_flagged=True).order_by(Review.created_at.desc()).all()
    return render_template('admin/reviews.html', reviews=items, status=status)


@admin_bp.route('/reviews/<int:review_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_review(review_id):
    review = Review.query.get_or_404(review_id)
    review.is_approved = True
    review.is_flagged = False
    db.session.commit()
    flash(f'Review #{review_id} approved.', 'success')
    return redirect(url_for('admin.reviews'))


@admin_bp.route('/reviews/<int:review_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash(f'Review #{review_id} deleted.', 'info')
    return redirect(url_for('admin.reviews'))


@admin_bp.route('/salaries')
@login_required
@admin_required
def salaries():
    items = Salary.query.filter_by(is_approved=False).order_by(Salary.created_at.desc()).all()
    return render_template('admin/salaries.html', salaries=items)


@admin_bp.route('/salaries/<int:salary_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_salary(salary_id):
    salary = Salary.query.get_or_404(salary_id)
    salary.is_approved = True
    db.session.commit()
    flash('Salary approved.', 'success')
    return redirect(url_for('admin.salaries'))


@admin_bp.route('/salaries/<int:salary_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_salary(salary_id):
    salary = Salary.query.get_or_404(salary_id)
    db.session.delete(salary)
    db.session.commit()
    flash('Salary removed.', 'info')
    return redirect(url_for('admin.salaries'))


@admin_bp.route('/interviews')
@login_required
@admin_required
def interviews():
    items = Interview.query.filter_by(is_approved=False).order_by(Interview.created_at.desc()).all()
    return render_template('admin/interviews.html', interviews=items)


@admin_bp.route('/interviews/<int:interview_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_interview(interview_id):
    interview = Interview.query.get_or_404(interview_id)
    interview.is_approved = True
    db.session.commit()
    flash('Interview approved.', 'success')
    return redirect(url_for('admin.interviews'))


@admin_bp.route('/interviews/<int:interview_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_interview(interview_id):
    interview = Interview.query.get_or_404(interview_id)
    db.session.delete(interview)
    db.session.commit()
    flash('Interview removed.', 'info')
    return redirect(url_for('admin.interviews'))


@admin_bp.route('/companies')
@login_required
@admin_required
def companies():
    items = Company.query.order_by(Company.name).all()
    return render_template('admin/companies.html', companies=items)


@admin_bp.route('/companies/<int:company_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.is_active = not company.is_active
    db.session.commit()
    flash(f'{company.name} {"activated" if company.is_active else "deactivated"}.', 'info')
    return redirect(url_for('admin.companies'))


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    items = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=items)


@admin_bp.route('/make-admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def make_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash(f'User promoted to admin.', 'success')
    return redirect(url_for('admin.users'))
