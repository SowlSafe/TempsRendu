#!/usr/bin/env python3
"""Génère le site statique Humatiq (pages HTML complètes, sans étape de build côté Cloudflare)."""
import os, shutil, datetime

SRC = os.path.join(os.path.dirname(__file__), 'src')
OUT = os.path.join(os.path.dirname(__file__), 'dist')
FORMS_ENDPOINT = ''  # adresse du webhook Make, à renseigner

LOGO = ('<svg width="30" height="30" viewBox="0 0 30 30" aria-hidden="true"><circle cx="15" cy="15" r="13" fill="none" '
        'stroke="currentColor" stroke-width="2.5"/><path d="M15 15 L15 6 A9 9 0 0 1 23.5 18 Z" fill="var(--accent)"/>'
        '<path d="M15 8v7l5 3" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>')

NAV = [
    ('index', 'Accueil', 'index.html'),
    ('entreprises', 'Entreprises', 'entreprises.html'),
    ('formations', 'Formations', 'formations.html'),
    ('masterclass', 'Masterclass', 'masterclass.html'),
    ('outils', 'Outils', 'outils.html'),
    ('reseau', 'Réseau', 'reseau.html'),
    ('tarifs', 'Tarifs', 'tarifs.html'),
    ('a-propos', 'À propos', 'a-propos.html'),
]


# Réseaux sociaux : coller l'adresse de chaque profil entre les guillemets
SOCIAL = [
    ('LinkedIn', ''),
    ('Instagram', ''),
    ('TikTok', ''),
]
SHARE_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4"/></svg>'


def social_links():
    out = []
    for name, url in SOCIAL:
        if url:
            out.append(f'<a class="social" href="{url}" target="_blank" rel="noopener">{SHARE_ICON}<span>{name}</span><span class="sr"> (nouvel onglet)</span></a>')
        else:
            out.append(f'<span class="social soon">{SHARE_ICON}<span>{name}</span><small>bientôt</small></span>')
    return ''.join(out)


def layout(slug, title, description, body):
    cur = ' aria-current="page"'
    nav = ''.join(
        f'<a href="{href}"{cur if s == slug else ""}>{label}</a>' for s, label, href in NAV)
    cta_current = ' aria-current="page"' if slug == 'contact' else ''
    full_title = 'Humatiq · Automatiser le répétitif, rendre du temps' if slug == 'index' else f'{title} · Humatiq'
    year = datetime.date.today().year
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full_title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Humatiq">
<meta name="theme-color" content="#13231E">
<meta name="forms-endpoint" content="{FORMS_ENDPOINT}">
<script>try{{var c=JSON.parse(localStorage.getItem('tr-confort')||'{{}}');for(var k in c){{if(c[k])document.documentElement.setAttribute('data-'+k,c[k]);}}}}catch(e){{}}</script>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@500;600;700&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<div class="topline"><div class="wrap topline-row"><div class="ticker" aria-label="Annonces">
  <p class="tick on">Automatiser le répétitif, <b>rendre du temps</b> à vos équipes.</p>
  <p class="tick"><b>Nouveau</b> · Masterclass « Ma première automatisation » : <a href="masterclass.html">voir les dates</a></p>
  <p class="tick"><b>Bientôt</b> · votre espace apprenant : supports, replays et visios</p>
  </div>
  <div class="top-actions">
  <div class="pop">
    <button class="top-btn" id="nl-toggle" type="button" aria-expanded="false" aria-controls="nl-panel"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M3 6.5l9 6.5 9-6.5"/></svg><span>Newsletter</span></button>
    <div class="pop-panel" id="nl-panel" hidden>
      <p class="pop-title">La newsletter des outils</p>
      <p class="muted">Un outil et un cas concret tous les quinze jours. Gratuite, désinscription en un clic.</p>
      <form class="stack-form" data-form="newsletter" data-success="Merci, vous recevrez le prochain numéro.">
        <label for="top-mail">Votre e-mail</label>
        <input id="top-mail" name="email" type="email" required autocomplete="email">
        <button class="btn" type="submit">S'inscrire</button>
        <p class="msg" data-msg hidden role="status"></p>
      </form>
    </div>
  </div>
  <a class="top-btn" href="espace.html"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg><span>Mon espace</span></a>
  <div class="comfort">
    <button class="top-btn" id="comfort-toggle" type="button" aria-expanded="false" aria-controls="comfort-panel"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="4.5" r="2"/><path d="M4 8.5l8 1.5 8-1.5M12 10v5m0 0l-3.5 6.5M12 15l3.5 6.5"/></svg><span>Confort</span></button>
    <div class="comfort-panel" id="comfort-panel" hidden>
      <p class="comfort-title">Confort de lecture</p>
      <fieldset><legend>Taille du texte</legend><div class="seg"><button type="button" data-set="text" data-val="">A</button><button type="button" data-set="text" data-val="lg">A+</button><button type="button" data-set="text" data-val="xl">A++</button></div></fieldset>
      <fieldset><legend>Espacement</legend><div class="seg"><button type="button" data-set="spacing" data-val="">Standard</button><button type="button" data-set="spacing" data-val="wide">Aéré</button></div></fieldset>
      <fieldset><legend>Animations</legend><div class="seg"><button type="button" data-set="motion" data-val="">Activées</button><button type="button" data-set="motion" data-val="off">Désactivées</button></div></fieldset>
      <fieldset><legend>Contraste</legend><div class="seg"><button type="button" data-set="contrast" data-val="">Standard</button><button type="button" data-set="contrast" data-val="high">Renforcé</button></div></fieldset>
    </div>
  </div>
  </div>
</div></div>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="index.html" aria-label="Humatiq, accueil">{LOGO}<span>Humatiq</span></a>
    <button class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Navigation principale">{nav}<a class="btn small" href="contact.html"{cta_current}>Nous contacter</a></nav>
  </div>
</header>
<main id="contenu">
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div><p class="footer-title">Offres</p><a href="entreprises.html">Prestations entreprises</a><a href="formations.html">Formation des collaborateurs</a><a href="masterclass.html">Masterclass et parcours</a><a href="tarifs.html">Tarifs</a></div>
    <div><p class="footer-title">Ressources</p><a href="outils.html">Les outils et la newsletter</a><a href="reseau.html">Devenir partenaire</a><a href="a-propos.html">À propos</a></div>
    <div><p class="footer-title">Contact</p><a href="contact.html#entreprise">Demande entreprise</a><a href="contact.html#particulier">Demande particulier</a><a href="mentions-legales.html">Mentions légales et confidentialité</a></div>
  </div>
  <div class="wrap footer-social"><p class="footer-title">Suivez-nous</p><div class="socials">{social_links()}</div></div>
  <div class="wrap footer-bottom"><p>© {year} Humatiq. Des automatisations simples, fiables et respectueuses des données.</p></div>
