# 3PL WMS - Third-Party Logistics Warehouse Management System
# 精炼版功能规格说明书

## 1. 项目概述

### 1.1 项目名称
3PL WMS - 基于 Odoo 18 的第三方物流仓储管理系统

### 1.2 项目定位
本项目不是从零开发仓储管理系统，而是在充分利用 Odoo 18 原生功能的基础上，针对 3PL（第三方物流）业务场景进行专业化的定制化增强和最佳实践配置。Odoo 已具备多货主、智能上架/下架、波次拣货、越库作业等核心功能，本项目专注于：

1. 为原生功能提供 3PL 专用配置界面
2. 增强 3PL 特有业务流程
3. 提供 3PL 专用报表和分析工具
4. 简化 3PL 管理员的配置操作
5. 加强多货主数据隔离和安全性

### 1.3 价值主张
- **充分利用原生功能**：基于 Odoo 原生强大的仓储功能，避免重复造轮子
- **专业定制**：专门针对 3PL 场景优化用户体验和管理效率
- **降低成本**：基于成熟平台，降低开发和维护成本
- **快速实施**：利用 Odoo 生态，缩短上线时间

---

## 2. 原生功能与增强对比

### 2.1 多货主管理
**Odoo 原生功能**：
- `stock.quant.owner_id` - 库存按货主隔离
- `stock.move_line.owner_id` - 库存移动追踪
- 权限控制基础框架

**3PL 增强功能**：
- 货主维度的专用报表
- 货主专属的计费规则管理
- 货主数据安全隔离增强
- 货主库存可视化看板

### 2.2 智能上架
**Odoo 原生功能**：
- `stock.putaway.rule` - 基础上架规则
- 按产品、类别配置上架策略

**3PL 增强功能**：
- 按货主维度的上架规则
- ABC 分类上架策略
- 库位容量智能检查
- 动态上架优化算法

### 2.3 波次拣货
**Odoo 原生功能**：
- `stock.picking.batch` - 原生波次管理（企业版）
- 批量处理拣货单

**3PL 增强功能**：
- 智能波次自动生成
- 波次优化算法（路径、负载）
- 多人协同拣货界面
- 波次进度监控看板

### 2.4 越库作业
**Odoo 原生功能**：
- Cross-dock routes - 原生越库路线配置
- 链式移动支持

**3PL 增强功能**：
- 智能越库订单匹配
- 部分越库支持
- 越库监控看板
- 越库效率分析

---

## 3. 核心模块规格

### 3.1 货主管理模块（wms_owner）

#### 3.1.1 增强功能
| 功能点 | 原生功能 | 3PL增强 | 技术实现 | 优先级 |
|--------|----------|---------|----------|--------|
| 货主主数据 | res.partner 基础字段 | 3PL 专用字段扩展 | 继承 res.partner，添加计费相关字段 | P0 |
| 库存隔离 | stock.quant.owner_id | 强化权限隔离规则 | 基于 ir.rule 的数据级权限控制 | P0 |
| 货主报表 | 基础查询 | 货主维度专用报表 | 定制化报表视图和模型 | P1 |
| 货主看板 | 标准看板视图 | 3PL 货主专用看板 | 定制化看板视图 | P1 |

#### 3.1.2 数据模型增强
```python
class ResPartner(models.Model):
    _inherit = 'res.partner'

    # 3PL 特有字段
    is_warehouse_owner = fields.Boolean('Is Warehouse Owner', default=False)
    owner_code = fields.Char('Owner Code', size=20, copy=False)
    billing_rules = fields.One2many('wms.billing.rule', 'owner_id', 'Billing Rules')
    storage_fee_rate = fields.Float('Storage Fee Rate (per day per unit)')
    inbound_fee = fields.Float('Inbound Handling Fee')
    outbound_fee = fields.Float('Outbound Handling Fee')
    contract_start_date = fields.Date('Contract Start Date')
    contract_end_date = fields.Date('Contract End Date')
```

### 3.2 智能上架模块（wms_putaway）

#### 3.2.1 增强功能
| 功能点 | 原生功能 | 3PL增强 | 技术实现 | 优先级 |
|--------|----------|---------|----------|--------|
| 基础上架规则 | stock.putaway.rule | 按货主扩展规则 | 继承 putaway.rule 添加 owner_id | P0 |
| ABC 分类 | 无 | ABC 分类上架策略 | 新增 abc_category 字段 | P1 |
| 容量检查 | 无 | 库位容量智能检查 | 扩展 _get_putaway_strategy() | P1 |
| 动态优化 | 无 | 动态上架策略调整 | 定时任务优化规则 | P2 |

#### 3.2.2 数据模型增强
```python
class StockPutawayRule(models.Model):
    _inherit = 'stock.putaway.rule'

    # 3PL 扩展字段
    owner_id = fields.Many2one('res.partner', 'Owner',
                               domain=[('is_warehouse_owner', '=', True)])
    abc_category = fields.Selection([
        ('A', 'A - High Turnover'),
        ('B', 'B - Medium Turnover'),
        ('C', 'C - Low Turnover')
    ], 'ABC Category')
    max_capacity = fields.Float('Max Capacity')
    priority = fields.Integer('Priority', default=10)
```

### 3.3 波次管理模块（wms_wave）

#### 3.3.1 增强功能
| 功能点 | 原生功能 | 3PL增强 | 技术实现 | 优先级 |
|--------|----------|---------|----------|--------|
| 基础波次 | stock.picking.batch | 自动波次生成 | ir.cron 定时任务 | P0 |
| 波次分配 | 手动分配 | 智能分配算法 | 优化分配逻辑 | P1 |
| 波次优化 | 无 | 拣货路径优化 | 路径优化算法 | P1 |
| 协同拣货 | 基础支持 | 多人协同界面 | 扩展 batch 模型 | P1 |

#### 3.3.2 数据模型增强
```python
class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    # 3PL 扩展字段
    wave_type = fields.Selection([
        ('single', 'Single Order'),
        ('multi', 'Multi Order'),
        ('zone', 'Zone Picking'),
        ('wave', 'Auto Wave')
    ], 'Wave Type', default='multi')
    estimated_time = fields.Float('Estimated Time (hours)')
    actual_time = fields.Float('Actual Time (hours)')
    optimizer_used = fields.Boolean('Optimized', default=False)
```

### 3.4 计费管理模块（wms_billing）

#### 3.4.1 增强功能
| 功能点 | 原生功能 | 3PL增强 | 技术实现 | 优先级 |
|--------|----------|---------|----------|--------|
| 基础库存移动 | stock.move | 计费记录生成 | 监听 move done 事件 | P0 |
| 基础计费 | 无 | 计费规则配置 | wms.billing.rule 模型 | P0 |
| 账单生成 | 无 | 自动账单生成 | 定时任务生成 account.move | P0 |
| 对账功能 | 无 | 客户对账界面 | 专门的对账视图 | P1 |

