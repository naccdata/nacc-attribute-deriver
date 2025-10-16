"""Derived variables from form B1: Physical.

Form B1 is optional, so may not have been submitted.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_attribute import (
    UDSAttributeCollection,
)


class UDSFormB1Attribute(UDSAttributeCollection):
    """Class to collect UDS B1 attributes."""

    @property
    def submitted(self) -> bool:
        return self.uds.get_value("b1sub", int) == 1

    def get_height(self) -> Optional[float]:
        """Get height; may need to add decimal.

        Min 36 UDSv3+, max is 87.9, UDSv2 and earlier max is 96.0
        """
        height = self.uds.get_value("height", float)

        if height is None or height == 99 or (self.formver == 3 and height == 88):
            return None

        heigdec = self.uds.get_value("heigdec", float)
        if heigdec is not None and heigdec != 0:
            height += heigdec / 10

        return None if height < 36 else height

    def get_weight(self) -> Optional[int]:
        """Get weight; min 50, max 400."""
        weight = self.uds.get_value("weight", int)
        if weight is None or weight < 50 or weight > 400:
            return None

        return weight

    def _create_naccbmi(self) -> Optional[float]:
        """Creates NACCBMI (body max index)."""
        # seems QAF before expects 888.8 if not
        # submitted on initial visit, -4/None otherwise
        if not self.submitted:
            if self.uds.is_initial():
                return 888.8
            return None

        height = self.get_height()
        weight = self.get_weight()

        if height is not None and weight is not None:
            naccbmi = (weight * 703) / (height * height)

            # + 0.0001 so we ensure exact halves round up, not down
            return round(naccbmi + 0.0001, 1)

        return 888.8
