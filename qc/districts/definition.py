# coding: utf-8
from __future__ import unicode_literals

from datetime import date

from unidecode import unidecode

import boundaries

# Generated by sets.rb
sets = {
    48028: ["Acton Vale", "districts"],
    31056: ["Adstock", "districts"],
    92030: ["Albanel", "districts"],
    93042: ["Alma", "districts"],
    78070: ["Amherst", "districts"],
    7047: ["Amqui", "districts"],
    55008: ["Ange-Gardien", "districts"],
    96020: ["Baie-Comeau", "districts"],
    16013: ["Baie-Saint-Paul", "districts"],
    88022: ["Barraute", "districts"],
    66107: ["Beaconsfield", "districts"],
    27028: ["Beauceville", "districts"],
    70022: ["Beauharnois", "districts"],
    19105: ["Beaumont", "districts"],
    57040: ["Beloeil", "districts"],
    52035: ["Berthierville", "districts"],
    73015: ["Blainville", "districts"],
    73005: ["Boisbriand", "districts"],
    21045: ["Boischatel", "districts"],
    58033: ["Boucherville", "districts"],
    46078: ["Bromont", "districts"],
    58007: ["Brossard", "districts"],
    76043: ["Brownsburg-Chatham", "districts"],
    67020: ["Candiac", "districts"],
    82020: ["Cantley", "districts"],
    4047: ["Cap-Chat", "districts"],
    34030: ["Cap-Santé", "districts"],
    57010: ["Carignan", "districts"],
    7018: ["Causapscal", "districts"],
    57005: ["Chambly", "districts"],
    2028: ["Chandler", "districts"],
    60005: ["Charlemagne", "districts"],
    67050: ["Châteauguay", "districts"],
    82025: ["Chelsea", "districts"],
    62047: ["Chertsey", "districts"],
    15035: ["Clermont", "districts"],
    42110: ["Cleveland", "districts"],
    3010: ["Cloridorme", "districts"],
    44071: ["Compton", "districts"],
    59035: ["Contrecoeur", "districts"],
    41038: ["Cookshire-Eaton", "districts"],
    66058: ["Côte-Saint-Luc", "districts"],
    71040: ["Coteau-du-Lac", "districts"],
    72010: ["Deux-Montagnes", "districts"],
    66142: ["Dollard-Des Ormeaux", "districts"],
    # Municipality has names. DGEQ doesn't.
    # 66087: ["Dorval", "districts"],
    49058: ["Drummondville", "districts"],
    46050: ["Dunham", "districts"],
    31122: ["East Broughton", "districts"],
    46112: ["Farnham", "districts"],
    22010: ["Fossambault-sur-le-Lac", "districts"],
    30025: ["Frontenac", "districts"],
    81017: ["Gatineau", "districts"],
    47017: ["Granby", "districts"],
    93020: ["Hébertville", "districts"],
    71100: ["Hudson", "districts"],
    61025: ["Joliette", "districts"],
    # Municipality has names. DGEQ doesn't.
    # 66102: ["Kirkland", "districts"],
    23057: ["L'Ancienne-Lorette", "districts"],
    82005: ["L'Ange-Gardien", "districts"],
    93065: ["L'Ascension-de-Notre-Seigneur", "districts"],
    60028: ["L'Assomption", "districts"],
    60035: ["L'Épiphanie", "districts"],
    71060: ["L'Île-Perrot", "districts"],
    17078: ["L'Islet", "districts"],
    15013: ["La Malbaie", "districts"],
    82035: ["La Pêche", "districts"],
    67015: ["La Prairie", "districts"],
    90012: ["La Tuque", "districts"],
    7057: ["Lac-au-Saumon", "districts"],
    46075: ["Lac-Brome", "districts"],
    79078: ["Lac-des-Écorces", "districts"],
    77055: ["Lac-des-Seize-Îles", "districts"],
    30030: ["Lac-Mégantic", "districts"],
    22015: ["Lac-Saint-Joseph", "districts"],
    78095: ["Lac-Supérieur", "districts"],
    76020: ["Lachute", "districts"],
    52017: ["Lanoraie", "districts"],
    65005: ["Laval", "districts"],
    52007: ["Lavaltrie", "districts"],
    67055: ["Léry", "districts"],
    71050: ["Les Cèdres", "districts"],
    71033: ["Les Coteaux", "districts"],
    1023: ["Les Îles-de-la-Madeleine", "districts"],
    25213: ["Lévis", "districts"],  # district names from the city's shapefile are not extant
    58227: ["Longueuil", "districts"],
    32065: ["Lyster", "districts"],
    87058: ["Macamic", "districts"],
    45072: ["Magog", "districts"],
    89015: ["Malartic", "districts"],
    52095: ["Mandeville", "districts"],
    55048: ["Marieville", "districts"],
    64015: ["Mascouche", "districts"],
    8053: ["Matane", "districts"],
    57025: ["McMasterville", "districts"],
    67045: ["Mercier", "districts"],
    93012: ["Métabetchouan—Lac-à-la-Croix", "districts"],
    74005: ["Mirabel", "districts"],
    9077: ["Mont-Joli", "districts"],
    66072: ["Mont-Royal", "districts"],
    57035: ["Mont-Saint-Hilaire", "districts"],
    78102: ["Mont-Tremblant", "districts"],
    78055: ["Montcalm", "districts"],
    18050: ["Montmagny", "districts"],
    66023: ["Montréal", "districts"],
    66007: ["Montréal-Est", "districts"],
    30045: ["Nantes", "districts"],
    71065: ["Notre-Dame-de-l'Île-Perrot", "districts"],
    30010: ["Notre-Dame-des-Bois", "districts"],
    61030: ["Notre-Dame-des-Prairies", "districts"],
    37235: ["Notre-Dame-du-Mont-Carmel", "districts"],
    72032: ["Oka", "districts"],
    57030: ["Otterburn Park", "districts"],
    2005: ["Percé", "districts"],
    71070: ["Pincourt", "districts"],
    32040: ["Plessisville", "districts"],
    96030: ["Pointe-aux-Outardes", "districts"],
    72020: ["Pointe-Calumet", "districts"],
    66097: ["Pointe-Claire", "districts"],
    96025: ["Pointe-Lebel", "districts"],
    82030: ["Pontiac", "districts"],
    2047: ["Port-Daniel—Gascons", "districts"],
    75040: ["Prévost", "districts"],
    32033: ["Princeville", "districts"],
    23027: ["Québec", "districts"],
    96040: ["Ragueneau", "districts"],
    62037: ["Rawdon", "districts"],
    60013: ["Repentigny", "districts"],
    55057: ["Richelieu", "districts"],
    42098: ["Richmond", "districts"],
    71133: ["Rigaud", "districts"],
    10043: ["Rimouski", "districts"],
    12072: ["Rivière-du-Loup", "districts"],
    55037: ["Rougemont", "districts"],
    86042: ["Rouyn-Noranda", "districts"],
    47047: ["Roxton Pond", "districts"],
    94068: ["Saguenay", "districts"],
    33045: ["Saint-Agapit", "districts"],
    62025: ["Saint-Alphonse-Rodriguez", "districts"],
    94255: ["Saint-Ambroise", "districts"],
    61040: ["Saint-Ambroise-de-Kildare", "districts"],
    76008: ["Saint-André-d'Argenteuil", "districts"],
    69070: ["Saint-Anicet", "districts"],
    12015: ["Saint-Antonin", "districts"],
    17055: ["Saint-Aubert", "districts"],
    23072: ["Saint-Augustin-de-Desmaures", "districts"],
    34038: ["Saint-Basile", "districts"],
    57020: ["Saint-Basile-le-Grand", "districts"],
    93030: ["Saint-Bruno", "districts"],
    85045: ["Saint-Bruno-de-Guigues", "districts"],
    58037: ["Saint-Bruno-de-Montarville", "districts"],
    63055: ["Saint-Calixte", "districts"],
    55023: ["Saint-Césaire", "districts"],
    19097: ["Saint-Charles-de-Bellechasse", "districts"],
    39060: ["Saint-Christophe-d'Arthabaska", "districts"],
    69017: ["Saint-Chrysostome", "districts"],
    42100: ["Saint-Claude", "districts"],
    75005: ["Saint-Colomban", "districts"],
    29057: ["Saint-Côme—Linière", "districts"],
    67035: ["Saint-Constant", "districts"],
    49070: ["Saint-Cyrille-de-Wendover", "districts"],
    54017: ["Saint-Damase", "districts"],
    62075: ["Saint-Damien", "districts"],
    94245: ["Saint-David-de-Falardeau", "districts"],
    42025: ["Saint-Denis-de-Brompton", "districts"],
    54060: ["Saint-Dominique", "districts"],
    62060: ["Saint-Donat", "districts"],
    63030: ["Saint-Esprit", "districts"],
    72005: ["Saint-Eustache", "districts"],
    10070: ["Saint-Fabien", "districts"],
    78047: ["Saint-Faustin—Lac-Carré", "districts"],
    62007: ["Saint-Félix-de-Valois", "districts"],
    32013: ["Saint-Ferdinand", "districts"],
    21010: ["Saint-Ferréol-les-Neiges", "districts"],
    33052: ["Saint-Flavien", "districts"],
    42020: ["Saint-François-Xavier-de-Brompton", "districts"],
    94235: ["Saint-Fulgence", "districts"],
    52080: ["Saint-Gabriel", "districts"],
    93035: ["Saint-Gédéon", "districts"],
    29073: ["Saint-Georges", "districts"],
    49048: ["Saint-Germain-de-Grantham", "districts"],
    19068: ["Saint-Henri", "districts"],
    93070: ["Saint-Henri-de-Taillon", "districts"],
    94240: ["Saint-Honoré", "districts"],
    54048: ["Saint-Hyacinthe", "districts"],
    52045: ["Saint-Ignace-de-Loyola", "districts"],
    26063: ["Saint-Isidore", "districts"],
    57033: ["Saint-Jean-Baptiste", "districts"],
    56083: ["Saint-Jean-sur-Richelieu", "districts"],
    75017: ["Saint-Jérôme", "districts"],
    27043: ["Saint-Joseph-de-Beauce", "districts"],
    72025: ["Saint-Joseph-du-Lac", "districts"],
    58012: ["Saint-Lambert", "districts"],
    71105: ["Saint-Lazare", "districts"],
    50042: ["Saint-Léonard-d'Aston", "districts"],
    63048: ["Saint-Lin—Laurentides", "districts"],
    70035: ["Saint-Louis-de-Gonzague", "districts"],
    57045: ["Saint-Mathieu-de-Beloeil", "districts"],
    37230: ["Saint-Maurice", "districts"],
    68050: ["Saint-Michel", "districts"],
    93045: ["Saint-Nazaire", "districts"],
    67010: ["Saint-Philippe", "districts"],
    54008: ["Saint-Pie", "districts"],
    72043: ["Saint-Placide", "districts"],
    68055: ["Saint-Rémi", "districts"],
    63035: ["Saint-Roch-de-l'Achigan", "districts"],
    15058: ["Saint-Siméon", "districts"],
    70040: ["Saint-Stanislas-de-Kostka", "districts"],
    61027: ["Saint-Thomas", "districts"],
    35027: ["Saint-Tite", "districts"],
    16055: ["Saint-Urbain", "districts"],
    71025: ["Saint-Zotique", "districts"],
    77022: ["Sainte-Adèle", "districts"],
    66117: ["Sainte-Anne-de-Bellevue", "districts"],
    53065: ["Sainte-Anne-de-Sorel", "districts"],
    4037: ["Sainte-Anne-des-Monts", "districts"],
    73035: ["Sainte-Anne-des-Plaines", "districts"],
    22045: ["Sainte-Brigitte-de-Laval", "districts"],
    67030: ["Sainte-Catherine", "districts"],
    45060: ["Sainte-Catherine-de-Hatley", "districts"],
    22005: ["Sainte-Catherine-de-la-Jacques-Cartier", "districts"],
    19055: ["Sainte-Claire", "districts"],
    68020: ["Sainte-Clotilde", "districts"],
    52040: ["Sainte-Geneviève-de-Berthier", "districts"],
    59010: ["Sainte-Julie", "districts"],
    63060: ["Sainte-Julienne", "districts"],
    72015: ["Sainte-Marthe-sur-le-Lac", "districts"],
    61050: ["Sainte-Mélanie", "districts"],
    75028: ["Sainte-Sophie", "districts"],
    73010: ["Sainte-Thérèse", "districts"],
    2010: ["Sainte-Thérèse-de-Gaspé", "districts"],
    70052: ["Salaberry-de-Valleyfield", "districts"],
    66127: ["Senneville", "districts"],
    97007: ["Sept-Îles", "districts"],
    36033: ["Shawinigan", "districts"],
    43027: ["Sherbrooke", "districts"],
    53052: ["Sorel-Tracy", "districts"],
    13073: ["Témiscouata-sur-le-Lac", "districts"],
    64008: ["Terrebonne", "districts"],
    31084: ["Thetford Mines", "districts"],
    37067: ["Trois-Rivières", "districts"],
    89008: ["Val-d'Or", "districts"],
    78010: ["Val-David", "districts"],
    82015: ["Val-des-Monts", "districts"],
    59020: ["Varennes", "districts"],
    71083: ["Vaudreuil-Dorion", "districts"],
    59025: ["Verchères", "districts"],
    39062: ["Victoriaville", "districts"],
    47025: ["Waterloo", "districts"],
    41098: ["Weedon", "districts"],
    77060: ["Wentworth-Nord", "districts"],
    66032: ["Westmount", "districts"],
    46080: ["Cowansville", "quartiers"],
    67025: ["Delson", "quartiers"],
    93005: ["Desbiens", "quartiers"],
    3005: ["Gaspé", "quartiers"],
    2015: ["Grande-Rivière", "quartiers"],
    69055: ["Huntingdon", "quartiers"],
    87090: ["La Sarre", "quartiers"],
    34120: ["Lac-Sergent", "quartiers"],
    83065: ["Maniwaki", "quartiers"],
    13095: ["Pohénégamook", "quartiers"],
    53050: ["Saint-Joseph-de-Sorel", "quartiers"],
    89040: ["Senneterre", "quartiers"],
    11040: ["Trois-Pistoles", "quartiers"],
}


