# -*- mode: python -*-
from kivy.deps import sdl2, glew
block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\ejrfl\\Desktop\\Point do Espetinho\\PontDoEspetinhoCaixa\\Projeto'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PointDoEspetinho',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='img\\icone.ico')
coll = COLLECT(exe, Tree('C:\\Users\\ejrfl\\Desktop\\Point do Espetinho\\PontDoEspetinhoCaixa\\Projeto'),
               a.binaries,
               a.zipfiles,
               a.datas,
			   *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='Point Do Espetinho')
