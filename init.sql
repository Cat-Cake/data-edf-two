-- Create a new database
CREATE DATABASE mydatabase;

-- Create a user and grant privileges
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;

-- Optional: Create tables or insert data
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
INSERT INTO users (name) VALUES ('Alice'), ('Bob');

CREATE TABLE IF NOT EXISTS indisponibilite_edf (
    id BIGSERIAL PRIMARY KEY,

    identifiant VARCHAR(100) UNIQUE NOT NULL,
    source_id VARCHAR(100) UNIQUE,

    perimetre_spatial TEXT,
    perimetre_juridique TEXT,

    date_de_debut TIMESTAMPTZ NOT NULL,
    date_de_fin TIMESTAMPTZ NOT NULL,
    date_de_publication TIMESTAMPTZ,

    cause TEXT,
    type VARCHAR(100),
    nom VARCHAR(255) NOT NULL,
    filiere VARCHAR(100),
    status VARCHAR(50),

    puissance_maximale_mw NUMERIC(10,2) NOT NULL,
    puissance_disponible_mw NUMERIC(10,2) NOT NULL,

    numero_de_version INTEGER,

    centrale VARCHAR(200),
    tranche VARCHAR(50),
    annee INTEGER,

    production_estimee_mw NUMERIC(10,2),
    indisponibilite_mw NUMERIC(10,2),
    taux_indisponibilite NUMERIC(8,4),

    duree_heures NUMERIC(12,2),

    production_zero BOOLEAN,
    indisponibilite_avec_production BOOLEAN,

    created_at TIMESTAMPTZ DEFAULT NOW()
    updated_at TIMESTAMPTZ DEFAULT NOW()
);