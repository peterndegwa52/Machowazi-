from flask import Blueprint, render_template, request, jsonify
from ..models import Company, Review, Salary, Interview
from .. import db
from sqlalchemy import func, or_

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    # Top companies by review count
    top_companies = (Company.query
                     .filter_by(is_active=True)
                     .join(Review, Review.company_id == Company.id, isouter=True)
                     .filter(or_(Review.is_approved == True, Review.id == None))
                     .group_by(Company.id)
                     .order_by(func.count(Review.id).desc())
                     .limit(6).all())

    # Recent approved reviews
    recent_reviews = (Review.query
                      .filter_by(is_approved=True)
                      .order_by(Review.created_at.desc())
                      .limit(5).all())

    # Stats
    total_reviews = Review.query.filter_by(is_approved=True).count()
    total_companies = Company.query.filter_by(is_active=True).count()
    total_salaries = Salary.query.filter_by(is_approved=True).count()

    return render_template('index.html',
                           companies=top_companies,
                           recent_reviews=recent_reviews,
                           total_reviews=total_reviews,
                           total_companies=total_companies,
                           total_salaries=total_salaries)


@main_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    results = []
    if q:
        results = Company.query.filter(
            Company.name.ilike(f'%{q}%'),
            Company.is_active == True
        ).limit(10).all()
    return render_template('search.html', results=results, query=q)


@main_bp.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify([])
    results = Company.query.filter(
        Company.name.ilike(f'%{q}%'),
        Company.is_active == True
    ).limit(8).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'slug': c.slug,
        'industry': c.industry,
        'avg_rating': c.avg_rating,
        'review_count': c.review_count,
        'logo_initials': c.logo_initials
    } for c in results])


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')


@main_bp.route('/for-employers')
def for_employers():
    return render_template('for_employers.html')
