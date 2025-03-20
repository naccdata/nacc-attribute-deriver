# NACC Attribute Deriver

This process is currently actively in development and highly subject to change.

## TODOs

* Ingest the SCAN data into all projects so we can test/curate it
    * I have a [crude script here](https://github.com/naccdata/flywheel-monitoring/blob/feature/add-scan-notebook/notebooks/ingest-scan.ipynb) that kicks off the ingestion pipeline
* Attribute Curation scheduling needs to be updated to support an unordered heap instead of MinHeap for curation types that have no ordering (e.g. APOE data)
* Test and review data - I did testing in the Sample Project but would be good to get other eyes on it
* Release this module (probably version 0.1.0 or similar) and make this repo **public** - this is necessary for `flywheel-gear-extensions` to publically find it
* Also finalize and release the Attribute Curation gear, and push to Flywheel
* Write a script to kick off curation for all curation types (UDS, NP, APOE, and SCAN) over all projects
    * Rough draft has been [pushed here](https://github.com/naccdata/flywheel-monitoring/blob/feature/add-scan-notebook/notebooks/curate.ipynb)

Currently the code should be up-to-date with MQT V2. The main thing left to do is to test, which requires 1) ingesting the SCAN data and 2) running the Attribute Curation gear over each project and each file, and then checking the results. We currently do not have an MQT baseline so they will need to be manually checked. The test code in this repo should be fairly in-depth per attribute, but not so much end to end.

Currently I have been running the gear locally, which also means installing this package through a local wheel. There are probably better ways to do this but I generally:

1. Increment/change the package version in `nacc_attribute_deriver/BUILD`, under the `python_distribution`
    - It needs to be different otherwise pants doesn't know to reinstall the wheel - there might be a command for it that I don't know
2. Run `pants package ::` and copy the resulting `dist/*.whl` to `flywheel-gear-extensions/dist`
3. Update the `requirements.txt` in `flywheel-gear-extensions` to match the version in step 1, e.g. something like `nacc_attribute_deriver@ file:///workspaces/flywheel-gear-extensions/dist/nacc_attribute_deriver-0.0.1.dev3-py3-none-any.whl`
4. Run `cd gear/attribute-curator` and `pants package src/docker` to build the image
5. Make sure your environment is set up per the "Running a gear locally" dev docs to run it locally

Eventually, the wheel actually needs to be released, and this repo made public so that `flywheel-gear-extensions` can find and install it. The `requirements.txt` line will then instead be `nacc_attribute_deriver@ https://github.com/naccdata/nacc-attribute-deriver/releases/download/v0.0.1/nacc_form_validator-0.0.1-py3-none-any.whl`. The gear in turn can be built and pushed to Flywheel.

## Workflow

### Curation Gear

