"""MP imaging namespace."""

from datetime import date, datetime
from typing import Optional

from nacc_attribute_deriver.attributes.namespace.namespace import BaseNamespace
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
        study_date = self.get_value("StudyDate", str)
        if not study_date:
            raise AttributeDeriverError("No StudyDate found for image")

        self.__study_date = datetime.strptime(study_date, "%Y%m%d").date()

    @property
    def study_date(self) -> date:
        return self.__study_date
