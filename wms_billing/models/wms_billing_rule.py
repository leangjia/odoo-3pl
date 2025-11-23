from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WmsBillingRule(models.Model):
    _name = 'wms.billing.rule'
    _description = 'WMS Billing Rule'

    name = fields.Char('Rule Name', required=True)
    owner_id = fields.Many2one('wms.owner', 'Owner', required=True)
    operation_type = fields.Selection([
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
        ('storage', 'Storage'),
        ('value_added', 'Value Added Service'),
        ('special_handling', 'Special Handling'),
        ('pick_pack', 'Pick & Pack'),
        ('palletizing', 'Palletizing'),
        ('repackaging', 'Repackaging'),
        ('overweight', 'Overweight Handling'),
        ('oversize', 'Oversize Handling'),
    ], 'Operation Type', required=True)
    service_type = fields.Char('Service Type')
    unit_price = fields.Float('Unit Price', required=True)
    price_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('per_unit', 'Per Unit'),
        ('per_kg', 'Per KG'),
        ('per_cbm', 'Per CBM'),
        ('per_pallet', 'Per Pallet'),
        ('per_hour', 'Per Hour'),
        ('per_order', 'Per Order'),
        ('percentage', 'Percentage'),
    ], 'Price Type', required=True, default='per_unit')
    min_charge = fields.Float('Minimum Charge')
    calculation_basis = fields.Selection([
        ('quantity', 'Quantity'),
        ('weight', 'Weight'),
        ('volume', 'Volume'),
        ('time', 'Time'),
        ('pallet', 'Pallet'),
        ('order', 'Order'),
        ('area', 'Area'),
        ('distance', 'Distance'),
    ], 'Calculation Basis')
    max_charge = fields.Float('Maximum Charge')
    apply_seasonal_factor = fields.Boolean('Apply Seasonal Factor')
    seasonal_factor = fields.Float('Seasonal Factor', default=1.0)
    active = fields.Boolean('Active', default=True)

    @api.constrains('unit_price', 'min_charge', 'max_charge')
    def _check_positive_prices(self):
        for rule in self:
            if rule.unit_price < 0:
                raise ValidationError("Unit price must be positive.")
            if rule.min_charge < 0:
                raise ValidationError("Minimum charge must be positive.")
            if rule.max_charge and rule.max_charge < 0:
                raise ValidationError("Maximum charge must be positive.")

    @api.constrains('seasonal_factor')
    def _check_seasonal_factor(self):
        for rule in self:
            if rule.apply_seasonal_factor and rule.seasonal_factor <= 0:
                raise ValidationError("Seasonal factor must be positive.")