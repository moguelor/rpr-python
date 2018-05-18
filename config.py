#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

# Nombre del servidor de test.
name_server_test = 'test-swapwink'

# Nombre del servidor de producción.
name_server_prod = 'ec2.swapwink.com'

# Proyectos activos.
active_projects = ['cu', 'cp', 'au', 'ap', 'mar']

# Environments válidos, solo se ejecutarán los environments que esten configurados en esta variable.
active_enviroments = ['dev', 'test', 'demo']

# Proyecto donde se incluira los compilados dependiendo del environment.
project_dst_path_test = {
    'cu': 'stable-contest', 
    'cp': 'stable-mybusiness',
    'au': 'stable-ask', 
    'ap': 'stable-mybusiness', 
    'mar': 'stable-mybusiness',
    'ru' : 'stable-rewards'
}
project_dst_path_demo = {
    'cu': 'demo-contest', 
    'cp': 'demo-mybusiness',
    'au': 'demo-ask', 
    'ap': 'demo-mybusiness', 
    'mar': 'demo-mybusiness',
    'ru' : 'demo-rewards'
}
project_dst_path_prod = {
    'cu': 'contest', 
    'cp': 'mybusiness',
    'au': 'ask', 
    'ap': 'mybusiness', 
    'mar': 'mybusiness',
    'ru' : 'rewards'
}

# Nombre del archivo generado representando el Asset.php.
file_asset_name = {
    'cu': 'ContestAsset', 
    'cp': 'ContestAsset',
    'au': 'ApplyAsset', 
    'ap': 'AskAsset', 
    'mar': 'MyBusinessAffiliateReactAsset',
    'ru': 'ReactAffiliateAsset'
}

# Carpeta especifica donde se incluyen los compilados dentro de frontend/web
folder_web_name = {
    'cu': 'contest', 
    'cp': 'contest',
    'au': 'apply', 
    'ap': 'ask', 
    'mar': 'mybusiness-affiliate-react',
    'ru' : 'react'
}