#### 3.4.2 新增数据模型
```python
class WmsBillingRule(models.Model):
    _name = 'wms.billing.rule'
    _description = 'WMS Billing Rule'

    name = fields.Char('Rule Name', required=True)
    owner_id = fields.Many2one('res.partner', 'Owner', required=True)
    operation_type = fields.Selection([
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
        ('storage', 'Storage'),
        ('value_added', 'Value Added Service')
    ], 'Operation Type', required=True)
    billing_method = fields.Selection([
        ('per_unit', 'Per Unit'),
        ('per_weight', 'Per Weight (kg)'),
        ('per_volume', 'Per Volume (m³)'),
        ('per_order', 'Per Order')
    ], 'Billing Method', required=True)
    unit_price = fields.Float('Unit Price', required=True)
    min_charge = fields.Float('Minimum Charge')

class WmsBillingRecord(models.Model):
    _name = 'wms.billing.record'
    _description = 'WMS Billing Record'

    name = fields.Char('Reference', required=True, default='New')
    owner_id = fields.Many2one('res.partner', 'Owner', required=True)
    move_id = fields.Many2one('stock.move', 'Stock Move')
    operation_type = fields.Selection([...], 'Operation Type', required=True)
    quantity = fields.Float('Quantity')
    unit_price = fields.Float('Unit Price')
    amount = fields.Float('Amount', compute='_compute_amount', store=True)
    invoice_id = fields.Many2one('account.move', 'Invoice')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('invoiced', 'Invoiced')
    ], 'State', default='draft')
```

### 3.5 基础设置增强模块（wms_setup_enhanced）

#### 3.5.1 工作区管理模块（wms_workzone）
**功能描述**: 实现物理作业区域管理（收货区、拣选区、包装区、发货区）

**数据模型**:
```python
class WmsWorkzone(models.Model):
    _name = 'wms.workzone'
    _description = 'Work Zone'

    name = fields.Char('Zone Name', required=True)
    code = fields.Char('Zone Code', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True)
    zone_type = fields.Selection([
        ('receiving', 'Receiving Zone'),
        ('picking', 'Picking Zone'),
        ('packing', 'Packing Zone'),
        ('shipping', 'Shipping Zone'),
        ('storage', 'Storage Zone')
    ], 'Zone Type', required=True)
    location_ids = fields.Many2many('stock.location', 'workzone_location_rel',
                                    'zone_id', 'location_id', 'Locations')
    user_ids = fields.Many2many('res.users', 'workzone_user_rel',
                                'zone_id', 'user_id', 'Assigned Users')
```

#### 3.5.2 货类管理模块（wms_cargo_type）
**功能描述**: 实现货物分类管理（普货、危险品、冷藏品等）

**数据模型**:
```python
class WmsCargoType(models.Model):
    _name = 'wms.cargo.type'
    _description = 'Cargo Type'

    name = fields.Char('Type Name', required=True)
    code = fields.Char('Type Code', required=True)
    special_handling = fields.Text('Special Handling Requirements')
    storage_conditions = fields.Text('Storage Conditions')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cargo_type_id = fields.Many2one('wms.cargo.type', 'Cargo Type')
```

#### 3.5.3 库区管理模块（wms_storage_area）
**功能描述**: 实现逻辑分区管理

**数据模型**:
```python
class WmsStorageArea(models.Model):
    _name = 'wms.storage.area'
    _description = 'Storage Area'

    name = fields.Char('Area Name', required=True)
    code = fields.Char('Area Code', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True)
    area_type = fields.Selection([
        ('high_rack', 'High Rack'),
        ('floor_stack', 'Floor Stack'),
        ('cold_storage', 'Cold Storage'),
        ('hazmat', 'Hazardous Materials')
    ], 'Area Type')
    location_ids = fields.Many2many('stock.location', 'area_location_rel',
                                    'area_id', 'location_id', 'Locations')
```

### 3.6 RF 移动端增强模块（wms_rf_enhanced）

#### 3.6.1 按箱收货增强（wms_rf_container）
**功能描述**: 实现完整的按箱收货流程

**核心功能**:
```python
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    container_ids = fields.One2many('wms.container', 'picking_id', 'Containers')

    def action_receive_by_container(self, container_barcode):
        """按箱收货"""
        container = self.env['wms.container'].search([
            ('barcode', '=', container_barcode)
        ], limit=1)

        if not container:
            container = self.env['wms.container'].create({
                'barcode': container_barcode,
                'picking_id': self.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wms.container',
            'res_id': container.id,
            'view_mode': 'form',
            'target': 'new',
        }

class WmsContainer(models.Model):
    _name = 'wms.container'
    _description = 'Container'

    barcode = fields.Char('Container Barcode', required=True)
    picking_id = fields.Many2one('stock.picking', 'Picking')
    line_ids = fields.One2many('wms.container.line', 'container_id', 'Lines')

class WmsContainerLine(models.Model):
    _name = 'wms.container.line'
    _description = 'Container Line'

    container_id = fields.Many2one('wms.container', 'Container', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    quantity = fields.Float('Quantity', required=True)
```

#### 3.6.2 盲收入库（wms_rf_blind_receive）
**功能描述**: 支持无单据收货

**核心功能**:
```python
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_blind_receive = fields.Boolean('Blind Receive')

    @api.model
    def create_blind_receive(self, owner_id, warehouse_id):
        """创建盲收单"""
        picking_type = self.env['stock.picking.type'].search([
            ('warehouse_id', '=', warehouse_id),
            ('code', '=', 'incoming')
        ], limit=1)

        return self.create({
            'picking_type_id': picking_type.id,
            'owner_id': owner_id,
            'is_blind_receive': True,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
        })
```

#### 3.6.3 库存冻结/释放（wms_inventory_freeze）
**功能描述**: 实现库存冻结功能

**数据模型**:
```python
class StockQuant(models.Model):
    _inherit = 'stock.quant'

    is_frozen = fields.Boolean('Is Frozen', default=False)
    freeze_reason = fields.Text('Freeze Reason')
    freeze_date = fields.Datetime('Freeze Date')
    freeze_user_id = fields.Many2one('res.users', 'Frozen By')

    def action_freeze(self, reason):
        """冻结库存"""
        self.write({
            'is_frozen': True,
            'freeze_reason': reason,
            'freeze_date': fields.Datetime.now(),
            'freeze_user_id': self.env.user.id,
        })

    def action_unfreeze(self):
        """释放库存"""
        self.write({
            'is_frozen': False,
            'freeze_reason': False,
            'freeze_date': False,
            'freeze_user_id': False,
        })

    def _gather(self, product_id, location_id, lot_id=None, package_id=None,
                owner_id=None, strict=False):
        """重写库存预留逻辑，排除冻结库存"""
        quants = super()._gather(product_id, location_id, lot_id, package_id,
                                 owner_id, strict)
        return quants.filtered(lambda q: not q.is_frozen)
```

### 3.7 业务流程增强模块（wms_process_enhanced）

#### 3.7.1 复核装箱流程（wms_packing_check）
**功能描述**: 增加独立的复核确认步骤

**数据模型**:
```python
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    packing_check_state = fields.Selection([
        ('pending', 'Pending Check'),
        ('checking', 'Checking'),
        ('checked', 'Checked'),
        ('exception', 'Exception')
    ], 'Packing Check State', default='pending')
    checker_id = fields.Many2one('res.users', 'Checker')
    check_date = fields.Datetime('Check Date')

    def action_start_packing_check(self):
        """开始复核"""
        self.write({
            'packing_check_state': 'checking',
            'checker_id': self.env.user.id,
        })

    def action_confirm_packing_check(self):
        """确认复核"""
        # 验证实际数量与计划数量
        for line in self.move_line_ids:
            if line.quantity != line.quantity_product_uom:
                raise UserError('数量不符，请检查')

        self.write({
            'packing_check_state': 'checked',
            'check_date': fields.Datetime.now(),
        })
```

#### 3.7.2 出库交接管理（wms_handover）
**功能描述**: 实现出库交接确认流程

**数据模型**:
```python
class WmsHandover(models.Model):
    _name = 'wms.handover'
    _description = 'Handover Record'

    name = fields.Char('Reference', required=True, default='New')
    date = fields.Datetime('Handover Date', required=True, default=fields.Datetime.now)
    picking_ids = fields.Many2many('stock.picking', 'handover_picking_rel',
                                   'handover_id', 'picking_id', 'Pickings')
    carrier_id = fields.Many2one('res.partner', 'Carrier', required=True)
    driver_name = fields.Char('Driver Name')
    vehicle_number = fields.Char('Vehicle Number')
    signature = fields.Binary('Signature')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed')
    ], 'State', default='draft')
```

