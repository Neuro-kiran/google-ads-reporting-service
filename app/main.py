"""
Google Ads Reporting Service - FastAPI Application
Production-ready microservice for Google Ads API integration
"""

import os
import logging
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# ========== Configuration ==========
class Settings(BaseModel):
    developer_token: str
    client_id: str
    client_secret: str
    refresh_token: str
    login_customer_id: str | None = None

def load_settings() -> Settings:
    try:
        return Settings(
            developer_token=os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
            client_id=os.environ["GOOGLE_ADS_CLIENT_ID"],
            client_secret=os.environ["GOOGLE_ADS_CLIENT_SECRET"],
            refresh_token=os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
            login_customer_id=os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
        )
    except KeyError as e:
        raise RuntimeError(f"Missing required env var: {e.args[0]}")

settings = load_settings()

# ========== Logging ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google_ads_service")

# ========== Schemas ==========
class CampaignStats(BaseModel):
    campaign_id: str
    campaign_name: str
    impressions: int
    clicks: int
    cost_micros: int

class CampaignStatsResponse(BaseModel):
    customer_id: str
    rows: List[CampaignStats]

# ========== Client Factory ==========
def get_google_ads_client() -> GoogleAdsClient:
    config = {
        "developer_token": settings.developer_token,
        "client_id": settings.client_id,
        "client_secret": settings.client_secret,
        "refresh_token": settings.refresh_token,
        "login_customer_id": settings.login_customer_id,
        "use_proto_plus": True,
    }
    return GoogleAdsClient.load_from_dict({"google_ads": config})

# ========== FastAPI App ==========
app = FastAPI(
    title="Google Ads Reporting Service",
    version="1.0.0",
    description="Production-ready Google Ads API microservice with FastAPI",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/healthz")
def healthz():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/campaign-stats", response_model=CampaignStatsResponse)
def get_campaign_stats(customer_id: str):
    """
    Fetch campaign stats for last 7 days
    
    Args:
        customer_id: Google Ads customer ID
    
    Returns:
        Campaign statistics with impressions, clicks, and cost
    """
    client = get_google_ads_client()
    ga_service = client.get_service("GoogleAdsService")
    
    query = """
        SELECT
          campaign.id,
          campaign.name,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros
        FROM campaign
        WHERE campaign.status = 'ENABLED'
          AND segments.date DURING LAST_7_DAYS
        ORDER BY metrics.impressions DESC
    """
    
    rows: List[CampaignStats] = []
    
    try:
        logger.info(f"Fetching stats for customer_id={customer_id}")
        stream = ga_service.search_stream(customer_id=customer_id, query=query)
        
        for batch in stream:
            for r in batch.results:
                rows.append(
                    CampaignStats(
                        campaign_id=str(r.campaign.id),
                        campaign_name=r.campaign.name,
                        impressions=r.metrics.impressions,
                        clicks=r.metrics.clicks,
                        cost_micros=r.metrics.cost_micros,
                    )
                )
    except GoogleAdsException as ex:
        logger.error(f"GoogleAds Error: {ex.failure}")
        raise HTTPException(
            status_code=400,
            detail={"message": ex.error.code().name, "request_id": ex.request_id}
        )
    
    return CampaignStatsResponse(customer_id=customer_id, rows=rows)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
