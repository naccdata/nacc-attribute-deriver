"""MP imaging namespace."""

from datetime import date, datetime
from typing import Optional

from nacc_attribute_deriver.attributes.base.namespace import BaseNamespace
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable


class MixedProtocolNamespace(BaseNamespace):
    """Mixed protocol namespace (DICOM image)."""

    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix: str = "file.info.header.dicom.",
        required: frozenset[str] = frozenset(["StudyDate"]),
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(
            table=table,
            attribute_prefix=attribute_prefix,
            required=required,
            date_attribute=date_attribute,
        )
        # TODO: this is hacky, but we know an image is a nifti
        # if the ONLY thing in file.info.header is the dicom dict
        # we assume dicom first, then nifti, since nifti is
        # created from the dicom and may not always be created
        # being able to see the filename would be more appropriate, but
        # would require some refactoring of how information is passed in,
        # so just do this for now
        self.__nifti = False
        if "file.info.header" in table and len(table.get("file.info.header", [])) == 1:
            self.__nifti = True

        acq_date = self.get_value("StudyDate", str)
        if not acq_date:
            raise AttributeDeriverError("No StudyDate found for image")

        self.__acquisition_date = datetime.strptime(acq_date, "%Y%m%d").date()

    @property
    def is_nifti(self) -> bool:
        return self.__nifti

    @property
    def acquisition_date(self) -> date:
        return self.__acquisition_date

    def _create_image_session(self) -> str:
        """Create variable to keep track of unique image sessions, based on
        acquisition date."""
        return str(self.acquisition_date)
