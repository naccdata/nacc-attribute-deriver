# NACC Attribute Deriver

This process is currently actively in development and highly subject to change.

## Workflow

### Curation Gear

The NACC Attribute deriver works in coordination with the Attribute Curation gear in [flywheel-gear-extensions](https://github.com/naccdata/flywheel-gear-extensions).

The Attribute Curation gear is launched **per project and per curation type**, e.g. all UDS forms. The files are scheduled using a MinHeap ordered by a specified date key, if applicable (some curation types such as NCARD APOE curation have no ordering).

The gear creates an instance of the NACC Attribute Deriver, passing it

1. The curation rules CSV - these are specific per curation type. Examples can be seen under the `config` directory
2. (Optionally) a date key to order by. This is the same key used to order the above MinHeap, and is only required if the above curation rules require date ordering (e.g. initial or latest)

Next, for each file, both the file's AND parent subject's `.info` metadata is pulled and stored in a SymbolTable under `file.info` and `subject.info` respectively. As a result, the deriver expects to find file-specific fields to curate on in either `file.info.forms.json` (for forms like UDS or NP) or `file.info.raw` (for external raw data like genetic or SCAN data). Similarly, it expects to find global fields required for longitudinal/cross-section derivations under `subject.info`.

> Since `subject.info` is global, we cannot parallelize mutliple curations on different files if they are writing to the same subject in order to avoid read/write conflicts.

The SymbolTable works exactly like a normal dict, but understands dot-notation. So for example, calling `table['file.info.forms.json.visitdate']` grabs the following field:

```json
{
	"file": {
		"info": {
			"forms": {
				"json": {
					"visitdate"
				}
			}
		}
	}
}
```

This table is then passed to the deriver's `curate` function, which will curate that file based on the curation rule definitions - those curated variables are written back into the same SymbolTable. Once curation is done, the gear writes `file.info.derived` and `subject.info` back to Flywheel, and then moves onto the next file.

### Attribute Deriver

The overall infrastructure of this code is loosely based on [plugin infrastructures](https://eli.thegreenplace.net/2012/08/07/fundamental-concepts-of-plugin-infrastructures). Each "plugin", or attribute in our case, is defined as a `_create_{func}` function, organized by the different curation types, and can all be found under `attributes`. At the highest level, it is split by NACC and MQT attributes, the latter having the specific requirement of being reliant on NACC attributes being curated first. Each of these `_create_` functions is added to a global registry that can be specified by the curation rules CSV.

The main class is the `AttributeDeriver` defined under `attribute_deriver.py`. As mentioned above, it takes in both the curation rules CSV and an optional date key to define the overall curation behavior.

The following fields are critical for a valid curation rule:

| Column | Description |
| ------ | ----------- |
| `func` | Defines exactly which function to call to derive the variable - should match a known `_create_{func}` method in the global registry. |
| `location` | Where in the SymbolTable the derived variable should be written to. As mentioned above, this is generally expected to be somewhere under `file.info.derived` or `subject.info`. |
| `operation` | The operation to perform on the resulting data. This is more critical for global `subject.info` rules where it may be aggregating data in a set, or only setting the value from the latest file. See [Operations](#operations) for more information. |

The order of the rows determines the curation order, so all NACC variables should be derived before MQT ones. For each row

1. The `_create_{func}` pulls the information it needs from the SymbolTable and returns the derived variables
2. The `operation` is then applied on the raw derived variable, and the result is saved at `location`

#### Operations

The following operations are currently supported (defined under `schema/operation.py`):

| Operation | Description |
| --------- | ----------- |
| `update` | Updates the value |
| `set` | Adds the value to a set, so no duplicates are preserved |
| `sortedlist` | Adds the value to a lexicographically sorted list - duplicate are preserved |
| `count` | Counts (e.g. adds 1) to the target `location` if the value is valid. **NOTE** This is currently unreliable if curation is run over the same file multiple times. |
| `initial` | Updates the value IF the current file's order date is BEFORE the one already stored in the target `location` |
| `latest` | Updates the value IF the current file's order date is AFTER the one already stored in the target `location` |
| `min` | Updates the value IF the current value is less than the one already stored in the target `location`. Assumes values can be compared with the `<` operator, e.g. numbers. |
| `max` | Updates the value IF the current value is greater than the one already stored in the target `location`. Assumes values can be compared with the `>` operator, e.g. numbers. |

#### Rule Guards

Ideally, all `_create_{func}` attributes have some notion of recognizing whether or not the `file.info` data it is looking at actually belongs to the file it is meant to curate. At the moment, this is accomplished by looking for key fields in the data and throwing an error if the key field is not found. For example, `UDSAttribute` looks for the `module` field and that it equals "UDS"; if that condition is not satisfied, an error is thrown.
