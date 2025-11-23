from odoo import models, fields


class StockPutawayRule(models.Model):
    _inherit = 'stock.putaway.rule'

    owner_id = fields.Many2one('wms.owner', 'Owner',
                               domain=[('is_warehouse_owner', '=', True)])
    abc_category = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    ], 'ABC Category')
    max_capacity = fields.Float('Max Capacity')
    priority = fields.Integer('Priority', default=10)
    active = fields.Boolean('Active', default=True)