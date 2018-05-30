#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

# Comandos disponibles:
#
# rpr - Libera todos los proyectos en el environment "dev".
# rpr {project} - Libera el proyecto especificado en el enviroment "dev".
# rpr {project} {environment}  - Libera el proyecto en el environment especificado.
# rpr all {environment}  - Libera todos los proyectos en el environment especificado.
# rpr {project} all  - Libera el proyecto en todos los environments.
# rpr all  - Libera todos los proyectos en todos los environments.
# rpr {project} {environment} {branch} - Libera el compilado desde la rama especificada del proyecto.
# rpr {project1,project2} {environment} - Libera los proyectos en el environment especificado.

import os
import sys
import shutil
from common import (confirmMessage, printWithColor,getBasePathSource, getNameServer)
from config.settings import (active_projects, active_enviroments, project_dst_path, file_asset_name, folder_web_name)
from config.local_settings import (temp_path, project_names, project_dst_path_dev)

# Rama master
master_branch_name = 'master'

# Obtener la rama master.
def getBranchMaster():
    return master_branch_name

# Asignar la rama master.
def setBranchMaster(branch):
    global master_branch_name
    master_branch_name = branch

# Valida si el proyecto es uno registrado en la configuración.
def validProject(project):
    if not project in active_projects:
        printWithColor('\033[91m The project {'+ project +'} is not valid.')
        return False
    return True

# Verifica si es un enviroment que se require conectar a un servidor, se le concatena el ssh.
def verifyServer(command_to_run, env="dev", force = False):
    name_server = getNameServer(env)
   
    if env == 'test' or env == 'demo' or env == 'prod':
        if force:
            command_to_run = 'sudo ' + command_to_run
        return 'ssh ' + name_server + ' "' + command_to_run + '" '
    elif env == 'dev':
        return command_to_run

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

# Obtener proyecto donde se guardaran los compilados.
def getDstProject(project, env="dev"):
    if env == "dev":
        return project_dst_path_dev[project]
    if env == "test":
        project_prefix = 'stable-'
    if env == "demo":
        project_prefix = 'demo-'
    if env == "prod":
        project_prefix = ''
    return project_prefix + project_dst_path[project]

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

    if project in ['ru']:
        file += '       \'css/react.css\', \n'
        file += '       \'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css\', \n'
        file += '       \'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css\', \n'
        file += '       \'https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.6.0/slick.min.css\', \n'
        file += '       \'https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.6.0/slick-theme.min.css\', \n'

    file += '   ]; \n'
    file += '   public $js = []; \n'
    file += '   public $depends = [ \n'
    file += '       \'yii\web\YiiAsset\', \n'
    if project not in ['ru']:
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
    if project in ['mar', 'ru']:
        file += '       $this->js[] = \'//maps.googleapis.com/maps/api/js?key=\'. Yii::$app->params[\'googleMapsApiKey\'] .\'&libraries=geometry,drawing,places\'; \n'     

    # Estos proyectos necesitan del api de maps.
    if project in ['ru']:
        file += '       $this->js[] = \'https://code.jquery.com/jquery-3.2.1.slim.min.js\'; \n'
        file += '       $this->js[] = \'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js\'; \n'     
        file += '       $this->js[] = \'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js\'; \n'     

    
    file += '\n'
    file += '   } \n'
    file += '}'

    archivo.write(file + '\n')
    archivo.close()

# Mueve un archivo de un directorio a otro.
def moveFile(src, dst):
    shutil.move(src, dst)

# Sube un archivo del local al servidor.
def uploadFileLocalToServer(src, dst, name_server):
    command = 'scp ' + src + ' ' + name_server + ':' + dst
    printWithColor('command: `' + command)
    os.system(command)

# Subir los archivos especificados.
def uploadFile(src, dst, env="dev"):
    if env == "dev":
        moveFile(src, dst)
    if env == "test" or env == "demo" or env == "prod":
        uploadFileLocalToServer(src, dst, getNameServer(env))


