from sqlalchemy import Table, Column, Integer, Float, String
from flask_sqlalchemy_core import FlaskSQLAlchemy
from sqlalchemy.sql.expression import null
from colixpress_api import metadata, db

clients = Table('client', metadata,
    Column('id_client', Integer, primary_key=True),
    Column('id_ville', Integer, nullable=False),
    Column('nom_client', String(30), nullable=False),
    Column('prenom_client', String(30), nullable=False),
    Column('adresse_client', String(200), nullable=False),
    Column('login_client', String(200), nullable=False),
    Column('mdp_client', String(200), nullable= False)
)

fournisseurs = Table('fournisseur', metadata,
    Column('id_fournisseur', Integer, primary_key=True),
    Column('id_ville', Integer, nullable=False),
    Column('ref_fournisseur', String(15), nullable=False),
    Column('nom_fournisseur', String(100), nullable=False),
    Column('adresse_fournisseur', String(100), nullable=False),
    Column('activite', String(50), nullable= False),
    Column('login_fournisseur', String(100), nullable= False),
    Column('mdp_fournisseur', String(256), nullable= False)
)

villes = Table('ville', metadata,
    Column('id_ville', Integer, primary_key=True, nullable=False),
    Column('id_pld', Integer, nullable=False),
    Column('nom_ville', String(100), nullable=False),
    Column('cp', String(5), nullable=False),
    Column('insee_code', String(5), nullable=False),
    Column('gps_lat', Float, nullable=False),
    Column('gps_lng', Float, nullable=False)
)

suivicolis = Table('suivicolis', metadata,
    Column('id_colis', Integer, primary_key=True),
    Column('ref_colis', String(25), nullable=False),
    Column('type_colis', String(15), nullable=False),
    Column('id_fournisseur', Integer, nullable=False),
    Column('id_client', Integer, nullable=False),
    Column('id_pld_depart', Integer, nullable=False),
    Column('id_pld_arrive', Integer, nullable=False),
    Column('etat_colis', Integer, nullable=False),
    Column('date_depot', String(16), nullable=False),
    Column('date_modif', String(16), nullable=False)
)

statuscolis = Table('statuscolis', metadata,
    Column('id_colis', Integer, nullable=False),
    Column('ref_colis', String(25), nullable=False),
    Column('id_pld_actuel', Integer, nullable=False),
    Column('id_pld_direction', Integer, nullable=True),
    Column('id_plr_direction', Integer, nullable=True),
)

pld = Table('pld', metadata,
    Column('id_pld', Integer, nullable=False),
    Column('id_plr', Integer, nullable=False),
    Column('ref_pld', String(6), nullable=False),
    Column('nom_pld', String(50), nullable=False),
)