from sqlalchemy import Column, Integer, Text, BigInteger, Boolean, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship, backref, DeclarativeBase


class Base(DeclarativeBase):
    id = Column(Integer(), primary_key=True)


class User(Base):
    __tablename__ = 'user'

    user = Column(BigInteger(), unique=True)
    note = Column(Text(), )

    def __repr__(self):
        return f'{self.user}'


class BlockList(Base):
    __tablename__ = 'block_list'

    user = relationship('User', backref=backref('block_list', cascade='all, delete-orphan', ))
    user_id = Column(Integer, ForeignKey('user.id'))
    is_block = Column(Boolean(), )
    reason = Column(Text(), )

    def __repr__(self):
        return f'{self.user} - {self.is_block} '


class Subscriber(Base):
    __tablename__ = 'subscriber'

    user = relationship('User', backref=backref('sub', cascade='all, delete-orphan', ))
    user_id = Column(Integer, ForeignKey('user.id'))
    lvl_sub = Column(String(20), )
    buy_at = Column(DateTime(timezone=False), server_default=func.now())

    def __repr__(self):
        return f'{self.user} - {self.lvl_sub} '
