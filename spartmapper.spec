# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import site
p = site.getsitepackages()[-1] + '/'
data_sites = [
  (p + 'branca/templates','templates'),
  (p + 'branca','branca'),
  (p + 'branca-0.4.2.dist-info','branca-0.4.2.dist-info'),
  (p + 'folium/templates','templates'),
  (p + 'folium/plugins','plugins'),
  (p + 'folium-0.12.1.dist-info','folium-0.12.1.dist-info'),
  (p + 'folium','folium'),
  (p + 'pyzmq.libs','pyzmq.libs'),
]


hiddenimports = [
  'numpy',
  'dendropy',
  'scipy.integrate.lsoda',
  'sklearn.utils._cython_blas',
  'sklearn.neighbors.typedefs',
  'sklearn.neighbors.quad_tree',
  'sklearn.tree',
  'sklearn.tree._utils',
  'pandas._libs.tslibs.timedeltas',
  'scipy.special._ufuncs_cxx',
  'scipy.linalg.cython_blas',
  'scipy.linalg.cython_lapack',
  'scipy.integrate',
  'scipy.integrate.quadrature',
  'scipy.integrate.odepack',
  'scipy.integrate._odepack',
  'scipy.integrate.quadpack',
  'scipy.integrate._quadpack',
  'scipy.integrate._ode',
  'scipy.integrate.vode',
  'scipy.integrate._dop',
  'scipy.integrate.lsoda',
  'scipy._lib.messagestream' ,
]


a = Analysis(['mapper_spart.py'],
             binaries=[],
             datas=([('icon','icon'),
                   ('test.ui', '.'),
                   ('mapper_model.py', '.'),
                   ('photo.qrc', '.'),
                   ('photo_rc.py', '.'),
                ] + data_sites),
             hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
         a.scripts,
         a.binaries,
         a.zipfiles,
         a.datas,
         [],
         name='spartmapper',
         debug=False,
         bootloader_ignore_signals=False,
         strip=False,
         upx=True,
         upx_exclude=[],
         runtime_tmpdir=None,
         console=False,
         icon='icons/Spart mapper ICON.ico' )
