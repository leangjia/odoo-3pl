# 3PL WMS Documentation Index

## Overview
This index provides an organized view of all documentation files for the 3PL WMS system. The documentation is structured to support different use cases and audiences.

## Core Documentation

### 1. System Specifications
- **spec.md** - Complete 3PL WMS specification with functional requirements and implementation mapping
  - Comprehensive overview of the 3PL WMS system
  - Feature comparison with existing WMS systems
  - Technical architecture and implementation details

### 2. User Stories by Epic
- **epic.md** - User stories organized by epic structure for better understanding and management
  - 25+ functional epics covering all major areas
  - Cross-reference mapping to all user stories
  - Strategic organization by functional area

### 3. Individual Module User Stories
- **wms_*.md** - Individual user story files for each module
  - Contains detailed user story, acceptance criteria, and business value
  - One file per module for easy reference and maintenance

## Supporting Documentation

### 4. User Stories (Historical/Alternative Views)
> **Note**: These files represent alternative organization of user stories. The individual module files and epic organization are preferred.

- **user_stories.md** - User stories and acceptance criteria for P2 modules (English)
- **user_stories_from_spec.md** - User stories based on 3PL WMS specification (Chinese)
- **module_user_stories.md** - Module-specific user stories from specification (Chinese)

### 5. Reference Files
- **README.md** - Basic overview and setup instructions
- **INDEX.md** - This documentation index

## Module Documentation Coverage

### Core WMS Modules
- wms_owner - Multi-owner management for 3PL warehouses
- wms_putaway - Enhanced putaway rules for 3PL warehouses
- wms_wave - Wave picking management for 3PL warehouses
- wms_crossdock - Crossdock management for 3PL warehouses
- wms_billing - Billing management for 3PL warehouses

### Analytics and Reporting Modules
- wms_eiq_analysis - EIQ (Entry-Item-Quantity) analysis
- wms_location_usage - Location usage and capacity analysis
- wms_performance - Performance monitoring and tracking
- wms_inventory_age - Inventory aging analysis
- wms_abc_analysis - ABC classification analysis

### Process Enhancement Modules
- wms_packing_rule - Packing optimization and rules
- wms_packing_check - Packing verification and quality control
- wms_handover - Outbound handover and sign-off management
- wms_returns_management - Return merchandise authorization and processing

### RF and Mobile Enhancement Modules
- wms_rf_container - Container-based receiving with RF/RFID scanning
- wms_rf_blind_receive - Blind receiving for unexpected shipments
- wms_inventory_freeze - Inventory freezing for quality control

### Integration Modules
- wms_courier - Courier company integration
- wms_wcs - Warehouse Control System integration
- wms_rfid - RFID technology integration
- wms_wechat - WeChat Mini Program integration

### Extended Functionality Modules
- wms_value_added - Value-added services management
- wms_document_management - Document handling and versioning
- wms_quality_control - Quality inspection and compliance
- wms_workzone - Work zone management
- wms_cargo_type - Cargo classification and handling
- wms_storage_area - Storage area configuration
- wms_energy_management - Energy consumption tracking
- wms_safety_management - Safety incident and compliance management
- wms_finance_integration - Financial system integration
- wms_labor_management - Labor activity and productivity tracking
- wms_performance_dashboard - Performance analytics and visualization
- wms_batch_receive - Batch receiving for multiple orders

## Recommended Reading Path

For new users:
1. Start with **spec.md** for system overview
2. Review **wms_user_stories_by_epic.md** for functional understanding
3. Explore individual module files for specific details

For developers:
1. **spec.md** for implementation requirements
2. Relevant **wms_*.md** files for module-specific features
3. **wms_user_stories_by_epic.md** for cross-module dependencies

For business stakeholders:
1. **spec.md** for business requirements
2. **wms_user_stories_by_epic.md** for functional organization
3. Individual module files for detailed feature understanding