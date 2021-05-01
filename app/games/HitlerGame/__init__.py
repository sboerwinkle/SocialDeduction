from flask import Blueprint

template_folder = "templates"
static_folder = "static"

hitler_bp = Blueprint('hitler', __name__,
                    template_folder=template_folder,
                    static_folder=static_folder)
