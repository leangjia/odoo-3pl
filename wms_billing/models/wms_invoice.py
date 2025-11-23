from odoo import models, fields, api


class WmsInvoice(models.Model):
    _name = 'wms.invoice'
    _description = 'WMS Invoice'
    _inherit = 'account.move'

    billing_records_ids = fields.Many2many(
        'wms.billing.record',
        'wms_invoice_billing_record_rel',
        'invoice_id',
        'billing_record_id',
        string='Billing Records'
    )
    owner_id = fields.Many2one('wms.owner', 'Owner', compute='_compute_owner', store=True)
    billing_period_start = fields.Date('Billing Period Start')
    billing_period_end = fields.Date('Billing Period End')

    @api.depends('partner_id')
    def _compute_owner(self):
        for invoice in self:
            # Try to find the owner based on the partner
            owner = self.env['wms.owner'].search([('partner_id', '=', invoice.partner_id.id)], limit=1)
            invoice.owner_id = owner

    def action_post(self):
        """Override to update billing records state when invoice is posted"""
        result = super().action_post()

        # Update related billing records
        for invoice in self:
            if invoice.billing_records_ids:
                invoice.billing_records_ids.write({'state': 'invoiced'})

        return result

    def mark_as_paid(self):
        """Override to update billing records when invoice is marked as paid"""
        result = super().mark_as_paid()

        # Update related billing records
        for invoice in self:
            if invoice.billing_records_ids:
                invoice.billing_records_ids.write({'state': 'paid'})

        return result