</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
'''


def hero(eyebrow, title, lead, buttons='', side=''):
    crumbs = ''
    inner = f'''<div class="hero-copy">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
      {f'<div class="row">{buttons}</div>' if buttons else ''}
    </div>'''
    if side:
        return f'<section class="page-hero band-night"><div class="wrap split">{inner}<div>{side}</div></div></section>'
    return f'<section class="page-hero band-night"><div class="wrap">{inner}</div></section>'


def cta(title, text, buttons):
    return f'''<section class="band-night"><div class="wrap cta"><div><h2>{title}</h2><p class="lead">{text}</p></div><div class="row">{buttons}</div></div></section>'''


PAGES = {}

# ---------------------------------------------------------------- Accueil
SECTORS = [
    ('Santé et médico-social', 'Cabinets, centres de santé, EHPAD', ['Rappels de rendez-vous', 'Documents administratifs préremplis', 'Suivi des commandes de matériel'], 'Les données de santé ne passent que par des outils certifiés HDS, ou restent hors des automatisations.'),
    ('Tertiaire et services', 'Cabinets comptables, agences, assurances', ['Relances de pièces manquantes', 'Tri des demandes clients', 'Comptes rendus classés automatiquement'], ''),
    ('Artisans et BTP', 'Entreprises du bâtiment, artisans', ['Devis et relances', 'Planning des chantiers partagé', 'Photos de chantier rangées par client'], ''),
    ('Industrie et logistique', 'PME industrielles, transport', ['Alertes de maintenance', 'Suivi qualité dans un tableau', 'Bons de livraison archivés'], ''),
    ('Commerce', 'Boutiques, e-commerce', ['Commandes vers la comptabilité', 'Avis clients collectés', 'Alertes de stock bas'], ''),
    ('Associations et collectivités', 'Associations, mairies, structures publiques', ['Inscriptions et adhésions', 'Convocations et rappels', 'Tableaux de bord pour les financeurs'], ''),
]
SECTORS_SHORT = ''.join(f'<div class="sector"><h3>{n}</h3><p class="muted">{w}</p></div>' for n, w, ex, note in SECTORS)
SECTORS_FULL = ''.join(f'<div class="card"><p class="who">{w}</p><h3>{n}</h3><ul class="muted">' + ''.join(f'<li>{e}</li>' for e in ex) + '</ul>' + (f'<p class="note" style="margin:0">{note}</p>' if note else '') + '</div>' for n, w, ex, note in SECTORS)

PAGES['index'] = ('Accueil', "Automatisation des tâches répétitives et formation des collaborateurs. Le temps gagné revient au travail qui compte.", f'''
<section class="band-night home-hero">
<div class="wrap hero">
  <div>
    <p class="eyebrow">Automatisation · Formation · Productivité</p>
    <h1>Automatiser le répétitif, <em>rendre du temps</em> à vos équipes.</h1>
    <p class="lead">Nous automatisons vos tâches répétitives et formons vos collaborateurs. Le temps gagné revient au travail qui compte.</p>
    <div class="row"><button class="btn amber" type="button" id="open-calc" aria-expanded="false" aria-controls="calcul">Estimer mon temps perdu</button><a class="btn ghost" href="contact.html">Nous contacter</a></div>
  </div>
  <figure class="week" aria-label="Exemple : semaine d'une assistante commerciale avant et après automatisation">
    <div class="week-head"><span>Une semaine d'assistante commerciale</span><span>matinées · 9 h – 13 h</span></div>
    <div class="grid" aria-hidden="true">
      <span></span><span class="d">Lun</span><span class="d">Mar</span><span class="d">Mer</span><span class="d">Jeu</span><span class="d">Ven</span>
      <span class="h">9 h</span><span class="slot free">Temps rendu</span><span class="slot">Rendez-vous</span><span class="slot free" style="animation-delay:.2s">Temps rendu</span><span class="slot">Rendez-vous</span><span class="slot free" style="animation-delay:.4s">Temps rendu</span>
      <span class="h">10 h</span><span class="slot">Devis</span><span class="slot free" style="animation-delay:.6s">Temps rendu</span><span class="slot">Devis</span><span class="slot free" style="animation-delay:.8s">Temps rendu</span><span class="slot">Équipe</span>
      <span class="h">11 h</span><span class="slot">Clients</span><span class="slot">Clients</span><span class="slot free" style="animation-delay:1s">Temps rendu</span><span class="slot">Clients</span><span class="slot free" style="animation-delay:1.2s">Temps rendu</span>
      <span class="h">12 h</span><span class="slot empty"></span><span class="slot">Équipe</span><span class="slot empty"></span><span class="slot">Projet</span><span class="slot empty"></span>
    </div>
    <div class="legend"><span><i style="background:var(--task)"></i>Travail à valeur</span><span><i style="background:var(--free)"></i>Saisies, relances, tri : automatisés</span></div>
    <div class="week-foot"><span class="muted">Temps rendu sur la semaine</span><b>7 h</b></div>
    <figcaption class="muted" style="font-size:.78rem">Exemple illustratif.</figcaption>
  </figure>
</div>
</section>

<section class="band-soft" id="calcul" hidden>
<div class="wrap">
  <div class="head"><p class="eyebrow">Simulateur</p><h2 id="calc-title" tabindex="-1">Combien de temps vos équipes perdent-elles ?</h2><p class="lead">Déplacez les curseurs pour voir le temps que l'automatisation pourrait rendre à vos équipes. Base : 220 jours travaillés par an.</p></div>
  <div class="calc">
    <form id="calc-form" onsubmit="return false">
      <div class="field"><div class="top"><label for="c-people">Personnes concernées</label><span class="val" id="v-people"></span></div><input type="range" id="c-people" min="1" max="50" value="5"></div>
      <div class="field"><div class="top"><label for="c-min">Minutes par jour sur des tâches répétitives</label><span class="val" id="v-min"></span></div><input type="range" id="c-min" min="10" max="180" step="5" value="45"></div>
      <div class="field"><div class="top"><label for="c-part">Part automatisable</label><span class="val" id="v-part"></span></div><input type="range" id="c-part" min="10" max="80" step="5" value="50"></div>
    </form>
    <div class="result" aria-live="polite">
      <p>Temps rendu chaque année</p>
      <p class="big" id="r-hours">0 h</p>
      <p class="sub" id="r-days">soit 0 jours de travail</p>
      <p>Soit <b id="r-week">0 h</b> par personne et par semaine, rendues à son vrai métier : la relation avec les clients, le soin, la rédaction, le terrain.</p>
      <small>Estimation indicative. Le diagnostic mesure le temps réel, tâche par tâche.</small>
    </div>
  </div>
</div>
</section>

