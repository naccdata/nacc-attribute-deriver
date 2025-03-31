## TODOs

* Ingest the SCAN data into all projects so we can test/curate it
    * I have a [crude script here](https://github.com/naccdata/flywheel-monitoring/blob/feature/add-scan-notebook/notebooks/ingest-scan.ipynb) that kicks off the ingestion pipeline
* Write a script to kick off curation for all curation types (UDS, NP, APOE, and SCAN) over all projects
    * Rough draft has been [pushed here](https://github.com/naccdata/flywheel-monitoring/blob/feature/add-scan-notebook/notebooks/curate.ipynb)

Currently the code should be up-to-date with MQT V2. The main thing left to do is to test, which requires 1) ingesting the SCAN data and 2) running the Attribute Curation gear over each project and each file, and then checking the results. We currently do not have an MQT baseline so they will need to be manually checked. The test code in this repo should be fairly in-depth per attribute, but not so much end to end.

Currently I have been running the gear locally, which also means installing this package through a local wheel. There are probably better ways to do this but I generally:

1. Increment/change the package version in `nacc_attribute_deriver/BUILD`, under the `python_distribution`
    - It needs to be different otherwise pants doesn't know to reinstall the wheel - there might be a command for it that I don't know
2. Run `pants package ::` and copy the resulting `dist/*.whl` to `flywheel-gear-extensions/dist`
3. Update the `requirements.txt` in `flywheel-gear-extensions` to match the version in step 1, e.g. something like `nacc_attribute_deriver@ file:///workspaces/flywheel-gear-extensions/dist/nacc_attribute_deriver-0.0.1.dev3-py3-none-any.whl`
4. Regenerate lockfiles with `pants generate-lockfiles` - combined with the new version this will force reinstall the wheel
4. Run `cd gear/attribute-curator` and `pants package src/docker` to build the image
5. Make sure your environment is set up per the "Running a gear locally" dev docs to run it locally

Eventually, the wheel actually needs to be released, and this repo made public so that `flywheel-gear-extensions` can find and install it. The `requirements.txt` line will then instead be `nacc_attribute_deriver@ https://github.com/naccdata/nacc-attribute-deriver/releases/download/v0.0.1/nacc_form_validator-0.0.1-py3-none-any.whl`. The gear in turn can be built and pushed to Flywheel.