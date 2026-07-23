from sqlalchemy.orm import Session

from database.models import (
    Document,
    Section,
    ExtractedTable,
    TableColumn,
    TableRow,
    TableCell
)

# ==========================================================
# DOCUMENT CRUD
# ==========================================================

def create_document(
    db: Session,
    filename: str,
    filepath: str,
    total_pages: int
):
    document = Document(
        filename=filename,
        filepath=filepath,
        total_pages=total_pages,
        status="Uploaded"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_document(
    db: Session,
    document_id: int
):
    return (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )


def get_all_documents(db: Session):
    return (
        db.query(Document)
        .order_by(Document.id.desc())
        .all()
    )


def update_document_status(
    db: Session,
    document_id: int,
    status: str
):
    document = get_document(db, document_id)

    if document:
        document.status = status
        db.commit()
        db.refresh(document)

    return document


def delete_document(
    db: Session,
    document_id: int
):
    document = get_document(db, document_id)

    if document:
        db.delete(document)
        db.commit()

    return document


# ==========================================================
# SECTION CRUD
# ==========================================================

def create_section(
    db: Session,
    document_id: int,
    section_name: str,
    start_page: int,
    end_page: int
):
    section = Section(
        document_id=document_id,
        section_name=section_name,
        start_page=start_page,
        end_page=end_page
    )

    db.add(section)
    db.commit()
    db.refresh(section)

    return section


def get_sections(
    db: Session,
    document_id: int
):
    return (
        db.query(Section)
        .filter(Section.document_id == document_id)
        .all()
    )


# ==========================================================
# TABLE CRUD
# ==========================================================

def create_table(
    db: Session,
    section_id: int,
    table_number: str,
    table_title: str,
    page_number: int,
    json_path: str
):
    table = ExtractedTable(
        section_id=section_id,
        table_number=table_number,
        table_title=table_title,
        page_number=page_number,
        json_path=json_path
    )

    db.add(table)
    db.commit()
    db.refresh(table)

    return table


def get_tables(
    db: Session,
    section_id: int
):
    return (
        db.query(ExtractedTable)
        .filter(ExtractedTable.section_id == section_id)
        .all()
    )


# ==========================================================
# COLUMN CRUD
# ==========================================================

def create_column(
    db: Session,
    table_id: int,
    column_name: str,
    parent_column_id=None,
    column_order: int = 0
):
    column = TableColumn(
        table_id=table_id,
        column_name=column_name,
        parent_column_id=parent_column_id,
        column_order=column_order
    )

    db.add(column)
    db.commit()
    db.refresh(column)

    return column


def get_columns(
    db: Session,
    table_id: int
):
    return (
        db.query(TableColumn)
        .filter(TableColumn.table_id == table_id)
        .order_by(TableColumn.column_order)
        .all()
    )


# ==========================================================
# ROW CRUD
# ==========================================================

def create_row(
    db: Session,
    table_id: int,
    row_number: int
):
    row = TableRow(
        table_id=table_id,
        row_number=row_number
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return row


def get_rows(
    db: Session,
    table_id: int
):
    return (
        db.query(TableRow)
        .filter(TableRow.table_id == table_id)
        .order_by(TableRow.row_number)
        .all()
    )


# ==========================================================
# CELL CRUD
# ==========================================================

def create_cell(
    db: Session,
    row_id: int,
    column_id: int,
    cell_value: str,
    rowspan: int = 1,
    colspan: int = 1
):
    cell = TableCell(
        row_id=row_id,
        column_id=column_id,
        cell_value=cell_value,
        rowspan=rowspan,
        colspan=colspan
    )

    db.add(cell)
    db.commit()
    db.refresh(cell)

    return cell


def get_cells(
    db: Session,
    row_id: int
):
    return (
        db.query(TableCell)
        .filter(TableCell.row_id == row_id)
        .all()
    )