<section class="band-soft offers-band">
<div class="wrap">
  <div class="head"><p class="eyebrow">Nos offres</p><h2>Nous le faisons pour vous, ou nous vous apprenons</h2></div>
  <div class="offer-group">
    <h3 class="group-title">Pour les entreprises</h3>
    <div class="offers"><article class="offer"><div class="offer-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="5" cy="6" r="2.5"/><circle cx="19" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7.5 6h9M6.3 8.2l4.4 7.6M17.7 8.2l-4.4 7.6"/></svg></div><h4>Automatisation sur mesure</h4><p class="offer-pitch">Nous automatisons vos tâches répétitives avec les outils que vous utilisez déjà.</p><ul class="ticks"><li>Diagnostic du temps perdu</li><li>Mise en place et tests sur vos vrais cas</li><li>Suivi et évolutions</li></ul><p class="offer-price">À partir de <b>590 € HT</b></p><a class="btn" href="entreprises.html">Découvrir l\'offre<span class="sr"> : Automatisation sur mesure</span></a></article><article class="offer"><div class="offer-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M2.5 20c0-3.3 2.5-5.5 5.5-5.5s5.5 2.2 5.5 5.5M14 15.2c.9-.5 1.9-.7 3-.7 2.5 0 4.5 1.8 4.5 4.5"/></svg></div><h4>Formation des équipes</h4><p class="offer-pitch">Vos collaborateurs apprennent à repérer et automatiser leurs propres tâches.</p><ul class="ticks"><li>Atelier de 3 h ou formation d\'1 à 2 jours</li><li>Jusqu\'à 8 personnes, sur site ou à distance</li><li>Sur vos outils : Google ou Microsoft</li></ul><p class="offer-price">À partir de <b>690 € HT</b> le groupe</p><a class="btn" href="formations.html">Découvrir l\'offre<span class="sr"> : Formation des équipes</span></a></article></div>
  </div>
  <div class="offer-group">
    <h3 class="group-title">Pour les particuliers et indépendants</h3>
    <div class="offers"><article class="offer"><div class="offer-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="4" width="19" height="13" rx="2"/><path d="M10 8l5 2.5-5 2.5z"/><path d="M8 21h8"/></svg></div><h4>Masterclass et parcours</h4><p class="offer-pitch">2 heures pour créer votre première automatisation, 6 semaines pour en faire un métier.</p><ul class="ticks"><li>Masterclass en direct, replay inclus</li><li>Parcours Intégrateur sur un projet réel</li><li>Accès au réseau de partenaires</li></ul><p class="offer-price">À partir de <b>49 € TTC</b></p><a class="btn" href="masterclass.html">Découvrir l\'offre<span class="sr"> : Masterclass et parcours</span></a></article><article class="offer"><div class="offer-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M3 6.5l9 6.5 9-6.5"/></svg></div><h4>Newsletter des outils</h4><p class="offer-pitch">Un outil expliqué simplement et un cas concret à reproduire, tous les quinze jours.</p><ul class="ticks"><li>Fiches outils sans jargon</li><li>Un scénario pas à pas</li><li>Faut-il vraiment de l\'IA ?</li></ul><p class="offer-price"><b>Gratuite</b></p><a class="btn" href="outils.html#newsletter">S\'inscrire<span class="sr"> : Newsletter des outils</span></a></article></div>
  </div>
</div>
</section>

<section>
<div class="wrap">
  <div class="head"><p class="eyebrow">Secteurs</p><h2>Pour qui ?</h2><p class="lead">Toutes les structures qui passent trop de temps sur de l'administratif.</p></div>
  <div class="sectors">{SECTORS_SHORT}</div>
  <div class="row" style="margin-top:1.6rem"><a class="btn ghost" href="entreprises.html#secteurs">Exemples par secteur</a></div>
</div>
</section>
''' + cta('Parlons de votre temps perdu', 'Un premier échange de 20 minutes, sans engagement.', '<a class="btn amber" href="contact.html">Nous contacter</a>'))

# ---------------------------------------------------------------- Entreprises
PAGES['entreprises'] = ('Prestations entreprises', "Diagnostic des tâches répétitives, mise en place d'automatisations avec vos outils et suivi mensuel, pour TPE, PME et indépendants.",
hero('Entreprises · Prestations', 'Vos équipes ne sont pas là pour copier-coller', "Nous repérons les tâches répétitives qui grignotent les journées, nous les automatisons avec les outils que vous utilisez déjà et nous assurons le suivi.",
     '<a class="btn amber" href="contact.html#entreprise">Demander un diagnostic</a><a class="btn ghost" href="tarifs.html#entreprises">Voir les tarifs</a>') + '''
<section>
<div class="wrap">
  <div class="head"><p class="eyebrow">Par service</p><h2>Où se cache le temps perdu</h2><p class="lead">Chaque service a ses tâches répétitives. Voici celles que nous automatisons le plus souvent.</p></div>
  <div class="cards">
    <div class="card"><p class="who">Commercial</p><h3>Devis, relances, CRM</h3><ul class="muted"><li>Relances automatiques des devis</li><li>Fiches clients créées depuis les formulaires</li><li>Prise de rendez-vous sans échange de mails</li></ul></div>
    <div class="card"><p class="who">Ressources humaines</p><h3>Arrivées, absences, entretiens</h3><ul class="muted"><li>Parcours d'arrivée d'un salarié</li><li>Demandes de congés centralisées</li><li>Rappels d'entretiens et de visites médicales</li></ul></div>
    <div class="card"><p class="who">Administration</p><h3>Factures, documents, tableaux</h3><ul class="muted"><li>Factures fournisseurs classées et suivies</li><li>Documents générés à partir d'un modèle</li><li>Tableaux de bord mis à jour tout seuls</li></ul></div>
    <div class="card"><p class="who">Service client</p><h3>Demandes, tri, réponses</h3><ul class="muted"><li>Demandes triées par priorité</li><li>Accusés de réception personnalisés</li><li>Alertes quand une demande attend trop</li></ul></div>
  </div>
</div>
</section>

<section class="band-soft" id="secteurs">
<div class="wrap">
  <div class="head"><p class="eyebrow">Par secteur</p><h2>Des exemples dans votre métier</h2></div>
  <div class="cards">''' + SECTORS_FULL + '''</div>
</div>
</section>

<section>
<div class="wrap">
  <div class="head"><p class="eyebrow">Exemples concrets</p><h2>Ce qu'on automatise le plus souvent</h2></div>
  <div class="examples">
    <div class="example"><h3>Les demandes de contact</h3><div class="chain"><span>Formulaire du site</span><span class="arrow">→</span><span>Tableau de suivi</span><span class="arrow">→</span><span>Tri par priorité</span><span class="arrow">→</span><span>Réponse avec lien de rendez-vous</span></div><p class="muted">Plus aucune demande oubliée, et le client choisit lui-même son créneau.</p></div>
    <div class="example"><h3>Les devis et les relances</h3><div class="chain"><span>Devis envoyé</span><span class="arrow">→</span><span>Relance à J+7</span><span class="arrow">→</span><span>Alerte si pas de réponse</span></div><p class="muted">Les relances partent toutes seules, au bon moment.</p></div>
    <div class="example"><h3>L'arrivée d'un salarié</h3><div class="chain"><span>Fiche d'arrivée</span><span class="arrow">→</span><span>Comptes créés</span><span class="arrow">→</span><span>Mail de bienvenue</span><span class="arrow">→</span><span>Check-list manager</span></div><p class="muted">Rien n'est oublié, même quand tout le monde est débordé.</p></div>
    <div class="example"><h3>Les factures fournisseurs</h3><div class="chain"><span>Facture reçue par mail</span><span class="arrow">→</span><span>Classée dans le bon dossier</span><span class="arrow">→</span><span>Ligne ajoutée au suivi</span></div><p class="muted">La comptabilité retrouve tout, sans copier-coller.</p></div>
  </div>
