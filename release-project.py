#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

# Comandos disponibles:
#
# python3 release-project - Actualiza todos los proyectos en local.
# python3 release-project {project} - Actualiza el proyecto local especificado.
# python3 release-project {project} {environment}  - Actualiza el proyecto en el environment especificado.

import subprocess
import os
import sys
from common import (confirmMessage, printWithColor, getBasePathSource, getNameServer) 

# Proyectos válidos.
active_projects = ['mybusiness', 'coupon', 'contest', 'ask', 'rewards']

# Ambientes válidos.
active_enviroments = ['dev', 'test', 'demo', 'prod']

# Relacion enviroment -> rama
enviroment_map_branch = {'dev':'development', 'test' : 'stable', 'demo' : 'demo', 'prod' : 'master'}

# Dependencia de proyecto
project_react = {
    'mybusiness' : ['cp', 'ap', 'mar'],
    'contest' : ['cu'],
    'ask' : ['au'],
    'coupon' : [],
    'rewards' : []
}

# Relaciones nombre_clave -> proyecto por enviroment
project_names_dev = { 'contest' : 'contest-backend', 'ask' : 'ask-backend', 'rewards' : 'social', 'coupon' : 'coupon', 'mybusiness' : 'core'}
project_names_test = { 'contest' : 'stable-contest', 'ask' : 'stable-ask', 'rewards' : 'stable-rewards', 'coupon' : 'stable-coupon', 'mybusiness' : 'stable-mybusiness'}
project_names_demo = { 'contest' : 'demo-contest', 'ask' : 'demo-ask', 'rewards' : 'demo-rewards', 'coupon' : 'demo-coupon', 'mybusiness' : 'demo-mybusiness'}
project_names_prod = { 'contest' : 'contest', 'ask' : 'ask', 'rewards' : 'rewards', 'coupon' : 'coupon', 'mybusiness' : 'mybusiness'}

# Proyectos en react.
project_react_path_dev = {'cu': 'contest-user-react', 'cp': 'contest-panel-react','au': 'ask-apply', 'ap': 'ask-panel-react', 'mar': 'mybusiness-affiliate-react'}
project_react_path_test = {'cu': 'stable-contest-user-react', 'cp': 'stable-contest-panel-react','au': 'stable-ask-apply', 'ap': 'stable-ask-panel-react', 'mar': 'stable-mybusiness-affiliate-react'}
project_react_path_demo = {'cu': 'demo-contest-user-react', 'cp': 'demo-contest-panel-react','au': 'demo-ask-apply', 'ap': 'demo-ask-panel-react', 'mar': 'demo-mybusiness-affiliate-react'}
project_react_path_prod = {'cu': 'contest-user-react', 'cp': 'contest-panel-react','au': 'ask-apply', 'ap': 'ask-panel-react', 'mar': 'mybusiness-affiliate-react'}

# Obtener el nombre del proyecto.
def getProjectName(project, env = 'dev'):
    if(env == 'dev'):
        return project_names_dev[project]
    elif(env == 'test'):
        return project_names_test[project]
    elif(env == 'demo'):
        return project_names_demo[project]
    elif(env == 'prod'):
        return project_names_prod[project]

# Obtener el nombre del proyecto en react.
def getReactProjectName(project, env="dev"):
    if env == "dev":
        return project_react_path_dev[project]
    if env == "test":
        return project_react_path_test[project]
    if env == "demo":
        return project_react_path_demo[project]
    if env == "prod":
        return project_react_path_prod[project]

# Obtener el nombre de la rama.
def getBranchName(env = 'dev'):
    return enviroment_map_branch[env]

# Valida si el proyecto se encuentre dentro de la lista de permitidos.
def validProject(project):
    if not project in active_projects:
        printWithColor('\033[91m The project is not valid.')
        return False
    return True

