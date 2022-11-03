import json, requests, sys
import os.path, os

from getcbd import site_url, transform_doi

try:
    with open('list_cache.json') as fp:
        a = json.load(fp)
except:
    print('Reading the cache failed, please run getcbd with -r option!', file=sys.stderr)
    sys.exit(1)

def get_product_info(prodname):
    ''' Returns the information on the product, given its name in full.

    The returned tuple contains a URL and the maximum number of its images.
    For example, ('https://127.0.0.1/files', 5, '10.1038/NCHEM.1072')
    The spaces in the path will be replaced by %20.

    Raises ValueError if the name was not found.
    '''
    path = None
    for route in a:
        if route['full'] == prodname:
            path = route['path']
            break
    if path is None:
        raise ValueError("The product was not found!")
    resp = requests.get(site_url + 'infoJSON.php?dir=' + path).json()
    return (site_url + resp['path'].replace(' ', '%20'), int(resp['max']), transform_doi(resp['doi']))

if os.path.isfile('info_cache.json'):
    print('There is already a info_cache.json in this directory!')
    if os.system('choice /m "Start from scratch?"') == 1:
        lengths = dict()
    else:
        with open('info_cache.json') as fp:
            lengths = json.load(fp)
else:
    lengths = dict()
n = len(lengths)

try:
    for (number, prod) in enumerate(a):
        if number < n:
            continue
        print(f'Getting info of number {number}')
        # lengths.append((getcbd.get_product_info(prod['full']), prod['full']))
        lengths[prod['full']] = get_product_info(prod['full'])
except BaseException as ex:
    print(ex.args)
json.dump(lengths, open('info_cache.json', 'w'))
