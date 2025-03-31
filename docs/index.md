# NACC Attribute Deriver

This process is currently actively in development and highly subject to change.

## Curation Concepts

Subjects and files have *attributes* which are assigned values.
In Flywheel, an attribute is stored as custom information.
And, we use the convention that a subject attribute has a prefix `subject.info` while 
a file attribute has a prefix `file.info`.

A *raw* file attribute corresponds to a field in or associated with a file.
So the value of the attribute is directly determined by the file itself, and the value of a raw attributes should not be modified.
We use the conventions that the prefix for a raw attribute is `file.info.forms` for form data, and `file.info.raw` for non-form data.

A *derived* attribute of a file or subject is defined in terms of other attributes.

We can make this more precise using these concepts:

- A subject *s* has a set of associated files denoted *files*(*s*).
- A file *f* is associated with only one subject denoted *subject*(*f*)

The value of a derived attribute of a subject *s* may only use the values of other attributes of the subject, or attributes of a file in *files*(*s*).
The value of a derived attribute of a file *f* may only be determined by the values of other attributes of the file, or attributes of *subject*(*f*).

The implication of this is that we only need to consider a single subject and it's associated files to curate all of the derived attributes.

### Curation rules

We compute the value of a derived variable using a *curation rule*, which is defined by

* the name of the derived attribute,
* an expression of the other attributes used to compute the value of the derived attribute, and
* the operator used to assign the value of the expression to the the derived attribute

We constrain curation rules so that they are only defined over the attributes of a subject, and the attributes of a single file.
So, a curation rule has a *scope* that determines which kinds of file can be applied to.

### Curation order

The implication of the constraint is that if a value derived from a file is needed in the computation of an attribute of a different file, there must be a rule applied first that assigns the value to an attribute of the subject.

For this to work, we must ensure files are visited in order of dependency of the attributes.
Though, in practice, this can be handled by ordering how files are visited in curation, which is handled by the curation gear.



## Workflow

### Curation Gear

The NACC Attribute deriver works in coordination with the Attribute Curation gear in [flywheel-gear-extensions](https://github.com/naccdata/flywheel-gear-extensions).

The Attribute Curation gear is launched **per project and curation type**, e.g. all UDS forms for a single center. The files are scheduled using a MinHeap ordered by a specified date key, if applicable (some curation types such as NCARD APOE curation have no ordering).

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
