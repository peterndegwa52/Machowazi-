from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, jsonify, abort)
from flask_login import login_required, current_user
from ..models import Company, Review, ReviewVote
from ..forms import ReviewForm
from .. import db
import bleach

reviews_bp = Blueprint('reviews', __name__)

ALLOWED_TAGS = []  # plain text only


def sanitize(text):
    return bleach.clean(text, tags=ALLOWED_TAGS, strip=True).strip()


@reviews_bp.route('/write', methods=['GET', 'POST'])
@reviews_bp.route('/write/<int:company_id>', methods=['GET', 'POST'])
@login_required
def write_review(company_id=None):
    company = None
    if company_id:
        company = Company.query.get_or_404(company_id)

    form = ReviewForm()

    # Populate company choices dynamically
    companies = Company.query.filter_by(is_active=True).order_by(Company.name).all()

    if form.validate_on_submit():
        cid = int(form.company_id.data) if form.company_id.data else company_id
        if not cid:
            flash('Please select a company.', 'error')
            return render_template('reviews/write.html', form=form,
                                   companies=companies, company=company)

        # Prevent duplicate reviews for same company
        existing = Review.query.filter_by(
            company_id=cid, user_id=current_user.id
        ).first()
        if existing:
            flash('You have already submitted a review for this company.', 'warning')
            return redirect(url_for('companies.company_detail',
                                    slug=Company.query.get(cid).slug))

        try:
            review = Review(
                company_id=cid,
                user_id=current_user.id,
                job_title=sanitize(form.job_title.data),
                employment_status=form.employment_status.data,
                years_at_company=float(form.years_at_company.data),
                location=form.location.data,
                headline=sanitize(form.headline.data),
                overall_rating=float(form.overall_rating.data),
                culture_rating=float(form.culture_rating.data),
                management_rating=float(form.management_rating.data),
                worklife_rating=float(form.worklife_rating.data),
                pay_rating=float(form.pay_rating.data),
                growth_rating=float(form.growth_rating.data),
                pros=sanitize(form.pros.data),
                cons=sanitize(form.cons.data),
                advice_to_management=sanitize(form.advice_to_management.data) if form.advice_to_management.data else None,
                would_recommend=form.would_recommend.data,
                ceo_approval=form.ceo_approval.data,
                is_approved=False  # requires admin approval
            )
            db.session.add(review)
            db.session.commit()
            flash('Thank you! Your review has been submitted and will appear after a quick check.', 'success')
            comp = Company.query.get(cid)
            return redirect(url_for('companies.company_detail', slug=comp.slug))

        except Exception as e:
            db.session.rollback()
            flash('Something went wrong. Please try again.', 'error')

    if company:
        form.company_id.data = str(company.id)

    return render_template('reviews/write.html', form=form,
                           companies=companies, company=company)


@reviews_bp.route('/vote/<int:review_id>', methods=['POST'])
@login_required
def vote(review_id):
    review = Review.query.get_or_404(review_id)
    is_helpful = request.json.get('helpful', True)

    existing = ReviewVote.query.filter_by(
        review_id=review_id, user_id=current_user.id
    ).first()

    if existing:
        existing.is_helpful = is_helpful
    else:
        vote = ReviewVote(
            review_id=review_id,
            user_id=current_user.id,
            is_helpful=is_helpful
        )
        db.session.add(vote)

    db.session.commit()
    return jsonify({
        'helpful': review.helpful_count,
        'not_helpful': review.not_helpful_count
    })


@reviews_bp.route('/flag/<int:review_id>', methods=['POST'])
@login_required
def flag_review(review_id):
    review = Review.query.get_or_404(review_id)
    reason = request.json.get('reason', 'Inappropriate content')
    review.is_flagged = True
    review.flag_reason = reason
    db.session.commit()
    return jsonify({'status': 'flagged'})
