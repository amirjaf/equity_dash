# notes
'''
This file is used for handling anything image related.
I suggest handling the local file encoding/decoding here as well as fetching any external images.
'''

# package imports
import base64
import os

# logo information - dvrpc logo
cwd = os.getcwd()
logo_path = os.path.join(cwd, 'src', 'assets', 'logos', '1a_ColorPrimarySmall.png')
logo_tunel = base64.b64encode(open(logo_path, 'rb').read())
logo_encoded = 'data:image/png;base64,{}'.format(logo_tunel.decode())
# logo information - equity dash logo
logo_path_equity_dash = os.path.join(cwd, 'src', 'assets', 'logos', 'dvrpc_equity_dash_logo.svg')
with open(logo_path_equity_dash, 'rb') as logo_file:
    logo_tunel_equity_dash = base64.b64encode(logo_file.read())
logo_encoded_equity_dash = 'data:image/svg+xml;base64,{}'.format(logo_tunel_equity_dash.decode())