def namer(f):
    if f.get('CO_MUNCP') == 23027:  # Québec
        return {
            'Cap-Rouge-Laurentien': 'Cap-Rouge—Laurentien',
            'La Chute-Montmorency-Seigneurial': 'La Chute-Montmorency—Seigneurial',
            'Lac-Saint-Charles-Saint-Émile': 'Lac-Saint-Charles—Saint-Émile',
            'Montcalm-Saint-Sacrement': 'Montcalm—Saint-Sacrement',
            'Monts': 'Les Monts',
            'Plateau': 'Le Plateau',
            'Pointe-de-Sainte-Foy': 'La Pointe-de-Sainte-Foy',
            'Saint-Louis-Sillery': 'Saint-Louis—Sillery',
            'Saint-Roch-Saint-Sauveur': 'Saint-Roch—Saint-Sauveur',
        }.get(f.get('NM_DIS'), f.get('NM_DIS'))
    elif f.get('CO_MUNCP') == 58227:  # Longueuil
        return re.sub(r"\b(?:d'|de |du |des )", '', f.get('NM_DIS'))
    elif f.get('CO_MUNCP') == 66097:  # Pointe-Claire
        return f.get('NM_DIS').replace('/ ', '/')
    elif f.get('CO_MUNCP') == 81017:  # Gatineau
        return {
            'de Hull-Val-Tétreau': 'de Hull—Val-Tétreau',
            'de Saint-Raymond-Vanier': 'de Saint-Raymond—Vanier',
            'de Wright-Parc-de-la-Montagne': 'Wright—Parc-de-la-Montagne',
            'du Plateau-Manoir-des-Trembles': 'du Plateau—Manoir-des-Trembles',
        }.get(f.get('NM_DIS'), f.get('NM_DIS'))
    else:
        if f.get('NM_DIS'):
            return f.get('NM_DIS')
        elif f.get('MODE_SUFRG') == 'Q':
            return 'Quartier %s' % int(f.get('NO_DIS'))
        else:
            return 'District %s' % int(f.get('NO_DIS'))


