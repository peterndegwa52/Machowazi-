#!/usr/bin/env python3
"""
Run this script once after deployment to create your admin account.

Usage:
    python create_admin.py your@email.com yourpassword

This script creates an admin user. Keep credentials secure.
"""
import sys
from app import create_app, db
from app.models import User


def create_admin(email, password):
    app = create_app()
    with app.app_context():
        email_hash = User.hash_email(email)
        existing = User.query.filter_by(email_hash=email_hash).first()

        if existing:
            existing.is_admin = True
            existing.is_verified = True
            db.session.commit()
            print(f'✅ Existing user promoted to admin.')
        else:
            user = User(
                email_hash=email_hash,
                display_token=User.generate_token(),
                is_verified=True,
                is_admin=True
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f'✅ Admin account created successfully.')
            print(f'   Login with: {email}')
            print(f'   Admin panel: /admin')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python create_admin.py <email> <password>')
        sys.exit(1)

    email    = sys.argv[1]
    password = sys.argv[2]

    if len(password) < 8:
        print('❌ Password must be at least 8 characters.')
        sys.exit(1)

    create_admin(email, password)
