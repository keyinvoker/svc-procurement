from traceback import format_exc

from eproc import error_logger


def get_next_document_number(
    year: int,
    month: int,
    sequence_number: int,
) -> str:

    try:
        year_string = str(year)[::2]
        month_string = str(month).zfill(2)
        sequence_string = str(sequence_number).zfill(4)

        document_number = f"BSS/RFQ/{year_string}{month_string}{sequence_string}"

        return document_number

    except Exception as e:
        error_logger.error(f"Error on helpers:rfq:get_next_document_number() :: {e}, {format_exc()}")
