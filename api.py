from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from x_analyzer import XAnalyzer
import pandas as pd
from datetime import datetime
import os

app = FastAPI(title="X-EA Awards API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize XAnalyzer
analyzer = XAnalyzer()

# Pydantic models for request/response
class AccountBase(BaseModel):
    username: str
    name: str
    location: str
    country: str
    followers_count: int
    annual_posts: int
    thread_count: int
    category: str
    verified: bool
    engagement_score: float
    intensity_score: float
    ai_rank: float

class SearchResponse(BaseModel):
    accounts: List[AccountBase]
    total_count: int

class DashboardStats(BaseModel):
    total_influencers: int
    average_engagement: float
    active_countries: int
    category_distribution: dict
    engagement_trends: dict

@app.get("/")
async def root():
    return {"message": "X-EA Awards API is running"}

@app.get("/search", response_model=SearchResponse)
async def search_accounts(
    topic: str,
    country: Optional[str] = None,
    category: Optional[str] = None,
    min_followers: Optional[int] = None,
    min_engagement: Optional[float] = None,
    sort_by: str = "ai_rank",
    page: int = 1,
    limit: int = 10
):
    try:
        # Get accounts from analyzer
        df = analyzer.analyze_accounts(topic)
        
        if df.empty:
            return SearchResponse(accounts=[], total_count=0)
        
        # Apply filters
        if country and country != "all":
            df = df[df["country"].str.lower() == country.lower()]
        if category and category != "all":
            df = df[df["category"].str.lower() == category.lower()]
        if min_followers:
            df = df[df["followers_count"] >= min_followers]
        if min_engagement:
            df = df[df["engagement_score"] >= min_engagement]
            
        # Sort results
        if sort_by in df.columns:
            df = df.sort_values(sort_by, ascending=False)
            
        # Pagination
        total_count = len(df)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        df_page = df.iloc[start_idx:end_idx]
        
        # Convert to response model
        accounts = []
        for _, row in df_page.iterrows():
            account = AccountBase(
                username=row["username"],
                name=row["name"],
                location=row["location"],
                country=row["country"],
                followers_count=row["followers_count"],
                annual_posts=row["annual_posts"],
                thread_count=row["thread_count"],
                category=row["category"],
                verified=row["verified"],
                engagement_score=float(row["engagement_score"]),
                intensity_score=float(row["intensity_score"]),
                ai_rank=float(row["ai_rank"])
            )
            accounts.append(account)
            
        return SearchResponse(accounts=accounts, total_count=total_count)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leaderboard/{category}")
async def get_leaderboard(
    category: str = "all",
    sort_by: str = "ai_rank",
    limit: int = 10
):
    try:
        # Get all accounts from saved results or recent searches
        results_dir = "results"
        all_accounts = []
        
        # Combine results from recent files
        for file in os.listdir(results_dir):
            if file.endswith(".csv"):
                df = pd.read_csv(os.path.join(results_dir, file))
                all_accounts.append(df)
                
        if not all_accounts:
            return []
            
        # Combine all results and remove duplicates
        df = pd.concat(all_accounts).drop_duplicates(subset=["username"])
        
        # Apply category filter
        if category != "all":
            df = df[df["category"].str.lower() == category.lower()]
            
        # Sort and limit results
        df = df.sort_values(sort_by, ascending=False).head(limit)
        
        # Convert to list of dicts for response
        return df.to_dict("records")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    try:
        # Get all accounts from saved results
        results_dir = "results"
        all_accounts = []
        
        for file in os.listdir(results_dir):
            if file.endswith(".csv"):
                df = pd.read_csv(os.path.join(results_dir, file))
                all_accounts.append(df)
                
        if not all_accounts:
            return DashboardStats(
                total_influencers=0,
                average_engagement=0.0,
                active_countries=0,
                category_distribution={},
                engagement_trends={}
            )
            
        # Combine all results and remove duplicates
        df = pd.concat(all_accounts).drop_duplicates(subset=["username"])
        
        # Calculate statistics
        total_influencers = len(df)
        average_engagement = float(df["engagement_score"].mean())
        active_countries = len(df["country"].unique())
        
        # Category distribution
        category_distribution = df["category"].value_counts().to_dict()
        
        # Engagement trends (last 6 months)
        engagement_trends = {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "data": [4.2, 4.5, 4.8, 4.6, 4.9, 5.1]  # Sample data
        }
        
        return DashboardStats(
            total_influencers=total_influencers,
            average_engagement=average_engagement,
            active_countries=active_countries,
            category_distribution=category_distribution,
            engagement_trends=engagement_trends
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/countries")
async def get_countries():
    """Get list of supported East African countries"""
    return list(analyzer.east_african_locations.keys())

@app.get("/categories")
async def get_categories():
    """Get list of influencer categories"""
    return list(analyzer.categories.keys()) 