</div>
</section>

<section class="band-soft">
<div class="wrap">
  <div class="head"><p class="eyebrow">Nos prestations</p><h2>Trois façons de travailler ensemble</h2></div>
  <div class="cards">
    <div class="card"><p class="who">Pour commencer</p><h3>Le diagnostic</h3><p class="muted">Une demi-journée d'observation et d'entretiens. Vous repartez avec la carte de vos tâches répétitives, le temps qu'elles coûtent et 3 automatisations prioritaires chiffrées.</p><p class="from">590 € HT, déduit si vous commandez la mise en place</p></div>
    <div class="card"><p class="who">Le plus choisi</p><h3>Le Pack Démarrage</h3><p class="muted">Diagnostic, 3 automatisations mises en place, 2 h de prise en main avec l'équipe et 1 mois de suivi offert.</p><p class="from">1 890 € HT</p></div>
    <div class="card"><p class="who">Dans la durée</p><h3>Le suivi mensuel</h3><p class="muted">Nous surveillons vos automatisations, nous les réparons si un outil change et nous les faisons évoluer.</p><p class="from">Dès 90 € HT par mois</p></div>
  </div>
</div>
</section>

<section>
<div class="wrap">
  <div class="head"><p class="eyebrow">Déroulé</p><h2>Comment se passe une mission</h2></div>
  <ol class="steps">
    <li><h3>Échange</h3><p class="muted">20 minutes pour comprendre votre activité et vos outils. Gratuit.</p></li>
    <li><h3>Diagnostic</h3><p class="muted">Observation du travail réel, mesure du temps, choix des priorités avec vous.</p></li>
    <li><h3>Mise en place</h3><p class="muted">Construction, tests sur vos vrais cas, documentation simple.</p></li>
    <li><h3>Prise en main</h3><p class="muted">Vos équipes savent utiliser, vérifier et ajuster chaque automatisation.</p></li>
  </ol>
</div>
</section>

<section class="band-soft">
<div class="wrap">
  <div class="head"><p class="eyebrow">Questions fréquentes</p><h2>Avant de vous lancer</h2></div>
  <details><summary>Faut-il changer nos outils ?</summary><p>Non. Nous partons de ce que vous utilisez déjà : Google, Microsoft, votre logiciel de facturation, votre CRM. Nous ajoutons seulement l'outil d'orchestration qui les relie.</p></details>
  <details><summary>Combien coûtent les outils eux-mêmes ?</summary><p>Beaucoup proposent une offre gratuite suffisante pour démarrer. Au-delà, comptez souvent quelques dizaines d'euros par mois. Le diagnostic chiffre ces abonnements avant toute décision.</p></details>
  <details><summary>Que se passe-t-il si une automatisation s'arrête ?</summary><p>Avec le suivi mensuel, nous surveillons vos flux et nous les réparons. Sans suivi, vos équipes sont formées pour repérer et corriger les erreurs simples.</p></details>
  <details><summary>Et les données personnelles ?</summary><p>Nous appliquons la minimisation : seules les données nécessaires circulent. Nous privilégions les outils hébergés en Europe et nous vous aidons à mettre à jour votre registre RGPD.</p></details>
  <details><summary>Utilisez-vous l'intelligence artificielle ?</summary><p>Seulement quand elle apporte quelque chose qu'une règle simple ne peut pas faire, par exemple lire des mails rédigés librement. Dans la plupart des cas, des règles claires sont plus fiables, moins chères et plus faciles à maintenir.</p></details>
</div>
</section>
''' + cta('Combien de temps perdez-vous chaque semaine ?', 'Le diagnostic vous donne la réponse en chiffres, et les 3 automatisations qui rapportent le plus.', '<a class="btn amber" href="contact.html#entreprise">Demander un diagnostic</a>'))

# ---------------------------------------------------------------- Formations
PAGES['formations'] = ('Formation des collaborateurs', "Formations intra-entreprise pour apprendre à repérer et automatiser les tâches répétitives : atelier de 3 h, formation d'1 ou 2 jours.",
hero('Entreprises · Formation', 'Former vos équipes à automatiser leurs propres tâches', "Personne ne connaît mieux un poste que celui qui l'occupe. Nos formations donnent à vos collaborateurs la méthode et les outils pour se libérer eux-mêmes des tâches répétitives.",
     '<a class="btn amber" href="contact.html#formation">Organiser une formation</a><a class="btn ghost" href="tarifs.html#formations">Voir les tarifs</a>') + '''
<section>
<div class="wrap">
  <div class="head"><p class="eyebrow">Trois formats</p><h2>Choisissez selon votre objectif</h2><p class="lead">En intra, jusqu'à 8 personnes, dans vos locaux ou à distance.</p></div>
  <div class="cards">
    <div class="card"><p class="who">3 heures</p><h3>Atelier Repérer</h3><p class="muted">Chacun cartographie sa semaine et repart avec la liste de ses tâches automatisables, classées par temps gagné.</p><p class="from">690 € HT le groupe</p></div>
    <div class="card"><p class="who">1 jour</p><h3>Automatiser sans coder</h3><p class="muted">Prise en main de Make ou de Power Automate. Chaque participant construit une automatisation utile à son poste.</p><p class="from">1 290 € HT le groupe</p></div>
    <div class="card"><p class="who">2 jours</p><h3>Formation sur vos cas</h3><p class="muted">Nous travaillons sur les vrais processus de l'entreprise. Les automatisations créées restent en service.</p><p class="from">2 290 € HT le groupe</p></div>
  </div>
</div>
</section>

<section class="band-soft">
<div class="wrap split2">
  <div class="head" style="margin:0"><p class="eyebrow">Programme type</p><h2>« Automatiser sans coder » en une journée</h2><p class="lead">Le programme est adapté à vos outils : Google Workspace ou Microsoft 365.</p></div>
  <div class="programme">
    <div class="module"><b>9 h – 10 h 30</b><div><h3>Repérer ce qui s'automatise</h3><p>Les 5 signes d'une tâche automatisable. Chacun liste les siennes.</p></div></div>
    <div class="module"><b>10 h 45 – 12 h 30</b><div><h3>Premiers pas avec l'outil</h3><p>Déclencheur, actions, données : construire un premier flux formulaire → tableau → mail.</p></div></div>
    <div class="module"><b>13 h 30 – 15 h</b><div><h3>Conditions et routes</h3><p>Trier, filtrer, envoyer au bon endroit selon le contenu.</p></div></div>
    <div class="module"><b>15 h 15 – 16 h 45</b><div><h3>Mon automatisation</h3><p>Chacun construit la sienne, accompagné, sur un cas réel de son poste.</p></div></div>
    <div class="module"><b>16 h 45 – 17 h 30</b><div><h3>Fiabilité et RGPD</h3><p>Surveiller, corriger une erreur, limiter les données qui circulent.</p></div></div>
  </div>
