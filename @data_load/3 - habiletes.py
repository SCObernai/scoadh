
from hab.models import *


# Sports

ski=Sport(nom="Ski Alpin", slug="skialpin")
ski.save()

snow=Sport(nom="Snow", slug="snow")
snow.save()

fond=Sport(nom="Ski de fond", slug="fond")
fond.save()

herbe=Sport(nom="Ski sur herbe", slug="herbe")
herbe.save()

# Systemes de notation

skesf=SystemeNotation(nom="Ski ESF", slug="skiesf", sport=ski)
skesf.save()

snesf=SystemeNotation(nom="Snow ESF", slug="snowesf", sport=snow)
snesf.save()

desc='''En ski alpin, les « CASQUES » symbolisent la progression \
nécessaire pour atteindre tes objectifs de pratique.

Pour être un bon skieur, il faut passer par des étapes essentielles \
dans l’apprentissage des habilités techniques, physiques, mentales et \
comportementales.

Après un temps de pratique, le skieur est donc appelé à évaluer ses acquis.

La validation du « CASQUE » constitue un moment particulier : 
il te permet de faire le point sur ta pratique et de te donner des axes de progression.

Les couleurs de casque balisent tes progrès de manière continue (sans examen), \
pour développer confiance en soi et plaisir de skier. 
Ils sont validés par les moniteurs et entraîneurs de la Fédération Française de Ski.

Les Pass’Neige correspondent à une approche éducative commune à toutes les disciplines \
et pratiques (loisir et compétition) de notre fédération.'''
casques=SystemeNotation(nom="Casques FFS", slug="casques", description=desc,  sport=ski)
casques.save()

boards=SystemeNotation(nom="Boards FFS", slug="boards", sport=snow)
boards.save()



# Niveau sportif

casque_Blanc=NiveauSportif.objects.create(nom="Casque Blanc", slug="casqueblanc", systeme=casques)
casque_Jaune=NiveauSportif.objects.create(nom="Casque Jaune", slug="casquejaune", systeme=casques)
casque_Orange=NiveauSportif.objects.create(nom="Casque Orange", slug="casqueorange", systeme=casques)
casque_Vert=NiveauSportif.objects.create(nom="Casque Vert", slug="casquevert", systeme=casques)
casque_Bleu=NiveauSportif.objects.create(nom="Casque Bleu", slug="casquebleu", systeme=casques)
casque_Rouge=NiveauSportif.objects.create(nom="Casque Rouge", slug="casquerouge", systeme=casques)
casque_Noir=NiveauSportif.objects.create(nom="Casque Noir", slug="casquenoir", systeme=casques)

hier_casques:dict[str,list[NiveauSportif]]={
    "blanc":[casque_Blanc],
    "jaune":[casque_Jaune],#, casque_Blanc],
    "orange":[casque_Orange],#, casque_Jaune, casque_Blanc],
    "vert":[casque_Vert],#, casque_Orange, casque_Jaune, casque_Blanc],
    "bleu":[casque_Bleu],#, casque_Vert, casque_Orange, casque_Jaune, casque_Blanc],
    "rouge":[casque_Rouge],#, casque_Bleu, casque_Vert, casque_Orange, casque_Jaune, casque_Blanc],
    "noir":[casque_Noir],#, casque_Rouge, casque_Bleu, casque_Vert, casque_Orange, casque_Jaune, casque_Blanc],
}

def affecte_hab_casque(habilete:Habilete, casque:str):
    lst:list[NiveauSportif]=hier_casques.get(casque)
    nv:NiveauSportif
    for nv in lst:
        nv.habiletes.add(habilete)

esf_Flocon=NiveauSportif.objects.create(nom="Flocon", slug="esfflocon", systeme=skesf)
esf_1ereEtoile=NiveauSportif.objects.create(nom="1 ère Étoile", slug="esf1etoile", systeme=skesf)
esf_2emeEtoile=NiveauSportif.objects.create(nom="2 ème Étoile", slug="esf2etoile", systeme=skesf)
esf_3emeEtoile=NiveauSportif.objects.create(nom="3 ème Étoile", slug="esf3etoile", systeme=skesf)
esf_Bronze=NiveauSportif.objects.create(nom="Étoile de Bronze", slug="esfbronze", systeme=skesf)
esf_Or=NiveauSportif.objects.create(nom="Étoile d'Or", slug="esfor", systeme=skesf)

