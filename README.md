# Release Project React (Python)

Build compiled react files in the many projects.

1. Install `python3` with `brew` or with installer in the page https://www.python.org/download/releases/3.0/.
2. Create the file `config/local_settings.py`
2. Config your react names folders depending your local:

```python
project_names = {
      'cu': 'contest-user-react', 
      'cp': 'contest-panel-react',
      'au': 'ask-apply', 
      'ap': 'ask-panel-react', 
      'mar': 'mybusiness-affiliate-react'
}
```
3. Config your project in your local where the compiled files will be included.
```python
project_dst_path_dev = {
  'cu': 'contest-backend', 
  'cp': 'core',
  'au': 'ask-backend', 
  'ap': 'core', 
  'mar': 'core'
}
```
4. Config the temp path, this directory will be the place to process the file.
  
```python 
  temp_path = "/Users/josemoguel/Documents/"
```

5. Config the base local source, this directory has all your swapwink's proyects.
  
```python
base_path_local_source = '/Users/josemoguel/Documents/fuentes/swapwink/'
```
6. Generate a link to file `release-project-react.py`.
```
ln -s /Users/josemoguel/Documents/scripts-python/release-project-react.py rpr
```
7. Search your python3 path with `which python3`
```
/usr/bin/python3
```
8. Move the file `rpr` to `/usr/bin/` to access the command globally.
```
mv rpr /usr/bin/rpr
```
9. Run rpr

# Commands

1. You can release all projects in the environment `dev`:
```
rpr
```

2. You can release the project in the environment `dev`:
```
rpr {project_key}
```

3. You can release the project in the environment specified.
```
rpr {project_key} {environment}
```

4. You can release all projects in the environment.
```
rpr all {environment}
```

5. You can release the project in all environments.
```
rpr {project_key} all
```

6. You can release all projects in all environments.
```
rpr all
```

7. You can release the project in the environment and version specified.
```
rpr {project_key} {environment} {tag_version}
```

7. You can release many projects in the environment and version specified.
```
rpr {project_key_1,project_key_2} {environment}
```

#Projects Keys

```
cu - contest.user.react
cp - contest.panel.react
au - ask.apply.react
ap - ask.panel.react
mar - mybusiness.affiliate.react
ru - rewards.user.react
```