#### 3.7.3 越库作业（wms_crossdock）
**功能描述**: 实现越库作业功能，支持收货后直接发货，无需上架

**数据模型**:
```python
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_crossdock = fields.Boolean('Is Cross-Dock')
    crossdock_partner_id = fields.Many2one('res.partner', 'Cross-Dock Partner')
    crossdock_date = fields.Datetime('Cross-Dock Date')

class StockMove(models.Model):
    _inherit = 'stock.move'

    is_crossdock_move = fields.Boolean('Is Cross-Dock Move')
    crossdock_picking_id = fields.Many2one('stock.picking', 'Cross-Dock Picking')

class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_crossdock_location = fields.Boolean('Is Cross-Dock Location')
    crossdock_type = fields.Selection([
        ('input', 'Input Zone'),
        ('output', 'Output Zone'),
        ('transit', 'Transit Zone')
    ], 'Cross-Dock Zone Type')
```

#### 3.7.4 自动波次生成规则（wms_wave_auto）
**功能描述**: 实现自动波次生成功能

**核心功能**:
```python
class WmsWaveRule(models.Model):
    _name = 'wms.wave.rule'
    _description = 'Wave Generation Rule'

    name = fields.Char('Rule Name', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True)
    trigger_type = fields.Selection([
        ('time', 'Time Based'),
        ('order_count', 'Order Count'),
        ('order_volume', 'Order Volume')
    ], 'Trigger Type', required=True)
    trigger_value = fields.Float('Trigger Value')
    max_orders_per_wave = fields.Integer('Max Orders per Wave', default=50)
    active = fields.Boolean('Active', default=True)

    @api.model
    def _cron_generate_waves(self):
        """定时任务：自动生成波次"""
        rules = self.search([('active', '=', True)])
        for rule in rules:
            rule._generate_wave()

    def _generate_wave(self):
        """生成波次"""
        pickings = self.env['stock.picking'].search([
            ('picking_type_id.warehouse_id', '=', self.warehouse_id.id),
            ('state', '=', 'assigned'),
            ('batch_id', '=', False),
        ], limit=self.max_orders_per_wave)

        if pickings:
            batch = self.env['stock.picking.batch'].create({
                'name': f'WAVE-{fields.Date.today()}',
                'picking_ids': [(6, 0, pickings.ids)],
            })
            return batch
```

#### 3.7.5 装箱规则（wms_packing_rule）
**功能描述**: 实现自动装箱建议

**数据模型**:
```python
class WmsPackingRule(models.Model):
    _name = 'wms.packing.rule'
    _description = 'Packing Rule'

    name = fields.Char('Rule Name', required=True)
    box_type_id = fields.Many2one('product.packaging', 'Box Type', required=True)
    max_weight = fields.Float('Max Weight (kg)')
    max_volume = fields.Float('Max Volume (m³)')
    priority = fields.Integer('Priority', default=10)

    @api.model
    def suggest_packing(self, picking_id):
        """推荐装箱方案"""
        picking = self.env['stock.picking'].browse(picking_id)
        total_weight = sum(line.product_id.weight * line.quantity
                          for line in picking.move_line_ids)
        total_volume = sum(line.product_id.volume * line.quantity
                          for line in picking.move_line_ids)

        rules = self.search([
            ('max_weight', '>=', total_weight),
            ('max_volume', '>=', total_volume)
        ], order='priority')

        return rules[0] if rules else False
```

### 3.8 统计分析报表模块（wms_reporting）

#### 3.8.1 库龄分析（wms_inventory_age）
**功能描述**: 分析库存积压情况

**数据模型**:
```python
class WmsInventoryAgeReport(models.Model):
    _name = 'wms.inventory.age.report'
    _description = 'Inventory Age Report'
    _auto = False

    owner_id = fields.Many2one('res.partner', 'Owner', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    location_id = fields.Many2one('stock.location', 'Location', readonly=True)
    quantity = fields.Float('Quantity', readonly=True)
    age_days = fields.Integer('Age (Days)', readonly=True)
    age_range = fields.Selection([
        ('0-30', '0-30 Days'),
        ('31-60', '31-60 Days'),
        ('61-90', '61-90 Days'),
        ('91-180', '91-180 Days'),
        ('180+', '180+ Days')
    ], 'Age Range', readonly=True)

    def init(self):
        """创建 SQL 视图"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    row_number() OVER () as id,
                    sq.owner_id,
                    sq.product_id,
                    sq.location_id,
                    sq.quantity,
                    EXTRACT(DAY FROM (NOW() - sq.in_date))::integer as age_days,
                    CASE
                        WHEN EXTRACT(DAY FROM (NOW() - sq.in_date)) <= 30 THEN '0-30'
                        WHEN EXTRACT(DAY FROM (NOW() - sq.in_date)) <= 60 THEN '31-60'
                        WHEN EXTRACT(DAY FROM (NOW() - sq.in_date)) <= 90 THEN '61-90'
                        WHEN EXTRACT(DAY FROM (NOW() - sq.in_date)) <= 180 THEN '91-180'
                        ELSE '180+'
                    END as age_range
                FROM stock_quant sq
                WHERE sq.quantity > 0
            )
        """)
```

#### 3.8.2 ABC 分析（wms_abc_analysis）
**功能描述**: 基于周转率的 ABC 分类分析

**数据模型**:
```python
class WmsAbcAnalysis(models.Model):
    _name = 'wms.abc.analysis'
    _description = 'ABC Analysis'

    name = fields.Char('Analysis Name', required=True)
    date_from = fields.Date('From Date', required=True)
    date_to = fields.Date('To Date', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse')
    owner_id = fields.Many2one('res.partner', 'Owner')
    line_ids = fields.One2many('wms.abc.analysis.line', 'analysis_id', 'Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], 'State', default='draft')

    def action_compute(self):
        """计算 ABC 分类"""
        self.line_ids.unlink()

        # 查询期间内的出库数据
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('state', '=', 'done'),
            ('location_dest_id.usage', '=', 'customer')
        ]
        if self.warehouse_id:
            domain.append(('warehouse_id', '=', self.warehouse_id.id))
        if self.owner_id:
            domain.append(('owner_id', '=', self.owner_id.id))

        moves = self.env['stock.move'].search(domain)

        # 按产品汇总出库量和金额
        product_data = {}
        for move in moves:
            if move.product_id.id not in product_data:
                product_data[move.product_id.id] = {
                    'product_id': move.product_id.id,
                    'quantity': 0,
                    'value': 0,
                }
            product_data[move.product_id.id]['quantity'] += move.product_uom_qty
            product_data[move.product_id.id]['value'] += move.product_uom_qty * move.product_id.standard_price

        # 按金额排序
        sorted_products = sorted(product_data.values(), key=lambda x: x['value'], reverse=True)
        total_value = sum(p['value'] for p in sorted_products)

        # 计算累计占比并分类
        cumulative_value = 0
        lines = []
        for product in sorted_products:
            cumulative_value += product['value']
            cumulative_percent = (cumulative_value / total_value * 100) if total_value else 0

            if cumulative_percent <= 80:
                category = 'A'
            elif cumulative_percent <= 95:
                category = 'B'
            else:
                category = 'C'

            lines.append((0, 0, {
                'product_id': product['product_id'],
                'quantity': product['quantity'],
                'value': product['value'],
                'category': category,
            }))

        self.write({
            'line_ids': lines,
            'state': 'done',
        })

class WmsAbcAnalysisLine(models.Model):
    _name = 'wms.abc.analysis.line'
    _description = 'ABC Analysis Line'

    analysis_id = fields.Many2one('wms.abc.analysis', 'Analysis', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    quantity = fields.Float('Quantity')
    value = fields.Float('Value')
    category = fields.Selection([
        ('A', 'A - High Value'),
        ('B', 'B - Medium Value'),
        ('C', 'C - Low Value')
    ], 'Category')
```

