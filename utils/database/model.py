from sqlalchemy import Column, Integer, Text, BigInteger, Boolean, ForeignKey
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
