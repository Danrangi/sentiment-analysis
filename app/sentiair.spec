# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all necessary hidden imports
hidden_imports = [
    'sklearn',
    'sklearn.svm',
    'sklearn.svm._classes',
    'sklearn.feature_extraction.text',
    'sklearn.naive_bayes',
    'sklearn.ensemble',
    'sklearn.preprocessing',
    'sklearn.metrics',
    'sklearn.utils',
    'sklearn.utils._bunch',
    'sklearn.utils.validation',
    'sklearn.utils._param_validation',
    'sklearn.pipeline',
    'joblib',
    'nltk',
    'nltk.tokenize',
    'nltk.corpus',
    'nltk.stem',
    'flask',
    'flask.templating',
    'jinja2',
    'werkzeug',
    'numpy',
    'scipy',
    'scipy.sparse',
    'scipy.sparse._compressed',
    'scipy.sparse._csr',
    'threadpoolctl',
]

# Data files to bundle
datas = [
    ('app/templates',  'app/templates'),
    ('app/static',     'app/static'),
    ('models',         'models'),
    ('data',           'data'),
]

# Bundle NLTK data
import nltk
nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
if os.path.exists(nltk_data_path):
    datas.append((nltk_data_path, 'nltk_data'))

a = Analysis(
    ['launcher.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'pandas', 'tkinter', 'PyQt5', 'wx'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SentiAir',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # ← no black terminal window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # ← add 'app/static/icon.ico' if you have one
)
