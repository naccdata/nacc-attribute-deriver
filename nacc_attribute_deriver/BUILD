python_sources(name="lib", dependencies=[":rules"])

python_distribution(
    name="dist",
    dependencies=[":lib", ":rules"],
    wheel=True,
    sdist=True,
    provides=python_artifact(
        name="nacc-attribute-deriver",
        version="0.0.1-dev1",
        description="Derives variables",
        author="NACC",
        author_email="nacchelp@uw.edu",
        url="https://github.com/naccdata/nacc-attribute-deriver"),
    entry_points={
        "console_scripts": {
            "nacc-attribute-deriver":
            "nacc_attribute_deriver.deriver_cli:entrypoint"
        }
    })

pex_binary(
    name="bin",
    entry_point="deriver_cli.py",
)

resource(name="rules", source="bin/derive_rules.csv")
