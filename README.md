# Sanic Scaffolding
Bootstrap a [Sanic](https://github.com/channelcat/sanic) project with [UVLoop](https://github.com/MagicStack/uvloop) to quickly prototype web projects using an insanely fast web framework combo - see [Sanic author's benchmark claims](https://github.com/channelcat/sanic#benchmarks).

This project provides scaffolding and auto discovery of blueprints to provide a basic structure to use for web server development.

The basic structure of this scaffold:

```
+-- project dir (sanic_scaffolding directory)
|   +-- blueprint1_package (dashboard directory)
|   |   +-- blueprint1_module (main.py)
|   +-- blueprint2_package (example only...)
|   .
|   .
|   .
|   +-- templates (template directory)
+-- run.py
```

This project dynamically imports blueprint modules from any directory under the project dir, that is not blacklisted in the IGNORE_NON_BLUEPRINTS configuration variable in the project_dir's __init__.py file.

As long as the <project dir>/__init__.py module remains intact, the structure of the website server can be extended by adding sub directories under the project dir, each of which contain an __init__.py file that declares a blueprints list. Each blueprint list item is a sanic::Blueprint object that has been configured. See the dashboard directory for an example

## Quick Start
Clone this repo, rename the sanic_scaffolding directory to the name of your project. Create your Python 3 virtual environment (`mkvirtualenv -p python3.5 sanic_project`) and install dependendencies: `pip3 install -r requirements.txt`

At this point, you can start the server by running `./run.py` and browsing to [http://localhost:8000/](http://localhost:8000) or [http://localhost:8000/main/](http://localhost:8000/main/).

## Enable SSL
If the USE_SSL environmental variable is set, or the USE_SSL variable is set to True in the '__init__.py file config section', a provide SSL certificate/key pair, which will be used to setup an SSL wrapped connection socket that is passed into sanic.

For instance to create SSL certificates: `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt`.

**DO NOT use the default certs for any sort of production environment; or anything not in development**

By default, the SSL feature uses recommended ciphers sourced from this website: (https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/)[https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/].

