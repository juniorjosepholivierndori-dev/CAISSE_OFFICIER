#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_user(
        username='admin',
        email='admin@gmmg.ci',
        password='Admin123!',
        first_name='Admin',
        last_name='GMMG',
        role='ADMIN'
    )
    print('✓ Compte Admin créé')

# Trésorier
if not User.objects.filter(username='tresorier').exists():
    User.objects.create_user(
        username='tresorier',
        email='tresorier@gmmg.ci',
        password='Tresorier123',
        first_name='Jean',
        last_name='Trésorier',
        role='TRESORIER'
    )
    print('✓ Compte Trésorier créé')

# Officier
if not User.objects.filter(username='officier').exists():
    User.objects.create_user(
        username='officier',
        email='officier@gmmg.ci',
        password='Officier123!',
        first_name='Paul',
        last_name='Officier',
        role='OFFICIER'
    )
    print('✓ Compte Officier créé')

print('\n✓ Comptes créés avec succès')
print(f'\nTotal utilisateurs: {User.objects.count()}')
