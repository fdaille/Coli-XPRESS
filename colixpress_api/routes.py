from flask import render_template, request, session, flash, redirect, url_for, jsonify, abort, make_response, g
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import select
from sqlalchemy.engine import result
from colixpress_api import app, db, auth
from colixpress_api.tables import fournisseurs, villes, suivicolis, clients, pld, statuscolis
from werkzeug.security import generate_password_hash, check_password_hash
import requests, json, re, random, datetime

@app.route("/")
@app.route("/home/")
def home():
    return render_template("index.html", title="Accueil")

@auth.error_handler
def unauthorized(e):
    return render_template('error401.html', title='401'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html', title='404'), 404

@app.errorhandler(400)
def page_not_found(e):
    return render_template('error400.html', title='400'), 400

@app.route('/api/clients', methods=['GET'])
def get_clients():
  record_clients = [] 
  with db.connect() as connexion:
    response = connexion.execute(select([clients])).fetchall()
    for row in response:
      client = {}
      for key, value in row.items():
        client[key] = value
      record_clients.append(client)
  return jsonify(record_clients)

@app.route('/api/clients/<int:id>', methods=['GET'])
def get_userByLogin(id):
    json_client = None
    with db.connect() as connexion:
        stat = select([clients]).where(clients.c.id_client==id)
        record_client = connexion.execute(stat).first()
        json_user = {}
        if not record_client:
            abort(404)
        for key, value in record_client.items():
            json_client[key] = value
        return jsonify(json_client)

@app.route('/api/clients/<string:login>', methods=['GET'])
def get_clientByLogin(login):
    json_client = None
    with db.connect() as connexion:
        stat = select([clients]).where(clients.c.login_client==login)
        record_client = connexion.execute(stat).first()
        json_client = {}
        if not record_client:
            abort(404)
        for key, value in record_client.items():
            json_client[key] = value
    return jsonify(json_client)

@app.route('/api/clients/<string:login>', methods=['PUT'])
def edit_Clients(login):
    datas = request.get_json()
    if not datas.get('login_client'):
        abort(400)
    with db.connect() as connexion:
        record_client = connexion.execute(select([clients]).where(clients.c.login_client==login)).first()
        if not record_client or record_client.login_client != datas.get('login_client'):
            abort(412)
        result = connexion.execute(clients.update().where(clients.c.login_client==login), datas)
    response = {"uri": url_for('get_clientByLogin', login=login, _external=True), 'login': datas.get('login_client')}
    return (jsonify(response), 201)

@app.route('/api/fournisseurs', methods=['GET'])
def get_fournisseurs():
  record_fournisseurs = [] 
  with db.connect() as connexion:
    response = connexion.execute(select([fournisseurs])).fetchall()
    for row in response:
      fournisseur = {}
      for key, value in row.items():
        fournisseur[key] = value
      record_fournisseurs.append(fournisseur)
  return jsonify(record_fournisseurs)

@app.route('/api/fournisseurs/<string:login>', methods=['GET'])
def get_fournisseurByLogin(login):
    json_fournisseur = None
    with db.connect() as connexion:
        stat = select([fournisseurs]).where(fournisseurs.c.login_fournisseur==login)
        record_fournisseur = connexion.execute(stat).first()
        json_fournisseur = {}
        if not record_fournisseur:
            abort(404)
        for key, value in record_fournisseur.items():
            json_fournisseur[key] = value
    return jsonify(json_fournisseur)

@app.route('/api/fournisseurs/<string:ref>', methods=['GET'])
def get_fournisseurByRef(ref):
    json_fournisseurRef = None
    with db.connect() as connexion:
        statRef = select([fournisseurs]).where(fournisseurs.c.ref_fournisseur==ref)
        record_fournisseurRef = connexion.execute(statRef).first()
        json_fournisseurRef = {}
        if not record_fournisseurRef:
            abort(404)
        for key, value in record_fournisseurRef.items():
            json_fournisseurRef[key] = value
    return jsonify(json_fournisseurRef)

@app.route('/api/fournisseurs/<string:login>', methods=['PUT'])
def edit_Fournisseur(login):
    datas = request.get_json()
    if not datas.get('login_fournisseur') or not datas.get('mdp_fournisseur'):
        abort(400)
    with db.connect() as connexion:
        record_fournisseur = connexion.execute(select([fournisseurs]).where(fournisseurs.c.login_fournisseur==login)).first()
        if not record_fournisseur or record_fournisseur.login_fournisseur != datas.get('login_fournisseur'):
            abort(412)
        result = connexion.execute(fournisseurs.update().where(fournisseurs.c.login_fournisseur==login), datas)
    response = {"uri": url_for('get_fournisseurByLogin', login=login, _external=True), 'login': datas.get('login_fournisseur'), "mdp": datas.get('mdp_fournisseur')}
    return (jsonify(response), 201)

@app.route('/api/villes', methods=['GET'])
def get_villes():
  record_villes = [] 
  with db.connect() as connexion:
    response = connexion.execute(select([villes])).fetchall()
    for row in response:
      ville = {}
      for key, value in row.items():
        ville[key] = value
      record_villes.append(ville)
  return jsonify(record_villes)

@app.route('/api/villes/<string:villeName>', methods=['GET'])
def get_villeByNom(villeName):
    json_ville = None
    with db.connect() as connexion:
        stat = select([villes]).where(villes.c.nom_ville==villeName)
        record_ville = connexion.execute(stat).first()
        json_ville = {}
        if not record_ville:
            abort(404)
        for key, value in record_ville.items():
            json_ville[key] = value
    return jsonify(json_ville)

@app.route('/api/villes/<int:villeId>', methods=['GET'])
def get_villeById(villeId):
    json_ville = None
    with db.connect() as connexion:
        stat = select([villes]).where(villes.c.id_ville==villeId)
        record_ville = connexion.execute(stat).first()
        json_ville = {}
        if not record_ville:
            abort(404)
        for key, value in record_ville.items():
            json_ville[key] = value
        return jsonify(json_ville)

@app.route('/api/suivicolis', methods=['GET'])
def get_suivicolis():
    record_suivicolis = [] 
    with db.connect() as connexion:
        response = connexion.execute(select([suivicolis])).fetchall()
        for row in response:
            suivicoli = {}
            for key, value in row.items():
                suivicoli[key] = value
            record_suivicolis.append(suivicoli)
    return jsonify(record_suivicolis)

@app.route('/api/suivicolis/<string:refColis>', methods=['GET'])
def get_suivicolisByRef(refColis):
    json_suivicolis = None
    with db.connect() as connexion:
        stat = select([suivicolis]).where(suivicolis.c.ref_colis==refColis)
        record_suivicolis = connexion.execute(stat).first()
        json_suivicolis = {}
        if not record_suivicolis:
            abort(404)
        for key, value in record_suivicolis.items():
            json_suivicolis[key] = value
    return jsonify(json_suivicolis)

@app.route('/api/pld/<int:pldId>', methods=['GET'])
def get_pldById(pldId):
    json_pld = None
    with db.connect() as connexion:
        stat = select([pld]).where(pld.c.id_pld==pldId)
        record_pld = connexion.execute(stat).first()
        json_pld = {}
        if not record_pld:
            abort(404)
        for key, value in record_pld.items():
            json_pld[key] = value
        return jsonify(json_pld)

@app.route('/api/statuscolis', methods=['GET'])
def get_statuscolis():
  record_statuscolis = [] 
  with db.connect() as connexion:
    response = connexion.execute(select([statuscolis])).fetchall()
    for row in response:
      statuscoli = {}
      for key, value in row.items():
        statuscoli[key] = value
      record_statuscolis.append(statuscoli)
  return jsonify(record_statuscolis)

@app.route('/api/statuscolis/<string:statuscolisREF>', methods=['GET'])
def get_statuscolisByRef(statuscolisREF):
    json_statuscolis = None
    with db.connect() as connexion:
        stat = select([statuscolis]).where(statuscolis.c.ref_colis==statuscolisREF)
        record_statuscolis = connexion.execute(stat).first()
        json_statuscolis = {}
        if not record_statuscolis:
            abort(404)
        for key, value in record_statuscolis.items():
            json_statuscolis[key] = value
    return jsonify(json_statuscolis)

@app.route("/suivi/", methods=['GET'])
def suivi():
    tracking_code = request.args.get('tracking_code')
    return render_template("suivi.html", title="Suivi", tracking_code=tracking_code)

@app.route("/envoi/", methods=['GET', 'POST'])
def envoi():
    if request.method == 'POST' and request.form['type_colis'] and request.form['nom_client'] and request.form['prenom_client'] and request.form['adresse_client'] and request.form['ville_client'] and request.form['login_client']:
        reponseVille = requests.get(f"http://127.0.0.1:5550/api/villes/{request.form['ville_client']}")
        validEmail = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if reponseVille.status_code >= 400:
            flash("Ville inconnue. Revoyez la syntaxe.", 'error')
        elif (re.search(validEmail, request.form['login_client'])):
            villeInfos = json.loads(reponseVille.text)
            with db.connect() as connexion:
                if connexion.execute(select([clients]).where(clients.c.login_client==request.form['login_client'])).first():
                    record_client = {
                        'nom_client': request.form['nom_client'],
                        'prenom_client': request.form['prenom_client'],
                        'adresse_client': request.form['adresse_client'],
                        'id_ville': villeInfos['id_ville'],
                        'login_client': request.form['login_client']
                    }
                    result = requests.put(f"http://127.0.0.1:5550/api/clients/{record_client['login_client']}", json=record_client)
                else:
                    record_client = {
                        'nom_client': request.form['nom_client'],
                        'prenom_client': request.form['prenom_client'],
                        'adresse_client': request.form['adresse_client'],
                        'id_ville': villeInfos['id_ville'],
                        'login_client': request.form['login_client']
                    }
                    result = connexion.execute(clients.insert(), record_client)
            getIDClient = requests.get(f"http://127.0.0.1:5550/api/clients/{request.form['login_client']}")
            clientInfos = json.loads(getIDClient.text)
            getIDFournisseur = requests.get(f"http://127.0.0.1:5550/api/fournisseurs/{session['user']['login']}")
            fournisseurInfos = json.loads(getIDFournisseur.text)
            refColis = str(((request.form['type_colis'][0:3]).upper())+str(session['user']['id_pld'])+str(villeInfos['id_pld'])+str("%04d" % fournisseurInfos['id_fournisseur'])+str("%04d" % clientInfos['id_client'])+str("%04d" % random.randint(0,99999))+"FR")
            dateTime = (datetime.datetime.now()).strftime('%d-%m-%Y %H:%M')
            record_colis = {
                'ref_colis': refColis,
                'type_colis': request.form['type_colis'],
                'id_fournisseur': fournisseurInfos['id_fournisseur'],
                'id_client': clientInfos['id_client'],
                'id_pld_depart': session['user']['id_pld'],
                'id_pld_arrive': villeInfos['id_pld'],
                'etat_colis': 0,
                'date_depot': dateTime,
                'date_modif': dateTime
            }
            with db.connect() as connexion:
                result = connexion.execute(suivicolis.insert(), record_colis)
            getIDColis = requests.get(f"http://127.0.0.1:5550/api/suivicolis/{refColis}")
            colisInfos = json.loads(getIDColis.text)
            getIDPldDepart = requests.get(f"http://127.0.0.1:5550/api/pld/{record_colis['id_pld_depart']}")
            pldInfosDep = json.loads(getIDPldDepart.text)
            getIDPldArrive = requests.get(f"http://127.0.0.1:5550/api/pld/{record_colis['id_pld_arrive']}")
            pldInfosArr = json.loads(getIDPldArrive.text)
            if record_colis['id_pld_depart'] == record_colis['id_pld_arrive']:
                record_statuscolis = {
                    'id_colis': colisInfos['id_colis'],
                    'ref_colis': refColis,
                    'id_pld_actuel': record_colis['id_pld_depart'],
                    'id_pld_direction': record_colis['id_pld_arrive']
                }
            else:
                record_statuscolis = {
                    'id_colis': colisInfos['id_colis'],
                    'ref_colis': refColis,
                    'id_pld_actuel': record_colis['id_pld_depart'],
                    'id_plr_direction': pldInfosDep['id_plr']
                }
            with db.connect() as connexion:
                result = connexion.execute(statuscolis.insert(), record_statuscolis)
        else:
            flash("L'adresse email entrée est incorrecte.", 'error')
    elif request.method == 'POST':
        flash("Des champs ne sont pas saisis.", 'error')
    return render_template("envoi.html", title="Envoyer un colis")

@app.route("/connexion/", methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST' and request.form['login-adresse-mail'] and request.form['login-mdp'] :
        user={
            "login": request.form['login-adresse-mail'], 
            "passwd": request.form['login-mdp']
            }
        #print(user)    #Pour vérifier l'entrée
        authent = requests.auth.HTTPBasicAuth(user['login'], user['passwd'])
        reponse = requests.get(f"http://127.0.0.1:5550/api/fournisseurs/{user['login']}", auth=authent)
        if(reponse.status_code >= 400):
            flash("Certaines de vos informations sont incorrectes. Veuillez réessayer.", 'error')
        else:
            loggeduser = json.loads(reponse.text)
            reponseVille = requests.get(f"http://127.0.0.1:5550/api/villes/{loggeduser['id_ville']}")
            villeInfos = json.loads(reponseVille.text)
            if check_password_hash(loggeduser['mdp_fournisseur'], user['passwd']):
                session['user'] = {
                    "adresse": loggeduser['adresse_fournisseur'],
                    "activite": loggeduser['activite'],
                    "login": loggeduser['login_fournisseur'],
                    "id_user": loggeduser['id_fournisseur'],
                    "nom_user": loggeduser['nom_fournisseur'],
                    "prenom_user": loggeduser['ref_fournisseur'],
                    "id_ville": loggeduser['id_ville'],
                    "nom_ville": villeInfos['nom_ville'],
                    "ref_user": loggeduser['ref_fournisseur'],
                    "insee_code": villeInfos['insee_code'],
                    'id_pld': villeInfos['id_pld']
                }
                status = "logged"
                return redirect(url_for('profil'))
            else:
                flash("Certaines de vos informations sont incorrectes. Veuillez réessayer.", 'error')
    elif request.method == 'POST':
        flash("Des champs ne sont pas saisis.", 'error')
    return render_template("connexion.html", title="Se connecter")

@app.route("/inscription/")
def inscription():
    return render_template("inscription.html", title="S'inscrire")

@app.route("/inscription/particulier/", methods=['GET', 'POST'])
def inscription_particulier():
    if request.method == 'POST' and request.form['nom_fournisseur'] and request.form['prenom_fournisseur'] and request.form['login_fournisseur'] and request.form['adresse_fournisseur'] and request.form['ville_fournisseur'] and request.form['mdp_fournisseur'] :
        reponseVille = requests.get(f"http://127.0.0.1:5550/api/villes/{request.form['ville_fournisseur']}")
        validEmail = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if(re.search(validEmail, request.form['login_fournisseur'])):
            if(reponseVille.status_code >= 400):
                flash("Ville inconnue. Revoyez la syntaxe.", 'error')
            else:
                villeInfos = json.loads(reponseVille.text)
                record_fournisseurs = {
                    'id_ville': villeInfos['id_ville'],
                    'ref_fournisseur': request.form['prenom_fournisseur'],
                    'nom_fournisseur': request.form['nom_fournisseur'],
                    'adresse_fournisseur': request.form['adresse_fournisseur'],
                    'activite': 'particulier',
                    'login_fournisseur': request.form['login_fournisseur'],
                    'mdp_fournisseur': request.form['mdp_fournisseur']
                }
                with db.connect() as connexion:
                    newUser = connexion.execute(select([fournisseurs]).where(fournisseurs.c.login_fournisseur==record_fournisseurs['login_fournisseur'])).first()
                    if newUser:
                        flash("Cette adresse email est déjà utilisée.", 'error')
                    else:
                        record_fournisseurs['mdp_fournisseur'] = generate_password_hash(record_fournisseurs['mdp_fournisseur'])
                        result = connexion.execute(fournisseurs.insert(), record_fournisseurs)
                        return render_template('index.html')
        else:
            flash("L'adresse email entrée est incorrecte.", 'error')
    elif request.method == 'POST':
        flash("Des champs ne sont pas saisis.", 'error')
    return render_template("inscription_particulier.html", title="S'inscrire")

@app.route("/inscription/professionnel/", methods=['GET', 'POST'])
def inscription_pro():
    if request.method == 'POST' and request.form['nom-entreprise'] and request.form['activite-entreprise'] and request.form['login-entreprise'] and request.form['adresse-entreprise'] and request.form['ville-entreprise'] and request.form['mdp-entreprise'] :
        reponseVille = requests.get(f"http://127.0.0.1:5550/api/villes/{request.form['ville-entreprise']}")
        validEmail = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if(re.search(validEmail, request.form['login-entreprise'])):
            if(reponseVille.status_code >= 400):
                flash("Ville inconnue. Revoyez la syntaxe.", 'error')
            else:
                refFournisseur = str((request.form['nom-entreprise'].replace(" ", ""))[0:4])+str(random.randint(0,9999))
                villeInfos = json.loads(reponseVille.text)
                record_fournisseurs = {
                    'id_ville': villeInfos['id_ville'],
                    'ref_fournisseur': refFournisseur,
                    'nom_fournisseur': request.form['nom-entreprise'],
                    'adresse_fournisseur': request.form['adresse-entreprise'],
                    'activite': request.form['activite-entreprise'],
                    'login_fournisseur': request.form['login-entreprise'],
                    'mdp_fournisseur': request.form['mdp-entreprise']
                }
                with db.connect() as connexion:
                    newUser = connexion.execute(select([fournisseurs]).where(fournisseurs.c.login_fournisseur==record_fournisseurs['login_fournisseur'])).first()
                    if newUser:
                        flash("Cette adresse email est déjà utilisée.", 'error')
                    else:
                        record_fournisseurs['mdp_fournisseur'] = generate_password_hash(record_fournisseurs['mdp_fournisseur'])
                        result = connexion.execute(fournisseurs.insert(), record_fournisseurs)
                        return render_template('index.html')
        else:
            flash("L'adresse email entrée est incorrecte.", 'error')
    elif request.method == 'POST':
        flash("Des champs ne sont pas saisis.", 'error')
    return render_template("inscription_pro.html", title="S'inscrire")

@app.route("/profil/", methods=['POST', 'GET'])
def profil():
    if session['user']['activite'] != 'particulier' and session['user']['activite'] != 'operateur':
        if request.method == 'POST' and request.form['nom_fournisseur'] and request.form['activite_fournisseur'] and request.form['login_fournisseur'] and request.form['adresse_fournisseur'] and request.form['mdp_fournisseur'] and request.form['ville_fournisseur']:
            mdpHASH = generate_password_hash(request.form['mdp_fournisseur'])
            reponseVille = requests.get(f"http://127.0.0.1:5550/api/villes/{request.form['ville_fournisseur']}")
            villeInfos = json.loads(reponseVille.text)
            datas = {
                'activite_fournisseur': request.form['activite_fournisseur'],
                'adresse_fournisseur': request.form['adresse_fournisseur'],
                'id_ville': villeInfos['id_ville'],
                'login_fournisseur': request.form['login_fournisseur'],
                'mdp_fournisseur': mdpHASH,
                'nom_fournisseur': request.form['nom_fournisseur']
            }
            username = requests.put(f"http://127.0.0.1:5550/api/fournisseurs/{datas['login_fournisseur']}", json=datas)
            if(username.status_code >= 400):
                flash("Une erreur a eu lieu, veuillez réessayer.", 'error')
            else:
                session.clear
                flash("Vos modifications ont été enregitrés, veuillez vous reconnecter.", 'error')
                return redirect(url_for('connexion'))
        elif request.method == 'POST':
            flash("Des champs ne sont pas saisis.", 'error')     
    else:
        if request.method == 'POST' and request.form['nom_fournisseur'] and request.form['prenom_fournisseur'] and request.form['login_fournisseur'] and request.form['adresse_fournisseur'] and request.form['ville_fournisseur'] and request.form['mdp_fournisseur']:
            mdpHASH = generate_password_hash(request.form['mdp_fournisseur'])
            reponseVille = requests.get(f"http://127.0.0.1:5550/api/villes/{request.form['ville_fournisseur']}")
            villeInfos = json.loads(reponseVille.text)
            datas = {
                "adresse_fournisseur": request.form['adresse_fournisseur'],
                "id_ville": villeInfos['id_ville'],
                "login_fournisseur":  request.form['login_fournisseur'],
                "mdp_fournisseur": mdpHASH,
                "nom_fournisseur": request.form['nom_fournisseur'],
                "ref_fournisseur": request.form['prenom_fournisseur']
            }
            username = requests.put(f"http://127.0.0.1:5550/api/fournisseurs/{datas['login_fournisseur']}", json=datas)
            if(username.status_code >= 400):
                flash("Une erreur a eu lieu, veuillez réessayer.", 'error')
            else:
                session.clear()
                flash("Vos modifications ont été enregitrés, veuillez vous reconnecter.", 'error')
                return redirect(url_for('connexion'))
        elif request.method == 'POST':
            flash("Des champs ne sont pas saisis.", 'error')
    return render_template("profil.html", title="Mon profil")

@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('home'))