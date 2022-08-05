import csv
from io import StringIO
from typing import (
    BinaryIO,
    TextIO,
)

from fastapi import Depends

from wallet.models.operations import OperationCreate, Operation
from wallet.services.operations import OperationsService


class ReportService:
    report_fields = [
        'date',
        'kind',
        'amount',
        'description',
    ]

    def __init__(self, operations_service: OperationsService = Depends()):
        self.operations_service = operations_service

    def import_csv(self, user_id: int, file: BinaryIO):
        """Uploads data from CSV-file to base."""
        reader = csv.DictReader(
            (line.decode() for line in file),  # Because there will be byte strings in the file,
            # before that you need to decode
            fieldnames=self.report_fields
        )
        operations = []

        next(reader, None)  # skip header
        for row in reader:
            operations_data = OperationCreate.parse_obj(row)
            # because csv can`t have none, replace to empty str
            operations_data.description = (None
                                           if operations_data.description == ''
                                           else '')
            operations.append(operations_data)

        self.operations_service.create_many(
            user_id=user_id,
            operations_data=operations,
        )

    def export_csv(self, user_id: int) -> TextIO:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=self.report_fields,
            extrasaction='ignore',
        )
        operations = self.operations_service.get_list(user_id=user_id)
        writer.writeheader()

        for operation in operations:
            operation_data = Operation.from_orm(operation)
            writer.writerow(operation_data.dict())
        output.seek(0)
        return output
