from odoo import models, fields


class WmsCargoType(models.Model):
    _name = 'wms.cargo.type'
    _description = 'Cargo Type'

    name = fields.Char('Cargo Type Name', required=True)
    code = fields.Char('Code', required=True)
    description = fields.Text('Description')
    handling_instructions = fields.Text('Handling Instructions')
    storage_requirements = fields.Text('Storage Requirements')
    temperature_range = fields.Char('Temperature Range')
    humidity_range = fields.Char('Humidity Range')
    special_equipment_required = fields.Boolean('Special Equipment Required')
    special_equipment_type = fields.Char('Special Equipment Type')
    insurance_required = fields.Boolean('Insurance Required')
    insurance_notes = fields.Text('Insurance Notes')
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Cargo type code must be unique!')
    ]