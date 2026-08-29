from batchplan.api import preview
from batchplan.importer import preview_row
from batchplan.model import BatchPlan


assert preview("0") == 1
assert preview("-4") == 1
assert preview_row({"batch_size": "0"}) == 1
assert BatchPlan().total_items() == 0
