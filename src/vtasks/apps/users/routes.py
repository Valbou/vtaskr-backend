from flask import Blueprint, request, jsonify


users_bp = Blueprint(
    name="users_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


# https://medium.com/swlh/creating-middlewares-with-python-flask-166bd03f2fd4
@users_bp.route("/login", methods=["POST"])
def login():
    """
    URL to login as an authorized user

    Need an email and a password
    Return a temporary token
    """
    if request.method == "POST":
        return jsonify()


@users_bp.route("/login/2fa", methods=["POST"])
def login2fa():
    """
    URL to send 2FA auth - Token required

    Need a temporary token and un numeric code
    Return an expiring token
    (30 minutes after last activity as a classique session)
    """


@users_bp.route("/logout", methods=["POST"])
def logout():
    """
    URL to logout a logged in user - Token required

    Need a expiring token
    Return a boolean
    """


@users_bp.route("/user", methods=["PUT", "PATCH"])
def user():
    """
    URL to modify user informations - Token required

    Need an expiring token
    Return a jsonify user updated
    """