#### 3.8.3 EIQ 分析（wms_eiq_analysis）
**功能描述**: Entry（入库）、Item（品项）、Quantity（数量）分析

**数据模型**:
```python
class WmsEiqAnalysis(models.Model):
    _name = 'wms.eiq.analysis'
    _description = 'EIQ Analysis'

    name = fields.Char('Analysis Name', required=True)
    date_from = fields.Date('From Date', required=True)
    date_to = fields.Date('To Date', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse')

    # E 分析（订单数）
    total_orders = fields.Integer('Total Orders', compute='_compute_eiq')
    avg_items_per_order = fields.Float('Avg Items per Order', compute='_compute_eiq')
    avg_qty_per_order = fields.Float('Avg Qty per Order', compute='_compute_eiq')

    # I 分析（品项数）
    total_items = fields.Integer('Total Items', compute='_compute_eiq')
    avg_orders_per_item = fields.Float('Avg Orders per Item', compute='_compute_eiq')
    avg_qty_per_item = fields.Float('Avg Qty per Item', compute='_compute_eiq')

    # Q 分析（数量）
    total_quantity = fields.Float('Total Quantity', compute='_compute_eiq')
    avg_qty_per_order_line = fields.Float('Avg Qty per Order Line', compute='_compute_eiq')

    @api.depends('date_from', 'date_to', 'warehouse_id')
    def _compute_eiq(self):
        for record in self:
            domain = [
                ('date', '>=', record.date_from),
                ('date', '<=', record.date_to),
                ('state', '=', 'done'),
                ('picking_type_code', '=', 'outgoing')
            ]
            if record.warehouse_id:
                domain.append(('warehouse_id', '=', record.warehouse_id.id))

            pickings = self.env['stock.picking'].search(domain)
            moves = pickings.mapped('move_ids')

            record.total_orders = len(pickings)
            record.total_items = len(moves.mapped('product_id'))
            record.total_quantity = sum(moves.mapped('product_uom_qty'))

            if record.total_orders:
                record.avg_items_per_order = len(moves) / record.total_orders
                record.avg_qty_per_order = record.total_quantity / record.total_orders

            if record.total_items:
                record.avg_orders_per_item = record.total_orders / record.total_items
                record.avg_qty_per_item = record.total_quantity / record.total_items

            if len(moves):
                record.avg_qty_per_order_line = record.total_quantity / len(moves)
```

#### 3.8.4 库位使用报表（wms_location_usage）
**功能描述**: 库位占用率和使用情况分析

**数据模型**:
```python
class WmsLocationUsageReport(models.Model):
    _name = 'wms.location.usage.report'
    _description = 'Location Usage Report'
    _auto = False

    location_id = fields.Many2one('stock.location', 'Location', readonly=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', readonly=True)
    total_capacity = fields.Float('Total Capacity', readonly=True)
    used_capacity = fields.Float('Used Capacity', readonly=True)
    usage_rate = fields.Float('Usage Rate (%)', readonly=True)
    product_count = fields.Integer('Product Count', readonly=True)
    owner_count = fields.Integer('Owner Count', readonly=True)

    def init(self):
        """创建 SQL 视图"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    sl.id,
                    sl.id as location_id,
                    sw.id as warehouse_id,
                    COALESCE(sl.max_capacity, 0) as total_capacity,
                    COALESCE(SUM(sq.quantity), 0) as used_capacity,
                    CASE
                        WHEN sl.max_capacity > 0 THEN
                            (COALESCE(SUM(sq.quantity), 0) / sl.max_capacity * 100)
                        ELSE 0
                    END as usage_rate,
                    COUNT(DISTINCT sq.product_id) as product_count,
                    COUNT(DISTINCT sq.owner_id) as owner_count
                FROM stock_location sl
                LEFT JOIN stock_quant sq ON sq.location_id = sl.id
                LEFT JOIN stock_warehouse sw ON sl.warehouse_id = sw.id
                WHERE sl.usage = 'internal'
                GROUP BY sl.id, sw.id
            )
        """)
```

#### 3.8.5 绩效报表（wms_performance）
**功能描述**: 操作员作业效率追踪

**数据模型**:
```python
class WmsPerformanceReport(models.Model):
    _name = 'wms.performance.report'
    _description = 'Performance Report'

    name = fields.Char('Report Name', required=True)
    date_from = fields.Date('From Date', required=True)
    date_to = fields.Date('To Date', required=True)
    user_id = fields.Many2one('res.users', 'User')
    line_ids = fields.One2many('wms.performance.report.line', 'report_id', 'Lines')

    def action_compute(self):
        """计算绩效数据"""
        self.line_ids.unlink()

        domain = [
            ('date_done', '>=', self.date_from),
            ('date_done', '<=', self.date_to),
            ('state', '=', 'done')
        ]
        if self.user_id:
            domain.append(('user_id', '=', self.user_id.id))

        pickings = self.env['stock.picking'].search(domain)

        # 按用户汇总
        user_data = {}
        for picking in pickings:
            if not picking.user_id:
                continue

            user_id = picking.user_id.id
            if user_id not in user_data:
                user_data[user_id] = {
                    'user_id': user_id,
                    'picking_count': 0,
                    'total_lines': 0,
                    'total_quantity': 0,
                    'total_time': 0,
                }

            user_data[user_id]['picking_count'] += 1
            user_data[user_id]['total_lines'] += len(picking.move_line_ids)
            user_data[user_id]['total_quantity'] += sum(picking.move_line_ids.mapped('quantity'))

            if picking.date_done and picking.scheduled_date:
                time_diff = (picking.date_done - picking.scheduled_date).total_seconds() / 3600
                user_data[user_id]['total_time'] += time_diff

        lines = []
        for data in user_data.values():
            lines.append((0, 0, {
                'user_id': data['user_id'],
                'picking_count': data['picking_count'],
                'total_lines': data['total_lines'],
                'total_quantity': data['total_quantity'],
                'avg_time_per_picking': data['total_time'] / data['picking_count'] if data['picking_count'] else 0,
                'avg_lines_per_picking': data['total_lines'] / data['picking_count'] if data['picking_count'] else 0,
            }))

        self.line_ids = lines

class WmsPerformanceReportLine(models.Model):
    _name = 'wms.performance.report.line'
    _description = 'Performance Report Line'

    report_id = fields.Many2one('wms.performance.report', 'Report', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', 'User', required=True)
    picking_count = fields.Integer('Picking Count')
    total_lines = fields.Integer('Total Lines')
    total_quantity = fields.Float('Total Quantity')
    avg_time_per_picking = fields.Float('Avg Time per Picking (hours)')
    avg_lines_per_picking = fields.Float('Avg Lines per Picking')
    efficiency_score = fields.Float('Efficiency Score', compute='_compute_efficiency_score')

    @api.depends('picking_count', 'avg_time_per_picking')
    def _compute_efficiency_score(self):
        """计算效率评分（拣货单数/小时）"""
        for line in self:
            if line.avg_time_per_picking > 0:
                line.efficiency_score = 1 / line.avg_time_per_picking
            else:
                line.efficiency_score = 0
```

