from pkg_resources import resource_filename

import deform.template

from .schemas import (create_printer_subscription_schema,
                      cups_add_modify_class_schema,
                      cups_add_modify_printer_schema,
                      cups_reject_jobs_schema,
                      )

default_dir = resource_filename('pyipptool', 'templates/')
renderer = deform.template.ZPTRendererFactory((default_dir,))

deform.Form.set_default_renderer(renderer)


create_printer_subscription_form = deform.Form(
    create_printer_subscription_schema)
cups_add_modify_printer_form = deform.Form(cups_add_modify_printer_schema)
cups_add_modify_class_form = deform.Form(cups_add_modify_class_schema)
cups_reject_jobs_form = deform.Form(cups_reject_jobs_schema)
