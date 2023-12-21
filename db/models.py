from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    code = Column(String(3), unique=True)


class Rate(Base):
    __tablename__ = 'rates'
    __table_args__ = (UniqueConstraint('currency_base_id', 'currency_target_id', 'date'),)

    id = Column(Integer, primary_key=True)
    currency_base_id = Column(Integer, ForeignKey('currencies.id'))
    currency_target_id = Column(Integer, ForeignKey('currencies.id'))
    date = Column(Date, nullable=False)
    rate = Column(Float, nullable=False)

    currency_base_rel = relationship(
        'Currency',
        primaryjoin=currency_base_id == Currency.id,
        innerjoin=True,
        uselist=False,
        viewonly=True,
    )
    currency_base = association_proxy('currency_base_rel', 'code')

    currency_target_rel = relationship(
        'Currency',
        primaryjoin=currency_target_id == Currency.id,
        innerjoin=True,
        uselist=False,
        viewonly=True,
    )
    currency_target = association_proxy('currency_target_rel', 'code')
