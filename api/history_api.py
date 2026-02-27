from flask import Blueprint, request
from api.helper import success
import init_database
from datetime import datetime


history_bp=Blueprint(
    "history",
    __name__,
    url_prefix="/api"
)



@history_bp.route("/history", methods=["POST", "GET"])
def history():

    edge = request.args.get("edge")
    angle = request.args.get("angle")
    by = request.args.get("by")

    start = request.args.get("start")
    end = request.args.get("end")


    with init_database.get_session() as s:

        query = s.query(
            init_database.TriangleDomain
        )


        # ===== FILTER =====

        if edge:
            query = query.filter(init_database.TriangleDomain.edge_type == edge)

        if angle:
            query = query.filter(init_database.TriangleDomain.angle_type == angle)

        if by:
            query = query.filter(init_database.TriangleDomain.by == by)


        # ===== DATE FILTER =====
        if start:
            start_dt = datetime.fromisoformat(start)
            query = query.filter(init_database.TriangleDomain.created_at >= start_dt)

        if end:
            end_dt = datetime.fromisoformat(end)
            query = query.filter(init_database.TriangleDomain.created_at <= end_dt)

        rows = query.order_by(init_database.TriangleDomain.created_at.desc()).limit(100).all()


        data = [
            {
                "id": r.id,
                "x1": round(r.x1, 6),
                "y1": round(r.y1, 6),
                "x2": round(r.x2, 6),
                "y2": round(r.y2, 6),
                "x3": round(r.x3, 6),
                "y3": round(r.y3, 6),
                "edge_type": r.edge_type,
                "angle_type": r.angle_type,
                "by": r.by,
                "created_at": r.created_at.isoformat()
            }
            for r in rows
        ]
        return success(data)