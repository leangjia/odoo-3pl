{
    "name": "WMS Performance Dashboard",
    "summary": "Performance analytics and dashboard for 3PL warehouse operations",
    "description": """
        Advanced performance dashboard system for 3PL warehouses including:
        - Real-time KPI monitoring and visualization
        - Performance metrics and analytics
        - Customizable dashboards and widgets
        - Trend analysis and forecasting
        - Benchmarking and comparison tools
        - Alert and notification systems
        - Performance scorecards
        - Executive reporting
    """,
    "version": "17.0.1.0.0",
    "category": "Inventory/Inventory",
    "depends": [
        "base",
        "stock",
        "hr",
        "sale",
        "board",
        "web",
        "wms_owner"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/performance_dashboard_views.xml",
        "views/menu_views.xml"
    ],
    "demo": [
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "license": "LGPL-3"
}