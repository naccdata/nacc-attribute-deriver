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

The Attribute Curation gear runs over an entire project with a single instance of the NACC Attribute Deriver. Each subject's files are scheduled using a `MinHeap` ordered by scope. Within each scope, the files are ordered by a form-specific date key, if applicable (some curation types such as NCARD APOE curation have no ordering).

The curation order matters since many derived variables, particularly for UDS, assume certain variables have already been derived before it (scope), and it also affects the behavior of longitudinal and cross-sectional values (dates). In general, the UDS namespace is always the last to be curated.

For each file, both the file AND parent subject's `.info` metadata is pulled and stored in a SymbolTable under `file.info.x` and `subject.info`, respectively. In turn, the deriver expects to find file-specific fields to curate on in either `file.info.forms.json` (for forms like UDS or NP) or `file.info.raw` (for external raw data like genetic or SCAN data), which is most NACC derived variables. Similarly, it expects to find global fields required for deriving across all forms under `subject.info`, which is most of the MQT derived variables.

Cross-sectional rules have some special behavior. Throughout curation, each is globally updated under `subject.info.derived.cross-sectional`, as specified by the curation rules. Once curation of a subject is complete, the resulting final values under `subject.info.derived.cross-sectional` are all back-propogated into each UDS file's `file.info.derived`. 

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

Curated variables are written back into the same SymbolTable (location defined by curation rule) and the gear similarly pushes `file.info.derived` and `subject.info` back to Flywheel, before moving onto the next file.

### Attribute Deriver

The overall infrastructure is based on [plugin infrastructures](https://eli.thegreenplace.net/2012/08/07/fundamental-concepts-of-plugin-infrastructures). Each "plugin", or attribute in our case, is defined as a `_create_{func}` function, organized by the different curation types, and can all be found under `attributes`. At the highest level, it is split by NACC and MQT attributes, the latter having the specific requirement of being reliant on NACC attributes being curated first. Each of these `_create_` functions is added to a global registry that can be specified by the curation rules CSV.

The main class is the `AttributeDeriver` defined under `attribute_deriver.py`. Each file corresponds to a specific scope, which is then used to pull out a set of curation rules defined under `config/curation_rules.csv`. Each rule denotes the following:

| Field | Description |
| ------ | ----------- |
| `scope` | The scope the rule belongs to. All rules in the scope will be executed on the given file. |
| `function` | Which `_create` function to call to derive the variable - should match a known `_create_{function}` method in the global registry. |
| `location` | Where in the SymbolTable the derived variable should be written to. As mentioned above, this is generally expected to be somewhere under `file.info.derived` or `subject.info`. |
| `operation` | The operation to perform on the resulting data. See [Operations](#./operations.md) for more information. |
| `dated` | Whether or not the value should be dated. Must be True for certain operations. |

For each rule, a value is derived based on the passed SymbolTable. Each rule belongs to an `AttributeCollection` class which in turn expects certain namespaces, and within these namespaces, certain fields may be required. If the passed SymbolTable does not have these required variables, an error will be thrown. Curation order once again is emphasized here - some of these required variables are expected to have been already curated by other scopes.

If `dated` is True, the derived value is further wrapped into a `DateTaggedValue`. The rule's `operation` is then applied against this value, usually comparing against the value that already exists at `location`, and then written to `location`. See [Operations](./operations) for more details).

In the curation rules, it is common to see the same `function` applied to multiple `operation/location` combinations - for example, we may be interested in the latest and earliest instance of `NACCAGE`.


## Adding New Variables

For the most part, adding a new variable just involves defining a new `_create_{func}` rule under the appropriate `AttributeCollection` class under `attributes`, and then adding the corresponding rule(s) to the configs CSV. Each method can assume that the attribute instance's SymbolTable will have appropriately populated `file.info.x` and `subject.info`.

It is a good idea to then add tests for your new attribute, which follows a similar directory structure as `attributes` under `tests`. Mosts tests target the specific attribute class, with one test function per attribute.
