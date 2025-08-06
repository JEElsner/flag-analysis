from functools import partial
from io import StringIO
from pathlib import Path
import re
import urllib
import urllib.request

from bs4 import BeautifulSoup

import pandas as pd

URL = 'https://en.wikipedia.org/wiki/List_of_national_flags_of_sovereign_states'

def get_tables(url=URL):
    """
    see: `URL`
    """

    list_of_flags_page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(list_of_flags_page, 'html.parser')
    tables = soup.find_all('table')
    
    return tables

split_ratio = re.compile('[∶:]').split

def parse_aspect_ratio(s: str) -> float:
    try:
        n, d = map(int, split_ratio(s))
        return n / d
    except ValueError:
        return float('nan')

strip_citations = partial(re.compile(r'\s*\[.*\]').sub, "")

def parse_table(table):
    table = pd.read_html(StringIO(table.prettify()), flavor='bs4')[0]

    table = table.map(strip_citations)
    table.columns = map(strip_citations, table.columns) # type: ignore
    table.drop('Refs.', axis=1, inplace=True)
    table['Aspect ratio'] = table['Aspect ratio'].apply(parse_aspect_ratio)
    table['Date of latest adoption'] = pd.to_datetime(table['Date of latest adoption'], format='mixed', errors='coerce')
    table['Designer(s)'] = table['Designer(s)'].apply(lambda s: None if s == '—' else s)

    return table


def get_all_flags(tables):
    all_flags = pd.concat(list(map(parse_table, tables[:2])), axis=0, ignore_index=True)
    return all_flags



def download_flags(table, folder, idx_offset=0):
    folder  = Path(folder)
    images = table.find_all('img')
    for i, image in enumerate(images):
        src = image['src']
        name = src.split('/')[-1]

        with open(folder / f'{i+idx_offset}-{name}', mode='wb') as f:
            f.write(urllib.request.urlopen('http:' + src).read())

    return len(images) + idx_offset


def download_and_save(path):
    path = Path(path)

    tables = get_tables()
    all_flags = get_all_flags(tables)
    
    flag_img_path = path / 'flags'

    last = 0
    for table in tables:
        last = download_flags(tables[0], flag_img_path, idx_offset=last)

    # I have no idea what this is doing
    paths = pd.DataFrame.from_records([{'index': int(flag.name.split('-')[0]), 'path': str(flag)} for flag in Path(flag_img_path).glob('*')], index='index')

    all_flags = all_flags.join(paths)

    all_flags.to_feather(path / 'flag_data.feather')
    
    return all_flags

def get_flag_data(path = '../data'):
    path = Path(path)
    
    needs_download = False
    
    if not path.exists():
        path.mkdir()
        needs_download = True

    flag_img_path = path / 'flags'
    if not flag_img_path.exists():
        flag_img_path.mkdir()
        needs_download = True

    db_path = path / 'flag_data.feather'
    if not db_path.exists():
        db_path.mkdir()
        needs_download = True

    if needs_download:
        return download_and_save(path)
    else:
        return pd.read_feather(db_path)
