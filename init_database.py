from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy import create_engine, DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column, Mapped

load_dotenv()
DB_FILE = os.getenv("DB_FILE")

engine = create_engine(DB_FILE)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()

class TriangleDomain(Base):
    __tablename__ = "triangle"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    x1 : Mapped[float] = mapped_column(Float, comment = "Tọa độ x của đỉnh 1")
    y1 : Mapped[float] = mapped_column(Float, comment = "Tọa độ y của đỉnh 1")
    x2 : Mapped[float] = mapped_column(Float, comment = "Tọa độ x của đỉnh 2")
    y2 : Mapped[float] = mapped_column(Float, comment = "Tọa độ y của đỉnh 2")
    x3 : Mapped[float] = mapped_column(Float, comment = "Tọa độ x của đỉnh 3")
    y3 : Mapped[float] = mapped_column(Float, comment = "Tọa độ y của đỉnh 3")
    by : Mapped[str] = mapped_column(String, comment = "Thực hiện trên web / Gọi api")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("DB & tables created")
