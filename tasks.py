# coding: utf8

import csv, codecs, cStringIO
from collections import OrderedDict
from datetime import datetime
from ftplib import FTP
from getpass import getpass
from glob import glob
import os
import os.path
import re
import stat
import sys
from StringIO import StringIO
from urlparse import urlparse
from zipfile import ZipFile, BadZipfile

import boundaries
import gdata.spreadsheet.service
from git import Repo
from invoke import run, task
import lxml.html
import requests
from rfc6266 import parse_headers

from constants import (
  open_data_licenses,
  some_rights_reserved_licenses,
  all_rights_reserved_licenses,
  all_rights_reserved_terms_re,
  terms,
  terms_re,
  valid_keys,
  valid_metadata_keys,
  authorities,
  no_municipal_subdivisions,
  request_headers,
  receipt_headers,
  headers,
)

# Returns the directory in which a shapefile exists.
def dirname(path):
  # GitPython can't handle paths starting with "./".
  if path.startswith('./'):
    path = path[2:]
  if os.path.isdir(path):
    return path
  else:
    return os.path.dirname(path)


# Reads `definition.py` files.
def registry(base='.'):
  boundaries.autodiscover(base)
  return boundaries.registry


# Reads a remote CSV file.
def csv_reader(url):
  return csv.reader(StringIO(requests.get(url).content))


ocd_codes_memo = {}
# Maps Standard Geographical Classification codes to the OCD identifiers of provinces and territories.
def ocd_codes():
  if not ocd_codes_memo:
    ocd_codes_memo['01'] = 'ocd-division/country:ca'
    for row in csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-sgc/ca_provinces_and_territories.csv'):
      ocd_codes_memo[row[1]] = row[0]
    for row in csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_census_subdivisions.csv'):
      ocd_codes_memo[row[0].split(':')[-1]] = row[0]
  return ocd_codes_memo


ocd_names_memo = {}
# Maps OCD identifiers and Standard Geographical Classification codes to names.
def ocd_names():
  if not ocd_names_memo:
    urls = [
      'https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_manual.csv',
      'https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_provinces_and_territories.csv',
      'https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_census_divisions.csv',
      'https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_census_subdivisions.csv',
      'https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/census_subdivision-montreal-arrondissements.csv',
    ]
    for url in urls:
      for row in csv_reader(url):
        ocd_names_memo[row[0].decode('utf8')] = row[1].decode('utf8')
  return ocd_names_memo


# Returns the Open Civic Data division identifier and Standard Geographical Classification code.
def get_ocd_division(slug, config):
  ocd_division = config['metadata'].get('ocd_division')
  geographic_code = config['metadata'].get('geographic_code')
  if ocd_division:
    if geographic_code:
      raise Exception('%s: Set ocd_division or geographic_code' % slug)
  else:
    if geographic_code:
      length = len(geographic_code)
      if length == 2:
        ocd_division = ocd_codes()[geographic_code]
      elif length == 4:
        ocd_division = 'ocd-division/country:ca/cd:%s' % geographic_code
      elif length == 7:
        ocd_division = 'ocd-division/country:ca/csd:%s' % geographic_code
      else:
        raise Exception('%s: Unrecognized geographic code %s' % (slug, geographic_code))
  return ocd_division


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# Check that all data directories contain a `LICENSE.txt`.
@task
def licenses(base='.'):
  for (dirpath, dirnames, filenames) in os.walk(base, followlinks=True):
    if '.git' in dirnames:
      dirnames.remove('.git')
    if '.DS_Store' in filenames:
      filenames.remove('.DS_Store')
    if filenames and 'LICENSE.txt' not in filenames:
      print '%s No LICENSE.txt' % dirpath


