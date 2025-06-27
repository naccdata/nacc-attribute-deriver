# Operations

The following table summarizes the available operations.

| Name | Requirements | Description |
| - | - | - |
| `update` | None | Updates the destination value with the current value. |
| `list` | Destination is a list | Inserts the current value at the end of a list, retaining insert order. |
| `sortedlist` | Destination is a list, and `DateTaggedValue`s are not mixed with other types | Inserts the current value into a lexicographically sorted list. |
| `set` | Destination is a set, and `DateTaggedValue`s are not mixed with other types | Inserts the current value into a set (no duplicates). The set is sorted for consistency since it is ultimately converted to a list since Flywheel only supports lists. Can alternatively be thought of as a `sortedlist` where every value is unique. |
| `initial` | Value is a `DateTaggedValue` | Updates the destination value if the current value's date comes BEFORE the destination value's. |
| `latest` | Value is a `DateTaggedValue` | Updates the destination value if the current value's date comes AFTER the destination value's. |
| `min` | Raw values comparable | Updates the destination value if the current value is LESS (`<`) than the desetination. If the value is `DateTaggedValue`, compares `value.value`. |
| `max` | Raw values comparable | Updates the destination value if the current value is GREATER (`>`) than the destination. If the value is `DateTaggedValue`, compares `value.value`. |

"Destination value" refers to the value already sitting in the input SymbolTable (Flywheel metadata). "Current value" refers to the value that is currently being derived, and may override the destination value based on the operation.

Aside from standard types (e.g. int), dated values are also supported and represented by a `DateTaggedValue`, which when serialized look like a dict:

```json
{
	"date": "YYYY-MM-DD",
	"value": "any JSON-serializable data"
}
```

All operations support dated values, but some explicitly require it. For all operations, None values are ignored (e.g. operation is not executed and the destination value is not updated).
