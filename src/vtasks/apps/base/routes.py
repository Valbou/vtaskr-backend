from flask import render_template, jsonify, Blueprint


base_bp = Blueprint(
    name="base_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


@base_bp.route("/")
def hello():
    """Just a logo displayed to curious users"""
    return render_template("home.html")


@base_bp.route("/tests", methods=["GET"])
def tests():
    """URL to test flask - REMOVE ME"""
    # TODO: to remove when tests are done
    return jsonify({"test_num": 456, "test_str": "test"})