### 3.9 入库管理增强模块（wms_inbound_enhanced）

#### 3.9.1 汇总入库（wms_batch_receive）
**功能描述**: 支持批量收货汇总功能

**数据模型**:
```python
class WmsBatchReceive(models.Model):
    _name = 'wms.batch.receive'
    _description = 'Batch Receive'

    name = fields.Char('Batch Number', required=True, default='New')
    date = fields.Datetime('Receive Date', required=True, default=fields.Datetime.now)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True)
    owner_id = fields.Many2one('res.partner', 'Owner', domain=[('is_warehouse_owner', '=', True)])
    picking_ids = fields.Many2many('stock.picking', 'batch_receive_picking_rel',
                                   'batch_id', 'picking_id', 'Pickings')
    line_ids = fields.One2many('wms.batch.receive.line', 'batch_id', 'Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], 'State', default='draft')

    def action_start_receive(self):
        """开始批量收货"""
        self.write({'state': 'in_progress'})
        # 汇总所有拣货单的产品
        product_summary = {}
        for picking in self.picking_ids:
            for move in picking.move_ids:
                key = (move.product_id.id, move.lot_id.id)
                if key not in product_summary:
                    product_summary[key] = {
                        'product_id': move.product_id.id,
                        'lot_id': move.lot_id.id,
                        'planned_qty': 0,
                        'received_qty': 0,
                    }
                product_summary[key]['planned_qty'] += move.product_uom_qty

        # 创建汇总行
        lines = [(0, 0, data) for data in product_summary.values()]
        self.write({'line_ids': lines})

    def action_confirm_receive(self):
        """确认收货"""
        # 将实际收货数量分配回原始拣货单
        for line in self.line_ids:
            remaining_qty = line.received_qty
            for picking in self.picking_ids:
                if remaining_qty <= 0:
                    break
                for move in picking.move_ids.filtered(
                    lambda m: m.product_id.id == line.product_id.id
                ):
                    qty_to_assign = min(remaining_qty, move.product_uom_qty)
                    move.quantity = qty_to_assign
                    remaining_qty -= qty_to_assign

        self.write({'state': 'done'})

class WmsBatchReceiveLine(models.Model):
    _name = 'wms.batch.receive.line'
    _description = 'Batch Receive Line'

    batch_id = fields.Many2one('wms.batch.receive', 'Batch', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    lot_id = fields.Many2one('stock.lot', 'Lot/Serial Number')
    planned_qty = fields.Float('Planned Quantity')
    received_qty = fields.Float('Received Quantity')
    variance = fields.Float('Variance', compute='_compute_variance')

    @api.depends('planned_qty', 'received_qty')
    def _compute_variance(self):
        for line in self:
            line.variance = line.received_qty - line.planned_qty
```

### 3.10 增值服务模块（wms_value_added）

#### 3.10.1 库内加工（wms_value_added）
**功能描述**: 实现简单的库内加工服务

**数据模型**:
```python
class WmsValueAddedService(models.Model):
    _name = 'wms.value.added.service'
    _description = 'Value Added Service'

    name = fields.Char('Service Name', required=True)
    code = fields.Char('Service Code', required=True)
    service_type = fields.Selection([
        ('labeling', 'Labeling'),
        ('repackaging', 'Repackaging'),
        ('assembly', 'Assembly'),
        ('quality_check', 'Quality Check'),
        ('customization', 'Customization')
    ], 'Service Type', required=True)
    unit_price = fields.Float('Unit Price')
    estimated_time = fields.Float('Estimated Time (minutes)')

class WmsValueAddedOrder(models.Model):
    _name = 'wms.value.added.order'
    _description = 'Value Added Service Order'

    name = fields.Char('Order Number', required=True, default='New')
    date = fields.Datetime('Order Date', required=True, default=fields.Datetime.now)
    owner_id = fields.Many2one('res.partner', 'Owner', required=True,
                               domain=[('is_warehouse_owner', '=', True)])
    service_id = fields.Many2one('wms.value.added.service', 'Service', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    location_id = fields.Many2one('stock.location', 'Location', required=True)
    assigned_user_id = fields.Many2one('res.users', 'Assigned To')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], 'State', default='draft')
    start_time = fields.Datetime('Start Time')
    end_time = fields.Datetime('End Time')
    actual_time = fields.Float('Actual Time (minutes)', compute='_compute_actual_time')

    @api.depends('start_time', 'end_time')
    def _compute_actual_time(self):
        for order in self:
            if order.start_time and order.end_time:
                delta = order.end_time - order.start_time
                order.actual_time = delta.total_seconds() / 60
            else:
                order.actual_time = 0
```

#### 3.10.2 快递对接（wms_courier）
**功能描述**: 实现快递系统集成

**数据模型**:
```python
class WmsCourierConfig(models.Model):
    _name = 'wms.courier.config'
    _description = 'Courier Configuration'

    name = fields.Char('Courier Name', required=True)
    code = fields.Char('Courier Code', required=True)
    api_url = fields.Char('API URL')
    api_key = fields.Char('API Key')
    api_secret = fields.Char('API Secret')
    active = fields.Boolean('Active', default=True)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    courier_id = fields.Many2one('wms.courier.config', 'Courier')
    tracking_number = fields.Char('Tracking Number')
    waybill_number = fields.Char('Waybill Number')
    shipping_label = fields.Binary('Shipping Label')

    def action_print_shipping_label(self):
        """打印快递面单"""
        self.ensure_one()
        if not self.courier_id:
            raise UserError('请先选择快递公司')

        # 调用快递 API 获取面单
        courier_api = self.courier_id._get_api_client()
        label_data = courier_api.create_waybill({
            'sender': self.picking_type_id.warehouse_id.partner_id,
            'receiver': self.partner_id,
            'items': self.move_ids,
        })

        self.write({
            'tracking_number': label_data['tracking_number'],
            'waybill_number': label_data['waybill_number'],
            'shipping_label': label_data['label_pdf'],
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/stock.picking/{self.id}/shipping_label',
            'target': 'new',
        }
```

#### 3.10.3 WCS 对接（wms_wcs）
**功能描述**: 实现仓库控制系统（WCS）接口

**数据模型**:
```python
class WmsWcsInterface(models.Model):
    _name = 'wms.wcs.interface'
    _description = 'WCS Interface'

    name = fields.Char('Interface Name', required=True)
    wcs_url = fields.Char('WCS URL', required=True)
    wcs_port = fields.Integer('WCS Port', default=8080)
    auth_token = fields.Char('Auth Token')
    active = fields.Boolean('Active', default=True)

    def send_task(self, task_type, task_data):
        """发送任务到 WCS"""
        import requests

        url = f"{self.wcs_url}:{self.wcs_port}/api/task"
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'task_type': task_type,
            'task_data': task_data,
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()

class StockMove(models.Model):
    _inherit = 'stock.move'

    wcs_task_id = fields.Char('WCS Task ID')
    wcs_status = fields.Selection([
        ('pending', 'Pending'),
        ('sent', 'Sent to WCS'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], 'WCS Status')

    def _action_assign(self):
        """重写分配方法，发送任务到 WCS"""
        res = super()._action_assign()

        # 如果启用了 WCS，发送任务
        wcs_interface = self.env['wms.wcs.interface'].search([('active', '=', True)], limit=1)
        if wcs_interface and self.location_id.wcs_enabled:
            task_data = {
                'move_id': self.id,
                'product': self.product_id.name,
                'quantity': self.product_uom_qty,
                'from_location': self.location_id.name,
                'to_location': self.location_dest_id.name,
            }
            result = wcs_interface.send_task('move', task_data)
            self.write({
                'wcs_task_id': result.get('task_id'),
                'wcs_status': 'sent',
            })

        return res
```

