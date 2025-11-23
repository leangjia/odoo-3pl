from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import datetime


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    age_days = fields.Integer('Age (Days)', compute='_compute_inventory_age', store=True, compute_sudo=True)
    aging_period = fields.Selection([
        ('current', 'Current (0-30 days)'),
        ('30_60', '30-60 Days'),
        ('60_90', '60-90 Days'),
        ('90_180', '90-180 Days'),
        ('180_365', '180-365 Days'),
        ('over_365', 'Over 365 Days'),
    ], 'Aging Period', compute='_compute_aging_period', store=True, compute_sudo=True)
    is_aged_inventory = fields.Boolean('Is Aged', compute='_compute_is_aged_inventory', store=True, compute_sudo=True)

    @api.depends('create_date', 'in_date')
    def _compute_inventory_age(self):
        """Compute the age of inventory in days"""
        today = fields.Date.today()
        for quant in self:
            # Use in_date if available, otherwise use create_date
            inventory_date = quant.in_date.date() if quant.in_date else quant.create_date.date()

            if inventory_date <= today:
                age = today - inventory_date
                quant.age_days = age.days
            else:
                # If the date is in the future for some reason, set to 0
                quant.age_days = 0

    @api.depends('age_days')
    def _compute_aging_period(self):
        """Compute the aging period based on age in days"""
        for quant in self:
            if quant.age_days <= 30:
                quant.aging_period = 'current'
            elif quant.age_days <= 60:
                quant.aging_period = '30_60'
            elif quant.age_days <= 90:
                quant.aging_period = '60_90'
            elif quant.age_days <= 180:
                quant.aging_period = '90_180'
            elif quant.age_days <= 365:
                quant.aging_period = '180_365'
            else:
                quant.aging_period = 'over_365'

    @api.depends('age_days')
    def _compute_is_aged_inventory(self):
        """Determine if inventory is aged based on configuration"""
        for quant in self:
            # Get the age configuration for the owner or default
            if hasattr(quant, 'owner_id') and quant.owner_id:
                config = self.env['wms.inventory.age.config'].search([('owner_id', '=', quant.owner_id.id)], limit=1)
            else:
                config = self.env['wms.inventory.age.config'].search([], limit=1)

            if config:
                quant.is_aged_inventory = quant.age_days > config.warning_age_days
            else:
                # Default: inventory older than 180 days is considered aged
                quant.is_aged_inventory = quant.age_days > 180

    def action_view_inventory_age_report(self):
        """Action to view inventory age for this quant"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wms.inventory.age.report',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_date_as_of': fields.Date.today(),
                'default_location_id': self.location_id.id,
                'default_product_category_id': self.product_id.categ_id.id,
            }
        }