# Auto Wave Generation (wms_wave_auto) User Story

## User Story
As a warehouse manager, I want to automatically generate picking waves based on configurable rules so that I can optimize picking efficiency and reduce manual work.

## Acceptance Criteria
- System can create wave rules with time-based triggers (fixed time, intervals, rolling windows)
- System can create wave rules with quantity-based triggers (min/max orders, volume, weight)
- System can filter pickings by warehouse, operation type, priority, and carrier
- System can sort pickings using different strategies (FIFO, LIFO, priority, delivery date, volume/weight optimization)
- System can automatically confirm waves after generation
- System can limit wave size based on maximum picking count
- System tracks rule execution statistics (last execution time, execution count)
- Users can manually execute wave rules
- System validates rule constraints (min orders cannot exceed max orders)

## Business Value
This feature will significantly reduce the manual effort required to create picking waves, improve picking efficiency through optimized wave creation, and ensure consistent application of warehouse policies. It will also provide better visibility into wave generation performance and enable data-driven optimization of warehouse operations.