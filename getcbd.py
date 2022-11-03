import json, re, requests, sys
import PIL.Image, PIL.ImageDraw, PIL.ImageFont

site_url = 'http://chemistrybydesign.oia.arizona.edu/'

def cache_list():
    ''' Sends a request to get the list. Useful for caching.'''
    resp = requests.get(site_url + 'listJSON.php').json()
    with open('list_cache.json', 'w') as fp:
        json.dump(resp, fp)

def listjoin(data, sep):
    ''' Joins data with sep as separators.
    
    For example, list(listjoin([1, 2, 3], [4, 5])) yields [1, 4, 2, 5, 3].
    Requires that len(data) == len(sep) + 1.
    '''
    if len(data) != len(sep) + 1:
        raise ValueError("Lengths of data and sep don't differ by one!")
    it1 = iter(data)
    it2 = iter(sep)
    try:
        while True:
            yield next(it1)
            yield next(it2)
    except StopIteration:
        pass

def transform_doi(doi):
    ''' Turns %2a format into normal characters. '''
    reg = re.compile('%[0-9A-Fa-f]{2}')
    return ''.join(listjoin(reg.split(doi), [chr(int(x[1:], 16)) for x in reg.findall(doi)]))

def local_info(prodname):
    ''' Gets the information from local storage. None if not found. '''
    try:
        with open("info_cache.json") as fp:
            infos = json.load(fp)
    except FileNotFoundError:
        return None
    if prodname not in infos:
        return None
    return tuple(infos[prodname])

def get_product_info(prodname):
    ''' Returns the information on the product, given its name in full.

    The returned tuple contains a URL and the maximum number of its images.
    For example, ('https://127.0.0.1/files', 5, '10.1038/NCHEM.1072')
    The spaces in the path will be replaced by %20.

    Raises ValueError if the name was not found.
    '''
    try:
        with open('list_cache.json') as fp:
            resp = json.load(fp)
    except:
        print('Reading the cache failed, please run again with -r option!', file=sys.stderr)
        sys.exit(1)
    print(f"There are a total of {len(resp)} syntheses.")
    path = None
    for route in resp:
        if route['full'] == prodname:
            path = route['path']
            break
    if path is None:
        raise ValueError("The product was not found!")
    # First try the local one
    local = local_info(prodname)
    if local is not None:
        print("Using local copy of the info")
        return local
    resp = requests.get(site_url + 'infoJSON.php?dir=' + path).json()
    return (site_url + resp['path'].replace(' ', '%20'), int(resp['max']), transform_doi(resp['doi']))

def download_images(path, max_number):
    ''' Download all the images to images/ '''
    import os.path
    if not os.path.isdir('images'):
        os.mkdir('images')
    for i in range(1, max_number + 1):
        with open(f'images/{i}.png', 'wb') as f:
            f.write(requests.get(path + f'/{i}.png').content)
        if i % 5 == 0:
            print('Checkpoint:', i)

def resize_condition(name : str):
    ''' Resize the condition called 'name'. See resize_images. '''
    src = PIL.Image.open(name)
    # src = src.resize((src.width // 2, src.height // 2))
    ans = PIL.Image.new('RGBA', (src.width, src.height * 2 + 10), (0,) * 4)
    ans.paste(src)
    draw = PIL.ImageDraw.Draw(ans)
    black = (0, 0, 0, 256)
    draw.line(((0, src.height + 5), (src.width - 20, src.height + 5)), fill = black, width = 3)
    draw.polygon(
        ((src.width - 20, src.height), (src.width, src.height + 5), (src.width - 20, src.height + 10)),
        fill = black
    )
    ans.save(name)

def get_blank_equiv(name : str):
    ''' Gets a blank image of the same size for the image called `name`. 
    
    Output: for example, if name is 1.png, the output is 1blank.png
    '''
    src = PIL.Image.open(name)
    # Finding the first dot should suffice for our needs.
    dotpos = name.find('.')
    resname = name[0:dotpos] + 'blank' + name[dotpos:]
    ans = PIL.Image.new('RGBA', src.size, (0,) * 4)
    draw = PIL.ImageDraw.Draw(ans)
    num = int(re.compile(R'.*?(\d+).+').match(name)[1]) // 2
    font = PIL.ImageFont.truetype('arial.ttf', 28)
    draw.text((src.width / 2, src.height / 2), str(num), fill = (0, 0, 0, 256), font = font)
    ans.save(resname)

def process_images(max_number):
    ''' Resizes the conditions and substrates in images/ to half its size and do a few things.
    
    We will resize the condition images to half its size, add an arrow and add a blank padding below.
    We will generate a blank image of exactly the same size for each substrate.
    '''
    for i in range(2, max_number, 2):
        resize_condition(f'images/{i}.png')
    for i in range(1, max_number, 2):
        get_blank_equiv(f'images/{i}.png')

def make_page(prodname, max_number, doi):
    ''' Outputs the page to result.html. '''
    with open('result.html', 'w') as fout:
        # The site to be linked to.
        link = 'doi.org'
        if '-s' in sys.argv:
            s_pos = sys.argv.index('-s')
            if s_pos == len(sys.argv) - 1:
                print('-s has a mandatory argument!', file = sys.stderr)
                print('Warning: Using default site.')
            else:
                link = sys.argv[s_pos + 1]
        fout.write(f'''<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="utf-8" />
    <title>{prodname}</title>
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" type="text/css" href="mystyle.css" />
    <script src="synmanip.js"></script>
</head>
<body>
    <div id="tools">
        <button onclick="toggle_blanks();" id="blank-toggler" type="button">Hide blanks</button>
        <button onclick="show_all_products();" type="button">Show all</button>
        <a href="https://{link}/{doi}" target="_blank">{doi}</a>
        <p>Scale:<input type="range" min="10" max="200" value="100" oninput="zoom_main(this);" id="zoom-scroll" /></p>
    </div>
    <div id="main">
'''
        )
        # Now we will output each picture individually.
        for i in range(1, max_number + 1):
            if i % 2 == 0:
                fout.write(f'<img src="images/{i}.png" class="cond" title="conditions"/>')
            elif i == 1:
                fout.write('<img src="images/1.png" class="sub" onclick="toggle_vis(this);" title="start here" />')
            elif i == max_number:
                fout.write(f'<img src="images/{i}.png" class="sub" onclick="toggle_vis(this);" title="product" />')
            else:
                fout.write(f'<img src="images/{i}blank.png" class="sub" onclick="toggle_vis(this);" title="intermediate" />')
            fout.write('\n')
        # The last part.
        fout.write(f'</div>\n</body></html>\n')

if __name__ == '__main__':
    prodname = input('Please input the full name of the synthesis: ').strip()
    if '-r' in sys.argv or '/r' in sys.argv:
        print('Updating local copy of the list...')
        cache_list()
    else:
        print('Using local copy of the list, run with -r to update.')
    path, maxnum, doi = get_product_info(prodname)
    print('There are', maxnum, 'images to download.')
    download_images(path, maxnum)
    print('Prepping the images...')
    process_images(maxnum)
    print('Generating HTML result...')
    make_page(prodname, maxnum, doi)