def ider(f):
    if f.get('CO_MUNCP') in (43027, 66023):  # Sherbrooke, Montréal
        return '%d' % (int(f.get('NO_DIS') * 10))
    else:
        return int(f.get('NO_DIS'))

for geographic_code, (name, type) in sets.items():
    boundaries.register('%s %s' % (name, type),
        file='%s-24%05d.shp' % (unidecode(name), geographic_code),
        domain='%s, QC' % name,
        last_updated=date(2014, 2, 28),
        name_func=namer,
        id_func=ider,
        authority='Directeur général des élections du Québec',
        licence_url='http://www.electionsquebec.qc.ca/francais/conditions-d-utilisation-de-notre-site-web.php',
        encoding='iso-8859-1',
        metadata={'geographic_code': '24%05d' % geographic_code},
        ogr2ogr='''-where "CO_MUNCP='%d'"''' % geographic_code,
        base_file='Districts Elec Mun 2014-02-28_DetU_region.shp',
    )

boundaries.register('Paroisse de Plessisville districts',
    file='Plessisville-2432045.shp',
    domain='Plessisville, QC',
    last_updated=date(2014, 2, 28),
    name_func=namer,
    id_func=ider,
    authority='Directeur général des élections du Québec',
    licence_url='http://www.electionsquebec.qc.ca/francais/conditions-d-utilisation-de-notre-site-web.php',
    encoding='iso-8859-1',
    metadata={'geographic_code': '2432045'},
    ogr2ogr='''-where "CO_MUNCP='32045'"''',
    base_file='Districts Elec Mun 2014-02-28_DetU_region.shp',
)

