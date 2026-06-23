from flask import Blueprint, render_template, request, abort, jsonify
from ..models import Company, Review, Salary, Interview
from .. import db
from sqlalchemy import func

companies_bp = Blueprint('companies', __name__)


@companies_bp.route('/')
def all_companies():
    industry = request.args.get('industry', 'all')
    sort = request.args.get('sort', 'reviews')

    query = Company.query.filter_by(is_active=True)

    companies = query.all()

    # Sort in Python since avg_rating is a property
    if sort == 'rating':
        companies = sorted(companies, key=lambda c: c.avg_rating, reverse=True)
    elif sort == 'name':
        companies = sorted(companies, key=lambda c: c.name)
    else:
        companies = sorted(companies, key=lambda c: c.review_count, reverse=True)

    return render_template('companies/all.html',
                           companies=companies,
                           sort=sort,
                           industry=industry)


@companies_bp.route('/<slug>')
def company_detail(slug):
    company = Company.query.filter_by(slug=slug, is_active=True).first_or_404()

    tab = request.args.get('tab', 'reviews')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    reviews = (Review.query
               .filter_by(company_id=company.id, is_approved=True)
               .order_by(Review.created_at.desc())
               .paginate(page=page, per_page=per_page, error_out=False))

    salaries = (Salary.query
                .filter_by(company_id=company.id, is_approved=True)
                .order_by(Salary.monthly_gross.desc())
                .all())

    interviews = (Interview.query
                  .filter_by(company_id=company.id, is_approved=True)
                  .order_by(Interview.created_at.desc())
                  .all())

    # Rating breakdown
    all_reviews = Review.query.filter_by(company_id=company.id, is_approved=True).all()
    rating_breakdown = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for r in all_reviews:
        bucket = round(r.overall_rating)
        rating_breakdown[bucket] = rating_breakdown.get(bucket, 0) + 1

    # Sub-ratings averages
    sub_ratings = {}
    if all_reviews:
        sub_ratings = {
            'Culture & Values': round(sum(r.culture_rating for r in all_reviews) / len(all_reviews), 1),
            'Management': round(sum(r.management_rating for r in all_reviews) / len(all_reviews), 1),
            'Work-Life Balance': round(sum(r.worklife_rating for r in all_reviews) / len(all_reviews), 1),
            'Compensation': round(sum(r.pay_rating for r in all_reviews) / len(all_reviews), 1),
            'Career Growth': round(sum(r.growth_rating for r in all_reviews) / len(all_reviews), 1),
        }

    # Salary stats
    salary_avg = 0
    if salaries:
        salary_avg = round(sum(s.monthly_gross for s in salaries) / len(salaries))

    # Similar companies
    similar = (Company.query
               .filter(Company.id != company.id, Company.is_active == True)
               .limit(4).all())

    return render_template('companies/detail.html',
                           company=company,
                           reviews=reviews,
                           salaries=salaries,
                           interviews=interviews,
                           rating_breakdown=rating_breakdown,
                           sub_ratings=sub_ratings,
                           salary_avg=salary_avg,
                           similar=similar,
                           tab=tab)
