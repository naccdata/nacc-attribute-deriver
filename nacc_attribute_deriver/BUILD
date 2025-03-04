python_sources(name="lib")

python_distribution(
    name="dist",
    dependencies=[
        "nacc_attribute_deriver/attributes:lib",
        "nacc_attribute_deriver/bin:lib",
        "nacc_attribute_deriver/deriver:lib",
        "nacc_attribute_deriver/schema:lib"
    ],
    entry_points={
        "console_scripts": {
            "nacc-attribute-deriver": "nacc_attribute_deriver.bin.deriver_cli:entrypoint"
        }
    },
    wheel=True,
    sdist=True,
    provides=python_artifact(
        name="nacc-attribute-deriver",
        version="0.0.1-dev1",
        description="Derives variables",
        author="NACC",
        author_email="nacchelp@uw.edu",
        url="https://github.com/naccdata/nacc-attribute-deriver"),
)
