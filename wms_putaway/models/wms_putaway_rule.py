from odoo import models, fields, api


class WmsPutawayRule(models.Model):
    _name = 'wms.putaway.rule'
    _description = 'WMS Putaway Rule'

    name = fields.Char('Rule Name', required=True)
    owner_id = fields.Many2one('wms.owner', 'Owner',
                               domain=[('is_warehouse_owner', '=', True)])
    product_id = fields.Many2one('product.product', 'Product')
    product_category_id = fields.Many2one('product.category', 'Product Category')
    abc_category = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    ], 'ABC Category')
    location_in_id = fields.Many2one('stock.location', 'Apply In', required=True)
    location_out_id = fields.Many2one('stock.location', 'Put Into', required=True)
    max_capacity = fields.Float('Max Capacity')
    priority = fields.Integer('Priority', default=10)
    active = fields.Boolean('Active', default=True)

    @api.model
    def _get_putaway_strategy(self, product, quantity, location, package=None, from_move_id=None):
        """Override to include owner-specific putaway rules"""
        # First try to find a specific rule for the owner
        if hasattr(self.env.context, 'current_owner_id'):
            owner_id = self.env.context.get('current_owner_id')
            domain = [
                ('owner_id', '=', owner_id),
                ('product_id', '=', product.id),
                ('location_in_id', 'child_of', location.id),
                ('active', '=', True)
            ]
            rule = self.search(domain, order='priority desc', limit=1)
            if rule:
                return rule.location_out_id

        # Then try without owner for general rules
        domain = [
            ('owner_id', '=', False),
            ('product_id', '=', product.id),
            ('location_in_id', 'child_of', location.id),
            ('active', '=', True)
        ]
        rule = self.search(domain, order='priority desc', limit=1)
        if rule:
            return rule.location_out_id

        # Finally try by category
        domain = [
            ('owner_id', '=', False),
            ('product_category_id', '=', product.categ_id.id),
            ('location_in_id', 'child_of', location.id),
            ('active', '=', True)
        ]
        rule = self.search(domain, order='priority desc', limit=1)
        if rule:
            return rule.location_out_id

        return False