# Configuration PostgreSQL pour la Caisse du GMMG

## Variables d'environnement requises

```bash
# .env ou à ajouter au système

POSTGRES_DB=caisse_gmmg
POSTGRES_USER=postgres
POSTGRES_PASSWORD=votre_mot_de_passe
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

## Étapes de setup PostgreSQL

### 1. Installer PostgreSQL
- Windows: https://www.postgresql.org/download/windows/
- Ou utiliser WSL2: `sudo apt-get install postgresql postgresql-contrib`

### 2. Créer la base de données
```sql
psql -U postgres
CREATE DATABASE caisse_gmmg;
CREATE USER caisse_user WITH PASSWORD 'caisse_password';
ALTER ROLE caisse_user SET client_encoding TO 'utf8';
ALTER ROLE caisse_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE caisse_user SET default_transaction_deferrable TO on;
ALTER ROLE caisse_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE caisse_gmmg TO caisse_user;
\q
```

### 3. Installer le driver PostgreSQL Python
```bash
pip install psycopg2-binary
```

### 4. Faire les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer un superadmin
```bash
python manage.py createsuperuser
```
