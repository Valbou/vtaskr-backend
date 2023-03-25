from flask import render_template, Blueprint


base_bp = Blueprint(
    name="base_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


@base_bp.route("/", methods=["GET"])
def hello():
    """Just a logo displayed to curious users"""
    return render_template("home.html")