#### 3.10.4 RFID 接口（wms_rfid）
**功能描述**: 实现 RFID 读写器集成

**数据模型**:
```python
class WmsRfidReader(models.Model):
    _name = 'wms.rfid.reader'
    _description = 'RFID Reader'

    name = fields.Char('Reader Name', required=True)
    reader_ip = fields.Char('Reader IP', required=True)
    reader_port = fields.Integer('Reader Port', default=5084)
    location_id = fields.Many2one('stock.location', 'Location')
    active = fields.Boolean('Active', default=True)

    def read_tags(self):
        """读取 RFID 标签"""
        # 实现 RFID 读取逻辑
        import socket

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.reader_ip, self.reader_port))
        sock.send(b'READ\n')
        data = sock.recv(1024)
        sock.close()

        # 解析标签数据
        tags = data.decode('utf-8').split(',')
        return tags

class ProductProduct(models.Model):
    _inherit = 'product.product'

    rfid_tag = fields.Char('RFID Tag')

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    rfid_tag = fields.Char(related='product_id.rfid_tag', string='RFID Tag', readonly=True)
```

---

## 4. 实施策略

### 4.1 实施原则
1. **最小化开发** - 最大程度利用 Odoo 原生功能
2. **渐进式增强** - 在原生功能基础上逐步添加 3PL 特性
3. **配置优于代码** - 优先使用 Odoo 配置功能而非硬编码
4. **用户体验优先** - 简化 3PL 管理员的操作流程

### 4.2 分阶段实施

#### 阶段 1：基础配置（2-3 周）
- 激活并配置 Odoo 原生多货主功能
- 配置基础的上架和下架策略
- 启用波次拣货功能（企业版）
- 创建基本的货主和仓库设置

#### 阶段 2：3PL 增强模块（4-6 周）
- wms_owner 模块开发（货主管理增强）
- wms_putaway 模块开发（智能上架增强）
- wms_billing 模块开发（计费管理）
- 基础报表开发

#### 阶段 3：自动化与优化（3-4 周）
- wms_wave 模块开发（波次自动化）
- 优化算法集成
- 高级报表开发
- RF 端增强

#### 阶段 4：集成与完善（2-3 周）
- 客户端集成接口
- 高级功能模块
- 用户培训材料
- 系统优化

---

## 5. 技术架构

### 5.1 原生功能依赖
- `stock` 模块 - 核心仓储功能
- `stock_picking_batch` - 波次管理（企业版）
- `stock_dropshipping` - 越库功能
- `base` - 权限和用户管理

### 5.2 增强技术栈
- Python 3.10+ - 业务逻辑
- JavaScript (OWL) - 前端组件
- PostgreSQL 14+ - 数据存储
- XML - 视图和配置

### 5.3 集成接口
- REST API / XML-RPC - 外部系统集成
- Odoo 原生接口 - 数据交互
- 企业版特性 - 高级功能

---

## 6. 配置 vs 开发

### 6.1 配置为主的功能
- 仓库和库位设置
- 基础上架规则配置
- 下架策略设置
- 用户权限配置
- 基础报表设置

### 6.2 开发为辅的功能
- 3PL 专用界面
- 计费逻辑自动化
- 智能算法集成
- 专业报表开发
- 外部系统集成

---

## 7. 项目优势

### 7.1 架构优势
1. **成熟稳定** - 基于经过验证的 Odoo 原生功能
2. **成本效益** - 避免重复开发核心功能
3. **可维护性** - 利用 Odoo 更新和社区支持
4. **扩展性** - 基于 Odoo 生态系统

### 7.2 业务优势
1. **快速上线** - 利用现有功能快速部署
2. **专业适配** - 专门针对 3PL 业务优化
3. **灵活配置** - 适应不同 3PL 业务模式
4. **持续升级** - 随 Odoo 版本演进

---

## 8. 项目交付物

### 8.1 核心交付物
- wms_owner - 货主管理增强模块
- wms_putaway - 智能上架增强模块
- wms_wave - 波次管理增强模块
- wms_billing - 计费管理模块
- 3PL 专用报表套件
- 用户配置指南

### 8.2 交付标准
- 100% 兼容 Odoo 原生功能
- 3PL 业务场景完全覆盖
- 用户体验优化
- 性能基准达成

---

## 9. 风险与应对

### 9.1 技术风险
| 风险 | 影响 | 应对措施 |
|------|------|----------|
| Odoo 版本升级兼容 | 中 | 遵循 Odoo 开发最佳实践 |
| 企业版功能依赖 | 低 | 提供社区版替代方案 |
| 性能瓶颈 | 低 | 基于原生功能，性能有保障 |

### 9.2 业务风险
| 风险 | 影响 | 应对措施 |
|------|------|----------|
| 需求变更 | 中 | 迭代开发，快速响应 |
| 业务复杂度 | 低 | 基于成熟业务模型 |

---

## 10. 总结

本 3PL WMS 解决方案采用"原生功能 + 专业增强"的架构策略，充分利用 Odoo 18 强大的原生仓储管理功能，在此基础上提供专业的 3PL 业务增强。这种架构既保证了系统的稳定性和成熟度，又提供了专业的 3PL 特性，实现了开发效率、系统稳定性和业务专业性的完美平衡。

## 11. 实现映射与功能对比

### 11.1 对比表映射分析

根据"Odoo与您提供的 WMS 系统功能对比表"的要求，以下是本解决方案对各项功能的实现映射：

