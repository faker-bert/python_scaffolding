from {{project_name}}.utils.module_importer import import_string
from {{project_name}}.settings import global_settings


router = APIRouter()


for module in global_settings.enable_module:
    router.include_router(
        import_string('{{project_name}}.www.modules' + {module} + '.endpoints.router'),
        prefix=f'/{module}',
        tags=[module]
    )