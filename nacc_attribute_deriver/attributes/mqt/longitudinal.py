"""All longtitudinal MQT derived variables.

Assumes NACC-derived variables are already set
"""
from nacc_attribute_deriver.attributes.attribute_collection import MQTAttribute
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    datetime_from_form_date,
)


class LongitudinalAttribute(MQTAttribute):
    """Class to collect longitudinal attributes."""

    def _create_total_uds_visits(self) -> int:
        """Total number of UDS visits.

        This is an accumulative variable, assumes its called
        for each form

        Location:
            subject.info.longitudinal-data.uds.count.latest
        Operation:
            latest
        Type:
            mqt-longitudinal
        Description:
            Total number of UDS visits
        """
        count = self.table.get(
            'subject.info.longitudinal-data.uds.count.latest.value', 0)
        module = self.get_value('module')

        if module and module.lower() == 'uds':
            count += 1

        return count

    def _create_years_of_uds(self) -> int:
        """Creates subject.info.longitudinal-data.uds.year-count.

        Location:
            subject.info.longitudinal-data.uds.year-count
        Operation:
            max
        Type:
            mqt-longitudinal
        Description:
            Number of years of UDS visits available
        """
        result = self.assert_required(['uds_years'],
                                      prefix='subject.info.derived.')

        result = result['uds_years']
        return len(result) if result else 0
