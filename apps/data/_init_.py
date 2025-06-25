# -*- encoding: utf-8 -*-

import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

db = SQLAlchemy()
login_manager = LoginManager()

# Add this import
from apps.data.tables import ChineseCalendar  # Add this line

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
