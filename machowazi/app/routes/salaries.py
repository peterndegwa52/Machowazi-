from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, jsonify)
from flask_login import login_required, current_user
from ..models import Company, Salary, Interview
from ..forms import SalaryForm, InterviewForm
from .. import db
import bleach

salaries_bp = Blueprint('salaries', __name__)
ALLOWED_TAGS = []


def sanitize(text):
    return bleach.clean(text or '', tags=ALLOWED_TAGS, strip=True).strip()


# ── SALARIES ────────────────────────────────────────────────────────────────

@salaries_bp.route('/')
def salary_explorer():
    company_id = request.args.get('company', type=int)
    department = request.args.get('dept', '')
    level = request.args.get('level', '')

    query = Salary.query.filter_by(is_approved=True)

    if company_id:
        query = query.filter_by(company_id=company_id)
    if department:
        query = query.filter_by(department=department)
    if level:
        query = query.filter_by(job_level=level)

    salaries = query.order_by(Salary.monthly_gross.desc()).all()
    companies = Company.query.filter_by(is_active=True).order_by(Company.name).all()

    # Stats
    avg_salary = round(sum(s.monthly_gross for s in salaries) / len(salaries)) if salaries else 0
    max_salary = max((s.monthly_gross for s in salaries), default=0)
    min_salary = min((s.monthly_gross for s in salaries), default=0)

    departments = db.session.query(Salary.department).filter_by(
        is_approved=True).distinct().all()
    departments = [d[0] for d in departments if d[0]]

    levels = ['Junior', 'Mid', 'Senior', 'Manager', 'Director', 'C-Suite']

    return render_template('salaries/explorer.html',
                           salaries=salaries,
                           companies=companies,
                           departments=departments,
                           levels=levels,
                           avg_salary=avg_salary,
                           max_salary=max_salary,
                           min_salary=min_salary,
                           selected_company=company_id,
                           selected_dept=department,
                           selected_level=level)


@salaries_bp.route('/share', methods=['GET', 'POST'])
@salaries_bp.route('/share/<int:company_id>', methods=['GET', 'POST'])
@login_required
def share_salary(company_id=None):
    company = None
    if company_id:
        company = Company.query.get_or_404(company_id)

    form = SalaryForm()
    companies = Company.query.filter_by(is_active=True).order_by(Company.name).all()

    if form.validate_on_submit():
        cid = int(form.company_id.data) if form.company_id.data else company_id
        if not cid:
            flash('Please select a company.', 'error')
            return render_template('salaries/share.html', form=form,
                                   companies=companies, company=company)

        salary = Salary(
            company_id=cid,
            user_id=current_user.id,
            job_title=sanitize(form.job_title.data),
            job_level=form.job_level.data,
            department=form.department.data,
            monthly_gross=form.monthly_gross.data,
            monthly_net=form.monthly_net.data,
            allowances=form.allowances.data or 0,
            bonus_annual=form.bonus_annual.data or 0,
            years_experience=float(form.years_experience.data),
            location=form.location.data,
            is_approved=False
        )
        db.session.add(salary)
        db.session.commit()
        flash('Salary shared! It will appear after a quick review. Thank you.', 'success')
        return redirect(url_for('salaries.salary_explorer'))

    if company:
        form.company_id.data = str(company.id)

    return render_template('salaries/share.html', form=form,
                           companies=companies, company=company)


# ── INTERVIEWS ───────────────────────────────────────────────────────────────

@salaries_bp.route('/interviews')
def interviews():
    company_id = request.args.get('company', type=int)
    experience = request.args.get('exp', '')

    query = Interview.query.filter_by(is_approved=True)

    if company_id:
        query = query.filter_by(company_id=company_id)
    if experience:
        query = query.filter_by(experience=experience)

    interviews_list = query.order_by(Interview.created_at.desc()).all()
    companies = Company.query.filter_by(is_active=True).order_by(Company.name).all()

    return render_template('salaries/interviews.html',
                           interviews=interviews_list,
                           companies=companies,
                           selected_company=company_id,
                           selected_exp=experience)


@salaries_bp.route('/interviews/share', methods=['GET', 'POST'])
@salaries_bp.route('/interviews/share/<int:company_id>', methods=['GET', 'POST'])
@login_required
def share_interview(company_id=None):
    company = None
    if company_id:
        company = Company.query.get_or_404(company_id)

    form = InterviewForm()
    companies = Company.query.filter_by(is_active=True).order_by(Company.name).all()

    if form.validate_on_submit():
        cid = int(form.company_id.data) if form.company_id.data else company_id
        if not cid:
            flash('Please select a company.', 'error')
            return render_template('salaries/share_interview.html', form=form,
                                   companies=companies, company=company)

        interview = Interview(
            company_id=cid,
            user_id=current_user.id,
            job_title=sanitize(form.job_title.data),
            experience=form.experience.data,
            got_offer=form.got_offer.data,
            how_applied=form.how_applied.data,
            difficulty=int(form.difficulty.data),
            num_rounds=form.num_rounds.data,
            duration_weeks=form.duration_weeks.data,
            process_description=sanitize(form.process_description.data),
            questions_asked=sanitize(form.questions_asked.data),
            tips=sanitize(form.tips.data),
            is_approved=False
        )
        db.session.add(interview)
        db.session.commit()
        flash('Interview experience shared! It will appear after a quick review.', 'success')
        return redirect(url_for('salaries.interviews'))

    if company:
        form.company_id.data = str(company.id)

    return render_template('salaries/share_interview.html', form=form,
                           companies=companies, company=company)
