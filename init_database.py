from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy import create_engine, DateTime, Float, Integer, String, Index
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column, Mapped
from models.triangle import TriangleWithCoords

load_dotenv()
DB_FILE = os.getenv("DB_FILE")

engine = create_engine(DB_FILE, pool_pre_ping=True, pool_recycle=300)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()

class TriangleDomain(Base):
    __tablename__ = "triangle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    x1: Mapped[float] = mapped_column(Float)
    y1: Mapped[float] = mapped_column(Float)

    x2: Mapped[float] = mapped_column(Float)
    y2: Mapped[float] = mapped_column(Float)

    x3: Mapped[float] = mapped_column(Float)
    y3: Mapped[float] = mapped_column(Float)

    by: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # ✔ 2 cột riêng
    edge_type: Mapped[str] = mapped_column(String)

    angle_type: Mapped[str] = mapped_column(String)


    def __init__(self, x1, y1, x2, y2, x3, y3, by):

        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

        self.x3 = x3
        self.y3 = y3

        self.by = by


        tri = TriangleWithCoords(
            x1, y1,
            x2, y2,
            x3, y3
        )

        # ✔ Tính loại tam giác
        edge = tri.triangle_edges.edge_type()
        angle = tri.triangle_edges.angle_type()

        if edge is None:
            self.edge_type = "Không tồn tại"
            self.angle_type = "Không tồn tại"
        else:
            self.edge_type = edge
            self.angle_type = angle


    __table_args__ = (
        # lọc theo cạnh
        Index(
            "idx_edge",
            "edge_type"
        ),

        # lọc theo góc
        Index(
            "idx_angle",
            "angle_type"
        ),

        # lọc theo ngày
        Index(
            "idx_date",
            "created_at"
        ),

        # lọc theo nguồn
        Index(
            "idx_source",
            "by"
        ),
    )


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("DB & tables created")
