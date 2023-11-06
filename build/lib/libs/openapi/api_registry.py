class OpenApiRegistry:
    """
    A simple class to register OpenApiv3 elements

    https://spec.openapis.org/oas/v3.1.0
    https://swagger.io/specification/
    Validator: https://www.postman.com/
    """

    def __init__(self) -> None:
        self.infos = None
        self.servers = []
        self.tags = []
        self.paths = dict()
        self.components = {
            "schemas": {},
            "requestBodies": {},
            "headers": {},
            "parameters": {},
            "responses": {},
            "securitySchemes": {},
        }

    def register_infos(self, infos: dict):
        self.infos = infos

    def register_server(self, url: str, description: str = ""):
        self.servers.append(
            {
                "url": url,
                "description": description,
            }
        )

    def register_path(self, path_name: str, path: dict):
        self.paths[path_name] = path

    def register_schemas_components(self, component_name: str, component: dict):
        self.components["schemas"][component_name] = component

    def register_request_components(self, component_name: str, component: dict):
        self.components["requestBodies"][component_name] = component

    def register_headers_components(self, component_name: str, component: dict):
        self.components["headers"][component_name] = component

    def register_parameters_components(self, component_name: str, component: dict):
        self.components["parameters"][component_name] = component

    def register_responses_components(self, component_name: str, component: dict):
        self.components["responses"][component_name] = component

    def register_security(self, security_name: str, security: dict):
        self.components["securitySchemes"][security_name] = security

    def register_tag(self, tag: dict):
        self.tags.append(tag)
