import hashlib
import math
import os

import pickle
import dropbox
import pandas as pd
from dropbox_config import FULL_FILE_INDEX
from dropbox_content_hasher import DropboxContentHasher

DROPBOX_HASH_CHUNK_SIZE = 4*1024*1024

def get_filetype_from_fname(fname):
    extension = fname.split('.')[-1].lower()
    if len(extension) > 4 or len(extension) < 3:
        return 'System'
    if extension in ['mp3', 'wav', 'ogg', 'm4a']:
        return 'Audio'
    if extension in ['jpg', 'jpeg', 'png', 'gif', 'dg1__ds_dir_hdr']:
        return 'Image'
    if extension in ['doc', 'docx', 'pdf']:
        return 'Document'
    if extension in ['mp4', 'avi', 'mov', 'flv']:
        return 'Video'
    if extension in ['xls', 'xlsx', 'csv']:
        return 'Spreadsheet'
    if extension in ['ppt', 'pptx']:
        return 'Presentation'
    if extension in ['zip', 'tar', 'gz', 'pak', '7z']:
        return 'Archive'
    if extension in ['json', 'dll', '0', 'so', 'xml', 'log', 'mo', 'strings', 'plist',
                     'js', 'stringsdict', 'txt',
                     'db', 'apk', 'css', 'html', 'j', 'luac', 'exe', 'blk',
                     'asc', 'ucae', 'clog', 'ufd', 'ufdx', 'ufdr', 'cfe', 'nsh', 'pset',
                     'ini', 'odex', 'htm']:
        return 'System'
    if extension in ['eml', 'msg']:
        return 'Email'
    return 'Other'

def load_full_file_index(unified_only=True, filter_to_files=True):
    with open(FULL_FILE_INDEX, 'rb') as f:
        files = pickle.load(f)
    print(f'loaded {len(files)} files')
    if unified_only:
        files = [f for f in files if 'organized discovery' in f.path_lower]
        print(f'filtered to {len(files)} files and folders')
    if filter_to_files:
        files = [f for f in files if type(f) == dropbox.files.FileMetadata]
        print(f'filtered to {len(files)} files')
    return files

def get_df_from_files(files):
    # filter out folders if present
    files = [f for f in files if type(f) == dropbox.files.FileMetadata]
    atts = dir(files[0])
    atts = [a for a in atts if not a.startswith('_')]
    atts = [
        'name',
        'path_display',
        'size',
        'path_lower',
        'content_hash',
        'media_info',]
    file_df = pd.DataFrame([{a: getattr(f, a) for a in atts} for f in files])
    file_df['extension'] = file_df.name.apply(lambda x: x.split('.')[-1])
    file_df['filetype'] = file_df.name.apply(get_filetype_from_fname)
    return file_df


def get_folder_at_depth(path, depth):
    return path.split('/')[depth]

def get_folder_at_depths(path, start_depth, end_depth):
    path_chunks = path.split('/')[start_depth:end_depth + 1]
    return '/'.join(path_chunks)


def compute_dropbox_hash(fn):
    """Uses sample code from Dropbox to compute the hash of a file."""
    hasher = DropboxContentHasher()
    with open(fn, 'rb') as f:
        while True:
            chunk = f.read(1024)  # or whatever chunk size you want
            if len(chunk) == 0:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

def compute_sha_hash(fn):
    """Computes a more traditional sha hash"""
    sha_hash = hashlib.sha256()
    with open(fn, 'rb') as f:
        for block in iter(lambda: f.read(4096), b""):
            sha_hash.update(block)
    return sha_hash.hexdigest()