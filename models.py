from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Domain(Base):
    """A metadata asset."""

    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String(length=250), unique=False)
    root_domain_name = Column(String, unique=False, default="usfs")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    asset = relationship("Asset", back_populates="domain")

    def __str__(self):
        return f"{self.name}"


class Asset(Base):
    """A metadata asset."""

    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    domain_id = Column(Integer(), ForeignKey("domains.id"))
    domain = relationship("Domain", back_populates="asset")
    metadata_url = Column(String(1000), unique=True)

    def __str__(self):
        return f"{self.title}"
