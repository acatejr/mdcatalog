from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text, UniqueConstraint

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Domain(Base):
    """A metadata asset."""

    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    description = Column(String(length=250), unique=False)
    root_domain_name = Column(String, unique=False, default="usfs")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    asset = relationship("Asset", back_populates="domain")

    def __str__(self):
        return f"{self.name}"


class AssetKeyword(Base):
    __tablename__ = "asset_keyword"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    keyword_id = Column(Integer, ForeignKey("keywords.id"))


class Asset(Base):
    """A metadata asset."""

    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    domain_id = Column(Integer(), ForeignKey("domains.id"))
    domain = relationship("Domain", back_populates="assets")
    metadata_url = Column(String(1000), unique=True)
    keywords = relationship("keywords", secondary=AssetKeyword, backref="assets") # back_populates="asset", cascade="all, delete")

    def __str__(self):
        return f"{self.title}"


class Keyword(Base):
    """Metadata asset keywords"""

    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String(250))
    # asset_id = Column(Integer(), ForeignKey("assets.id"))
    assets = relationship("assets", secondary=AssetKeyword, backref="keywords") # back_populates="keywords")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
