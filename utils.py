import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import base64

def load_css():
    """Load custom CSS for styling"""
    st.markdown("""
    <style>
    /* Flow Ads brand colors */
    :root {
        --flowads-blue: #0098DA;
        --flowads-yellow: #FFBC00;
        --flowads-rose: #FF6B6B;
        --flowads-dark-blue: #006699;
        --flowads-light-gray: #f8f9fa;
    }

    /* Button styling */
    .stButton > button {
        background-color: var(--flowads-yellow) !important;
        color: #333 !important;
        font-weight: bold !important;
        transition: transform 0.2s !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        background-color: var(--flowads-light-gray) !important;
        color: var(--flowads-blue) !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--flowads-blue) !important;
        color: white !important;
    }

    /* Accent elements */
    .accent-text {
        color: var(--flowads-rose) !important;
    }

    /* Cards and containers */
    .card {
        background-color: white !important;
        border-left: 4px solid var(--flowads-rose) !important;
    }
    
    /* Header and typography styling */
    h1, h2, h3 {
        color: var(--flowads-blue);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #e6f2ff;
        border-radius: 4px 4px 0 0;
        padding: 10px 16px;
        color: var(--flowads-blue);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--flowads-blue);
        color: white;
    }
    
    /* Card elements */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Campaign card styling */
    .campaign-card {
        padding: 15px;
        border-left: 4px solid var(--flowads-blue);
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    
    /* Custom metric styling */
    .metric-container {
        background-color: var(--flowads-light-gray);
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: var(--flowads-blue);
    }
    
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables if they don't already exist"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
        
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    
    if "active_campaigns" not in st.session_state:
        st.session_state.active_campaigns = generate_mock_campaigns()
        
    if "drivers" not in st.session_state:
        st.session_state.drivers = generate_mock_drivers()
        
    if "ad_templates" not in st.session_state:
        st.session_state.ad_templates = generate_mock_templates()
        
    if "high_viewership_locations" not in st.session_state:
        st.session_state.high_viewership_locations = generate_high_viewership_locations()
    
    if "notifications" not in st.session_state:
        st.session_state.notifications = generate_mock_notifications()
        
    if "help_tickets" not in st.session_state:
        st.session_state.help_tickets = generate_mock_help_tickets()
        
    if "otp_verified" not in st.session_state:
        st.session_state.otp_verified = False
        
    if "generated_otp" not in st.session_state:
        st.session_state.generated_otp = None
        
    if "payment_methods" not in st.session_state:
        st.session_state.payment_methods = []
        
    if "faqs" not in st.session_state:
        st.session_state.faqs = []
        st.session_state.payment_methods = []

def generate_mock_campaigns():
    """Generate sample campaign data for demonstration"""
    # First try to get campaigns from the database
    try:
        import db
        # Get campaigns from the database
        campaigns_list = db.get_campaigns()
        
        if campaigns_list:
            # Convert database records to expected format
            campaigns = []
            for campaign in campaigns_list:
                # Generate ad_file name based on campaign name and type
                ad_type = campaign["ad_type"]
                file_ext = "jpg" if ad_type == "image" else "mp4"
                ad_file = f"{campaign['name'].lower().replace(' ', '_')}.{file_ext}"
                
                campaigns.append({
                    "id": campaign["id"],
                    "name": campaign["name"],
                    "advertiser": campaign["advertiser"],
                    "status": campaign["status"],
                    "ad_type": campaign["ad_type"],
                    "regions": campaign["regions"],
                    "budget": campaign["budget"],
                    "spent": campaign["spent"],
                    "start_date": str(campaign["start_date"]) if campaign["start_date"] else None,
                    "end_date": str(campaign["end_date"]) if campaign["end_date"] else None,
                    "views": campaign["views"],
                    "impressions": campaign["impressions"],
                    "ad_file": ad_file
                })
            return campaigns
    except Exception as e:
        st.warning(f"Unable to get campaigns from database: {e}. Using mock data.")
    
    # Fall back to mock data if database access fails
    campaigns = [
        {
            "id": 1,
            "name": "Summer Sale Promotion",
            "advertiser": "CityMall",
            "status": "Active",
            "start_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d"),
            "budget": 24000,
            "spent": 10450,
            "impressions": 18345,
            "views": 12567,
            "regions": ["Vijay Nagar", "Palasia", "MG Road"],
            "ad_type": "video",
            "ad_file": "citymall_sale.mp4"
        },
        {
            "id": 2,
            "name": "New Restaurant Launch",
            "advertiser": "Spice Garden",
            "status": "Active",
            "start_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=25)).strftime("%Y-%m-%d"),
            "budget": 18000,
            "spent": 4320,
            "impressions": 9876,
            "views": 7543,
            "regions": ["Palasia", "AB Road", "Sapna Sangeeta"],
            "ad_type": "image",
            "ad_file": "spice_garden.jpg"
        },
        {
            "id": 3,
            "name": "College Admission Campaign",
            "advertiser": "Indore University",
            "status": "Scheduled",
            "start_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=35)).strftime("%Y-%m-%d"),
            "budget": 30000,
            "spent": 0,
            "impressions": 0,
            "views": 0,
            "regions": ["Vijay Nagar", "Bhawarkuan", "Geeta Bhawan"],
            "ad_type": "video",
            "ad_file": "indore_university.mp4"
        },
        {
            "id": 4,
            "name": "Premium Property Showcase",
            "advertiser": "Indore Realtors",
            "status": "Completed",
            "start_date": (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "budget": 250000,
            "spent": 250000,
            "impressions": 115432,
            "views": 89654,
            "regions": ["Vijay Nagar", "Palasia", "MG Road", "AB Road", "Rajwada"],
            "ad_type": "video",
            "ad_file": "premium_property.mp4"
        }
    ]
    return campaigns

def generate_mock_drivers():
    """Generate sample driver data for demonstration"""
    # Try to get drivers from the database
    try:
        import db
        # Get drivers from the database
        db_drivers = db.get_drivers()
        
        if db_drivers:
            # Convert database records to expected format
            drivers = []
            for driver in db_drivers:
                # Create driver object with database data
                hourly_rate = 32  # Rs. 32 per hour
                hours_active = driver.get("hours_active", 0)
                base_earnings = hours_active * hourly_rate
                kms_today = driver.get("kms_today", 0)
                incentives = 0
                if kms_today > 100:
                    incentives = round(random.uniform(0, 500), 2)
                total_earnings = base_earnings + incentives
                
                # Format location data
                location_area = driver.get("current_location_area", "Indore")
                location_lat = driver.get("current_location_lat", 22.7196)
                location_lon = driver.get("current_location_lon", 75.8577)
                
                # Add calculated data
                drivers.append({
                    "id": driver["id"],
                    "name": driver["name"],
                    "phone": driver.get("phone", ""),
                    "city": "Indore",
                    "vehicle_model": driver.get("vehicle_model", "Swift Dzire"),
                    "vehicle_number": driver.get("vehicle_number", ""),
                    "status": driver.get("status", "Inactive"),
                    "current_location": {
                        "area": location_area,
                        "lat": float(location_lat),
                        "lon": float(location_lon)
                    },
                    "kms_today": kms_today,
                    "hours_active": hours_active,
                    "rating": 4.5,  # Not stored in DB, use default
                    "earnings": {
                        "today": total_earnings,
                        "base": base_earnings,
                        "incentives": incentives
                    },
                    "documents": {
                        "license": {"status": "Verified", "expiry": (datetime.now() + timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d")},
                        "insurance": {"status": "Verified", "expiry": (datetime.now() + timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d")},
                        "vehicle_registration": {"status": "Verified", "expiry": (datetime.now() + timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d")}
                    },
                    "current_ad_displaying": driver.get("current_ad_displaying", 1)
                })
            return drivers
    except Exception as e:
        st.warning(f"Unable to get drivers from database: {e}. Using mock data.")
    
    # Fall back to mock data if database access fails
    cities = ["Indore"]
    areas = ["Vijay Nagar", "Palasia", "MG Road", "AB Road", "Rajwada", "Sapna Sangeeta", "Bhawarkuan", "Geeta Bhawan", "LIG", "Navlakha"]
    vehicle_models = ["Swift Dzire", "Hyundai Xcent", "Tata Indigo", "Toyota Etios", "Maruti Suzuki WagonR"]
    
    drivers = []
    for i in range(1, 31):
        active_status = random.choice(["Active", "Inactive", "On Break"])
        kms_today = random.randint(40, 150) if active_status != "Inactive" else 0
        hours_active = random.randint(2, 10) if active_status != "Inactive" else 0
        
        # Random location coordinates around Indore
        lat = 22.7196 + (random.random() - 0.5) * 0.1
        lon = 75.8577 + (random.random() - 0.5) * 0.1
        
        # Calculate earnings based on hours
        hourly_rate = 32  # Rs. 32 per hour
        base_earnings = hours_active * hourly_rate
        incentives = round(random.uniform(0, 500), 2) if kms_today > 100 else 0
        total_earnings = base_earnings + incentives
        
        drivers.append({
            "id": i,
            "name": f"Driver {i}",
            "phone": f"98765{43210 + i}",
            "city": cities[0],
            "vehicle_model": random.choice(vehicle_models),
            "vehicle_number": f"MP-{random.randint(1,20)}-{random.choice('ABCDEFGH')}-{random.randint(1000,9999)}",
            "status": active_status,
            "current_location": {
                "area": random.choice(areas),
                "lat": lat,
                "lon": lon
            },
            "kms_today": kms_today,
            "hours_active": hours_active,
            "rating": round(random.uniform(3.0, 5.0), 1),
            "earnings": {
                "today": total_earnings,
                "base": base_earnings,
                "incentives": incentives
            },
            "documents": {
                "license": {"status": "Verified", "expiry": (datetime.now() + timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d")},
                "insurance": {"status": "Verified", "expiry": (datetime.now() + timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d")},
                "vehicle_registration": {"status": "Verified", "expiry": (datetime.now() + timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d")}
            },
            "current_ad_displaying": random.randint(1, 4)
        })
    return drivers

def generate_mock_templates():
    """Generate sample ad templates for the platform"""
    templates = [
        {
            "id": 1,
            "name": "Summer Sale",
            "category": "Retail",
            "description": "Bright, colorful template for summer promotions and sales",
            "thumbnail": "https://images.unsplash.com/photo-1607083206968-13611e3d76db",
            "color_scheme": "Blue, Yellow",
            "orientation": "Landscape"
        },
        {
            "id": 2,
            "name": "Restaurant Promotion",
            "category": "Food & Beverage",
            "description": "Elegant template highlighting food imagery and special offers",
            "thumbnail": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
            "color_scheme": "Red, White",
            "orientation": "Landscape"
        },
        {
            "id": 3,
            "name": "Corporate Announcement",
            "category": "Business",
            "description": "Professional template for business announcements and events",
            "thumbnail": "https://images.unsplash.com/photo-1573164574572-cb89e39749b4",
            "color_scheme": "Blue, Grey",
            "orientation": "Landscape"
        },
        {
            "id": 4,
            "name": "Property Showcase",
            "category": "Real Estate",
            "description": "Showcase properties with this premium template design",
            "thumbnail": "https://images.unsplash.com/photo-1560518883-ce09059eeffa",
            "color_scheme": "Green, White",
            "orientation": "Landscape"
        },
        {
            "id": 5,
            "name": "Educational Institute",
            "category": "Education",
            "description": "Perfect for schools, colleges and educational promotions",
            "thumbnail": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1",
            "color_scheme": "Blue, Yellow",
            "orientation": "Landscape"
        },
        {
            "id": 6,
            "name": "Fashion Sale",
            "category": "Fashion",
            "description": "Stylish template for fashion brands and clothing stores",
            "thumbnail": "https://images.unsplash.com/photo-1445205170230-053b83016050",
            "color_scheme": "Black, Pink",
            "orientation": "Landscape"
        }
    ]
    return templates

def generate_high_viewership_locations():
    """Generate sample high viewership locations data"""
    # Try to get locations from the database
    try:
        import db
        # Get locations from the database
        db_locations = db.get_high_viewership_locations()
        
        if db_locations:
            # Convert database records to expected format
            locations = []
            for loc in db_locations:
                locations.append({
                    "location": loc["location_name"],
                    "views": loc["views"],
                    "campaigns": loc.get("importance", 3),
                    "peak_time": "17:00-19:00",  # Not stored in DB, use default
                    "lat": float(loc["lat"]),
                    "lon": float(loc["lon"])
                })
            return locations
    except Exception as e:
        st.warning(f"Unable to get locations from database: {e}. Using mock data.")
    
    # Fall back to mock data if database access fails
    locations = [
        {"location": "Vijay Nagar", "views": 15240, "campaigns": 5, "peak_time": "17:00-19:00", "lat": 22.7533, "lon": 75.8937},
        {"location": "Palasia", "views": 12750, "campaigns": 4, "peak_time": "18:00-20:00", "lat": 22.7244, "lon": 75.8839},
        {"location": "MG Road", "views": 10900, "campaigns": 3, "peak_time": "10:00-12:00", "lat": 22.7196, "lon": 75.8577},
        {"location": "Rajwada", "views": 9850, "campaigns": 4, "peak_time": "11:00-13:00", "lat": 22.7185, "lon": 75.8545},
        {"location": "AB Road", "views": 8970, "campaigns": 3, "peak_time": "09:00-11:00", "lat": 22.7089, "lon": 75.8800}
    ]
    return locations

def generate_mock_notifications():
    """Generate sample notifications data"""
    notifications = [
        {
            "id": 1,
            "user_id": "advertiser_1",
            "title": "Campaign Performance Alert",
            "message": "Your 'Summer Sale' campaign has reached 10,000 views!",
            "timestamp": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "read": False,
            "category": "campaign"
        },
        {
            "id": 2,
            "user_id": "advertiser_1",
            "title": "High Traffic Location Alert",
            "message": "Vijay Nagar is currently showing high engagement. Consider boosting your ad display in this area.",
            "timestamp": (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "read": True,
            "category": "insight"
        },
        {
            "id": 3,
            "user_id": "driver_1",
            "title": "Earnings Update",
            "message": "You've earned ₹256 today so far. Great job!",
            "timestamp": (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
            "read": False,
            "category": "earnings"
        },
        {
            "id": 4,
            "user_id": "driver_1",
            "title": "Document Expiry Reminder",
            "message": "Your vehicle insurance will expire in 30 days. Please renew it soon.",
            "timestamp": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "read": True,
            "category": "document"
        },
        {
            "id": 5,
            "user_id": "admin_1",
            "title": "New Driver Registration",
            "message": "A new driver has registered and is awaiting document verification.",
            "timestamp": (datetime.now() - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S"),
            "read": False,
            "category": "system"
        }
    ]
    return notifications

def generate_mock_help_tickets():
    """Generate sample help desk tickets"""
    statuses = ["Open", "In Progress", "Resolved", "Closed"]
    priorities = ["Low", "Medium", "High", "Urgent"]
    categories = ["Technical Issue", "Billing Query", "Ad Display Problem", "Driver Complaint", "General Inquiry"]
    
    tickets = []
    for i in range(1, 11):
        created_date = datetime.now() - timedelta(days=random.randint(0, 30))
        
        # For closed/resolved tickets, add resolution date
        status = random.choice(statuses)
        resolved_date = created_date + timedelta(days=random.randint(1, 5)) if status in ["Resolved", "Closed"] else None
        
        tickets.append({
            "ticket_id": i,
            "subject": f"Ticket #{i} - {random.choice(categories)}",
            "description": f"This is a sample ticket description for ticket #{i}",
            "user_id": f"user_{random.randint(1, 10)}",
            "user_name": f"User {random.randint(1, 10)}",
            "user_type": random.choice(["Advertiser", "Driver", "Admin"]),
            "status": status,
            "priority": random.choice(priorities),
            "category": random.choice(categories),
            "created_at": created_date.strftime("%Y-%m-%d %H:%M:%S"),
            "resolved_at": resolved_date.strftime("%Y-%m-%d %H:%M:%S") if resolved_date else None,
            "conversation": [
                {
                    "sender": f"User {random.randint(1, 10)}",
                    "sender_type": "User",
                    "message": f"Initial ticket message for ticket #{i}",
                    "timestamp": created_date.strftime("%Y-%m-%d %H:%M")
                }
            ]
        })
        
        # Add some responses for older tickets
        if random.random() > 0.5 and i < 8:
            support_response_date = created_date + timedelta(hours=random.randint(1, 24))
            tickets[i-1]["conversation"].append({
                "sender": "Support Agent",
                "sender_type": "Support",
                "message": "Thank you for contacting Flow Ads Cab support. We're looking into your issue and will get back to you shortly.",
                "timestamp": support_response_date.strftime("%Y-%m-%d %H:%M")
            })
            
            # Add user reply in some cases
            if random.random() > 0.6:
                user_reply_date = support_response_date + timedelta(hours=random.randint(1, 12))
                tickets[i-1]["conversation"].append({
                    "sender": f"User {random.randint(1, 10)}",
                    "sender_type": "User",
                    "message": "Thank you for your response. I'm looking forward to a resolution.",
                    "timestamp": user_reply_date.strftime("%Y-%m-%d %H:%M")
                })
    
    return tickets