hier_esf:dict[str,list[NiveauSportif]]={
    "flocon":[esf_Flocon],
    "1ere":[esf_1ereEtoile],#, esf_Flocon],
    "2eme":[esf_2emeEtoile],#, esf_1ereEtoile, esf_Flocon],
    "3eme":[esf_3emeEtoile],#, esf_2emeEtoile, esf_1ereEtoile, esf_Flocon],
    "bronze":[esf_Bronze],#, esf_3emeEtoile, esf_2emeEtoile, esf_1ereEtoile, esf_Flocon],
    "rouge":[esf_Or],#, esf_Bronze, esf_3emeEtoile, esf_2emeEtoile, esf_1ereEtoile, esf_Flocon]
}

def affecte_hab_esf(habilete:Habilete, nivesf:str):
    lst:list[NiveauSportif]=hier_esf.get(nivesf)
    nv:NiveauSportif
    for nv in lst:
        nv.habiletes.add(habilete)



# Types habiletés

nomi='Techniques'
desc='''L’objectif central est d’adapter ses appuis aux situations de ski qui ne \
sont jamais identiques pour permettre de créer une trajectoire tout en laissant le ski glisser.\

C’est un jeu de combinaisons des habiletés ci-dessous qui permet d’atteindre cet objectif.'''
typehab_tech=TypeHabilete.objects.create(nom=nomi, description=desc, slug=slugify(nomi))
nomi='Comportementales'
typehab_comp=TypeHabilete.objects.create(nom=nomi, slug=slugify(nomi))
nomi='Physiques'
typehab_phys=TypeHabilete.objects.create(nom=nomi, slug=slugify(nomi))
nomi='Mentales'
typehab_ment=TypeHabilete.objects.create(nom=nomi, slug=slugify(nomi))

# Domaines habiletés

curtyp=typehab_tech
nomi='Gestion des inclinaisons'
desc="Gérer des déséquilibres latéraux et antéro-postérieur (l’engagement, la prise de carre…)"
dom_tech_1=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Gestion de la charge'
desc="Gérer des forces de contact ski-neige (jeu vertical, mobilité, contraction musculaire…)"
dom_tech_2=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Gestion des rotations'
desc="Dissocier et disponibilité du haut du corps (gainage, vissage, contre-vissage…)"
dom_tech_3=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Ligne de course/adaptation'
desc="Fluidité, temporalité et perception/adaptation à l’environnement"
dom_tech_4=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)

curtyp=typehab_comp
nomi='Nutrition et hydratation'
desc="Adapter ses besoins alimentaires à son effort"
dom_comp_1=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Hygiène de vie'
desc="Prendre soin de soi et conserver sa bonne santé"
dom_comp_2=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Echauffement / étirements'
desc="Savoir se préparer ou récupérer d’un effort physique"
dom_comp_3=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Matériel'
desc="Choisir, entretenir et préparer son matériel"
dom_comp_4=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Prévention santé'
desc="Tests simples de suivi de santé"
dom_comp_5=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)

curtyp=typehab_phys
nomi='Capacités athlétiques'
desc="Développement énergétique et de propulsion"
dom_phys_1=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Capacités gymniques'
desc="Perception et gestion de l’espace"
dom_phys_2=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Placements'
desc="Posture, préservation articulaire et développement de la force"
dom_phys_3=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Adresse / tâches'
desc="Adaptation motrice fine à la tâche"
dom_phys_4=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)

curtyp=typehab_ment
nomi='Motivation'
desc="Ce qui pousse à skier, à faire du sport"
dom_ment_1=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Perceptions'
desc="Prendre les informations sur l’environnement (piste, relief, neige...)"
dom_ment_2=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Engagement dans l’activité'
desc="Gérer la balance sécurité/risque"
dom_ment_3=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Emotions'
desc="Gérer ses états affectifs (peur, joie, dégout, tristesse, surprise, colère) pour mieux progresser"
dom_ment_4=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)
nomi='Imagerie mentale'
desc="Capacité à s’imaginer percevoir une situation (avant ou après une tâche, d’un point de vue intérieur ou extérieur)"
dom_ment_5=DomaineHabilete.objects.create(nom=nomi, slug=slugify(nomi), description=desc, type_habilete=curtyp)

# Habiletes
def creat_hab(dom_tech:DomaineHabilete, nom:str, desc:str, niv_casq:str, niv_esf:str|None=None):
    habilete=Habilete.objects.create(nom=nom[0:49], slug=slugify(nom[0:49]), 
        description=desc, sport=ski, domaine=dom_tech)
    affecte_hab_casque(habilete, niv_casq)
    if niv_esf is not None:
        affecte_hab_esf(habilete, niv_esf) 



# ========= TECH

# ------ CASQUE BLANC
niv_casq="blanc"

