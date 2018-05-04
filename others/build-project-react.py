#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# Created by obed ;)
# Comandos disponibles:
# release-project-react {project} {environment}  - Libera el proyecto en el environment especificado.

import subprocess
import os
import sys
import shutil
from common import (confirmMessage, printWithColor,getBasePathSource, getNameServer)

# Rama master
master_branch_name = 'master'

# Palabras clave de los proyectos válidos.
active_projects = ['cu', 'cp', 'au', 'ap', 'mar']

# Environments válidos.
active_enviroments = ['dev', 'test', 'demo', 'prod']

# Nombre real del proyecto en local.
project_names = {'cu': 'contest-user-react', 'cp': 'contest-panel-react','au': 'ask-apply', 'ap': 'ask-panel-react', 'mar': 'mybusiness-affiliate-react'}

# Proyecto donde se incluira los compilados dependiendo del environment.
project_src_path_dev = {'cu': 'contest-user-react', 'cp': 'contest-panel-react','au': 'ask-apply', 'ap': 'ask-panel-react', 'mar': 'mybusiness-affiliate-react'}
project_src_path_test = {'cu': 'stable-contest-user-react', 'cp': 'stable-contest-panel-react','au': 'stable-ask-apply', 'ap': 'stable-ask-panel-react', 'mar': 'stable-mybusiness-affiliate-react'}
project_src_path_demo = {'cu': 'demo-contest-user-react', 'cp': 'demo-contest-panel-react','au': 'demo-ask-apply', 'ap': 'demo-ask-panel-react', 'mar': 'demo-mybusiness-affiliate-react'}
project_src_path_prod = {'cu': 'contest-user-react', 'cp': 'contest-panel-react','au': 'ask-apply', 'ap': 'ask-panel-react', 'mar': 'mybusiness-affiliate-react'}

# Proyecto donde se incluira los compilados dependiendo del environment.
project_dst_path_dev = {'cu': 'contest-backend', 'cp': 'core','au': 'ask-backend', 'ap': 'core', 'mar': 'core'}
project_dst_path_test = {'cu': 'stable-contest', 'cp': 'stable-mybusiness','au': 'stable-ask', 'ap': 'stable-mybusiness', 'mar': 'stable-mybusiness'}
project_dst_path_demo = {'cu': 'demo-contest', 'cp': 'demo-mybusiness','au': 'demo-ask', 'ap': 'demo-mybusiness', 'mar': 'demo-mybusiness'}
project_dst_path_prod = {'cu': 'contest', 'cp': 'mybusiness','au': 'ask', 'ap': 'mybusiness', 'mar': 'mybusiness'}

# Nombre del archivo generado representando el Asset.php.
file_asset_name = {'cu': 'ContestAsset', 'cp': 'ContestAsset','au': 'ApplyAsset', 'ap': 'AskAsset', 'mar': 'MyBusinessAffiliateReactAsset'}

# Carpeta especifica donde se incluyen los compilados dentro de frontend/web
folder_web_name = {'cu': 'contest', 'cp': 'contest','au': 'apply', 'ap': 'ask', 'mar': 'mybusiness-affiliate-react'}

# Ruta temporal local para generar archivos antes de subirlos.
temp_path = "/Users/josemoguel/Documents/"

# Valida si el proyecto es uno registrado en la configuración.
def validProject(project):
    if not project in active_projects:
        printWithColor('\033[91m The project is not valid.')
        return False
    return True

# Busca los archivos .js y .css
def searchFiles(ruta):
    files = {'js': '', 'css': ''}
    for arch in os.scandir(ruta):
        filename, file_extension = os.path.splitext(arch.name)
        if file_extension == '.js':
            files['js'] = arch.name
        elif file_extension == '.css':
            files['css'] = arch.name
    return files

def getSrcProject(project, env="dev"):
    if env == "dev":
        return project_src_path_dev[project]
    if env == "test":
        return project_src_path_test[project]
    if env == "demo":
        return project_src_path_demo[project]
    if env == "prod":
        return project_src_path_prod[project]

# Obtener proyecto donde se guardaran los compilados.
def getDstProject(project, env="dev"):
    if env == "dev":
        return project_dst_path_dev[project]
    if env == "test":
        return project_dst_path_test[project]
    if env == "demo":
        return project_dst_path_demo[project]
    if env == "prod":
        return project_dst_path_prod[project]