</div>
</section>

<section>
<div class="wrap">
  <div class="head"><p class="eyebrow">Modalités</p><h2>En pratique</h2></div>
  <div class="cards">
    <div class="card"><h3>Pour qui</h3><p class="muted">Tous les collaborateurs qui utilisent un ordinateur. Aucune connaissance technique requise.</p></div>
    <div class="card"><h3>Où</h3><p class="muted">Dans vos locaux ou en visioconférence. Les déplacements sont facturés en plus.</p></div>
    <div class="card"><h3>Ce qu'ils gardent</h3><p class="muted">Les supports, les modèles d'automatisation et 30 jours de questions par e-mail après la formation.</p></div>
    <div class="card"><h3>Financement</h3><p class="muted">Pas encore finançable par les OPCO : la certification Qualiopi est en préparation.</p></div>
  </div>
</div>
</section>
''' + cta('Une formation pour votre équipe ?', 'Dites-nous vos outils et vos métiers, nous vous proposons un programme adapté.', '<a class="btn amber" href="contact.html#formation">Organiser une formation</a>'))

# ---------------------------------------------------------------- Masterclass
PAGES['masterclass'] = ('Masterclass et parcours', "Masterclass de 2 h en direct pour créer votre première automatisation, et Parcours Intégrateur de 6 semaines pour en faire un métier.",
hero('Particuliers et indépendants', 'Apprendre à automatiser, à votre rythme', "Une masterclass de 2 heures pour créer votre première automatisation. Un parcours de 6 semaines pour en faire un métier et rejoindre notre réseau.",
     '<a class="btn amber" href="#masterclass">Voir les masterclass</a><a class="btn ghost" href="#parcours">Le Parcours Intégrateur</a>') + '''
<section id="masterclass">
<div class="wrap">
  <div class="head"><p class="eyebrow">Masterclass · 2 h en direct · 49 € TTC</p><h2>Trois thèmes pour démarrer</h2><p class="lead">En visioconférence, en petit groupe. Le replay et les modèles sont inclus.</p></div>
  <div class="cards">
    <div class="card"><p class="who">Débutant</p><h3>Ma première automatisation</h3><p class="muted">Comprendre le principe déclencheur → actions et construire un premier flux qui vous servira dès le lendemain.</p><p class="from">Prochaine date : bientôt</p></div>
    <div class="card"><p class="who">Débutant</p><h3>Formulaires, mails et rendez-vous</h3><p class="muted">Recevoir une demande, la ranger dans un tableau, répondre automatiquement avec un lien de prise de rendez-vous.</p><p class="from">Prochaine date : bientôt</p></div>
    <div class="card"><p class="who">Intermédiaire</p><h3>Trier et router</h3><p class="muted">Filtres, conditions et routes : envoyer chaque demande au bon endroit, sans intelligence artificielle.</p><p class="from">Prochaine date : bientôt</p></div>
  </div>
  <div class="row" style="margin-top:1.6rem"><a class="btn" href="contact.html#masterclass">Être prévenu des prochaines dates</a></div>
</div>
</section>

<section class="band-soft" id="parcours">
<div class="wrap split2">
  <div class="head" style="margin:0"><p class="eyebrow">Parcours Intégrateur · 6 semaines · 690 € TTC</p><h2>Faire de l'automatisation un métier</h2><p class="lead">6 sessions en direct, un projet réel pour un vrai client, une évaluation finale. Les personnes qui le réussissent peuvent rejoindre le réseau Humatiq.</p><div class="row"><a class="btn" href="contact.html#parcours">Candidater</a><a class="btn ghost" href="reseau.html">Le réseau</a></div></div>
  <div class="programme">
    <div class="module"><b>Semaine 1</b><div><h3>Repérer et chiffrer</h3><p>Observer un poste, mesurer le temps perdu, prioriser.</p></div></div>
    <div class="module"><b>Semaine 2</b><div><h3>Les bases de l'orchestration</h3><p>Déclencheurs, actions, données, premiers scénarios.</p></div></div>
    <div class="module"><b>Semaine 3</b><div><h3>Conditions, routes, erreurs</h3><p>Construire des flux fiables qui ne s'arrêtent pas au premier imprévu.</p></div></div>
    <div class="module"><b>Semaine 4</b><div><h3>Données et RGPD</h3><p>Tableaux, documents, minimisation, hébergement des outils.</p></div></div>
    <div class="module"><b>Semaine 5</b><div><h3>Projet réel</h3><p>Diagnostic et construction pour un client, accompagné.</p></div></div>
    <div class="module"><b>Semaine 6</b><div><h3>Livrer et vendre</h3><p>Présenter, documenter, chiffrer une prestation. Évaluation finale.</p></div></div>
  </div>
</div>
</section>
''' + cta('Pas encore prêt à vous lancer ?', 'Commencez par la newsletter : un outil et un cas concret tous les quinze jours, gratuitement.', '<a class="btn amber" href="outils.html#newsletter">Recevoir la newsletter</a>'))

# ---------------------------------------------------------------- Outils
TOOLS = [
    ('make', 'Orchestration', 'Make', "Des scénarios visuels qui relient vos applications, avec des conditions et des routes.", "Idéal pour des flux à plusieurs étapes, avec des embranchements."),
    ('zapier', 'Orchestration', 'Zapier', "Le plus simple pour démarrer, avec un très grand catalogue d'applications.", "Idéal pour des automatisations courtes et rapides à mettre en place."),
    ('n8n', 'Orchestration', 'n8n', "Open source, installable sur vos propres serveurs.", "Idéal quand les données doivent rester chez vous."),
    ('power-automate', 'Microsoft 365', 'Power Automate', "L'outil d'automatisation de l'univers Microsoft.", "Idéal si vous travaillez déjà avec Outlook, Teams et SharePoint."),
    ('apps-script', 'Google Workspace', 'Apps Script', "De petits scripts pour automatiser Sheets, Gmail et Agenda.", "Idéal pour des besoins simples, sans abonnement supplémentaire."),
    ('tally', 'Formulaires', 'Tally et Google Forms', "Des formulaires bien construits, avec des listes de choix.", "La première étape de toute automatisation fiable."),
    ('airtable', 'Données', 'Airtable et Google Sheets', "Des tableaux qui servent de base de données.", "Idéal pour suivre des demandes, des clients ou des stocks."),
    ('calendly', 'Rendez-vous', 'Pages de réservation', "Google Agenda, Calendly : vos clients choisissent un créneau libre.", "Idéal pour supprimer les allers-retours de mails."),
    ('ia', 'IA', "Quand l'utiliser ?", "Trier des mails libres, résumer un document, préparer un brouillon.", "Utile seulement quand une règle simple ne suffit pas."),
]
tools_html = ''.join(
    f'<div class="card tool"><p class="who">{k}</p><h3>{n}</h3><p class="muted">{d}</p><p class="tool-use">{i}</p></div>'
    for slug, k, n, d, i in TOOLS)
PAGES['outils'] = ('Outils et newsletter', "Make, Zapier, n8n, Power Automate, Apps Script : les outils d'orchestration expliqués simplement, et une newsletter gratuite tous les quinze jours.",
hero('Ressources · Newsletter', "Les outils d'orchestration, expliqués simplement", "Chaque outil a ses forces. Nous les décrivons sans jargon, avec leurs limites, pour que vous choisissiez le bon.",
     '<a class="btn amber" href="#newsletter">Recevoir la newsletter</a>') + f'''