cur_dom=dom_tech_1
niv_esf="flocon"
creat_hab(cur_dom, "1 virage en remontant piste", "Faire un virage en remontant la piste", niv_casq, niv_esf)
creat_hab(cur_dom, "Avancer ski divergents sans bâton", "Dans une légère montée, avancer les skis divergents sans bâton",  niv_casq, niv_esf)
niv_esf="1ere"
creat_hab(cur_dom, "En schuss, appui languette et tige", "Maintenir une recherche de vitesse sur pente très faible. Alterner appui languette et appui tige arrière de la chaussure",   niv_casq, niv_esf)

cur_dom=dom_tech_2
niv_esf="flocon"
creat_hab(cur_dom, "Faire un tour entier G/D", "Sur le plat et sur place, faire un tour entier vers la gauche puis vers la droite",    niv_casq, niv_esf)
niv_esf="2eme"
creat_hab(cur_dom, "Dérapage en biais avec 3 arrêts", "Traverser une piste en dérapage et en biais avec 3 arrêts",    niv_casq, niv_esf)
creat_hab(cur_dom, "Virages moyens en regardant en bas", "Enchaîner des virages moyens et regarder en bas de la piste tout le long des virages",   niv_casq, niv_esf)

cur_dom=dom_tech_3
niv_esf="1ere"
creat_hab(cur_dom, "Dans traversée, 4 sauts verticaux", "Dans une traversée, enchaîner 4 sauts verticaux",   niv_casq, niv_esf)
niv_esf="2eme"
creat_hab(cur_dom, "Déraper skis parallèles, s'arrêter aux répères", "Dans un couloir, déraper skis parallèles en travers de la pente puis s’arrêter aux repères",    niv_casq, niv_esf)
niv_esf="1ere"
creat_hab(cur_dom, "Lever le pied aval / amont", "Dans une traversée, lever le pied aval puis le pied amont",    niv_casq, niv_esf)

cur_dom=dom_tech_4
niv_esf="flocon"
creat_hab(cur_dom, "Se relever dans pente sur du plat", "Se relever dans une pente moyenne dans différentes positions des skis",    niv_casq, niv_esf)
creat_hab(cur_dom, "Chausser ses skis dans pente", "Chausser ses skis dans une pente faible",   niv_casq, niv_esf)



# ------ CASQUE JAUNE
niv_casq="jaune"

cur_dom=dom_tech_1
niv_esf="3eme"
creat_hab(cur_dom, "4 grands virages skis parallèles", "Enchaîner 4 grands virages les skis parallèles sur une piste verte", niv_casq, niv_esf)
niv_esf="1ere"
creat_hab(cur_dom, "Feuille morte", "Faire la feuille morte dans un slalom rectiligne", niv_casq, niv_esf)

cur_dom=dom_tech_2
niv_esf="bronze"
creat_hab(cur_dom, "6 petits virages sautés", "Enchaîner 6 petits virages sautés sur une piste bleue", niv_casq, niv_esf)
creat_hab(cur_dom, "360° glissés G/D", "Faire un 360° glissé de chaque côté sur une piste verte. Prendre l’élan suffisant", niv_casq, niv_esf)

cur_dom=dom_tech_3
niv_esf="2eme"
creat_hab(cur_dom, "Décoler sur une bosse", "Passer une bosse avec prise d’élan, provoquant un décollement des skis, tout en restant équilibré", niv_casq, niv_esf)
niv_esf="3eme"
creat_hab(cur_dom, "Sauter par dessus 3 obstacles", "Être capable de sauter par-dessus un piquet en travers. Enchaîner 3 sauts", niv_casq, niv_esf)

cur_dom=dom_tech_4
niv_esf="2eme"
creat_hab(cur_dom, "8 petits virages, même rythme", "Enchaîner 8 petits virages avec le même rythme", niv_casq, niv_esf)
creat_hab(cur_dom, "Réaliser un parcours technique imposé", "Réaliser un parcours technique imposé avec des rayons de courbe variés sur piste balisée adaptée", niv_casq, niv_esf)


# ------ CASQUE ORANGE
niv_casq="orange"

cur_dom=dom_tech_1
niv_esf="bronze"
creat_hab(cur_dom, "Skier arrière, trace directe", "Skier en arrière, en trace directe", niv_casq, niv_esf)
niv_esf="1ere"
creat_hab(cur_dom, "3 pas tournants vers l'amont", "Enchaîner 3 pas tournants vers l’amont", niv_casq, niv_esf)
niv_esf="2eme"
creat_hab(cur_dom, "Maintenir un schuss trace directe", "Maintenir une position de recherche de vitesse, en trace directe sur pente faible", niv_casq, niv_esf)