The NACC Attribute deriver works in coordination with the Attribute Curation gear in [flywheel-gear-extensions](https://github.com/naccdata/flywheel-gear-extensions).

The Attribute Curation gear is launched **per project and per curation type**, e.g. all UDS forms for a single center. The files are scheduled using a MinHeap ordered by a specified date key, if applicable (some curation types such as NCARD APOE curation have no ordering).

The gear creates an instance of the NACC Attribute Deriver, passing it

1. The curation rules CSV - these are specific per curation type. Examples can be seen under the `config` directory
2. (Optionally) a date key to order by. This is the same key used to order the above MinHeap, and is only required if the above curation rules require date ordering (e.g. initial or latest)

Next, for each file, both the file's AND parent subject's `.info` metadata is pulled and stored in a SymbolTable under `file.info` and `subject.info`, respectively. As a result, the deriver expects to find file-specific fields to curate on in either `file.info.forms.json` (for forms like UDS or NP) or `file.info.raw` (for external raw data like genetic or SCAN data), which is most NACC derived variables. Similarly, it expects to find global fields required for deriving across all forms under `subject.info`, which is most of the MQT derived variables.

> The metadata locations are defined by the Form Importer gear which is generally run during the data's ingestion process. It simply copies the information inside the attached JSON and puts it under a defined prefix, which we set to `file.info.forms.json` for forms and `file.info.raw` for external raw data.

> Since `subject.info` is global, we cannot parallelize mutliple curations on different files if they are writing to the same subject in order to avoid read/write conflicts. In other words, there can only be a single curation gear running in a project at any given time.

The SymbolTable works exactly like a normal dict, but understands dot-notation. So for example, calling `table['file.info.forms.json.visitdate']` returns `2025-01-01`:

```json
{
    "file": {
        "info": {
            "forms": {
                "json": {
                    "visitdate": "2025-01-01"
                }
            }
        }
    }
}
```

This table is then passed to the deriver's `curate` function, which will curate that file based on the curation rule definitions - those curated variables are written back into the same SymbolTable. Once curation is done, the gear writes `file.info.derived` and `subject.info` back to Flywheel, and then moves onto the next file.

### Attribute Deriver

The overall infrastructure is based on [plugin infrastructures](https://eli.thegreenplace.net/2012/08/07/fundamental-concepts-of-plugin-infrastructures). Each "plugin", or attribute in our case, is defined as a `_create_{func}` function, organized by the different curation types, and can all be found under `attributes`. At the highest level, it is split by NACC and MQT attributes, the latter having the specific requirement of being reliant on NACC attributes being curated first. Each of these `_create_` functions is added to a global registry that can be specified by the curation rules CSV.

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
| `set` | Adds the value to a set - no duplicates are preserved |
| `sortedlist` | Adds the value to a lexicographically sorted list - duplicate are preserved |
| `count` | Counts (e.g. adds 1) to the target `location` if the value is valid. **NOTE** This is currently unreliable if curation is run over the same file multiple times. |
| `initial` | Updates the value IF the current file's order date is BEFORE the one already stored in the target `location` |
| `latest` | Updates the value IF the current file's order date is AFTER the one already stored in the target `location` |
| `min` | Updates the value IF the current value is less than the one already stored in the target `location`. Assumes values can be compared with the `<` operator, e.g. numbers. |
| `max` | Updates the value IF the current value is greater than the one already stored in the target `location`. Assumes values can be compared with the `>` operator, e.g. numbers. |

## Adding New Variables

For the most part, adding a new variable just involves defining a new `_create_{func}` rule under the appropriate class in `attributes`, and then adding the corresponding rule(s) to the appropriate config file under `configs`.

You can assume that the attribute instance's SymbolTable will have appropriately populated `file.info.x` and `subject.info`. In some special cases like cross-form variables, you may need to define special supplement paths, which the Attribute Curation gear must also be set up to handle.

It is a good idea to then add tests for your new attribute, which follows a similar directory structure as `attributes` under `tests`. Mosts tests target the specific attribute class, with one test function per attribute.

### Rule Guards

Ideally, all `_create_{func}` attributes have some notion of recognizing whether or not the `file.info` data it is looking at actually belongs to the file it is meant to curate. At the moment, this is accomplished by looking for key fields in the data and throwing an error if the key field is not found. For example, `UDSAttribute` looks for the `module` field and that it equals "UDS"; if that condition is not satisfied, an error is thrown.

### Attribute Hiearchy

Currently the attributes are split into two main classes: NACC attributes and MQT attributes. The main difference is that NACC attributes are typically scoped at the file-level and stored in `file.info.derived` or `subject.info.derived` (the latter is mainly used for intermediate variables between NACC and MQT), whereas MQT variables are typically derived from those same NACC attributes and scoped at the subject-level, and almost are always stored under their facet in `subject.info`.

Consequently, in order to curate both in a single pass, NACC attributes **must** be derived before MQT attributes. MQT attributes use an `assert_required` method to check that the NACC derived variable it needs has been derived first. If we switch to curating in two passes, the MQT values would not necessarily need this and could work on a flatter assumption similar to the NACC derived variables.

Each main class of attribute is then further subdivided into the raw source (NACC attributes) or the determined facets (MQT variables). Attributes derived from the same file/sources are generally grouped together as they have similar rule guards or assumptions about the data being curated.