<section>
<div class="wrap">
  <div class="head"><p class="eyebrow">Panorama</p><h2>Les outils que nous décortiquons</h2></div>
  <div class="cards">{tools_html}</div>
</div>
</section>

<section class="band-night" id="newsletter">
<div class="wrap split2">
  <div class="head" style="margin:0"><p class="eyebrow">Newsletter gratuite · tous les quinze jours</p><h2>Un outil, un cas, une question</h2><p class="lead">Une fiche outil, un scénario prêt à reproduire pas à pas, et la question qu'on ne pose jamais assez : faut-il vraiment de l'IA ?</p></div>
  <div>
    <form class="inline-form" data-form="newsletter" data-success="Merci, vous recevrez le prochain numéro.">
      <label class="skip" for="nl-mail">Votre e-mail</label>
      <input id="nl-mail" name="email" type="email" required placeholder="Votre e-mail" autocomplete="email">
      <button class="btn amber" type="submit">S'inscrire</button>
      <p class="msg" data-msg hidden role="status"></p>
    </form>
    <p class="muted" style="margin-top:.8rem;font-size:.9rem">Désinscription en un clic. Votre adresse n'est jamais transmise à des tiers.</p>
  </div>
</div>
</section>
''')

# ---------------------------------------------------------------- Réseau
PAGES['reseau'] = ('Réseau de partenaires', "Formé·e chez Humatiq, partenaire ensuite : nous confions des missions aux intégrateurs de notre réseau, avec une méthode et un cadre qualité.",
hero('Le réseau Humatiq', 'Formé·e chez nous, partenaire ensuite', "Les personnes qui réussissent le Parcours Intégrateur peuvent rejoindre notre réseau. Nous leur confions des missions auprès de nos clients et nous assurons le cadre.",
     '<a class="btn amber" href="contact.html#partenariat">Rejoindre le réseau</a><a class="btn ghost" href="masterclass.html#parcours">Le Parcours Intégrateur</a>') + '''
<section>
<div class="wrap split2">
  <div class="head" style="margin:0"><p class="eyebrow">Comment ça marche</p><h2>Un parcours en quatre étapes</h2><p class="lead">Nous apportons les clients, la méthode et le suivi qualité. Vous réalisez les missions en indépendant.</p></div>
  <div class="flow" aria-label="Parcours d'un partenaire">
    <div><span>Masterclass</span><span>2 h</span></div>
    <div><span>Parcours Intégrateur</span><span>6 semaines</span></div>
    <div><span>Projet réel évalué</span><span>validation</span></div>
    <div><span>Missions confiées par Humatiq</span><span>commission 15 %</span></div>
  </div>
</div>
</section>

<section class="band-soft">
<div class="wrap">
  <div class="head"><p class="eyebrow">Ce que chacun apporte</p><h2>Un partenariat clair</h2></div>
  <div class="cards two">
    <div class="card"><h3>Humatiq apporte</h3><ul class="muted"><li>Des missions auprès de clients qualifiés</li><li>La méthode de diagnostic et les modèles</li><li>Un suivi qualité et un appui sur les cas difficiles</li><li>La visibilité de la marque</li></ul></div>
    <div class="card"><h3>Le partenaire s'engage à</h3><ul class="muted"><li>Appliquer la méthode et la charte qualité</li><li>Respecter les règles RGPD et la confidentialité</li><li>Documenter chaque automatisation livrée</li><li>Facturer en indépendant, avec son propre statut</li></ul></div>
  </div>
  <p class="note">Sur chaque mission que nous apportons, Humatiq perçoit une commission de 15 % du montant facturé. Les conditions sont fixées dans un contrat de partenariat signé avant toute mission.</p>
</div>
</section>

<section>
<div class="wrap">
  <div class="head"><p class="eyebrow">Questions fréquentes</p><h2>Devenir partenaire</h2></div>
  <details><summary>Faut-il un statut d'indépendant ?</summary><p>Oui. Les partenaires facturent leurs missions eux-mêmes, par exemple en micro-entreprise. Nous pouvons vous orienter pour démarrer.</p></details>
  <details><summary>Peut-on rejoindre le réseau sans suivre le parcours ?</summary><p>Si vous avez déjà une expérience solide en automatisation, contactez-nous : une évaluation sur un cas pratique peut remplacer le parcours.</p></details>
  <details><summary>Combien de missions pouvez-vous confier ?</summary><p>Cela dépend de la demande et de votre région. Nous ne promettons pas de volume, mais nous privilégions les partenaires du réseau pour toutes les missions que nous ne réalisons pas nous-mêmes.</p></details>
