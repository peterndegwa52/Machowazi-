from . import db


def seed_data():
    from .models import Company, Review, Salary, Interview, User

    if Company.query.count() > 0:
        return

    companies = [
        Company(
            name='KCB Group',
            slug='kcb-group',
            logo_initials='KCB',
            logo_color='linear-gradient(135deg,#003087,#0052CC)',
            industry='Commercial Banking',
            headquarters='Nairobi, Kenya',
            founded=1896,
            website='https://kcbgroup.com',
            description='Kenya Commercial Bank Group is the largest commercial bank in Kenya by assets, with operations across East Africa.',
            size='10,000+ employees'
        ),
        Company(
            name='Equity Bank',
            slug='equity-bank',
            logo_initials='EQB',
            logo_color='linear-gradient(135deg,#C8102E,#8B0000)',
            industry='Commercial Banking',
            headquarters='Nairobi, Kenya',
            founded=1984,
            website='https://equitygroupholdings.com',
            description='Equity Group Holdings is a financial services conglomerate with banking operations across Africa, known for financial inclusion.',
            size='5,000-10,000 employees'
        ),
        Company(
            name='NCBA Bank',
            slug='ncba-bank',
            logo_initials='NCBA',
            logo_color='linear-gradient(135deg,#1A5276,#2E86C1)',
            industry='Commercial Banking',
            headquarters='Nairobi, Kenya',
            founded=2019,
            website='https://ke.ncbagroup.com',
            description='NCBA Bank Kenya was formed from the merger of NIC Bank and Commercial Bank of Africa in 2019.',
            size='2,000-5,000 employees'
        ),
        Company(
            name='Stanbic Bank Kenya',
            slug='stanbic-bank',
            logo_initials='SBK',
            logo_color='linear-gradient(135deg,#003366,#004A99)',
            industry='Commercial Banking',
            headquarters='Nairobi, Kenya',
            founded=1992,
            website='https://www.stanbicbank.co.ke',
            description='Stanbic Bank Kenya is a subsidiary of Standard Bank Group, Africa\'s largest bank by assets.',
            size='500-1,000 employees'
        ),
        Company(
            name='Co-operative Bank',
            slug='co-operative-bank',
            logo_initials='COP',
            logo_color='linear-gradient(135deg,#006400,#228B22)',
            industry='Commercial Banking',
            headquarters='Nairobi, Kenya',
            founded=1965,
            website='https://www.co-opbank.co.ke',
            description='Co-operative Bank of Kenya is owned by co-operative societies and serves as a key financial partner for Kenya\'s cooperative movement.',
            size='5,000-10,000 employees'
        ),
        Company(
            name='Absa Bank Kenya',
            slug='absa-bank',
            logo_initials='ABK',
            logo_color='linear-gradient(135deg,#CC0000,#990000)',
            industry='Commercial Banking',
            headquarters='Nairobi, Kenya',
            founded=1916,
            website='https://www.absa.co.ke',
            description='Absa Bank Kenya, formerly Barclays Bank of Kenya, is one of the oldest banks in the country with a strong retail banking presence.',
            size='2,000-5,000 employees'
        ),
        Company(
            name='I&M Bank',
            slug='im-bank',
            logo_initials='I&M',
            logo_color='linear-gradient(135deg,#8B0000,#B22222)',
            industry='Commercial Banking',
            headquarters='Nairobi, Kenya',
            founded=1974,
            website='https://www.imbank.com',
            description='I&M Bank is a leading regional bank with operations in Kenya, Rwanda, Tanzania, Uganda and Mauritius.',
            size='1,000-2,000 employees'
        ),
        Company(
            name='DTB Bank',
            slug='dtb-bank',
            logo_initials='DTB',
            logo_color='linear-gradient(135deg,#2C3E50,#4A6278)',
            industry='Commercial Banking',
            headquarters='Nairobi, Kenya',
            founded=1955,
            website='https://dtbbank.com',
            description='Diamond Trust Bank Group operates in Kenya, Uganda, Tanzania and Burundi, known for strong SME banking.',
            size='1,000-2,000 employees'
        ),
        Company(
            name='Family Bank',
            slug='family-bank',
            logo_initials='FAM',
            logo_color='linear-gradient(135deg,#FF6600,#CC5200)',
            industry='Commercial Banking',
            headquarters='Nairobi, Kenya',
            founded=1984,
            website='https://www.familybank.co.ke',
            description='Family Bank is a mid-tier Kenyan bank focused on retail and SME banking with a strong upcountry presence.',
            size='1,000-2,000 employees'
        ),
        Company(
            name='HF Group',
            slug='hf-group',
            logo_initials='HFG',
            logo_color='linear-gradient(135deg,#4B0082,#6A0DAD)',
            industry='Mortgage & Housing Finance',
            headquarters='Nairobi, Kenya',
            founded=1965,
            website='https://www.hfgroup.co.ke',
            description='Housing Finance Group is Kenya\'s leading mortgage and housing finance provider.',
            size='500-1,000 employees'
        ),
    ]

    db.session.add_all(companies)
    db.session.commit()

    # Create anonymous seed user
    seed_user = User(
        email_hash=User.hash_email('seed@machowazi.co.ke'),
        display_token=User.generate_token(),
        is_verified=True
    )
    seed_user.set_password('seedpassword123!')
    db.session.add(seed_user)
    db.session.commit()

    kcb = Company.query.filter_by(slug='kcb-group').first()
    equity = Company.query.filter_by(slug='equity-bank').first()
    ncba = Company.query.filter_by(slug='ncba-bank').first()
    stanbic = Company.query.filter_by(slug='stanbic-bank').first()
    coop = Company.query.filter_by(slug='co-operative-bank').first()
    absa = Company.query.filter_by(slug='absa-bank').first()

    reviews = [
        Review(
            company_id=kcb.id, user_id=seed_user.id,
            job_title='Senior Relationship Manager', employment_status='current',
            years_at_company=4, location='Nairobi',
            overall_rating=3.5, culture_rating=3.0, management_rating=3.0,
            worklife_rating=2.5, pay_rating=3.5, growth_rating=3.5,
            headline='Good stability, slow growth unless you know someone',
            pros='Excellent medical cover for entire family. Pension contributions are solid. Job security is unmatched — very hard to get fired. Brand name opens doors outside.',
            cons='Promotions are entirely political. Work-life balance at branch level is terrible. Core banking system is ancient. Management communication is top-down and opaque.',
            advice_to_management='Introduce a transparent promotion criteria. Employees are leaving because they cannot see a clear path forward.',
            would_recommend=True, ceo_approval=True, is_approved=True
        ),
        Review(
            company_id=kcb.id, user_id=seed_user.id,
            job_title='Branch Manager', employment_status='former',
            years_at_company=6, location='Mombasa',
            overall_rating=3.0, culture_rating=2.5, management_rating=2.5,
            worklife_rating=2.0, pay_rating=3.5, growth_rating=3.0,
            headline='Great pay, exhausting culture',
            pros='Salary is above industry average at manager level. Company car allowance is good. Training programs exist even if uptake is low.',
            cons='Branch managers work 7 days a week effectively. Customer complaints land on your personal phone at midnight. Head office targets are unrealistic.',
            advice_to_management='Branch managers need weekends. The burnout rate is destroying institutional knowledge.',
            would_recommend=False, ceo_approval=False, is_approved=True
        ),
        Review(
            company_id=equity.id, user_id=seed_user.id,
            job_title='Credit Analyst', employment_status='current',
            years_at_company=2, location='Nairobi',
            overall_rating=4.2, culture_rating=4.5, management_rating=4.0,
            worklife_rating=3.5, pay_rating=3.0, growth_rating=4.5,
            headline='Best place to start a banking career in Kenya',
            pros='The mission of financial inclusion feels genuine from the inside. Management is accessible — I have spoken to the CEO. Culture of innovation is real. Learning opportunities are everywhere.',
            cons='Pay is below industry average, especially for tech and analyst roles. Customer pressure at branches is extreme. Targets are very aggressive.',
            advice_to_management='Increase salaries for mid-level staff. You are losing good people to Stanbic and standard chartered for 30% more pay.',
            would_recommend=True, ceo_approval=True, is_approved=True
        ),
        Review(
            company_id=equity.id, user_id=seed_user.id,
            job_title='Digital Banking Officer', employment_status='current',
            years_at_company=1.5, location='Nairobi',
            overall_rating=4.0, culture_rating=4.5, management_rating=3.5,
            worklife_rating=3.5, pay_rating=3.0, growth_rating=4.0,
            headline='Purpose-driven culture with below-market pay',
            pros='You genuinely feel the work matters. The digital team is young, smart, and energetic. Management believes in empowering junior staff to lead projects.',
            cons='Salary is a problem. I did the math — Safaricom pays 40% more for the same role. Equity relies too much on the mission to compensate for market salary gaps.',
            advice_to_management='Run a market salary benchmarking exercise and publish results internally. Transparency would build trust.',
            would_recommend=True, ceo_approval=True, is_approved=True
        ),
        Review(
            company_id=ncba.id, user_id=seed_user.id,
            job_title='Software Developer', employment_status='former',
            years_at_company=1.5, location='Nairobi',
            overall_rating=3.2, culture_rating=2.5, management_rating=2.5,
            worklife_rating=2.5, pay_rating=4.0, growth_rating=3.0,
            headline='Good tech environment, toxic post-merger culture',
            pros='Best technology environment in Kenyan banking by far. Loop app team is genuinely talented. Salary for tech roles is competitive. Office is modern and comfortable.',
            cons='The NIC vs CBA cultural divide is still very visible 3 years post-merger. Two tribes exist and they fight for budget. Communication from leadership is inconsistent and causes anxiety.',
            advice_to_management='Invest seriously in culture integration. The merger was financial but the people never merged.',
            would_recommend=False, ceo_approval=False, is_approved=True
        ),
        Review(
            company_id=stanbic.id, user_id=seed_user.id,
            job_title='Relationship Manager Corporate', employment_status='current',
            years_at_company=3, location='Nairobi',
            overall_rating=4.4, culture_rating=4.0, management_rating=4.5,
            worklife_rating=4.0, pay_rating=5.0, growth_rating=4.5,
            headline='Best paying bank in Kenya. Full stop.',
            pros='Salary is the best in Kenyan banking at every level. Learning and development budget is real and generous. Pan-African exposure opens incredible doors. Management is professional and respectful.',
            cons='Smaller bank means fewer internal opportunities — the org chart is flat. Can feel slow-moving compared to larger banks. Some bureaucracy from Standard Bank Group head office.',
            advice_to_management='Create more leadership pathways for junior staff. The flat structure means people leave for bigger banks after they plateau.',
            would_recommend=True, ceo_approval=True, is_approved=True
        ),
        Review(
            company_id=coop.id, user_id=seed_user.id,
            job_title='Customer Service Officer', employment_status='current',
            years_at_company=5, location='Nakuru',
            overall_rating=3.5, culture_rating=3.5, management_rating=3.0,
            worklife_rating=3.5, pay_rating=2.5, growth_rating=2.5,
            headline='Stable and decent, not exciting',
            pros='Very stable employment — the cooperative ownership structure means politics are minimal. SACCO membership benefits are genuinely good. Management is human and fair.',
            cons='Salary growth is very slow — annual increments are tiny. Promotions take 5-7 years minimum. Technology is behind the tier-1 banks significantly.',
            advice_to_management='Accelerate digital transformation or risk losing market share to mobile-first competitors.',
            would_recommend=True, ceo_approval=True, is_approved=True
        ),
        Review(
            company_id=absa.id, user_id=seed_user.id,
            job_title='Risk and Compliance Officer', employment_status='current',
            years_at_company=2, location='Nairobi',
            overall_rating=3.9, culture_rating=4.0, management_rating=3.5,
            worklife_rating=3.5, pay_rating=4.0, growth_rating=3.5,
            headline='Culture improved dramatically after rebrand',
            pros='The Barclays to Absa rebrand genuinely changed the culture for better. More Kenyan leadership now. Pay is competitive. Risk and compliance team is professional and well-resourced.',
            cons='Some anxiety remains around long-term direction. Talent retention is a challenge — people leave for Stanbic and Standard Chartered. Restructuring happens too frequently.',
            advice_to_management='Communicate the 5-year strategy clearly to all staff levels. Uncertainty is the main reason people leave.',
            would_recommend=True, ceo_approval=True, is_approved=True
        ),
    ]

    db.session.add_all(reviews)
    db.session.commit()

    salaries = [
        Salary(company_id=kcb.id, user_id=seed_user.id, job_title='Branch Manager',
               job_level='Manager', department='Retail Banking',
               monthly_gross=185000, monthly_net=138000, allowances=25000,
               bonus_annual=180000, years_experience=8, is_approved=True),
        Salary(company_id=kcb.id, user_id=seed_user.id, job_title='Relationship Manager',
               job_level='Mid', department='Corporate Banking',
               monthly_gross=120000, monthly_net=92000, allowances=15000,
               bonus_annual=120000, years_experience=4, is_approved=True),
        Salary(company_id=kcb.id, user_id=seed_user.id, job_title='Customer Service Officer',
               job_level='Junior', department='Retail Banking',
               monthly_gross=55000, monthly_net=44000, allowances=5000,
               bonus_annual=0, years_experience=1, is_approved=True),
        Salary(company_id=equity.id, user_id=seed_user.id, job_title='Credit Analyst',
               job_level='Mid', department='Credit',
               monthly_gross=95000, monthly_net=74000, allowances=10000,
               bonus_annual=60000, years_experience=3, is_approved=True),
        Salary(company_id=equity.id, user_id=seed_user.id, job_title='Digital Banking Officer',
               job_level='Mid', department='Digital',
               monthly_gross=90000, monthly_net=70000, allowances=8000,
               bonus_annual=50000, years_experience=2, is_approved=True),
        Salary(company_id=ncba.id, user_id=seed_user.id, job_title='Software Developer',
               job_level='Mid', department='Technology',
               monthly_gross=155000, monthly_net=115000, allowances=12000,
               bonus_annual=100000, years_experience=4, is_approved=True),
        Salary(company_id=stanbic.id, user_id=seed_user.id, job_title='Relationship Manager Corporate',
               job_level='Senior', department='Corporate Banking',
               monthly_gross=210000, monthly_net=155000, allowances=30000,
               bonus_annual=300000, years_experience=6, is_approved=True),
        Salary(company_id=stanbic.id, user_id=seed_user.id, job_title='Risk Manager',
               job_level='Manager', department='Risk',
               monthly_gross=280000, monthly_net=205000, allowances=35000,
               bonus_annual=350000, years_experience=9, is_approved=True),
        Salary(company_id=coop.id, user_id=seed_user.id, job_title='Customer Service Officer',
               job_level='Junior', department='Retail',
               monthly_gross=52000, monthly_net=42000, allowances=4000,
               bonus_annual=0, years_experience=2, is_approved=True),
        Salary(company_id=absa.id, user_id=seed_user.id, job_title='Risk and Compliance Officer',
               job_level='Mid', department='Risk & Compliance',
               monthly_gross=175000, monthly_net=130000, allowances=20000,
               bonus_annual=150000, years_experience=5, is_approved=True),
    ]

    db.session.add_all(salaries)

    interviews = [
        Interview(
            company_id=kcb.id, user_id=seed_user.id,
            job_title='Graduate Management Trainee',
            experience='positive', got_offer='yes',
            how_applied='online', difficulty=3,
            process_description='Three round process. First was an online SHL aptitude test — verbal, numerical, and situational judgment. Study for this, it is timed strictly. Second round was a panel interview with HR and line manager, competency-based using STAR format. Third was a final interview with a senior director focused on business acumen and current affairs in banking.',
            questions_asked='Why banking? Where do you see yourself in 5 years? Tell me about a time you handled a difficult customer. What do you know about KCB\'s East African strategy?',
            tips='Research KCB\'s current expansion strategy especially Rwanda and DRC. Know your STAR stories cold. Dress formally — they are conservative.',
            duration_weeks=6, num_rounds=3, is_approved=True
        ),
        Interview(
            company_id=stanbic.id, user_id=seed_user.id,
            job_title='Risk and Compliance Officer',
            experience='positive', got_offer='yes',
            how_applied='headhunter', difficulty=4,
            process_description='Headhunted via LinkedIn by a recruiter. Very professional process throughout. Two structured behavioral interviews plus a psychometric assessment through Hogan. Both interviews were with senior managers who knew exactly what they were looking for. Felt respected throughout — they called at the promised times and gave clear feedback at each stage.',
            questions_asked='Describe your approach to building a compliance framework from scratch. Tell me about a time you escalated a risk issue against management preference. How do you stay current with CBK regulatory changes?',
            tips='Know Standard Bank Group\'s Africa footprint and strategy. They want regional thinkers. Have a strong view on CBK regulation updates — they test this.',
            duration_weeks=4, num_rounds=2, is_approved=True
        ),
        Interview(
            company_id=equity.id, user_id=seed_user.id,
            job_title='Digital Banking Analyst',
            experience='positive', got_offer='yes',
            how_applied='online', difficulty=3,
            process_description='Applied through their careers portal. HR screening call first — 20 minutes, basic background and motivation questions. Then a technical test sent via email — Excel and basic SQL. Final panel with the Digital team lead and HR Business Partner. Very relaxed and focused on potential more than experience.',
            questions_asked='What excites you about digital financial inclusion? Walk me through a data analysis project. What banking apps do you admire and why?',
            tips='They care deeply about the mission. Show genuine interest in financial inclusion not just technology. Know the M-Pesa ecosystem deeply.',
            duration_weeks=3, num_rounds=3, is_approved=True
        ),
    ]

    db.session.add_all(interviews)
    db.session.commit()

    print('✅ Macho Wazi seed data loaded successfully.')
