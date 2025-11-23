from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_crossdock = fields.Boolean('Is Cross-Dock')
    crossdock_operation_id = fields.Many2one('wms.crossdock.operation', 'Crossdock Operation')
    crossdock_partner_id = fields.Many2one('res.partner', 'Cross-Dock Partner')
    crossdock_date = fields.Datetime('Cross-Dock Date')
    crossdock_status = fields.Selection([
        ('pending', 'Pending'),
        ('matched', 'Matched'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], 'Crossdock Status', default='pending')
    crossdock_match_id = fields.Many2one('wms.crossdock.match', 'Crossdock Match')
    owner_id = fields.Many2one('wms.owner', 'Owner', domain=[('is_warehouse_owner', '=', True)])


class StockMove(models.Model):
    _inherit = 'stock.move'

    is_crossdock_move = fields.Boolean('Is Cross-Dock Move')
    crossdock_operation_id = fields.Many2one('wms.crossdock.operation', 'Crossdock Operation')
    crossdock_picking_id = fields.Many2one('stock.picking', 'Cross-Dock Picking')


class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_crossdock_location = fields.Boolean('Is Cross-Dock Location')
    crossdock_type = fields.Selection([
        ('input', 'Input Zone'),
        ('output', 'Output Zone'),
        ('transit', 'Transit Zone'),
        ('sorting', 'Sorting Area'),
        ('holding', 'Holding Area')
    ], 'Cross-Dock Zone Type')
    max_capacity = fields.Float('Max Capacity (CBM)')