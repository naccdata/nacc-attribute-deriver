"""NCRAD Biosample derived variables."""

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)


class NCRADBiosampleAttributeCollection(AttributeCollection):
    """Class to collect historical NCRAD biosample attributes."""

    def _create_naccncrd(self) -> int:
        """Create NACCNCRD. From makerddgen.sas.

        See docs/ncrad.md for notes on this variable. Basically if this
        is called at all, file exists, so set NACCNCRD to 1.
        """
        return 1