| **功能模块** | **详细功能点** | **您提供的WMS系统** | **Odoo 18** | **本方案实现方式** |
| :--- | :--- | :--- | :--- | :--- |
| **基础设置** | 产品档案 | ✅ | ✅ | 使用 Odoo 原生产品管理功能 |
| | 仓库 | ✅ | ✅ | 使用 Odoo 原生仓库管理功能 |
| | 工作区 | ✅ | ⚠️ | 通过 **wms_workzone** 模块实现 |
| | 库位 | ✅ | ✅ | 使用 Odoo 原生库位管理功能 |
| | 货主 | ✅ | ✅ | 通过 **wms_owner** 模块扩展，利用原生 `owner_id` |
| | 货类 | ✅ | ⚠️ | 通过 **wms_cargo_type** 模块实现 |
| | 客户档案 | ✅ | ✅ | 使用 Odoo 原生客户管理功能 |
| | 包装 | ✅ | ✅ | 使用 Odoo 原生包装管理功能 |
| | 库区 | ✅ | ⚠️ | 通过 **wms_storage_area** 模块实现 |
| | 贸易伙伴 | ✅ | ✅ | 使用 Odoo 原生客户/供应商管理功能 |
| | 资料导入 | ✅ | ✅ | 使用 Odoo 原生导入工具 |
| | 系统代码 | ✅ | ✅ | 通过 Odoo 配置实现 |
| **RF移动端** | 按单收货 | ✅ | ✅ | 使用 Odoo 企业版条码App或自研RF模块 |
| | 按箱收货 | ✅ | ⚠️ | 通过 **wms_rf_container** 模块实现 |
| | 盲收入库 | ✅ | ⚠️ | 通过 **wms_rf_blind_receive** 模块实现 |
| | 容器上架 | ✅ | ✅ | 利用 Odoo 原生包裹功能 |
| | 库存查询 | ✅ | ✅ | 使用 Odoo 原生库存查询功能 |
| | 库存盘点 | ✅ | ✅ | 使用 Odoo 原生盘点功能 |
| | 库存冻结 | ✅ | ⚠️ | 通过 **wms_inventory_freeze** 模块实现 |
| | 库存移动 | ✅ | ✅ | 使用 Odoo 原生库存移动功能 |
| | 按单拣货 | ✅ | ✅ | 使用 Odoo 原生拣货功能 |
| | 波次拣货 | ✅ | ✅ | 通过 **wms_wave** 模块增强，利用原生波次功能 |
| | 复核装箱 | ✅ | ⚠️ | 通过 **wms_packing_check** 模块实现 |
| | 装车发运 | ✅ | ✅ | 使用 Odoo 原生发运功能 |
| | 出库交接 | ✅ | ⚠️ | 通过 **wms_handover** 模块实现 |
| **业务规则** | 上架规则 | ✅ | ✅ | 通过 **wms_putaway** 模块增强，利用原生上架规则 |
| | 库存周转规则 | ✅ | ✅ | 利用 Odoo 原生 FIFO/FEFO/LIFO 等下架策略 |
| | 分配规则 | ✅ | ⚠️ | 通过 **wms_putaway** 模块增强实现智能分配 |
| | 打印规则 | ✅ | ✅ | 使用 Odoo 原生报表打印功能 |
| | 序列号规则 | ✅ | ✅ | 使用 Odoo 原生序列号追踪功能 |
| | 批次规则 | ✅ | ✅ | 使用 Odoo 原生批次追踪功能 |
| | 波次规则 | ✅ | ⚠️ | 通过 **wms_wave_auto** 模块实现自动波次生成 |
| | 快递规则 | ✅ | ⚠️ | 通过 **wms_courier** 模块实现快递对接 |
| | 装箱规则 | ✅ | ⚠️ | 通过 **wms_packing_rule** 模块实现自动装箱建议 |
| | 公司参数 | ✅ | ✅ | 使用 Odoo 原生配置功能 |
| | 货主参数 | ✅ | ⚠️ | 通过 **wms_owner** 模块实现货主参数体系 |
| | 导入导出规则 | ✅ | ✅ | 使用 Odoo 原生导入导出功能 |
| **库存管理** | 库存调整 | ✅ | ✅ | 使用 Odoo 原生库存调整功能 |
| | 盘点管理 | ✅ | ✅ | 使用 Odoo 原生盘点管理功能 |
| | 库存流水 | ✅ | ✅ | 使用 Odoo 原生库存移动记录 |
| | 库存移动 | ✅ | ✅ | 使用 Odoo 原生库存移动功能 |
| | 库位库存流水 | ✅ | ✅ | 使用 Odoo 原生库存移动记录 |
| | 库存冻结/释放 | ✅ | ⚠️ | 通过 **wms_inventory_freeze** 模块实现 |
| | 库存转移 | ✅ | ✅ | 使用 Odoo 原生库存转移功能 |
| | 库存查询 | ✅ | ✅ | 使用 Odoo 原生库存查询功能 |
| **统计分析** | 入库报表 | ✅ | ✅ | 使用 Odoo 原生报表功能 |
| | 出库报表 | ✅ | ✅ | 使用 Odoo 原生报表功能 |
| | 库存报表 | ✅ | ✅ | 使用 Odoo 原生报表功能 |
| | 进出存报表 | ✅ | ✅ | 使用 Odoo 原生报表功能 |
| | 库龄分析 | ✅ | ⚠️ | 通过 **wms_inventory_age** 模块实现 |
| | ABC分析 | ✅ | ⚠️ | 通过 **wms_abc_analysis** 模块实现 |
| | EIQ分析 | ✅ | ❌ | 通过 **wms_eiq_analysis** 模块实现 |
| | 库位使用报表 | ✅ | ⚠️ | 通过 **wms_location_usage** 模块实现 |
| | 绩效报表 | ✅ | ⚠️ | 通过 **wms_performance** 模块实现 |
| **入库管理** | 入库作业 | ✅ | ✅ | 使用 Odoo 原生入库功能 |
| | 按箱收货 | ✅ | ⚠️ | 通过 **wms_rf_container** 模块实现 |
| | 上架作业 | ✅ | ✅ | 使用 Odoo 原生上架功能 |
| | 越库管理 | ✅ | ✅ | 通过 **wms_crossdock** 模块增强，利用原生越库路线 |
| | 汇总入库 | ✅ | ⚠️ | 通过 **wms_batch_receive** 模块实现 |
| **出库管理** | 发货订单 | ✅ | ✅ | 使用 Odoo 原生发货功能 |
| | 订单打印 | ✅ | ✅ | 使用 Odoo 原生订单打印功能 |
| | 订单分配 | ✅ | ✅ | 使用 Odoo 原生订单分配功能 |
| | 波次计划 | ✅ | ✅ | 通过 **wms_wave** 模块增强 |
| | 拣货复核 | ✅ | ⚠️ | 通过 **wms_packing_check** 模块实现 |
| | 装箱交接 | ✅ | ⚠️ | 通过 **wms_handover** 模块实现 |
| **增值服务** | 库内加工 | ✅ | ⚠️ | 通过 **wms_value_added** 模块实现 |
| | 快递对接 | ✅ | ⚠️ | 通过 **wms_courier** 模块实现 |
| | WCS对接 | ✅ | ❌ | 通过 **wms_wcs** 模块实现 |
| | RFID接口 | ✅ | ❌ | 通过 **wms_rfid** 模块实现 |
| | 计费管理 | ✅ | ⚠️ | 通过 **wms_billing** 模块实现 |
| **组织架构** | 多仓库配置 | ✅ | ✅ | 使用 Odoo 原生多仓库功能 |
| | 多货主配置 | ✅ | ✅ | 通过 **wms_owner** 模块扩展原生货主功能 |
| | 企业级货品 | ✅ | ⚠️ | 通过 **wms_owner** 模块实现货主级产品过滤 |
| | 企业级盘点 | ✅ | ⚠️ | 通过 **wms_owner** 模块实现货主级盘点 |
| | 企业级查询 | ✅ | ⚠️ | 通过 **wms_owner** 模块实现货主级查询 |
| | 多级仓库管理 | ✅ | ✅ | 使用 Odoo 原生多级仓库功能 |
| **微信小程序** | 库存查询 | ✅ | ❌ | 通过 **wms_wechat** 模块实现 |
| | 入库查询 | ✅ | ❌ | 通过 **wms_wechat** 模块实现 |
| | 出库查询 | ✅ | ❌ | 通过 **wms_wechat** 模块实现 |
| | 在线下单 | ✅ | ⚠️ | 通过 **wms_wechat** 模块实现 |

### 11.2 核心增强功能实现说明

#### 11.2.1 P0 级别（必须实现）
- **wms_owner**：多货主管理，基于 Odoo 原生 `owner_id` 字段，扩展计费和参数功能
- **wms_putaway**：智能上架，扩展 Odoo 原生上架规则，增加货主维度和 ABC 分类
- **wms_wave**：波次管理，基于 Odoo 波次拣货功能，增加自动化和优化功能
- **wms_billing**：计费管理，完整实现 3PL 计费引擎

#### 11.2.2 P1 级别（重要功能）
- **wms_workzone**：工作区管理，实现物理作业区域划分
- **wms_cargo_type**：货类管理，支持不同类型货物的特殊处理
- **wms_storage_area**：库区管理，实现逻辑分区管理
- **wms_rf_container**：按箱收货，完整 RF 收货流程
- **wms_rf_blind_receive**：盲收入库，支持无单据收货
- **wms_inventory_freeze**：库存冻结/释放，支持库存锁定功能
- **wms_packing_check**：复核装箱，增加独立复核确认步骤
- **wms_handover**：出库交接，实现专门的交接确认流程
- **wms_crossdock**：越库作业，基于 Odoo 原生越库路线增强

