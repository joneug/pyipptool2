import colander
from .widgets import (IPPAttributeWidget, IPPBodyWidget, IPPDisplayWidget,
                      IPPGroupWidget, IPPNameWidget, IPPTupleWidget,
                      IPPConstantTupleWidget)


class Charset(colander.String):
    pass


class Enum(colander.String):
    pass


class Keyword(colander.String):
    pass


class Language(colander.String):
    pass


class Name(colander.String):
    pass


class Text(colander.String):
    def serialize(self, node, appstruct):
        value = super(Text, self).serialize(node, appstruct)
        if value is colander.null:
            return colander.null
        return '"{}"'.format(value)


class Uri(colander.String):
    pass


class OperationAttributes(colander.Schema):
    attributes_charset = colander.SchemaNode(Charset(),
                                             default='utf-8',
                                             widget=IPPAttributeWidget())
    attributes_natural_language = colander.SchemaNode(
        Language(),
        default='en',
        widget=IPPAttributeWidget())


class SubscriptionOperationAttributes(OperationAttributes):
    printer_uri = colander.SchemaNode(Uri(),
                                      widget=IPPAttributeWidget())
    requesting_user_name = colander.SchemaNode(Name(),
                                               widget=IPPAttributeWidget())


class HeaderIPPSchema(colander.Schema):
    name = colander.SchemaNode(colander.String(), widget=IPPNameWidget())
    operation = colander.SchemaNode(colander.String(), widget=IPPNameWidget())
    operation_attributes_tag = colander.SchemaNode(colander.String(),
                                                   widget=IPPGroupWidget())
    required_attributes = OperationAttributes(widget=IPPTupleWidget())
    object_attributes_tag = colander.SchemaNode(
        colander.String(),
        widget=IPPGroupWidget())


class BaseIPPSchema(colander.Schema):
    operation_attributes_tag = 'operation-attributes-tag'
    header = HeaderIPPSchema(widget=IPPConstantTupleWidget())


class CupsAddModifyPrinterSchema(BaseIPPSchema):
    name = 'CUPS Add Modify Printer'
    operation = 'CUPS-Add-Modify-Printer'
    object_attributes_tag = 'printer-object-attributes-tag'
    auth_info_required = colander.SchemaNode(Keyword(),
                                             widget=IPPAttributeWidget())
    job_sheets_default = colander.SchemaNode(Name(),
                                             widget=IPPAttributeWidget())
    device_uri = colander.SchemaNode(Uri(),
                                     widget=IPPAttributeWidget())
    port_monitor = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    ppd_name = colander.SchemaNode(Name(), widget=IPPAttributeWidget())
    printer_is_accepting_jobs = colander.SchemaNode(
        colander.Boolean(false_val=0, true_val=1),
        widget=IPPAttributeWidget())
    printer_info = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    printer_location = colander.SchemaNode(Text(), widget=IPPAttributeWidget())
    printer_more_info = colander.SchemaNode(Uri(), widget=IPPAttributeWidget())
    printer_state = colander.SchemaNode(Enum(), widget=IPPAttributeWidget())
    printer_state_message = colander.SchemaNode(
        Text(),
        widget=IPPAttributeWidget())
    requesting_user_name_allowed = colander.SchemaNode(
        Name(),
        widget=IPPAttributeWidget())
    requesting_user_name_denied = colander.SchemaNode(
        Name(),
        widget=IPPAttributeWidget())


class CupsAddModifyClassSchema(CupsAddModifyPrinterSchema):
    name = 'CUPS Add Modify Class'
    operation = 'CUPS-Add-Modify-Class'


class CupsRejectJobsSchema(BaseIPPSchema):
    name = 'CUPS Reject Jobs'
    operation = 'CUPS-Reject-Jobs'
    object_attributes_tag = 'printer-object-attributes-tag'
    printer_state_message = colander.SchemaNode(
        Text(),
        widget=IPPAttributeWidget())


class CreatePrinterSubscriptionSchema(BaseIPPSchema):
    name = 'Create Printer Subscription'
    operation = 'Create-Printer-Subscription'
    object_attributes_tag = 'subscription-attributes-tag'
    notify_recipient_uri = colander.SchemaNode(Uri(),
                                               widget=IPPAttributeWidget())
    notify_events = colander.SchemaNode(Keyword(),
                                        widget=IPPAttributeWidget())
    notify_lease_duration = colander.SchemaNode(colander.Integer(),
                                                widget=IPPAttributeWidget())
    notify_lease_expiration_time = colander.SchemaNode(
        colander.Integer(),
        widget=IPPAttributeWidget())
    notify_subscription_id = colander.SchemaNode(colander.String(),
                                                 widget=IPPDisplayWidget())


create_printer_subscription_schema = CreatePrinterSubscriptionSchema(
    widget=IPPBodyWidget())
create_printer_subscription_schema['header']['required_attributes'] =\
    SubscriptionOperationAttributes(widget=IPPTupleWidget())

cups_add_modify_class_schema = CupsAddModifyClassSchema(
    widget=IPPBodyWidget())

cups_add_modify_printer_schema = CupsAddModifyPrinterSchema(
    widget=IPPBodyWidget())

cups_reject_jobs_schema = CupsRejectJobsSchema(widget=IPPBodyWidget())
