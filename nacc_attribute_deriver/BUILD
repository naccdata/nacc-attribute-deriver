python_sources(name="lib", dependencies=["./config:rules"])

python_distribution(
    name="dist",
    dependencies=[":lib", "./config:rules"],
    wheel=True,
    sdist=True,
    provides=python_artifact(
        name="nacc-attribute-deriver",
        version="1.2.1",
        description="Uses rules to derive attribute values from file data",
        author="NACC",
        author_email="nacchelp@uw.edu",
        url="https://github.com/naccdata/nacc-attribute-deriver",
    ),
    entry_points={
        "console_scripts": {
            "nacc-attribute-deriver": "nacc_attribute_deriver.deriver_cli:entrypoint"
        }
    },
)

pex_binary(
    name="bin",
    entry_point="deriver_cli.py",
)