# Generacion del archivo Asset.php
def buildFile(filename, project, compiled_files):
    name_assets = file_asset_name[project]
    folder_web = folder_web_name[project]

    archivo = open(filename, 'w')

    file = '<?php \n'
    file += '/** \n'
    file += '* @link http://www.yiiframework.com/ \n'
    file += '* @copyright Copyright (c) 2008 Yii Software LLC \n'
    file += '* @license http://www.yiiframework.com/license/ \n'
    file += '*/ \n'
    file += '\n'
    file += 'namespace frontend\\assets; \n'
    file += '\n'
    file += 'use yii\web\AssetBundle; \n'
    file += 'use Yii; \n'
    file += '\n'
    file += '/** \n'
    file += '* @author Qiang Xue <qiang.xue@gmail.com> \n'
    file += '* @since 2.0 \n'
    file += '*/ \n'
    file += 'class ' + name_assets + ' extends AssetBundle \n'
    file += '{ \n'
    file += '   public $basePath = \'@webroot\'; \n'
    file += '   public $baseUrl = \'@web\'; \n'
    file += '   public $css = [ \n'
    file += '       \'' + folder_web + '/' + compiled_files['css'] + '\', \n'
    file += '       \'//fonts.googleapis.com/css?family=Open+Sans::300,300i,400,400i,600,600i,700,700i\', \n'
    file += '   ]; \n'
    file += '   public $js = []; \n'
    file += '   public $depends = [ \n'
    file += '       \'yii\web\YiiAsset\', \n'
    file += '       \'yii\\bootstrap\BootstrapAsset\', \n'
    
     # Estos proyectos necesitan de este asset.
    if project in ['cu', 'au']:
        file += '       \'frontend\\assets\FontAwesomeAsset\' \n'

    file += '   ]; \n'
    file += '\n'
    file += '   public function init() \n'
    file += '   { \n'
    file += '       parent::init(); \n'
    file += '\n'
    file += '       $this->js[] = "'+folder_web+'/' + compiled_files['js'] + '"; \n'

    # Estos proyectos necesitan del api de maps.
    if project in ['mar']:
        file += '       $this->js[] = \'//maps.googleapis.com/maps/api/js?key=\'. Yii::$app->params[\'googleMapsApiKey\'] .\'&libraries=geometry,drawing,places\'; \n'     

    file += '\n'
    file += '   } \n'
    file += '}'

    archivo.write(file + '\n')
    archivo.close()

# Mueve un archivo de un directorio a otro.
def moveFile(src, dst):
    shutil.move(src, dst)

# Update solutions
def updateSolution(project_key, env = "dev", version = None):

    base_path_source = getBasePathSource(env)
    project_name = getSrcProject(project_key, env)
    project_path = getBasePathSource(env) + project_name
    sources_compiled_path = getBasePathSource(env) + project_name + "/dist"
    sources_compiled_dst = base_path_source + getDstProject(project_key, env) + '/frontend/web/' + folder_web_name[project_key]
    name_file_asset = file_asset_name[project_key]
    asset_src = temp_path + name_file_asset + '.php'
    asset_dst = base_path_source + getDstProject(project_key, env) + '/frontend/assets/' + name_file_asset + '.php'
    base_command = 'cd ' + project_path

    os.system('clear')
    printWithColor('\033[94m ***** Updating project: (' + project_name + ') in environment {' + env + '}*****')
    print('\n')

    print('==== info ===')
    print('base_path_source:' + base_path_source)
    print('project_name:' + project_name)
    print('project_path:' + project_path)
    print('sources_compiled_path:' + sources_compiled_path)
    print('sources_compiled_dst:' + sources_compiled_dst)
    print('asset_src:' + asset_src)
    print('asset_dst:' + asset_dst)
    print('name_file_asset:' + name_file_asset)
    print('\n')

    # Elimina archivos .js y .css en la carpeta destino.
    if version:
        command = 'git checkout ' + version 
    else:
        command = 'git checkout ' + master_branch_name 

    printWithColor('==== Checkout... ===')
    printWithColor('\033[93m command: `' + command)
    os.system(command)
    print('\n')
        
    # Elimina archivos .js y .css en la carpeta destino.
    command = 'rm -rf ' + sources_compiled_dst + '/*.js && rm -rf ' + sources_compiled_dst + '/*.css '
    printWithColor('==== Deleting old files .css and .js ===')
    printWithColor('\033[93m command: `' + command)
    os.system(command)
    print('\n')

    # Eliminando archivo asset.
    command = 'rm -r ' + asset_dst
    printWithColor('==== Deleting old asset file ===')
    printWithColor('\033[93m command: `' + command)
    os.system(command)
    print('\n')

    # Genera compilado.
    command = base_command + ' && npm run build:' + env
    printWithColor('==== Compiling project react `'+project_name+'`===')
    printWithColor('\033[93m command: npm run build:' + env)
    os.system(command)
    print('\n')

    # Analiza el directorio de compilación en busqueda del .js y .css.
    printWithColor('==== Analizing compiled files ===')
    compiled_files = searchFiles(sources_compiled_path)
    print(compiled_files)
    print('\n')

    # Mueve archivo compilado .js
    printWithColor('==== Moving compiled .js===')
    moveFile(sources_compiled_path + '/' + compiled_files['js'], sources_compiled_dst + '/' + compiled_files['js'])
    printWithColor('\033[93m File to move: `' + sources_compiled_dst + '/' + compiled_files['js'])
    print('\n')

    # Mueve archivo compilado .css
    printWithColor('==== Moving compiled .css===')
    moveFile(sources_compiled_path + '/' +compiled_files['css'], sources_compiled_dst + '/' + compiled_files['css'])
    printWithColor('\033[93m File to move: `' + sources_compiled_dst + '/' + compiled_files['css'])
    print('\n')

    # Genera el archivo de assets.
    printWithColor('==== Generating asset file ===')
    buildFile(asset_src, project_key, compiled_files)
    printWithColor('\033[93m File: `' + asset_src)
    print('\n')

    # Mueve el archivo de assets al directorio destino
    printWithColor('==== Moving asset ===')
    moveFile(asset_src, asset_dst)
    printWithColor('\033[93m Dst: `' + asset_dst)
    print('\n')

def main():

    project = sys.argv[1]
    env = "dev"
    version = None

    if len(sys.argv) == 3:
        env = sys.argv[2]

    if len(sys.argv) == 4:
        version = sys.argv[3]
    
    # Actualiza el proyecto especificado en el environment especificado.
    updateSolution(project, env, version)

main()