# Update solutions
def updateSolution(project_key, env="dev"):
    base_path_source = getBasePathSource(env)
    project_name = project_names[project_key]
    project_path = getBasePathSource('dev') + project_name
    sources_compiled_path = getBasePathSource('dev') + project_name + "/dist"
    sources_compiled_dst = base_path_source + getDstProject(project_key, env) + '/frontend/web/' + folder_web_name[project_key]
    name_file_asset = file_asset_name[project_key]
    asset_src = temp_path + name_file_asset + '.php'
    asset_dst = base_path_source + getDstProject(project_key, env) + '/frontend/assets/' + name_file_asset + '.php'
    name_server = getNameServer(env)
    base_command = 'cd ' + project_path

    os.system('clear')
    printWithColor('\033[94m ***** Updating project: (' + project_name + ') in environment {' + env + '}*****')
    print('\n')

    if env == 'test' or env == 'demo' or env == 'prod':
        printWithColor('==== Conecting to server {' + name_server + '}===')
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

    # Checkout a rama del enviroment especificado por default es master.
    command = base_command + ' && git checkout ' + master_branch_name
    printWithColor('==== Checkout branch { ' + master_branch_name + ' } ===')
    printWithColor('\033[94m command: git checkout ' + master_branch_name)
    os.system(command)
    print('\n')

    # Baja los cambios de master.
    command = base_command + ' && git pull origin ' + master_branch_name
    printWithColor('==== Git pull { ' + master_branch_name + ' } ===')
    printWithColor('\033[94m command: git pull origin ' + master_branch_name)
    os.system(command)
    print('\n')

    # Elimina los assets dentro de frontend/web/
    command = verifyServer('rm -r ./' + getDstProject(project_key, env) + '/frontend/web/assets/*', env, True)
    printWithColor('==== Deleting assets from frontend/web/assets ===')
    printWithColor('\033[94m command: `' + command)
    os.system(command)
    print('\n')

    # Genera compilado.
    command = base_command + ' && npm run build:' + env
    printWithColor('==== Compiling project react `'+project_name+'`===')
    printWithColor('\033[94m command: npm run build:' + env)
    os.system(command)
    print('\n')

    # Analiza el directorio de compilación en busqueda del .js y .css.
    printWithColor('==== Analizing files compiled ===')
    compiled_files = searchFiles(sources_compiled_path)
    print(compiled_files)
    print('\n')

    # Subir archivo compilado .js
    printWithColor('==== Moving compiled .js===')
    uploadFile(sources_compiled_path + '/' + compiled_files['js'], sources_compiled_dst + '/' + compiled_files['js'], env)
    printWithColor('File to upload: `' + compiled_files['js'])
    print('\n')

    # Subir archivo compilado .css
    printWithColor('==== Moving compiled .css===')
    uploadFile(sources_compiled_path + '/' +compiled_files['css'], sources_compiled_dst + '/' + compiled_files['css'], env)
    printWithColor('\033[94m File to upload: `' + compiled_files['css'])
    print('\n')

    # Genera el archivo de assets.
    printWithColor('==== Generating asset file ===')
    buildFile(asset_src, project_key, compiled_files)
    printWithColor('\033[94m File: `' + asset_src)
    print('\n')

    # Mueve el archivo de assets al directorio destino
    printWithColor('==== Moving asset ===')
    uploadFile(asset_src, asset_dst, env)
    printWithColor('\033[94m Dst: `' + asset_dst)
    print('\n')

def main():

    numArguments = len(sys.argv)

    # El nombre del archivo lo toma como argumento.
    if numArguments == 1:
        # Si no tiene argumentos se actualizan en local todos los proyectos.
        if(confirmMessage('Are you sure to release { ALL } projects in ' + 'environment { dev }')):
            for project in active_projects:
                updateSolution(project)

    # Si se le pasa un parametro se toma en cuenta que es un proyecto de local a actualizar.
    elif numArguments == 2:
        project = sys.argv[1]
        projects = project.split(',')

        # Actualiza todos los proyectos en todos los environments
        if project == 'all':
            if(confirmMessage('Are you sure to release { ALL } projecst in { ALL } environments')):
                for env in active_enviroments:
                    for project in active_projects:
                        updateSolution(project, env)
        # Identifica si se pasó un arreglo de proyectos.
        elif isinstance(projects, list):
            names = ''
            for idx,project in enumerate(projects):
                if(validProject(project)):
                    names = names + project_names[project] 
                    if ((idx + 1) < len(projects)):
                        names += ', '
                
            if(confirmMessage('Are you sure to release { '+ names +' } projects in environment { dev }')):
                for project in projects:
                    if(validProject(project)):
                        updateSolution(project)

    # Si se le pasa dos parametros se toma en cuenta que el primero es el proyecto y el segundo es el environment.
    elif numArguments == 3 or numArguments == 4:

        project = sys.argv[1]
        projects = project.split(',')
        env = sys.argv[2]

        # Especifica la rama del proyecto base a compilar 'master | development '
        if numArguments == 4:
            setBranchMaster(sys.argv[3])

        # Actualiza todos los proyectos del environment especificados.
        if project == 'all':
            if(confirmMessage('Are you sure to release { ALL } projects in ' + 'environment {' + env + '}')):
                for project in active_projects:
                    updateSolution(project, env)

        # Actualiza el proyecto especificado en todos los environments disponibles.
        elif env == 'all':
            if(confirmMessage('Are you sure to release {' + project_names[project] + '} in { ALL } environments')):
                for env in active_enviroments:
                    updateSolution(project, env)
        # Identifica si se pasó un arreglo de proyectos.
        elif isinstance(projects, list):
            names = ''
            for idx,project in enumerate(projects):
                if(validProject(project)):
                    names = names + project_names[project] 
                    if ((idx + 1) < len(projects)):
                        names += ', '
            if(confirmMessage('Are you sure to release { '+ names +' } projects in environment {' + env + '}')):
                for project in projects:
                    if(validProject(project)):
                        updateSolution(project, env)
    else:
        printWithColor('\033[91m Num parameters invalid.')

main()
