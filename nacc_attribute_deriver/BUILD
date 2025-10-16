python_sources(name="lib", dependencies=["./config:rules", "./config:data"])

python_distribution(
    name="dist",
    dependencies=[":lib", "./config:rules"],
    wheel=True,
    sdist=True,
    provides=python_artifact(
        name="nacc-attribute-deriver",
        version="2.0.0.dev1",
        description="Uses rules to derive attribute values from file data",
        author="NACC",
        author_email="nacchelp@uw.edu",
        url="https://github.com/naccdata/nacc-attribute-deriver",
    ),
)
