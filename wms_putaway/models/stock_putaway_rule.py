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

    # Inherit the native storage_category_id field and enhance its domain if needed
    storage_category_id = fields.Many2one(
        'stock.storage.category', string='Storage Category', ondelete='cascade', check_company=True,
        domain=['|', ('company_id', '=', False), ('company_id', '=', 'company_id')]
    )