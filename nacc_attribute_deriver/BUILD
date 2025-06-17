python_sources(name="lib", dependencies=["./config:rules"])

python_distribution(
    name="dist",
    dependencies=[":lib", "./config:rules"],
    wheel=True,
    sdist=True,
    provides=python_artifact(
        name="nacc-attribute-deriver",
        version="1.5.0-dev6",
        description="Uses rules to derive attribute values from file data",
        author="NACC",
        author_email="nacchelp@uw.edu",
        url="https://github.com/naccdata/nacc-attribute-deriver",
    ),
)