# Fix file permissions.
@task
def permissions(base='.'):
  for (dirpath, dirnames, filenames) in os.walk(base, followlinks=True):
    if '.git' in dirnames:
      dirnames.remove('.git')
    if '.DS_Store' in filenames:
      filenames.remove('.DS_Store')
    for filename in filenames:
      path = os.path.join(dirpath, filename)
      if os.stat(path).st_mode != 33188:  # 100644 octal
        os.chmod(path, stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


# Check that all `definition.py` files are valid.
@task
def definitions(base='.'):
  # Map census type codes to names.
  census_division_type_names = {}
  document = lxml.html.fromstring(requests.get('http://www12.statcan.gc.ca/census-recensement/2011/ref/dict/table-tableau/table-tableau-4-eng.cfm').content)
  for abbr in document.xpath('//table/tbody/tr/th[1]/abbr'):
    census_division_type_names[abbr.text_content()] = re.sub(' /.+\Z', '', abbr.attrib['title'])
  census_subdivision_type_names = {}
  document = lxml.html.fromstring(requests.get('http://www12.statcan.gc.ca/census-recensement/2011/ref/dict/table-tableau/table-tableau-5-eng.cfm').content)
  for abbr in document.xpath('//table/tbody/tr/th[1]/abbr'):
    census_subdivision_type_names[abbr.text_content()] = re.sub(' /.+\Z', '', abbr.attrib['title'])

  # Map OCD identifiers to census subdivision types.
  types = {}
  reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-types/ca_census_divisions.csv')
  for row in reader:
    types[row[0]] = census_division_type_names[row[1].decode('utf8')]
  reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-types/ca_census_subdivisions.csv')
  for row in reader:
    types[row[0]] = census_subdivision_type_names[row[1].decode('utf8')]

  codes = ocd_codes()
  names = ocd_names()
  ocd_divisions = set()

  for slug, config in registry(base).items():
    directory = dirname(config['file'])

    # Validate LICENSE.txt.
    license_path = os.path.join(directory, 'LICENSE.txt')
    if os.path.exists(license_path):
      with open(license_path) as f:
        license_text = f.read().rstrip('\n')
      if config.get('licence_url'):
        licence_url = config['licence_url']
        if licence_url in open_data_licenses or licence_url in some_rights_reserved_licenses:
          if not terms.get(licence_url) and not terms_re.get(licence_url):
            print "%-50s No LICENSE.txt template for License URL %s" % (slug, licence_url)
          elif terms.get(licence_url) and license_text != terms[licence_url] or terms_re.get(licence_url) and not terms_re[licence_url].search(license_text):
            print "%-50s Expected LICENSE.txt to match license-specific template" % slug
        elif licence_url in all_rights_reserved_licenses:
          if not all_rights_reserved_terms_re.search(license_text):
            print '%-50s Expected LICENSE.txt to match "all rights reserved" template' % slug
        else:
          print '%-50s Unrecognized License URL %s' % (slug, licence_url)
      elif not all_rights_reserved_terms_re.search(license_text):
        print '%-50s Expected LICENSE.txt to match "all rights reserved" template' % slug

    # Check for invalid keys, non-unique or empty values.
    invalid_keys = set(config.keys()) - valid_keys
    if invalid_keys:
      print "%-50s Unrecognized key: %s" % (slug, ', '.join(invalid_keys))
    values = [value for key, value in config.items() if key != 'metadata']
    if len(values) > len(set(values)):
      print "%-50s Non-unique values" % slug
    for key, value in config.items():
      if not value:
        print "%-50s Empty value for %s" % (slug, key)

    # Check for missing required keys.
    for key in ('domain', 'last_updated', 'name_func', 'authority', 'encoding'):
      if not config.get(key):
        print "%-50s Missing %s" % (slug, key)
    if not config.get('source_url') and (config.get('licence_url') or config.get('data_url')):
      print "%-50s Missing source_url" % slug
    if config.get('source_url') and not config.get('licence_url') and not config.get('data_url'):
      print "%-50s Missing licence_url or data_url" % slug

    # Validate fields.
    for key in ('name', 'singular'):
      if config.get(key):
        print "%-50s Expected %s to be missing" % (slug, key)
    if config.get('encoding') and config['encoding'] != 'iso-8859-1':
      print "%-50s Expected encoding to be iso-8859-1 not %s" % (slug, config['encoding'])

    if slug not in ('Census divisions', 'Census subdivisions'):
      if config.get('metadata'):
        # Check for invalid keys or empty values.
        invalid_keys = set(config['metadata'].keys()) - valid_metadata_keys
        if invalid_keys:
          print "%-50s Unrecognized key: %s" % (slug, ', '.join(invalid_keys))
        for key, value in config['metadata'].items():
          if not value:
            print "%-50s Empty value for %s" % (slug, key)

        ocd_division = get_ocd_division(slug, config)
        geographic_code = config['metadata'].get('geographic_code')

        if ocd_division:
          # Ensure ocd_division is unique.
          if ocd_division in ocd_divisions:
            raise Exception('%s: Duplicate ocd_division %s' % (slug, ocd_division))
          else:
            ocd_divisions.add(ocd_division)

          sections = ocd_division.split('/')
          ocd_type, ocd_type_id = sections[-1].split(':')

          # Validate slug, domain and authority.
          name = names[ocd_division]
          if ocd_type == 'country':
            expected = 'Federal electoral districts'
            if slug != expected:
              print "%-50s Expected slug to be %s" % (slug, expected)

            if config['domain'] != name:
              print "%-50s Expected domain to be %s not %s" % (slug, name, config['domain'])

            expected = 'Her Majesty the Queen in Right of Canada'
            if config['authority'] != expected:
              print "%-50s Expected authority to be %s not %s" % (slug, expected, config['authority'])

          elif ocd_type in ('province', 'territory'):
            expected = '%s electoral districts' % name
            if slug != expected:
              print "%-50s Expected slug to be %s" % (slug, expected)

            if config['domain'] != name:
              print "%-50s Expected domain to be %s not %s" % (slug, name, config['domain'])

            expected = 'Her Majesty the Queen in Right of %s' % name
            if config['authority'] != expected:
              print "%-50s Expected authority to be %s not %s" % (slug, expected, config['authority'])

          elif ocd_type in ('cd', 'csd'):
            province_or_territory_code = ocd_type_id[:2]
            province_or_territory_abbreviation = codes[province_or_territory_code].split(':')[-1].upper()

            if province_or_territory_code == '24':
              expected = re.compile('\A%s (boroughs|districts)\Z' % name)
            else:
              expected = re.compile('\A%s (districts|divisions|wards)\Z' % name)
            if not expected.search(slug):
              print "%-50s Expected slug to match %s" % (slug, expected.pattern)

            expected = '%s, %s' % (name, province_or_territory_abbreviation)
            if config['domain'] != expected:
              print "%-50s Expected domain to be %s not %s" % (slug, expected, config['domain'])

            if province_or_territory_code == '24':
              preposition = 'de'
            else:
              preposition = 'of'
            expected = '%s %s %s' % (types[ocd_division], preposition, name)
            if config['authority'] != expected and config['authority'] not in authorities:
              print "%-50s Expected authority to be %s not %s" % (slug, expected, config['authority'])

          elif ocd_type == 'arrondissement':
            census_subdivision_ocd_division = '/'.join(sections[:-1])
            census_subdivision_name = names[census_subdivision_ocd_division]
            province_or_territory_code = census_subdivision_ocd_division.split(':')[-1][:2]
            province_or_territory_abbreviation = codes[province_or_territory_code].split(':')[-1].upper()

            expected = '%s districts' % name
            if slug != expected:
              print "%-50s Expected slug to be %s" % (slug, expected)

            expected = '%s, %s, %s' % (name, census_subdivision_name, province_or_territory_abbreviation)
            if config['domain'] != expected:
              print "%-50s Expected domain to be %s not %s" % (slug, expected, config['domain'])

            if province_or_territory_code == '24':
              preposition = 'de'
            else:
              preposition = 'of'
            expected = '%s %s %s' % (types[census_subdivision_ocd_division], preposition, census_subdivision_name)
            if config['authority'] != expected:
              print "%-50s Expected authority to be %s not %s" % (slug, expected, config['authority'])

          else:
            raise Exception('%s: Unrecognized OCD type %s' % (slug, ocd_type))
      else:
        print "%-50s Missing metadata" % slug


# Check that the source, data and license URLs work.
@task
def urls(base='.'):
  for slug, config in registry(base).items():
    for key in ('source_url', 'licence_url', 'data_url'):
      if config.get(key):
        url = config[key]
        result = urlparse(url)
        if result.scheme == 'ftp':
          ftp = FTP(result.hostname)
          ftp.login(result.username, result.password)
          ftp.cwd(os.path.dirname(result.path))
          if os.path.basename(result.path) not in ftp.nlst():
            print '404 %s' % url
          ftp.quit()
        else:
          try:
            arguments = {}
            if result.username:
              url = '%s://%s%s' % (result.scheme, result.hostname, result.path)
              arguments['auth'] = (result.username, result.password)
            response = requests.head(url, **arguments)
            status_code = response.status_code
            if status_code != 200:
              print '%d %s' % (status_code, url)
          except requests.exceptions.ConnectionError:
            print '404 %s' % url


# Update any out-of-date shapefiles.
@task
def shapefiles(base='.'):
  def process(slug, config, url, data_file_path):

    # We can only process KML, KMZ and ZIP files.
    extension = os.path.splitext(data_file_path)[1]
    if extension in ('.kml', '.kmz', '.zip'):
      repo_path = os.path.dirname(data_file_path)
      while not os.path.exists(os.path.join(repo_path, '.git')) and not repo_path == '/':
        repo_path = os.path.join(repo_path, '..')
      repo_path = os.path.realpath(repo_path)

      repo = Repo(repo_path)
      index = repo.index
      directory = dirname(config['file'])

      # Remove old files.
      for basename in os.listdir(directory):
        if basename not in ('.DS_Store', 'definition.py', 'LICENSE.txt', 'data.kml', 'data.kmz', 'data.zip'):
          os.unlink(os.path.join(directory, basename))
          index.remove([os.path.relpath(os.path.join(directory, basename), repo_path)])

      files_to_add = []

      # Unzip any zip file.
      error_thrown = False
      if extension == '.zip':
        try:
          zip_file = ZipFile(data_file_path)
          for name in zip_file.namelist():
            # Flatten the zip file hierarchy.
            extension = os.path.splitext(name)[1]
            if extension in ('.kml', '.kmz'):
              basename = 'data%s' % extension  # assumes one KML or KMZ file per archive
            else:
              basename = os.path.basename(name)  # assumes no collisions across hierarchy
            with open(os.path.join(directory, basename), 'wb') as f:
              f.write(zip_file.read(name))
            if extension not in ('.kml', '.kmz'):
              files_to_add.append(os.path.join(directory, basename))
        except BadZipfile:
          error_thrown = True
          print 'Bad ZIP file %s\n' % url
        finally:
          os.unlink(data_file_path)

      # Unzip any KMZ file.
      kmz_file_path = os.path.join(directory, 'data.kmz')
      if not error_thrown and os.path.exists(kmz_file_path):
        try:
          zip_file = ZipFile(kmz_file_path)
          for name in zip_file.namelist():
            # A KMZ file contains a single KML file and other supporting files.
            # @see https://developers.google.com/kml/documentation/kmzarchives
            if os.path.splitext(name)[1] == '.kml':
              with open(os.path.join(directory, 'data.kml'), 'wb') as f:
                f.write(zip_file.read(name))
        except BadZipfile:
          error_thrown = True
          print 'Bad KMZ file %s\n' % url
        finally:
          os.unlink(kmz_file_path)

      if not error_thrown:
        # Convert any KML to shapefile.
        kml_file_path = os.path.join(directory, 'data.kml')
        if os.path.exists(kml_file_path):
          result = run('ogrinfo -q %s | grep -v "3D Point"' % kml_file_path, hide='out').stdout
          if result.count('\n') > 1:
            print 'Too many layers %s' % url
          else:
            layer = re.search('\A\d+: (\S+)', result).group(1)
            run('ogr2ogr -f "ESRI Shapefile" %s %s -nlt POLYGON %s' % (directory, kml_file_path, layer), echo=True)
            for name in glob(os.path.join(directory, '*.[dps][bhr][fjpx]')):
              files_to_add.append(name)
            os.unlink(kml_file_path)

        # Merge multiple shapefiles into one.
        names = glob(os.path.join(directory, '*.shp'))
        if len(names) > 1:
          for name in names:
            run('ogr2ogr -f "ESRI Shapefile" %s %s -update -append -nln Boundaries' % (directory, name), echo=True)
            basename = os.path.splitext(os.path.basename(name))[0]
            for name in glob(os.path.join(directory, '%s.[dps][bhr][fjnpx]' % basename)):
              files_to_add.remove(name)
              os.unlink(name)

        shp_file_path = glob(os.path.join(directory, '*.shp'))
        if shp_file_path:
          shp_file_path = shp_file_path[0]
        if shp_file_path and os.path.exists(shp_file_path):
          # Convert any 3D shapefile into 2D.
          result = run('ogrinfo -q %s' % shp_file_path, hide='out').stdout
          if result.count('\n') > 1:
            print 'Too many layers %s' % url
          elif re.search('3D Polygon', result):
            run('ogr2ogr -f "ESRI Shapefile" %s %s -nlt POLYGON -overwrite' % (directory, shp_file_path), echo=True)
            for name in list(files_to_add):
              if not os.path.exists(name):
                files_to_add.remove(name)

          # Replace "Double_Stereographic" with "Oblique_Stereographic".
          prj_file_path = os.path.splitext(shp_file_path)[0] + '.prj'
          if prj_file_path and os.path.exists(prj_file_path):
            with open(prj_file_path) as f:
              prj = f.read()
            if 'Double_Stereographic' in prj:
              with open(prj_file_path, 'w') as f:
                f.write(prj.replace('Double_Stereographic', 'Oblique_Stereographic'))
          elif config.get('prj'):
            with open(prj_file_path, 'w') as f:
              f.write(requests.get(config['prj']).content)
            files_to_add.append(prj_file_path)
          else:
            print 'No PRJ file %s' % url

          # Run any additional commands on the shapefile.
          if config.get('ogr2ogr'):
            run('ogr2ogr -f "ESRI Shapefile" -overwrite %s %s %s' % (directory, shp_file_path, config['ogr2ogr']), echo=True)
            for name in list(files_to_add):
              if not os.path.exists(name):
                files_to_add.remove(name)

        # Add files to git.
        index.add([os.path.relpath(name, repo_path) for name in files_to_add])

        # Update last updated timestamp.
        definition_path = os.path.join(directory, 'definition.py')
        with open(definition_path) as f:
          definition = f.read()
        with open(definition_path, 'w') as f:
          f.write(re.sub('(?<=last_updated=date\()[\d, ]+', last_updated.strftime('%Y, %-m, %-d'), definition))

        # Print notes.
        notes = []
        if config.get('notes'):
          notes.append(config['notes'])
        if notes:
          print '%s\n%s\n' % (slug, '\n'.join(notes))
    else:
      print 'Unrecognized extension %s\n' % url

  # Retrieve shapefiles.
  for slug, config in registry(base).items():
    if config.get('data_url'):
      url = config['data_url']
      result = urlparse(url)

      if result.scheme == 'ftp':
        # Get the last modified timestamp.
        ftp = FTP(result.hostname)
        ftp.login(result.username, result.password)
        last_modified = ftp.sendcmd('MDTM %s' % result.path)

        # Parse the timestamp as a date.
        last_updated = datetime.strptime(last_modified[4:], '%Y%m%d%H%M%S').date()

        if config['last_updated'] < last_updated:
          # Determine the file extension.
          extension = os.path.splitext(url)[1]

          # Set the new file's name.
          data_file_path = os.path.join(dirname(config['file']), 'data%s' % extension)

          # Download new file.
          ftp.retrbinary('RETR %s' % result.path, open(data_file_path, 'wb').write)
          ftp.quit()

          process(slug, config, url, data_file_path)
      else:
        # Get the last modified timestamp.
        arguments = {'allow_redirects': True}
        if result.username:
          url = '%s://%s%s' % (result.scheme, result.hostname, result.path)
          arguments['auth'] = (result.username, result.password)
        response = requests.head(url, **arguments)
        if response.status_code == 405:  # if HEAD requests are not allowed
          response = requests.get(url, **arguments)
        last_modified = response.headers.get('last-modified')

        # Parse the timestamp as a date.
        if last_modified:
          last_updated = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S GMT')
        else:
          last_updated = datetime.now()
        last_updated = last_updated.date()

        if config['last_updated'] > last_updated:
          print '%s are more recent than the source\n' % slug
        elif config['last_updated'] < last_updated:
          # Determine the file extension.
          if response.headers.get('content-disposition'):
            filename = parse_headers(response.headers['content-disposition']).filename_unsafe
          else:
            filename = url
          extension = os.path.splitext(filename)[1].lower()

          # Set the new file's name.
          data_file_path = os.path.join(dirname(config['file']), 'data%s' % extension)

          # Download new file.
          arguments['stream'] = True
          response = requests.get(url, **arguments)
          with open(data_file_path, 'wb') as f:
            for chunk in response.iter_content():
              f.write(chunk)

          process(slug, config, url, data_file_path)


# Generate the spreadsheet for tracking progress on data collection.
@task
def spreadsheet(base='.', private_base='../represent-canada-private-data'):
  codes = ocd_codes()
  names = ocd_names()
  records = OrderedDict()

  for row in csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-subdivisions/ca_municipal_subdivisions.csv'):
    if row[1] == "N":
      no_municipal_subdivisions.append(row[0].split(':')[-1])

  abbreviations = {}
  for row in csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-abbr/ca_provinces_and_territories.csv'):
    abbreviations[row[1]] = row[0].split(':')[-1].upper()

  sgc_codes = {}
  for row in csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-sgc/ca_provinces_and_territories.csv'):
    sgc_codes[row[0]] = row[1]

  # Get scraper URLs.
  scraper_urls = {}
  for representative_set in requests.get('http://represent.opennorth.ca/representative-sets/?limit=0').json()['objects']:
    boundary_set_url = representative_set['related']['boundary_set_url']
    if boundary_set_url:
      if boundary_set_url != '/boundary-sets/census-subdivisions/':
        boundary_set = requests.get('http://represent.opennorth.ca%s' % boundary_set_url).json()
        if boundary_set.get('extra') and boundary_set['extra'].get('geographic_code'):
          scraper_urls[boundary_set['extra']['geographic_code']] = representative_set['data_about_url'] or representative_set['data_url']
        else:
          sys.stderr.write('%-60s No extra\n' % boundary_set_url)
    else:
      sys.stderr.write('%-60s No boundary_set_url\n' % representative_set['url'])

  # Create records for provinces and territories.
  for row in csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_provinces_and_territories.csv'):
    records[sgc_codes[row[0]]] = {
      'OCD': row[0],
      'Geographic code': sgc_codes[row[0]],
      'Geographic name': row[1],
      'Province or territory': row[0].split(':')[-1].upper(),
      'Population': '',
      'Scraper?': scraper_urls.get(sgc_codes[row[0]], ''),
      'Shapefile?': '',
      'Contact': '',
      'Highrise URL': '',
      'Request notes': '',
      'Received via': '',
      'Last boundary': '',
      'Next boundary': '',
      'Permission to distribute': '',
      'Type of license': '',
      'License URL': '',
      'Denial notes': '',
    }

  # Create records for census subdivisions.
  reader = csv_reader('http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/FullFile.cfm?T=301&LANG=Eng&OFT=CSV&OFN=98-310-XWE2011002-301.CSV')
  reader.next()  # title
  reader.next()  # headers
  for row in reader:
    if row:
      result = re.search('\A(.+) \((.+)\)\Z', row[1].decode('iso-8859-1'))
      if result:
        name = result.group(1)
        province_or_territory = abbreviations[result.group(2)]
      elif row[1] == 'Canada':
        name = 'Canada'
        province_or_territory = ''
      else:
        raise Exception('Unrecognized name "%s"' % row[1])

      record = {
        'OCD': codes[row[0]],
        'Geographic code': row[0],
        'Geographic name': name,
        'Province or territory': province_or_territory,
        'Population': row[4],
        'Scraper?': scraper_urls.get(row[0], ''),
        'Contact': '',
        'Highrise URL': '',
        'Request notes': '',
        'Received via': '',
        'Last boundary': '',
        'Next boundary': '',
        'Permission to distribute': '',
        'Type of license': '',
        'License URL': '',
        'Denial notes': '',
      }

      if row[0] in no_municipal_subdivisions or province_or_territory == 'BC':
        for header in ['Shapefile?'] + request_headers + receipt_headers:
          record[header] = 'N/A'
      else:
        record['Shapefile?'] = ''

      records[row[0]] = record
    else:
      break

  # Merge information from received data.
  for directory, permission_to_distribute in [(base, 'Y'), (private_base, 'N')]:
    boundaries.registry = {}
    for slug, config in registry(directory).items():
      if config.get('metadata'):
        geographic_code = config['metadata'].get('geographic_code')
        if geographic_code:
          license_path = os.path.join(dirname(config['file']), 'LICENSE.txt')
          license_text = ''
          if os.path.exists(license_path):
            with open(license_path) as f:
              license_text = f.read().rstrip('\n').decode('utf-8')

          record = records[geographic_code]
          record['Shapefile?'] = 'Y'
          record['Permission to distribute'] = permission_to_distribute
          record['License URL'] = config.get('licence_url', '')

          if config.get('last_updated'):
            record['Last boundary'] = config['last_updated'].strftime('%-m/%-d/%Y')

          if config.get('source_url'):
            record['Contact'] = 'N/A'
            record['Received via'] = 'online'
          else:
            match = all_rights_reserved_terms_re.search(license_text)
            if match:
              record['Contact'] = match.group(1)
            record['Received via'] = 'email'

          if config.get('licence_url'):
            licence_url = config['licence_url']
            if licence_url in open_data_licenses:
              record['Type of license'] = 'Open'
            elif licence_url in some_rights_reserved_licenses:
              record['Type of license'] = 'Most rights reserved'
            elif licence_url in all_rights_reserved_licenses:
              record['Type of license'] = 'All rights reserved'
            else:
              raise Exception(licence_url)
          elif all_rights_reserved_terms_re.search(license_text):
            record['Type of license'] = 'All rights reserved'
          else:
            record['Type of license'] = 'Custom'
        else:
          sys.stderr.write('%-60s No geographic_code\n' % slug)

  reader = csv.DictReader(StringIO(requests.get('https://docs.google.com/spreadsheet/pub?key=0AtzgYYy0ZABtdGpJdVBrbWtUaEV0THNUd2JIZ1JqM2c&single=true&gid=25&output=csv').content))
  for row in reader:
    geographic_code = row['Geographic code']
    record = records[geographic_code]

    for key in row:
      a = record[key]
      b = row[key].decode('utf-8')

      if a != b:
        # Columns that are always tracked manually.
        # Scrapers for municipalities without wards are tracked manually.
        # In-progress requests are tracked manually.
        # Contacts for in-progress requests and private data are tracked manually.
        # We may have a contact to confirm the nonexistence of municipal subdivisions.
        # MFIPPA requests are tracked manually.
        # Additional details about license agreements and written consent are tracked manually.
        # We may have information for a bad shapefile from an in-progress request.
        if b and \
           (key in ('Highrise URL', 'Request notes', 'Next boundary', 'Denial notes')) or \
           (key == 'Scraper?'         and not a         and record['Shapefile?'] == 'N/A') or \
           (key == 'Shapefile?'       and not a         and b in ('Request', 'Requested')) or \
           (key == 'Contact'          and not a         and (row['Shapefile?'] == 'Requested' or record['Permission to distribute'] == 'N')) or \
           (key == 'Contact'          and a == 'N/A'    and record['Shapefile?'] == 'N/A') or \
           (key == 'Received via'     and a == 'email'  and b == 'MFIPPA') or \
           (key == 'Type of license'  and '(' in b) or \
           (key in ('Received via', 'Type of license', 'Permission to distribute') and not a and row['Shapefile?'] == 'Requested'):
          record[key] = b
        elif key != 'Population':  # separators
          sys.stderr.write('%-25s %s: expected "%s" got "%s"\n' % (key, geographic_code, a, b))

  writer = UnicodeWriter(sys.stdout)
  writer.writerow(headers)
  for _, record in records.items():
    writer.writerow([record[header] for header in headers])

# Update the spreadsheet for tracking progress on data collection.
# @see https://code.google.com/p/gdata-python-client/source/browse/samples/oauth/oauth_example.py
# @see https://code.google.com/p/gdata-python-client/source/browse/samples/spreadsheets/spreadsheetExample.py
@task
def update_spreadsheet(filename=''):
  client = gdata.spreadsheet.service.SpreadsheetsService()
  client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, 'opennorth.ca', consumer_secret=getpass('OAuth consumer secret: '))
  client.SetOAuthToken(client.FetchOAuthRequestToken())
  raw_input('Press a key after authenticating at %s' % client.GenerateOAuthAuthorizationURL())
  client.UpgradeToOAuthAccessToken()

  feed = client.GetListFeed('tjIuPkmkThEtLsTwbHgRj3g', 'oci')
  for entry in feed.entry[1:]:
    client.DeleteRow(entry)

  # Deleting a row at a time is incredibly slow. I didn't get to inserting rows.
  # Just use Google Spreadsheets' import feature.

  client.RevokeOAuthToken()
