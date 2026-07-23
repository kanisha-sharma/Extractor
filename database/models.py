from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database.db import Base


# =====================================================
# Document
# =====================================================

class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    filepath = Column(Text, nullable=False)

    total_pages = Column(Integer)

    status = Column(String, default="Uploaded")

    uploaded_at = Column(DateTime(timezone=True),
                         server_default=func.now())

    sections = relationship(
        "Section",
        back_populates="document",
        cascade="all, delete"
    )


# =====================================================
# Section
# =====================================================

class Section(Base):

    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    section_name = Column(String)

    start_page = Column(Integer)

    end_page = Column(Integer)

    document = relationship(
        "Document",
        back_populates="sections"
    )

    tables = relationship(
        "ExtractedTable",
        back_populates="section",
        cascade="all, delete"
    )


# =====================================================
# Extracted Table
# =====================================================

class ExtractedTable(Base):

    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)

    section_id = Column(
        Integer,
        ForeignKey("sections.id")
    )

    table_number = Column(String)

    table_title = Column(Text)

    page_number = Column(Integer)

    json_path = Column(Text)

    section = relationship(
        "Section",
        back_populates="tables"
    )

    columns = relationship(
        "TableColumn",
        back_populates="table",
        cascade="all, delete"
    )

    rows = relationship(
        "TableRow",
        back_populates="table",
        cascade="all, delete"
    )


# =====================================================
# Table Column
# =====================================================

class TableColumn(Base):

    __tablename__ = "table_columns"

    id = Column(Integer, primary_key=True)

    table_id = Column(
        Integer,
        ForeignKey("tables.id")
    )

    parent_column_id = Column(
        Integer,
        ForeignKey("table_columns.id"),
        nullable=True
    )

    column_name = Column(Text)

    column_level = Column(Integer)

    column_order = Column(Integer)

    rowspan = Column(Integer, default=1)

    colspan = Column(Integer, default=1)

    table = relationship(
        "ExtractedTable",
        back_populates="columns"
    )

    parent = relationship(
        "TableColumn",
        remote_side=[id]
    )

    cells = relationship(
        "TableCell",
        back_populates="column"
    )


# =====================================================
# Table Row
# =====================================================

class TableRow(Base):

    __tablename__ = "table_rows"

    id = Column(Integer, primary_key=True)

    table_id = Column(
        Integer,
        ForeignKey("tables.id")
    )

    row_index = Column(Integer)

    table = relationship(
        "ExtractedTable",
        back_populates="rows"
    )

    cells = relationship(
        "TableCell",
        back_populates="row",
        cascade="all, delete"
    )


# =====================================================
# Table Cell
# =====================================================

class TableCell(Base):

    __tablename__ = "table_cells"

    id = Column(Integer, primary_key=True)

    row_id = Column(
        Integer,
        ForeignKey("table_rows.id")
    )

    column_id = Column(
        Integer,
        ForeignKey("table_columns.id")
    )

    value = Column(Text)

    rowspan = Column(Integer, default=1)

    colspan = Column(Integer, default=1)

    confidence = Column(Integer)

    is_header = Column(Boolean, default=False)

    row = relationship(
        "TableRow",
        back_populates="cells"
    )

    column = relationship(
        "TableColumn",
        back_populates="cells"
    )