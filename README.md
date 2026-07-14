# NACC Attribute Deriver

Module for deriving variables. See the [docs](./docs/index.md) for more information.

## Building the Distribution

To manually build the distribution, run

```bash
pants package ::
```

which will write the distributions to the `dist` directory

## Releasing a Distribution

To release a distribution, make sure you are on the `main` branch with all changes pulled. Make sure `nacc_attribute_deriver/BUILD` is set to the version you intend to release. Then, tag the current commit with that same version and a `v` prefixed, e.g.

```bash
git tag -a "v1.2.3" -m "Some short description about the release" 
```

Then push the tag; this will automatically kick off the build process (defined in `.github/workflows/build.yml`)

```bash
git push origin --tags
```