</div>
</section>
''' + cta('Envie de rejoindre le réseau ?', 'Parlez-nous de votre parcours et de vos disponibilités.', '<a class="btn amber" href="contact.html#partenariat">Nous écrire</a>'))

# ---------------------------------------------------------------- Tarifs
PAGES['tarifs'] = ('Tarifs', "Tarifs de lancement Humatiq : diagnostic, Pack Démarrage, automatisations, suivi, formations intra, masterclass et Parcours Intégrateur.",
hero('Tarifs', 'Des prix clairs, annoncés à l\'avance', "Tarifs de lancement. Chaque prestation commence par un échange gratuit de 20 minutes.") + '''
<section>
<div class="wrap">
  <div class="tabs" role="tablist" aria-label="Catégories de tarifs">
    <button class="tab" role="tab" id="t-ent" data-hash="entreprises" aria-controls="p-ent" aria-selected="true">Prestations entreprises</button>
    <button class="tab" role="tab" id="t-form" data-hash="formations" aria-controls="p-form" aria-selected="false">Formation collaborateurs</button>
    <button class="tab" role="tab" id="t-part" data-hash="particuliers" aria-controls="p-part" aria-selected="false">Particuliers</button>
  </div>
  <div class="prices" id="p-ent" role="tabpanel" aria-labelledby="t-ent">
    <div class="price"><span class="tag">Pour commencer</span><h3>Diagnostic</h3><p class="amount">590 € <small>HT</small></p><ul><li>Une demi-journée d'observation et d'entretiens</li><li>Carte des tâches répétitives et du temps perdu</li><li>3 automatisations prioritaires chiffrées</li><li>Montant déduit si vous commandez la mise en place</li></ul></div>
    <div class="price pick"><span class="tag">Le plus choisi</span><h3>Pack Démarrage</h3><p class="amount">1 890 € <small>HT</small></p><ul><li>Diagnostic inclus</li><li>3 automatisations mises en place</li><li>2 h de prise en main avec l'équipe</li><li>1 mois de suivi offert</li></ul></div>
    <div class="price"><span class="tag">À l'unité</span><h3>Automatisation</h3><p class="amount">dès 450 € <small>HT</small></p><ul><li>Essentielle (dès 450 €) : un flux simple, par ex. formulaire → tableau → mail</li><li>Avancée (dès 1 200 €) : plusieurs outils, conditions, documents</li><li>Suivi : 90 €/mois jusqu'à 5 flux, 240 €/mois avec 2 h d'évolutions</li></ul></div>
  </div>
  <div class="prices" id="p-form" role="tabpanel" aria-labelledby="t-form" hidden>
    <div class="price"><span class="tag">3 heures</span><h3>Atelier Repérer</h3><p class="amount">690 € <small>HT</small></p><ul><li>Jusqu'à 8 personnes</li><li>Chacun repart avec sa liste de tâches automatisables</li><li>Idéal avant un projet</li></ul></div>
    <div class="price pick"><span class="tag">1 jour</span><h3>Automatiser sans coder</h3><p class="amount">1 290 € <small>HT</small></p><ul><li>Jusqu'à 8 personnes</li><li>Prise en main de Make ou Power Automate</li><li>Chacun construit une automatisation utile à son poste</li></ul></div>
    <div class="price"><span class="tag">2 jours</span><h3>Formation sur vos cas</h3><p class="amount">2 290 € <small>HT</small></p><ul><li>Jusqu'à 8 personnes</li><li>Travail sur les vrais processus de l'entreprise</li><li>Les automatisations créées restent en service</li></ul></div>
  </div>
  <div class="prices" id="p-part" role="tabpanel" aria-labelledby="t-part" hidden>
    <div class="price"><span class="tag">Gratuit</span><h3>Newsletter</h3><p class="amount">0 €</p><ul><li>Tous les quinze jours</li><li>Une fiche outil et un cas pas à pas</li><li>Désinscription en un clic</li></ul></div>
    <div class="price pick"><span class="tag">2 h en direct</span><h3>Masterclass</h3><p class="amount">49 € <small>TTC</small></p><ul><li>« Ma première automatisation »</li><li>« Formulaires, mails et rendez-vous »</li><li>Replay et modèles inclus</li></ul></div>
    <div class="price"><span class="tag">6 semaines</span><h3>Parcours Intégrateur</h3><p class="amount">690 € <small>TTC</small></p><ul><li>6 sessions en direct et un projet réel</li><li>Évaluation finale</li><li>Accès au réseau de partenaires Humatiq</li></ul></div>
  </div>
  <p class="note">Tarifs de lancement. Les déplacements hors visioconférence sont facturés en plus. Les abonnements aux outils (Make, Zapier…) restent à la charge du client. Nos formations ne sont pas encore finançables par les OPCO : la certification Qualiopi est en préparation.</p>
</div>
</section>
''' + cta('Un besoin particulier ?', 'Nous établissons un devis précis après un premier échange gratuit.', '<a class="btn amber" href="contact.html">Demander un devis</a>'))

# ---------------------------------------------------------------- À propos
PAGES['a-propos'] = ('À propos', "Humatiq a été fondé par le Dr Florence Charquet Mazeres, spécialiste des facteurs humains : partir du travail réel, des règles simples, de l'IA seulement quand elle sert.",
hero('À propos', 'Rendre du temps, pas ajouter de la complexité', "Humatiq est né d'un constat simple : beaucoup d'équipes perdent des heures sur des tâches qu'un outil pourrait faire à leur place.") + '''
<section>
<div class="wrap founder">
  <div class="portrait" aria-hidden="true">FCM</div>
  <div class="head" style="margin:0"><p class="eyebrow">La fondatrice</p><h2>Dr Florence Charquet Mazeres</h2><p class="lead">Spécialiste des facteurs humains, elle s'intéresse à la façon dont l'organisation du travail pèse sur la fatigue, les erreurs et l'efficacité. Humatiq applique cette approche à l'automatisation : partir des personnes, puis choisir l'outil.</p></div>
</div>
</section>

<section class="band-night">
<div class="wrap split2">
  <div class="head" style="margin:0"><p class="eyebrow">Notre parti pris</p><h2>De l'IA seulement quand elle sert</h2><p class="lead">Beaucoup d'automatisations vendues « avec IA » fonctionneraient aussi bien, et de façon plus fiable, avec de simples règles. Nous choisissons l'outil le plus simple qui fait le travail.</p></div>
  <div class="rules">
    <div class="rule"><b>Observer</b><p>Le travail réel, pas l'organigramme : où le temps se perd, où les erreurs arrivent.</p></div>
    <div class="rule"><b>Simplifier</b><p>Des règles claires que vos équipes comprennent et peuvent modifier. L'IA seulement pour le texte libre que les règles ne savent pas lire.</p></div>
    <div class="rule"><b>Transmettre</b><p>Former les équipes pour qu'elles restent maîtres de leurs outils.</p></div>
    <div class="rule"><b>Protéger</b><p>Le minimum de données, des outils hébergés en Europe quand c'est possible, et un humain qui valide.</p></div>
  </div>
