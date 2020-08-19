
'''
CHRIS KIMMEL, AUGUST 2020

This script takes a local version of my website and prepares it for
publication.

For right now, all that means is copying the right files into an output
directory and changing their hyperlinks from "file://..." to "https://...".

Maybe I'll add other features as I need them.
'''

import re
import os


WEBSITE_BASEDIR = r'C:\Users\chris\Dropbox\Programming\website'
OUTPUT_BASEDIR = r'C:\Users\chris\Dropbox\Programming\website\PUBLISH'


def prep_links(page_source):
    '''
    Return the string page_source, but with all local "file://" hyperlinks
    replaced with "https://" hyperlinks that will work on the web.

    I make no guarantees as to edge-behavior of the regular expressions. They
    work fine for August 2020 Chris.

    Args:
        page_source (str): the contents of the html file being transformed

    Returns:
        str: the contents of the html file, but with links corrected
    '''
    # https://docs.python.org/3/library/re.html
    pattern = r'<a\s+href\s*=\s*([\'"])file://.+?website/(.+?)\1>'
    repl = r'<a href=\1https://www.chriskimmel.com/\2\1>'
    new_source = re.sub(pattern=pattern, repl=repl, string=page_source)

    return new_source


def is_publishable(basename):
    '''
    Return true if basename has an HTML or CSS filename extension (case
    INsensitive)

    Args:
        basename (str): the basename of a file

    Returns:
        bool: True iff basename has HTML or CSS filename extension
    '''
    pattern = r'\.(?i:html)|(?i:css)$'
    # re.match returns a re.Match object (truth value True), or else None
    return bool(re.search(pattern, basename))


# UNUSED - it turns out os.makedirs does what I need
def existing_portion(path, *, base):
    '''
    Return the maximum initial segment of `path` such that that segment exists.

    Args:
        path (str): A path (relative to `base`) which might not exist
        base (str): The base filepath to which `path` is relative

    Returns:
        str (str): The maximum proper initial segment of `path` that actually
            exists. (Don't split directory names in half, of course.)
    '''
    abs_path = os.path.join(base, path)
    if os.path.exists(abs_path):
        return path
    else:
        return existing_portion(os.path.dirname(abs_path), base=base)


def transform_and_copy(src_path, dest_path):
    '''
    Open the file at `src_path`, copy its contents, and write to `dest_path`.

    It is not necessary that the basedirectory of `dest_path` exist - this
    function will create it.

    Args:
        src_path (str): the file to read
        dest_path (str): the file to which transformed contents of `src_path`
            shall be written

    Returns:
        None
    '''
    # make directory for target before doing anything else
    basedir = os.path.dirname(dest_path)
    os.makedirs(basedir, exist_ok=True)

    # read, transform, and write
    with open(src_path, 'rt') as fh:
        contents = fh.read()
    root, ext = os.path.splitext(basedir)
    if ext.lower() == '.html':
        contents = prep_links(contents)
    with open(dest_path, 'wt') as fh:
        fh.write(contents)


def make_site():
    '''
    Copy files for publishing recursively into OUTPUT_BASEDIR, transforming
    their contents when necessary.

    Args:
        None

    Returns:
        None
    '''
    # build manifest of files to copy (paths relative to WEBSITE_BASEDIR)
    manifest = []
    for dirpath, dirnames, filenames in os.walk(WEBSITE_BASEDIR):
        publishables = [name for name in filenames if is_publishable(name)]
        abspaths = [os.path.join(dirpath, name) for name in publishables]
        relpaths = [os.path.relpath(abspath, start=WEBSITE_BASEDIR)
                    for abspath in abspaths]
        manifest.extend(relpaths)

    # copy (and transform!) files
    for relpath in manifest:
        src_path = os.path.join(WEBSITE_BASEDIR, relpath)
        dest_path = os.path.join(OUTPUT_BASEDIR, relpath)
        transform_and_copy(src_path, dest_path)


if __name__ == '__main__':
    make_site()