#### 11.2.3 P2 级别（扩展功能）
- **wms_wave_auto**：自动波次生成规则
- **wms_packing_rule**：装箱规则，自动推荐装箱方案
- **wms_batch_receive**：汇总入库，批量收货汇总功能
- **wms_abc_analysis**：ABC 分析，基于周转率的分类分析
- **wms_inventory_age**：库龄分析，库存积压情况分析
- **wms_eiq_analysis**：EIQ 分析，入库-品项-数量统计分析
- **wms_location_usage**：库位使用报表，库位占用率分析
- **wms_performance**：绩效报表，操作员效率追踪
- **wms_value_added**：库内加工，增值服务管理
- **wms_courier**：快递对接，快递系统集成
- **wms_wcs**：WCS 对接，仓库控制系统接口
- **wms_rfid**：RFID 接口，RFID 读写器集成
- **wms_wechat**：微信小程序，移动端查询和下单

### 11.3 技术实现策略

1. **充分利用原生功能**：基于 Odoo 18 原生强大的仓储功能，避免重复开发
2. **模块化扩展**：按功能模块独立开发，便于维护和部署
3. **性能优化**：针对大数据量场景进行数据库索引和查询优化
4. **用户体验**：优化操作流程，减少操作步骤和等待时间

---

### 3.11 微信小程序模块（wms_wechat）

#### 3.11.1 微信小程序接口（wms_wechat_api）
**功能描述**: 实现微信小程序接口，支持库存查询、入库查询、出库查询、在线下单等功能

**数据模型**:
```python
class WmsWechatConfig(models.Model):
    _name = 'wms.wechat.config'
    _description = 'WeChat Mini Program Config'

    name = fields.Char('Config Name', required=True)
    app_id = fields.Char('App ID', required=True)
    app_secret = fields.Char('App Secret', required=True)
    token = fields.Char('Token')
    encoding_aes_key = fields.Char('EncodingAESKey')
    active = fields.Boolean('Active', default=True)

    def get_access_token(self):
        """获取微信 Access Token"""
        import requests
        url = f'https://api.weixin.qq.com/cgi-bin/token'
        params = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret
        }
        response = requests.get(url, params=params)
        return response.json().get('access_token')

class WmsWechatController(http.Controller):

    @http.route('/api/wechat/inventory', type='json', auth='public', methods=['POST'])
    def query_inventory(self, **kwargs):
        """库存查询接口"""
        owner_code = kwargs.get('owner_code')
        product_code = kwargs.get('product_code')

        owner = request.env['res.partner'].sudo().search([
            ('owner_code', '=', owner_code),
            ('is_warehouse_owner', '=', True)
        ], limit=1)

        if not owner:
            return {'code': 404, 'message': '货主不存在'}

        domain = [('owner_id', '=', owner.id)]
        if product_code:
            product = request.env['product.product'].sudo().search([
                ('default_code', '=', product_code)
            ], limit=1)
            if product:
                domain.append(('product_id', '=', product.id))

        quants = request.env['stock.quant'].sudo().search(domain)

        data = []
        for quant in quants:
            data.append({
                'product_code': quant.product_id.default_code,
                'product_name': quant.product_id.name,
                'location': quant.location_id.complete_name,
                'quantity': quant.quantity,
                'available_quantity': quant.quantity - quant.reserved_quantity,
            })

        return {'code': 200, 'data': data}

    @http.route('/api/wechat/inbound', type='json', auth='public', methods=['POST'])
    def query_inbound(self, **kwargs):
        """入库查询接口"""
        owner_code = kwargs.get('owner_code')
        date_from = kwargs.get('date_from')
        date_to = kwargs.get('date_to')

        owner = request.env['res.partner'].sudo().search([
            ('owner_code', '=', owner_code),
            ('is_warehouse_owner', '=', True)
        ], limit=1)

        if not owner:
            return {'code': 404, 'message': '货主不存在'}

        domain = [
            ('owner_id', '=', owner.id),
            ('picking_type_code', '=', 'incoming'),
            ('state', '=', 'done')
        ]
        if date_from:
            domain.append(('date_done', '>=', date_from))
        if date_to:
            domain.append(('date_done', '<=', date_to))

        pickings = request.env['stock.picking'].sudo().search(domain)

        data = []
        for picking in pickings:
            data.append({
                'name': picking.name,
                'date': picking.date_done.strftime('%Y-%m-%d %H:%M:%S'),
                'origin': picking.origin,
                'state': picking.state,
                'lines': [{
                    'product_code': line.product_id.default_code,
                    'product_name': line.product_id.name,
                    'quantity': line.quantity,
                } for line in picking.move_line_ids]
            })

        return {'code': 200, 'data': data}

    @http.route('/api/wechat/outbound', type='json', auth='public', methods=['POST'])
    def query_outbound(self, **kwargs):
        """出库查询接口"""
        owner_code = kwargs.get('owner_code')
        date_from = kwargs.get('date_from')
        date_to = kwargs.get('date_to')

        owner = request.env['res.partner'].sudo().search([
            ('owner_code', '=', owner_code),
            ('is_warehouse_owner', '=', True)
        ], limit=1)

        if not owner:
            return {'code': 404, 'message': '货主不存在'}

        domain = [
            ('owner_id', '=', owner.id),
            ('picking_type_code', '=', 'outgoing'),
            ('state', '=', 'done')
        ]
        if date_from:
            domain.append(('date_done', '>=', date_from))
        if date_to:
            domain.append(('date_done', '<=', date_to))

        pickings = request.env['stock.picking'].sudo().search(domain)

        data = []
        for picking in pickings:
            data.append({
                'name': picking.name,
                'date': picking.date_done.strftime('%Y-%m-%d %H:%M:%S'),
                'partner': picking.partner_id.name,
                'state': picking.state,
                'lines': [{
                    'product_code': line.product_id.default_code,
                    'product_name': line.product_id.name,
                    'quantity': line.quantity,
                } for line in picking.move_line_ids]
            })

        return {'code': 200, 'data': data}

    @http.route('/api/wechat/order/create', type='json', auth='public', methods=['POST'])
    def create_order(self, **kwargs):
        """在线下单接口"""
        owner_code = kwargs.get('owner_code')
        order_lines = kwargs.get('order_lines', [])

        owner = request.env['res.partner'].sudo().search([
            ('owner_code', '=', owner_code),
            ('is_warehouse_owner', '=', True)
        ], limit=1)

        if not owner:
            return {'code': 404, 'message': '货主不存在'}

        # 创建出库单
        picking_type = request.env['stock.picking.type'].sudo().search([
            ('code', '=', 'outgoing'),
            ('warehouse_id.company_id', '=', owner.company_id.id)
        ], limit=1)

        picking = request.env['stock.picking'].sudo().create({
            'picking_type_id': picking_type.id,
            'owner_id': owner.id,
            'partner_id': owner.id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
            'origin': 'WeChat Order',
        })

        # 创建移动行
        for line in order_lines:
            product = request.env['product.product'].sudo().search([
                ('default_code', '=', line.get('product_code'))
            ], limit=1)

            if product:
                request.env['stock.move'].sudo().create({
                    'name': product.name,
                    'product_id': product.id,
                    'product_uom_qty': line.get('quantity', 0),
                    'product_uom': product.uom_id.id,
                    'picking_id': picking.id,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking.location_dest_id.id,
                })

        picking.action_confirm()

        return {
            'code': 200,
            'message': '订单创建成功',
            'data': {
                'order_number': picking.name,
                'order_id': picking.id
            }
        }
```

---