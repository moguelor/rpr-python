#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

servers = {
    'prod': 'ec2.swapwink.com',
    'test': 'test-swapwink',
}

# Proyectos activos.
active_projects = ['cu', 'cp', 'au', 'ap', 'mar', 'ru', 'tp', 'mpr']

# Environments válidos, solo se ejecutarán los environments que esten configurados en esta variable.
active_enviroments = ['dev', 'test', 'demo', 'prod']

# Proyecto donde se incluira los compilados dependiendo del environment.
project_dst_path = {
    'cu': 'contest',
    'cp': 'mybusiness',
    'au': 'ask',
    'ap': 'mybusiness',
    'mar': 'mybusiness',
    'ru' : 'rewards',
    'tp' : 'mybusiness',
    'mpr' : 'mybusiness'
}

# Nombre del archivo generado representando el Asset.php.
file_asset_name = {
    'cu': 'ContestAsset',
    'cp': 'ContestAsset',
    'au': 'ApplyAsset',
    'ap': 'AskAsset',
    'mar': 'MyBusinessAffiliateReactAsset',
    'ru': 'ReactAsset',
    'tp': 'TriviaAsset',
    'mpr': 'MyBusinessProductReactAsset'
}

# Carpeta especifica donde se incluyen los compilados dentro de frontend/web
folder_web_name = {
    'cu': 'contest',
    'cp': 'contest',
    'au': 'apply',
    'ap': 'ask',
    'mar': 'mybusiness-affiliate-react',
    'ru' : 'react',
    'tp' : 'trivia',
    'mpr' : 'mybusiness-product-react'
}