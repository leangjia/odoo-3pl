from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    batch_receive_picking_ids = fields.One2many('wms.batch.receive.picking', 'picking_id', 'Batch Receive Pickings')
    batch_receive_count = fields.Integer('Batch Receive Count', compute='_compute_batch_receive_count')

    @api.depends('batch_receive_picking_ids')
    def _compute_batch_receive_count(self):
        for picking in self:
            picking.batch_receive_count = len(picking.batch_receive_picking_ids)

    def action_add_to_batch_receive(self):
        """Add picking to an existing batch receive session"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wms.batch.receive.add.picking.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'default_picking_ids': [(6, 0, self.ids)]}
        }

    def action_start_batch_receive(self):
        """Start a batch receive session with this picking"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wms.batch.receive.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'default_picking_ids': [(6, 0, self.ids)], 'default_owner_id': self.owner_id.id if hasattr(self, 'owner_id') and self.owner_id else False}
        }

    def action_view_batch_receives(self):
        """View batch receives for this picking"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Batch Receives',
            'res_model': 'wms.batch.receive.picking',
            'view_mode': 'tree,form',
            'domain': [('picking_id', '=', self.id)],
            'context': {'default_picking_id': self.id}
        }