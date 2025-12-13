"""Derived variables from form B1: Physical."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)


class UDSFormB1Attribute(UDSAttributeCollection):
    """Class to collect UDS B1 attributes."""

    @property
    def submitted(self) -> bool:
        """Form B1 is optional, so may have not been submitted.

        See B1SUB for V3 and earlier, MODEB1 for V4.
        """
        if self.formver < 4:
            return self.uds.get_value("b1sub", int) == 1

        return self.uds.get_value("modeb1", int) == 1

    def get_height(self) -> Optional[float]:
        """Get height; may need to add decimal.

        Min 36 UDSv3+, max is 87.9, UDSv2 and earlier max is 96.0
        """
        height = self.uds.get_value("height", float)

        if height is None or height == 99 or (self.formver >= 3 and height >= 88):
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
            if self.uds.is_initial() and not self.uds.is_i4():
                return 888.8

            return INFORMED_MISSINGNESS

        height = self.get_height()
        weight = self.get_weight()

        if height is not None and weight is not None:
            naccbmi = (weight * 703) / (height * height)

            # + 0.0001 so we ensure exact halves round up, not down
            return round(naccbmi + 0.0001, 1)

        return 888.8

    def _compute_average(
        self, field1: str, field2: str, minimum: int, maximum: int
    ) -> Optional[int]:
        """Compute the average for the two fields (V4 only).

        Rounded to the nearest integer.
        """
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        if not self.submitted:
            if self.uds.is_initial():
                return INFORMED_MISSINGNESS
            return None

        value1 = self.uds.get_value(field1, int)
        value2 = self.uds.get_value(field2, int)

        if any(x is None or x == 888 for x in [value1, value2]):
            return 888

        result = (value1 + value2) / 2  # type: ignore
        # + 0.0001 so we ensure exact halves round up, not down
        result = round(result + 0.0001)

        # enforce min/max
        return max(minimum, min(maximum, result))

    def _create_naccwaist(self) -> Optional[int]:
        """Creates NACCWAIST - Waist circumference (inches),
        average of two measurements.
        """
        return self._compute_average("waist1", "waist2", 20, 60)

    def _create_nacchip(self) -> Optional[int]:
        """Creates NACCHIP - Hip circumference (inches),
        average of two measurements
        """
        return self._compute_average("hip1", "hip2", 25, 70)

    def _handle_v3_blood_pressure(
        self, gate: str, field: str, minimum: int, maximum: int
    ) -> int:
        """Handles V3 blood pressure variables, which looks to see if
        supplemental blood pressure information (form B1a) was provided and
        returns that if so.

        Args:
            gate: Field indicating if supplement blood pressure data
                was submitted (checking if it equals 777)
            field: The field to grab if the supplemnt blood pressure
                data was submitted
            minimum: minimum value
            maximum: maimum value

        Returns:
            value of field, if supplemental data provided, else -4
        """
        if self.uds.get_value(gate, int) == 777:
            value = self.uds.get_value(field, int)
            if value is None:
                # TODO: B1a is currently not handled, so these values are missing
                # for now just return 888 but should throw error once there
                # raise AttributeDeriverError(
                #     f"Missing expected value {field} when {gate} == 777 for V3"
                # )
                return 888

            return max(minimum, min(maximum, value))

        return INFORMED_MISSINGNESS

    def _create_naccbpsysl(self) -> Optional[int]:
        """Creates NACCBPSYSL - Participant blood pressure
        (average of two readings), systolic, left arm
        """
        if self.formver == 3:
            return self._handle_v3_blood_pressure("bpsys", "bpsysl", 70, 230)

        return self._compute_average("bpsysl1", "bpsysl2", 70, 230)

    def _create_naccbpsysr(self) -> Optional[int]:
        """Creates NACCBPSYSR - Participant blood pressure
        (average of two readings), systolic, right arm
        """
        if self.formver == 3:
            return self._handle_v3_blood_pressure("bpsys", "bpsysr", 70, 230)

        return self._compute_average("bpsysr1", "bpsysr2", 70, 230)

    def _create_naccbpdial(self) -> Optional[int]:
        """Creates NACCBPDIAL - Participant blood pressure
        (average of two readings), diastolic, left arm
        """
        if self.formver == 3:
            return self._handle_v3_blood_pressure("bpdias", "bpdiasl", 30, 140)

        return self._compute_average("bpdiasl1", "bpdiasl2", 30, 140)

    def _create_naccbpdiar(self) -> Optional[int]:
        """Creates NACCBPDIAR - Participant blood pressure
        (average of two readings), diastolic, right arm
        """
        if self.formver == 3:
            return self._handle_v3_blood_pressure("bpdias", "bpdiasr", 30, 140)

        return self._compute_average("bpdiasr1", "bpdiasr2", 30, 140)
