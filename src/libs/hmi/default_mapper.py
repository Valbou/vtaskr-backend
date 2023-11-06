from dataclasses import asdict


def list_models_to_list_dto(dto_cls, objs: list | None) -> list:
    """
    Give a mapper DTO class and the corresponding list objects
    And retrieve a list of DTO objects
    """
    return [dto_cls.model_to_dto(obj) for obj in objs] if objs else []


def list_dto_to_dict(dtos: list) -> list[dict]:
    """
    Give list of DTO objects and retrieve a list of dict (for serialization)
    """
    return [asdict(dto) for dto in dtos]


def dto_to_dict(dto) -> dict:
    return asdict(dto)
