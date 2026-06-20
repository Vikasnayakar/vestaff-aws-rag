from sqlalchemy.orm import Session
from sqlalchemy import func
from backend import models

def get_dashboard_metrics(db: Session) -> dict:
    """Calculates all key performance indicators for the dashboard."""
    
    # 1. Average Latency
    avg_latency = db.query(func.avg(models.QueryLog.latency_seconds)).scalar() or 0.0
    
    # 2. Unanswered/Fallback queries
    unanswered_count = db.query(models.QueryLog).filter(models.QueryLog.no_answer_found == True).count()
    
    # 3. Top 5 Most Frequent Queries
    frequent_queries = db.query(
        models.QueryLog.query_text, 
        func.count(models.QueryLog.query_text).label('qty')
    ).group_by(models.QueryLog.query_text).order_by(func.count(models.QueryLog.query_text).desc()).limit(5).all()
    
    top_queries = [{"query": q[0], "count": q[1]} for q in frequent_queries]
    
    return {
        "average_latency_seconds": round(avg_latency, 3),
        "unanswered_queries_count": unanswered_count,
        "top_queries": top_queries
    }