municipalities_with_boroughs = [
    {
        'name': 'Lévis',
        'geographic_code': 25213,
        'boroughs': {
            'ocd-division/country:ca/csd:2425213/borough:1': ['Desjardins', 'DESJARDINS'],
            'ocd-division/country:ca/csd:2425213/borough:2': ['Les Chutes-de-la-Chaudière-Est', 'LESCHUTESDELACHAUDIEREEST'],
            'ocd-division/country:ca/csd:2425213/borough:3': ['Les Chutes-de-la-Chaudière-Ouest', 'LESCHUTESDELACHAUDIEREOUEST'],
        },
    },
    {
        'name': 'Longueuil',
        'geographic_code': 58227,
        'boroughs': {
            'ocd-division/country:ca/csd:2458227/borough:1': ['Le Vieux-Longueuil', 'LEVIEUXLONGUEUIL'],
            'ocd-division/country:ca/csd:2458227/borough:2': ['Greenfield Park', 'GREENFIELDPARK'],
            'ocd-division/country:ca/csd:2458227/borough:3': ['Saint-Hubert', 'SAINTHUBERT'],
        },
    },
    {
        'name': 'Montréal',
        'geographic_code': 66023,
        'boroughs': {
            'ocd-division/country:ca/csd:2466023/borough:ahuntsic-cartierville': ["Ahuntsic-Cartierville", 'AHUNTSICCARTIERVILLE'],
            'ocd-division/country:ca/csd:2466023/borough:anjou': ["Anjou", 'ANJOU'],
            'ocd-division/country:ca/csd:2466023/borough:côte-des-neiges~notre-dame-de-grâce': ["Côte-des-Neiges—Notre-Dame-de-Grâce", 'COTEDESNEIGESNOTREDAMEDEGRACE'],
            'ocd-division/country:ca/csd:2466023/borough:lachine': ["Lachine", 'LACHINE'],
            'ocd-division/country:ca/csd:2466023/borough:lasalle': ["LaSalle", 'LASALLE'],
            'ocd-division/country:ca/csd:2466023/borough:le_plateau-mont-royal': ["Le Plateau-Mont-Royal", 'LEPLATEAUMONTROYAL'],
            'ocd-division/country:ca/csd:2466023/borough:le_sud-ouest': ["Le Sud-Ouest", 'LESUDOUEST'],
            'ocd-division/country:ca/csd:2466023/borough:l~île-bizard~sainte-geneviève': ["L'Île-Bizard—Sainte-Geneviève", 'LILEBIZARDSAINTGENEVIEVE'],
            'ocd-division/country:ca/csd:2466023/borough:mercier~hochelaga-maisonneuve': ["Mercier—Hochelaga-Maisonneuve", 'MERCIERHOCHELAGAMAISONNEUVE'],
            'ocd-division/country:ca/csd:2466023/borough:montréal-nord': ["Montréal-Nord", 'MONTREALNORD'],
            'ocd-division/country:ca/csd:2466023/borough:outremont': ["Outremont", 'OUTREMONT'],
            'ocd-division/country:ca/csd:2466023/borough:pierrefonds-roxboro': ["Pierrefonds-Roxboro", 'PIERREFONDROXBORO'],
            'ocd-division/country:ca/csd:2466023/borough:rivière-des-prairies~pointe-aux-trembles': ["Rivière-des-Prairies—Pointe-aux-Trembles", 'RIVIEREDESPRAIRIESPOINTEAUXTREMBLES'],
            'ocd-division/country:ca/csd:2466023/borough:rosemont~la_petite-patrie': ["Rosemont—La Petite-Patrie", 'ROSEMONTLAPETITEPATRIE'],
            'ocd-division/country:ca/csd:2466023/borough:saint-laurent': ["Saint-Laurent", 'SAINTLAURENT'],
            'ocd-division/country:ca/csd:2466023/borough:saint-léonard': ["Saint-Léonard", 'SAINTLEONARD'],
            'ocd-division/country:ca/csd:2466023/borough:verdun': ["Verdun", 'VERDUN'],
            'ocd-division/country:ca/csd:2466023/borough:ville-marie': ["Ville-Marie", 'VILLEMARIE'],
            'ocd-division/country:ca/csd:2466023/borough:villeray~saint-michel~parc-extension': ["Villeray—Saint-Michel—Parc-Extension", 'VILLERAYSAINTMICHELPARCEXTENSION'],
        },
    },
    {
        'name': 'Québec',
        'geographic_code': 23027,
        'boroughs': {
            'ocd-division/country:ca/csd:2423027/borough:1': ['La Cité-Limoilou', 'LACITELIMOILOU'],
            'ocd-division/country:ca/csd:2423027/borough:2': ['Les Rivières', 'LESRIVIERES'],
            'ocd-division/country:ca/csd:2423027/borough:3': ['Sainte-Foy–Sillery–Cap-Rouge', 'SAINTFOYSILLERYCAPROUGE'],
            'ocd-division/country:ca/csd:2423027/borough:4': ['Charlesbourg', 'CHARLESBOURG'],
            'ocd-division/country:ca/csd:2423027/borough:5': ['Beauport', 'BEAUPORT'],
            'ocd-division/country:ca/csd:2423027/borough:6': ['La Haute-Saint-Charles', 'LAHAUTESAINTCHARLES'],
        },
    },
    {
        'name': 'Saguenay',
        'geographic_code': 94068,
        'boroughs': {
            'ocd-division/country:ca/csd:2494068/borough:1': ['Chicoutimi', 'CHICOUTIMI'],
            'ocd-division/country:ca/csd:2494068/borough:2': ['Jonquière', 'JONQUIERE'],
            'ocd-division/country:ca/csd:2494068/borough:3': ['La Baie', 'LABAIE'],
        },
    },
    {
        'name': 'Sherbrooke',
        'geographic_code': 43027,
        'boroughs': {
            'ocd-division/country:ca/csd:2443027/borough:1': ['Brompton', 'BROMPTON'],
            'ocd-division/country:ca/csd:2443027/borough:2': ['Fleurimont', 'FLEURIMONT'],
            'ocd-division/country:ca/csd:2443027/borough:3': ['Lennoxville', 'LENNOXVILLE'],
            'ocd-division/country:ca/csd:2443027/borough:4': ['Mont-Bellevue', 'LEMONTBELLEVUE'],
            'ocd-division/country:ca/csd:2443027/borough:5': ['Rock Rorest—Saint-Élie—Deauville', 'ROCKRORESTSAINTELIEDEAUVILLE'],
            'ocd-division/country:ca/csd:2443027/borough:6': ['Jacques-Cartier', 'JACQUESCARTIER'],
        },
    },
]

for municipality in municipalities_with_boroughs:
    for ocd_division, (name, machine_name) in municipality['boroughs'].items():
        boundaries.register('%s districts' % name,
            file='%s-%s.shp' % (unidecode(municipality['name']), unidecode(name)),
            domain='%s, %s, QC' % (name, municipality['name']),
            last_updated=date(2014, 2, 28),
            name_func=namer,
            id_func=lambda f: int(f.get('NO_DIS')),
            authority='Directeur général des élections du Québec',
            licence_url='http://www.electionsquebec.qc.ca/francais/conditions-d-utilisation-de-notre-site-web.php',
            encoding='iso-8859-1',
            metadata={'ocd_division': ocd_division},
            ogr2ogr='''-where "CO_MUNCP='%d' AND NMTRI_ARON='%s'"''' % (municipality['geographic_code'], machine_name),
            base_file='Districts Elec Mun 2014-02-28_DetU_region.shp',
        )