# Verifica si es un enviroment que se require conectar a un servidor, se le concatena el ssh.
def verifyServer(command_to_run, env="dev"):
    name_server = getNameServer(env)
    if env == 'test' or env == 'demo' or env == 'prod':
        return 'ssh '+ name_server +' "'+ command_to_run +'" ' 
    elif env == 'dev':
        return command_to_run

def updateReactProjects(project, env):
    
    for projectReact in project_react[project]:
        printWithColor('==== Updating project react: `'+ getReactProjectName(projectReact, env) +'` ===')
        command = 'cd ' + getBasePathSource(env) + getReactProjectName(projectReact, env) +' && git checkout master && git pull'
        print(command)
        os.system(command)
        print('\n')

# Actualiza la solución especificada.
def updateSolution(project, env="dev"):
    os.system('clear')
    print('\n')
    printWithColor('\033[94m ***** Updating project: (' + project + ') in environment ' + env + '*****')
    print('\n')
   
    base_path_source = getBasePathSource(env)
    project_name = getProjectName(project, env)
    branch_name = getBranchName(env)
    directory = base_path_source + project_name
    name_server = getNameServer(env)
    
    base_command = 'cd  ' + directory

    if env=='test' or env=='demo':
        printWithColor('==== Conecting to server {'+ name_server +'}===')
        print('\n')

    # Checkout a rama del enviroment especificado.
    command = verifyServer(base_command +' && git checkout '+ branch_name, env)
    printWithColor('==== Checkout branch ' + branch_name + ' `' + command + '` ===')
    os.system(command)
    print('\n')

    # Hacer pull para bajar cambios.
    command = verifyServer(base_command +' && git pull ', env)
    printWithColor('==== Calling pull `'+ command +'` ===')
    os.system(command)
    print('\n')

    # DEPRECATED
    # Actualiza los proyectos dependientes en react.
    # updateReactProjects(project, env)

    # Actualiza composer
    noDev = ''
    if not env == 'dev':
        noDev = '--no-dev'

    command = verifyServer(base_command +' && composer update '+ noDev +' ', env)
    printWithColor('==== Updating composer `'+ command +'` ===')
    os.system(command)
    print('\n')

    # Inicializa la aplicación
    environment = env
    if env == 'dev':
        environment = 'Development'
    command = verifyServer(base_command +' && php init --env='+environment.capitalize()+' --overwrite=All', env)
    printWithColor('==== Init the project `'+command+'` ===')
    os.system(command)
    print('\n')

    # Corre migraciones
    command = verifyServer(base_command +' && php yii migrate --interactive=false', env)
    printWithColor('==== Run migrations  `'+command+'` ===')
    os.system(command)
    print('\n')

    # Aplica metas
    command = verifyServer(base_command +' && php yii metadata', env)
    printWithColor('==== Run metadatas  `'+command+'` ===')
    os.system(command)
    print('\n')

def init():

    numArguments = len(sys.argv)

    # El nombre del archivo lo toma como argumento.
    if numArguments == 1:
        # Si no tiene argumentos se actualizan en local todos los proyectos.
        if(confirmMessage('Are you sure to update all projects in ' + 'environment {development}')):
            for project in active_projects:
                updateSolution(project)

    # Si se le pasa un parametro se toma en cuenta que es un proyecto de local a actualizar.
    elif numArguments == 2:
        project = sys.argv[1]
        if(validProject(project)):
            if(confirmMessage('Are you sure to update {' + project + '} in ' + 'environment {development}')):
                updateSolution(project)

    # Si se le pasa dos parametros se toma en cuenta que el primero es el proyecto y el segundo es el environment.
    elif numArguments == 3:

            project = sys.argv[1]
            env = sys.argv[2]

            if(validProject(project)):
                if(confirmMessage('Are you sure to update {' + project + '} in ' + 'environment {' + env + '}')):
                    updateSolution(project, env)
    else:
        printWithColor('\033[91m Num parameters invalid.')


init()



