from flask import Blueprint

template_folder = "templates"
static_folder = "static"

avalon_bp = Blueprint('avalon', __name__,
                    template_folder=template_folder,
                    static_folder=static_folder)