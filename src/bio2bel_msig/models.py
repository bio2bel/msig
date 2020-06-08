# -*- coding: utf-8 -*-

"""Bio2BEL MSIG database models."""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from bio2bel.compath import CompathPathwayMixin, CompathProteinMixin

Base = declarative_base()

TABLE_PREFIX = 'msig'
PATHWAY_TABLE_NAME = f'{TABLE_PREFIX}_pathway'
PROTEIN_TABLE_NAME = f'{TABLE_PREFIX}_protein'
PROTEIN_PATHWAY_TABLE = f'{TABLE_PREFIX}_protein_pathway'

protein_pathway = Table(
    PROTEIN_PATHWAY_TABLE,
    Base.metadata,
    Column('protein_id', Integer, ForeignKey(f'{PROTEIN_TABLE_NAME}.id'), primary_key=True),
    Column('pathway_id', Integer, ForeignKey(f'{PATHWAY_TABLE_NAME}.id'), primary_key=True)
)


class Pathway(Base, CompathPathwayMixin):
    """Pathway Table"""

    __tablename__ = PATHWAY_TABLE_NAME

    id = Column(Integer, primary_key=True)

    identifier = Column(String(255), unique=True, index=True, nullable=False, doc='msig id')
    name = Column(String(255), unique=True, index=True, nullable=False, doc='pathway name')

    proteins = relationship(
        'Protein',
        secondary=protein_pathway,
        backref='pathways',
    )

    @property
    def url(self) -> str:
        return f'http://software.broadinstitute.org/gsea/msigdb/geneset_page.jsp?geneSetName={self.name}'


class Protein(Base, CompathProteinMixin):
    """Genes Table."""

    __tablename__ = PROTEIN_TABLE_NAME

    id = Column(Integer, primary_key=True)
    hgnc_id = Column(String(255), doc='hgnc id of the protein')
    hgnc_symbol = Column(String(255), unique=True, index=True, nullable=False, doc='hgnc symbol of the protein')

    def __repr__(self):
        return self.hgnc_symbol
