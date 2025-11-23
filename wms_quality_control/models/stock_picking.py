from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    quality_control_ids = fields.One2many('wms.quality.control', 'picking_id', 'Quality Controls')
    quality_control_count = fields.Integer('QC Count', compute='_compute_quality_control_count')

    @api.depends('quality_control_ids')
    def _compute_quality_control_count(self):
        for picking in self:
            picking.quality_control_count = len(picking.quality_control_ids)

    def action_create_quality_control(self):
        """Create a quality control session for this picking"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wms.quality.control.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'default_picking_id': self.id, 'default_owner_id': self.owner_id.id if hasattr(self, 'owner_id') and self.owner_id else False}
        }

    def action_view_quality_controls(self):
        """View quality controls for this picking"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quality Controls',
            'res_model': 'wms.quality.control',
            'view_mode': 'tree,form',
            'domain': [('picking_id', '=', self.id)],
            'context': {'default_picking_id': self.id}
        }