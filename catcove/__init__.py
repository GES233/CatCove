from .web.app import create_app

""" About `CatCove`.
    ~~~~
    
    `CatCove` is a free and open-source web-application 
    based on Sanic. This project is inspired by many 
    projects and ideas.

    My purpose for this is to build a tiny, fast, and 
    simple forum to avoid from the strictly cencorship.

    About this reposity.
    ~~~~

    I tried using "clean-architectrue" to biuld the 
    application, but the job only did half. What following 
    are package:

    catcove                         # Main package
    catcove.dependencies            # Some dependencies: e.g. ORM, Redis.
    catcove.dependencies.db         # Database
    catcove.commands                # Some custom commands
    catcove.entities                # Entities for business
    catcove.entities.tables         # ORM Objects
    catcove.entities.schemas        # Schemas for some interfaces
    catcove.services                # Middleware
    catcove.services.cors           # CORS
    catcove.services.security       # Some functions for encrypt.
    catcove.services.render         # Add a lister to storage the Jinja enviornment
    catcove.settings                # Settings (configure the app)
    catcove.settings.dev            # Develpoment settings
    catcove.settings.test           # Test settings
    catcove.settings.pro            # Production settings
    catcove.usecase
    catcove.usecase.api
    catcove.usecase.auth
    catcove.usecase.users
    catcove.utils                   # Some helper functions/classes
    catcove.web                     # Web applications
    catcove.web.app                 # 2 Application factory, one for running and one for configuring
    catcove.web.blueprints
    catcove.web.errorhanders        # Custome errorhander
    catcove.web.static              # Load static path to server

    where entities, usecase for domain;
    ...
    And here are other folders:

    catcove/static/                 # Static resources
    catcove/templates/              # HTML Templates
    migrate/                        # Migrate env and script for alembic
    instance/                       # Storge some config which not invisible for git.
    test/                           # Shown as its name

    Configure methods.
    ~~~~

    pass
"""