cur_dom=dom_tech_2
niv_esf="3eme"
creat_hab(cur_dom, "4 virages complets vers l'amont", "Enchaîner 4 virages complets vers l’amont (arriver face vers l’amont se retourner en faisant des petits pas sur le côté), sur piste verte ou bleue", niv_casq, niv_esf)
creat_hab(cur_dom, "Alterner 4 traces directes et 4 dérapages arrêt complet", "Face à la pente, alterner 4 traces directes et 4 dérapages avec arrêt complet", niv_casq, niv_esf)

cur_dom=dom_tech_3
niv_esf="3eme"
creat_hab(cur_dom, "Passer une bosse/whoops sans décoller", "Passer une bosse ou des whoops tout en gardant le contact « ski-neige »", niv_casq, niv_esf)
niv_esf="1ere"
creat_hab(cur_dom, "Pas de patineur, batons en guidon et perpendiculaires au ski qui glisse", "Dans une légère montée, avancer en pas de patineur avec les bâtons en guidon et perpendiculaires au ski qui glisse", niv_casq, niv_esf)

cur_dom=dom_tech_4
niv_esf="bronze"
creat_hab(cur_dom, "10 portes de GS en plumeaux", "Sur pente et neige facile, enchaîner, sans perdre le rythme ni la ligne, 10 portes simples de GS matérialisées par des boys ou des plumeaux", niv_casq, niv_esf)
niv_esf="2eme"
creat_hab(cur_dom, "Skier dans des conditions changeantes", "Skier dans des conditions changeantes : qualité de neige et/ou variation de pente", niv_casq, niv_esf)




# ------ CASQUE VERT
niv_casq="vert"

cur_dom=dom_tech_1
niv_esf="flocon"
creat_hab(cur_dom, "", "", niv_casq, niv_esf)
creat_hab(cur_dom, "", "", niv_casq, niv_esf)
creat_hab(cur_dom, "", "", niv_casq, niv_esf)

cur_dom=dom_tech_2
niv_esf="flocon"
creat_hab(cur_dom, "", "", niv_casq, niv_esf)
creat_hab(cur_dom, "", "", niv_casq, niv_esf)

cur_dom=dom_tech_3
niv_esf="flocon"
creat_hab(cur_dom, "", "", niv_casq, niv_esf)
creat_hab(cur_dom, "", "", niv_casq, niv_esf)
creat_hab(cur_dom, "", "", niv_casq, niv_esf)

cur_dom=dom_tech_4
niv_esf="flocon"
creat_hab(cur_dom, "", "", niv_casq, niv_esf)
creat_hab(cur_dom, "", "", niv_casq, niv_esf)




# ------ CASQUE ROUGE
niv_casq="rouge"

cur_dom=dom_tech_1
niv_esf="flocon"
creat_hab(cur_dom, "", "", niv_casq, niv_esf)
creat_hab(cur_dom, "", "", niv_casq, niv_esf)

cur_dom=dom_tech_2
niv_esf="flocon"
creat_hab(cur_dom, "", "", niv_casq, niv_esf)
creat_hab(cur_dom, "", "", niv_casq, niv_esf)

cur_dom=dom_tech_3
niv_esf="flocon"
creat_hab(cur_dom, "", "", niv_casq, niv_esf)
creat_hab(cur_dom, "", "", niv_casq, niv_esf)

cur_dom=dom_tech_4
niv_esf="flocon"
creat_hab(cur_dom, "", "", niv_casq, niv_esf)
creat_hab(cur_dom, "", "", niv_casq, niv_esf)







# ========= COMP

# ------ CASQUE BLANC
niv_casq="blanc"

niv_esf=None
cur_dom=dom_comp_1
creat_hab(cur_dom, "Casse-croute", "Avoir un en-cas dans la poche pour se ravitailler",   niv_casq, niv_esf)
cur_dom=dom_comp_2
creat_hab(cur_dom, "Activité Physique", "Faire une activité physique selon ses besoins",  niv_casq, niv_esf)
cur_dom=dom_comp_3
creat_hab(cur_dom, "Echauffement 1", "S’échauffer, guidé par l’entraîneur",   niv_casq, niv_esf)
cur_dom=dom_comp_4
creat_hab(cur_dom, "Gérer son matériel", "Gèrer tout seul son matériel : le repérer, le rassembler, le porter, le préserver, serrer ses chaussures", niv_casq, niv_esf)





#creat_hab(cur_dom, "", "critères",  niveaux)


