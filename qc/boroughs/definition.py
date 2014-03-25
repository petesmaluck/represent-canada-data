# coding: utf-8
from datetime import date

from unidecode import unidecode

import boundaries

sets = {
    '23027': u"Québec",
    '25213': u"Lévis",
    '43027': u"Sherbrooke",
    '58227': u"Longueuil",
    '66023': u"Montréal",
    '94068': u"Saguenay",
}

for geographic_code, name in sets.items():
    boundaries.register(u'%s boroughs' % name,
        file='%s.shp' % unidecode(name),
        domain=u'%s, QC' % name,
        last_updated=date(2014, 2, 28),
        name_func=boundaries.dashed_attr('NM_ARON'),
        id_func=boundaries.attr('NO_ARON'),
        authority=u'Directeur général des élections du Québec',
        licence_url='http://www.electionsquebec.qc.ca/francais/conditions-d-utilisation-de-notre-site-web.php',
        encoding='iso-8859-1',
        metadata={'geographic_code': '24%s' % geographic_code},
    )
