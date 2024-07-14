from datetime import timedelta

from flask import current_app, g, request
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import dto_to_dict, list_dto_to_dict, list_models_to_list_dto
from src.libs.redis import rate_limited
from src.users.hmi.dto import INVITATION_COMPONENT, InvitationMapperDTO
from src.users.hmi.flask.decorators import login_required
from src.users.services import UserService

from .. import V1, logger, openapi, users_bp

api_item = {
    "get": {
        "description": "Get invitations waiting for acceptation",
        "summary": "Get invitations",
        "operationId": "getInvitations",
        "parameters": [
            {
                "name": "group_id",
                "in": "path",
                "description": "Id of the group's invitations you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "An invitations list",
                "content": {
                    "application/json": {"schema": {"$ref": INVITATION_COMPONENT}}
                },
            },
        },
    },
}
openapi.register_path(f"{V1}/group/{{group_id}}/invitations", api_item)


@users_bp.route(f"{V1}/group/<string:group_id>/invitations", methods=["GET"])
@login_required(logger)
@rate_limited(logger=logger, hit=30, period=timedelta(seconds=60))
def group_invitations(group_id: str):
    user_service = UserService(current_app.dependencies)
    invitations = user_service.get_invitations(g.user.id, group_id)

    if invitations is not None:
        invitations_dto = list_models_to_list_dto(InvitationMapperDTO, invitations)
        return ResponseAPI.get_response(list_dto_to_dict(invitations_dto), 200)

    else:
        return ResponseAPI.get_403_response()


api_item = {
    "post": {
        "description": "Send invitation to join a group",
        "summary": "Invite in group",
        "operationId": "postInvitationGroup",
        "responses": {
            "201": {
                "description": "no response content",
                "content": {
                    "application/json": {"schema": {"$ref": INVITATION_COMPONENT}}
                },
            },
            "400": {
                "description": "Bad request format",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "Invitation data",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "to_user_email": {
                                "type": "string",
                                "format": "email",
                                "example": "my@email.com",
                            },
                            "in_group_id": {
                                "type": "string",
                            },
                            "with_roletype_id": {
                                "type": "string",
                            },
                        },
                        "required": [
                            "from_user_id",
                            "to_user_email",
                            "in_group_id",
                            "with_roletype_id",
                        ],
                    }
                }
            },
            "required": True,
        },
        "security": [],
    },
}
openapi.register_path(f"{V1}/invite", api_item)


@users_bp.route(f"{V1}/invite", methods=["POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=10, period=timedelta(seconds=300))
def invite():
    """
    URL to invite someone to contribute to an owned group

    Need to be logged in and the user invited email and some ids :
    group_id, roletype_id
    """

    payload: dict = request.get_json()

    to_user_email = payload.get("to_user_email", "")
    in_group_id = payload.get("in_group_id", "")
    with_roletype_id = payload.get("with_roletype_id", "")

    if not all([to_user_email, in_group_id, with_roletype_id]):
        logger.warning("400 Error: some required values missing")
        return ResponseAPI.get_400_response()

    try:
        user_service = UserService(services=current_app.dependencies)
        invitation = user_service.invite_user_by_email(
            user=g.user,
            user_email=to_user_email,
            group_id=in_group_id,
            roletype_id=with_roletype_id,
        )

        invitation_dto = InvitationMapperDTO.model_to_dto(invitation)
        return ResponseAPI.get_response(dto_to_dict(invitation_dto), 201)

    except PermissionError as e:
        logger.warning(f"403: Error permission denied in invitation process: {e}")
        return ResponseAPI.get_403_response("Check your role level for this group.")

    except Exception as e:
        logger.warning(f"400: Error during invitation process {e}")
        return ResponseAPI.get_400_response()


api_item = {
    "post": {
        "description": "Accept invitation with an account",
        "summary": "To join a group",
        "operationId": "postInvitationAccept",
        "responses": {
            "200": {
                "description": "no response content",
                "content": {},
            },
            "400": {
                "description": "Bad request format",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "To find the correct invitation",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "hash": {
                                "type": "string",
                                "example": "a91776c5fbbde1910bc55e7390417d54805a99b0",
                            },
                        },
                        "required": [
                            "hash",
                        ],
                    }
                }
            },
            "required": True,
        },
        "security": [],
    },
}
openapi.register_path(f"{V1}/invite/accepted", api_item)


@users_bp.route(f"{V1}/invite/accepted", methods=["POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=300))
def invitation_accepted():
    """
    URL to accept an invitation

    Need to be logged in
    """
    payload: dict = request.get_json()
    invitation_hash = payload.get("hash", "")

    try:
        user_service = UserService(services=current_app.dependencies)
        user_service.accept_invitation(user=g.user, hash=invitation_hash)

        data = {}
        return ResponseAPI.get_response(data, 200)

    except Exception as e:
        logger.warning(f"400: Error during invitation acceptation process {e}")
        return ResponseAPI.get_400_response()


api_item = {
    "delete": {
        "description": "Delete an invitation with specified id",
        "summary": "Delete an invitation",
        "operationId": "deleteInvitation",
        "parameters": [
            {
                "name": "invitation_id",
                "in": "path",
                "description": "Id of invitation you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "204": {
                "description": "no content",
                "content": {},
            },
        },
    },
}
openapi.register_path(f"{V1}/invite/{{invitation_id}}", api_item)


@users_bp.route(f"{V1}/invite/<string:invitation_id>", methods=["DELETE"])
@login_required(logger)
@rate_limited(logger=logger, hit=10, period=timedelta(seconds=300))
def invitation_cancel(invitation_id: str):
    """
    URL to delete an invitation

    Need to be logged in
    """

    try:
        user_service = UserService(services=current_app.dependencies)
        user_service.delete_invitation(user=g.user, invitation_id=invitation_id)

        data = {}
        return ResponseAPI.get_response(data, 204)

    except PermissionError as e:
        logger.warning(f"403: Error permission denied in invitation process: {e}")
        return ResponseAPI.get_403_response("Check your role level for this group.")

    except Exception as e:
        logger.warning(f"400: Error during invitation cancel process {e}")
        return ResponseAPI.get_400_response()