</div>
</section>
''' + cta('Travaillons ensemble', 'Un premier échange de 20 minutes, sans engagement.', '<a class="btn amber" href="contact.html">Nous contacter</a>'))

# ---------------------------------------------------------------- Contact
PAGES['contact'] = ('Contact', "Contactez Humatiq : diagnostic, automatisation, formation de vos équipes, masterclass, Parcours Intégrateur ou partenariat.",
hero('Contact', 'Parlons de votre temps perdu', "Décrivez votre besoin en quelques lignes. Nous vous répondons sous 48 h ouvrées.") + '''
<section>
<div class="wrap">
  <form class="form" data-form="contact" data-success="Merci, votre demande est bien partie. Nous vous répondons sous 48 h ouvrées.">
    <fieldset class="field">
      <legend>Je suis</legend>
      <div class="chips">
        <label class="chip"><input type="radio" name="profil" value="entreprise" id="c-entreprise" checked><span>Une entreprise ou organisation</span></label>
        <label class="chip"><input type="radio" name="profil" value="particulier" id="c-particulier"><span>Un particulier ou indépendant</span></label>
      </div>
    </fieldset>
    <div class="field">
      <label for="c-objet">Votre demande concerne</label>
      <select id="c-objet" name="objet" required>
        <option value="">Choisissez…</option>
        <option value="diagnostic">Un diagnostic de nos tâches répétitives</option>
        <option value="automatisation">La mise en place d'automatisations</option>
        <option value="formation">Une formation pour mon équipe</option>
        <option value="masterclass">Une masterclass</option>
        <option value="parcours">Le Parcours Intégrateur</option>
        <option value="partenariat">Rejoindre le réseau de partenaires</option>
        <option value="autre">Autre chose</option>
      </select>
    </div>
    <div class="form-row">
      <div class="field"><label for="c-prenom">Prénom</label><input id="c-prenom" name="prenom" required autocomplete="given-name"></div>
      <div class="field"><label for="c-nom">Nom</label><input id="c-nom" name="nom" required autocomplete="family-name"></div>
    </div>
    <div class="form-row">
      <div class="field"><label for="c-email">E-mail</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="c-tel">Téléphone <span class="field-hint">(facultatif)</span></label><input id="c-tel" name="telephone" type="tel" autocomplete="tel"></div>
    </div>
    <div data-show-if="profil=entreprise" style="display:grid;gap:1.1rem">
      <div class="form-row">
        <div class="field"><label for="c-org">Entreprise</label><input id="c-org" name="organisation" autocomplete="organization"></div>
        <div class="field"><label for="c-fonction">Fonction</label><input id="c-fonction" name="fonction" autocomplete="organization-title"></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="c-effectif">Effectif</label><select id="c-effectif" name="effectif"><option value="">Choisissez…</option><option>Moins de 10 salariés</option><option>10 à 49 salariés</option><option>50 à 249 salariés</option><option>250 salariés et plus</option></select></div>
        <div class="field"><label for="c-outils">Vos outils principaux</label><select id="c-outils" name="outils"><option value="">Choisissez…</option><option>Google Workspace</option><option>Microsoft 365</option><option>Les deux</option><option>Autre ou je ne sais pas</option></select></div>
      </div>
    </div>
    <div class="field"><label for="c-message">Quelles tâches vous prennent du temps ?</label><textarea id="c-message" name="message" required></textarea></div>
    <div class="field"><label for="c-pref">Vous préférez être recontacté·e par</label><select id="c-pref" name="preference_contact"><option>E-mail</option><option>Téléphone</option><option>Visioconférence</option></select></div>
    <label class="check" for="c-rgpd"><input type="checkbox" id="c-rgpd" name="consentement" required><span>J'accepte que mes informations soient utilisées pour répondre à ma demande (<a href="mentions-legales.html#confidentialite">confidentialité</a>).</span></label>
    <div><button class="btn" type="submit">Envoyer ma demande</button></div>
    <p class="msg" data-msg hidden role="status"></p>
  </form>
</div>
</section>
''')

# ---------------------------------------------------------------- Mentions légales
PAGES['mentions-legales'] = ('Mentions légales', "Mentions légales et politique de confidentialité du site Humatiq.",
hero('Informations légales', 'Mentions légales et confidentialité', "Qui édite ce site, qui l'héberge, et ce que nous faisons de vos données.") + '''
<section>
<div class="wrap" style="max-width:52rem">
  <div style="display:grid;gap:1rem">
    <h2 style="font-size:1.5rem">Éditeur du site</h2>
    <p class="muted">Humatiq · <mark>statut juridique, adresse et SIREN à compléter</mark><br>Directrice de la publication : Florence Charquet Mazeres<br>Contact : <mark>adresse e-mail à compléter</mark></p>
    <h2 style="font-size:1.5rem">Hébergement</h2>
    <p class="muted">Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, États-Unis.</p>
    <h2 style="font-size:1.5rem" id="confidentialite">Données personnelles</h2>
    <p class="muted">Les informations envoyées par les formulaires servent uniquement à répondre à votre demande et, si vous vous inscrivez, à vous envoyer la newsletter et les dates des masterclass.</p>
    <ul class="ticks muted">
      <li>Base légale : les mesures précontractuelles (demande de contact) et votre consentement (newsletter).</li>
      <li>Sous-traitants : Make (transmission des formulaires) et Google (tableau de suivi et messagerie).</li>
      <li>Aucune donnée n'est vendue ni transmise à des tiers à des fins commerciales.</li>
      <li>Durée de conservation : 3 ans après le dernier contact. Désinscription de la newsletter possible à tout moment.</li>
      <li>Vos droits : accès, rectification, effacement, opposition. Écrivez-nous à l'adresse ci-dessus. Vous pouvez aussi saisir la CNIL.</li>
    </ul>
  </div>
</div>
</section>
''')

PAGES['espace'] = ('Mon espace', "L'espace apprenant Humatiq : supports de cours, replays et liens des visios, au même endroit.",
hero('Espace apprenant', 'Vos supports, vos replays, vos visios', "Bientôt, chaque participant aura son compte pour retrouver tout ce qui concerne sa formation, au même endroit.") + '''
<section>
<div class="wrap split2">
  <div class="head" style="margin:0"><p class="eyebrow">Ce que vous y trouverez</p><h2>Tout votre parcours en un clic</h2>
    <ul class="ticks lead" style="color:var(--ink)">
      <li>Les supports de cours et les modèles d'automatisation</li>
      <li>Les replays des masterclass</li>
      <li>Les liens des prochaines visios</li>
      <li>Votre progression dans le Parcours Intégrateur</li>
    </ul>
  </div>
  <div class="panel">
    <h3>Ouverture prochainement</h3>
    <p class="muted">Laissez votre adresse : nous vous envoyons vos identifiants dès l'ouverture.</p>
    <form class="stack-form" data-form="espace" data-success="Merci, nous vous écrirons dès l'ouverture de l'espace.">
      <label for="esp-mail">Votre e-mail</label>
      <input id="esp-mail" name="email" type="email" required autocomplete="email">
      <button class="btn" type="submit">Être prévenu</button>
      <p class="msg" data-msg hidden role="status"></p>
    </form>
  </div>
</div>
</section>
''')

# ---------------------------------------------------------------- 404
PAGES['404'] = ('Page introuvable', "Cette page n'existe pas ou a été déplacée.",
hero('Erreur 404', 'Cette page a pris un jour de congé', "Elle n'existe pas ou a été déplacée. Le reste du site, lui, est bien là.", '<a class="btn amber" href="/">Retour à l\'accueil</a>'))


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, 'assets'), os.path.join(OUT, 'assets'))
    for f in ('favicon.svg', 'robots.txt'):
        shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))
    for slug, (title, desc, body) in PAGES.items():
        html = layout(slug, title, desc, body)
        if slug == '404':
            html = html.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/').replace('href="favicon.svg"', 'href="/favicon.svg"')
        with open(os.path.join(OUT, f'{slug}.html'), 'w', encoding='utf-8') as fh:
            fh.write(html)
    print('Pages :', len(PAGES))


if __name__ == '__main__':
    main()
