# coding: utf-8
from __future__ import unicode_literals

from datetime import date

import boundaries

boundaries.register('Quebec electoral districts',
    domain='Quebec',
    last_updated=date(2012, 2, 24),
    name_func=boundaries.clean_attr('NM_CEP'),
    id_func=boundaries.attr('CO_CEP'),
    authority='Directeur général des élections du Québec',
    source_url='http://electionsquebec.qc.ca/francais/provincial/carte-electorale/geometrie-des-circonscriptions-provinciales-du-quebec-2014.php',
    licence_url='http://www.electionsquebec.qc.ca/francais/conditions-d-utilisation-de-notre-site-web.php',
    data_url='http://electionsquebec.qc.ca/documents/zip/circonscriptions-electorales-2011-shapefile-v2.zip',
    encoding='windows-1252',
    metadata={'geographic_code': '24'},
)
