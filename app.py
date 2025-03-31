import streamlit as st
import pandas as pd
from datetime import datetime
import random
from utils import load_css, initialize_session_state
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Flow Ads Cab - Taxi Advertising Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS and initialize session state
load_css()
initialize_session_state()

# Main page header
def display_home():
    # Create a compact header for Flow Ads Cab
    st.markdown("""
    <div style='background: linear-gradient(135deg, #000046, #1CB5E0); padding:20px; border-radius:8px; margin-bottom:15px; text-align:center;'>
        <h1 style='color:#FFFFFF; margin:0; font-size:2em; font-weight:700;'>FLOW ADS CAB</h1>
        <p style='color:#E0E7FF; font-size:1em; margin:5px 0;'>REVOLUTIONARY TAXI LED ADVERTISING</p>
        <div style='display:flex; justify-content:center; gap:15px; margin-top:15px; font-size:0.9em;'>
            <span style='color:#FFFFFF;'>DYNAMIC</span>
            <span style='color:#FFFFFF;'>•</span>
            <span style='color:#FFFFFF;'>SMART</span>
            <span style='color:#FFFFFF;'>•</span>
            <span style='color:#FFFFFF;'>IMPACTFUL</span>
        </div>
    </div>
    <div style='display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:15px;'>
        <div style='background:linear-gradient(135deg, #000080, #0a4275); padding:15px; border-radius:8px; text-align:center; box-shadow: 0 2px 8px rgba(0,0,0,0.15);'>
            <h3 style='color:#FFFFFF; margin:0; font-size:1.5em; font-weight:700;'>100+ <span style='color:#4CAF50; font-size:0.7em;'>↑ 5</span></h3>
            <p style='color:#E0E7FF; margin:5px 0; font-size:1em; font-weight:600;'>ACTIVE ADS</p>
        </div>
        <div style='background:linear-gradient(135deg, #556B2F, #8FBC8F); padding:15px; border-radius:8px; text-align:center; box-shadow: 0 2px 8px rgba(0,0,0,0.15);'>
            <h3 style='color:#FFFFFF; margin:0; font-size:1.5em; font-weight:700;'>10000K <span style='color:#4CAF50; font-size:0.7em;'>↑ 15%</span></h3>
            <p style='color:#E0E7FF; margin:5px 0; font-size:1em; font-weight:600;'>VIEW PER DAY</p>
        </div>
        <div style='background:linear-gradient(135deg, #FFA500, #FFD700); padding:15px; border-radius:8px; text-align:center; box-shadow: 0 2px 8px rgba(0,0,0,0.15);'>
            <h3 style='color:#000000; margin:0; font-size:1.5em; font-weight:700;'>500+ <span style='color:#4CAF50; font-size:0.7em;'>↑ 8%</span></h3>
            <p style='color:#000000; margin:5px 0; font-size:1em; font-weight:600;'>ACTIVE CUSTOMER</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Showcase merged banner with blue theme
    st.markdown("""
    <div style='text-align:center; margin:30px 0; background: linear-gradient(135deg, #1e3c72, #2a5298); padding:25px; border-radius:15px;'>
        <img src="WhatsApp Image 2025-03-17 at 19.27.17 (1).jpeg" style='width: 200px; border-radius: 8px; margin-bottom: 12px;'>
        <h2 style='color:#ffffff; font-size:2em; margin-bottom:12px; font-weight:700;'>DYNAMIC CITY-WIDE COVERAGE & REAL-TIME IMPACT</h2>
        <p style='color:#e0e7ff; font-size:1.1em; margin-bottom:15px;'>Turn city traffic into your marketing advantage with real-time campaign tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # How It Works section
    st.markdown("""
    <div style='text-align:center; margin:40px 0;'>
        <h2 style='color:#333; font-size:2.2em; margin-bottom:30px;'>How It Works</h2>
    </div>
    """, unsafe_allow_html=True)

    # Create three columns for the process
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='background:linear-gradient(135deg, #0d47a1, #000000); padding:20px; border-radius:10px; text-align:center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
            <h3 style='color:#ffffff;'>1. Mount Display</h3>
            <p style='color:#ffffff;'>Smart LED displays mounted on taxi tops for maximum visibility</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:linear-gradient(135deg, #1565c0, #000000); padding:20px; border-radius:10px; text-align:center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
            <h3 style='color:#ffffff;'>2. Target Audience</h3>
            <p style='color:#ffffff;'>Dynamic content based on location and time of day</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background:linear-gradient(135deg, #1976d2, #000000); padding:20px; border-radius:10px; text-align:center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
            <h3 style='color:#ffffff;'>3. Track Results</h3>
            <p style='color:#ffffff;'>Real-time analytics and performance tracking</p>
        </div>
        """, unsafe_allow_html=True)

    # Key Features section
    st.markdown("""
    <div style='margin:50px 0;'>
        <h2 style='text-align:center; color:#333; margin-bottom:30px;'>Key Features</h2>
        <div style='display:grid; grid-template-columns:repeat(2, 1fr); gap:20px;'>
            <div style='background:linear-gradient(135deg, #0098DA, #00CA90); padding:20px; border-radius:10px; color:white;'>
                <h3>Location-Based Display</h3>
                <p>Smart targeting based on area demographics and time</p>
            </div>
            <div style='background:linear-gradient(135deg, #FF6B6B, #FF4B2B); padding:20px; border-radius:10px; color:white;'>
                <h3>Real-Time Analytics</h3>
                <p>Track views, engagement, and campaign performance</p>
            </div>
            <div style='background:linear-gradient(135deg, #FFBC00, #FF9966); padding:20px; border-radius:10px; color:white;'>
                <h3>Dynamic Content</h3>
                <p>Change content based on location and events</p>
            </div>
            <div style='background:linear-gradient(135deg, #6c5ce7, #81ecec); padding:20px; border-radius:10px; color:white;'>
                <h3>Driver Revenue</h3>
                <p>Additional income for taxi drivers</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # If not logged in, show login form
    if not st.session_state.logged_in:
        login_form()
    else:
        # Display the appropriate dashboard based on user role
        if st.session_state.user_role == 'advertiser':
            display_advertiser_summary()
        elif st.session_state.user_role == 'driver':
            display_driver_summary()
        elif st.session_state.user_role == 'admin':
            display_admin_summary()

def login_form():
    st.markdown("### Access Your Dashboard")

    # Create tabs for Login and Register
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Quick Demo Access")
            role = st.selectbox(
                "Select your role",
                ["Advertiser", "Driver", "Admin"],
                key="login_role"
            )

            if st.button("Demo Login"):
                st.session_state.user_role = role.lower()
                st.session_state.user_email = f"demo_{role.lower()}@flowadscab.com"
                st.session_state.user_name = f"Demo {role}"
                st.session_state.logged_in = True
                st.rerun()

        with col2:
            st.subheader("Custom Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login"):
                if email and password:
                    st.session_state.user_role = role.lower()
                    st.session_state.user_email = email
                    st.session_state.user_name = email.split('@')[0].title()
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Please fill in all fields")

    

    with register_tab:
        st.subheader("Create New Account")

        new_role = st.selectbox(
            "Select your role",
            ["Advertiser", "Driver"],
            key="register_role"
        )

        col1, col2 = st.columns(2)

        with col1:
            new_first_name = st.text_input("First Name")
            new_email = st.text_input("Email Address", key="register_email")
            new_password = st.text_input("Password", type="password", key="register_password")

        with col2:
            new_last_name = st.text_input("Last Name")
            new_phone = st.text_input("Phone Number")
            new_confirm_password = st.text_input("Confirm Password", type="password")

        if new_role == "Driver":
            st.subheader("Vehicle Information")

            col1, col2 = st.columns(2)

            with col1:
                vehicle_model = st.text_input("Vehicle Model")
                vehicle_number = st.text_input("Vehicle Registration Number")

            with col2:
                vehicle_color = st.text_input("Vehicle Color")
                driving_license = st.text_input("Driving License Number")

        terms_accepted = st.checkbox("I accept the terms and conditions")

        if st.button("Register"):
            if terms_accepted:
                st.success("Registration successful!")
                # Auto-login after registration
                st.session_state.user_role = new_role.lower()
                st.session_state.user_email = new_email
                st.session_state.user_name = f"{new_first_name} {new_last_name}"
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please accept the terms and conditions to register.")

def welcome_dashboard():
    # Create a colorful welcome banner
    welcome_html = f"""
    <div style='background: linear-gradient(90deg, #6c5ce7, #81ecec); padding:20px; border-radius:12px; margin-bottom:20px; text-align:center; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
        <h2 style='color:#FFFFFF; margin:0; font-size:2em; font-weight:700;'>Welcome, {st.session_state.user_name}!</h2>
        <p style='color:#F8F9FA; font-size:1.2em; margin-top:5px;'>You are logged in as: <span style='background:rgba(255,255,255,0.2); padding:3px 10px; border-radius:20px;'>{st.session_state.user_role.title()}</span></p>
    </div>
    """
    st.markdown(welcome_html, unsafe_allow_html=True)

    # Special Offers and Promotions Banners
    st.markdown("""
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin:25px 0;">
        <!-- Banner 1: Premium Plan Offer -->
        <div style="background: linear-gradient(135deg, #FF416C, #FF4B2B); padding:15px; border-radius:10px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); position:relative; overflow:hidden;">
            <div style="position:absolute; top:-10px; right:-10px; background:#FFD700; color:#000; padding:5px 20px; transform:rotate(45deg); font-size:0.7em; font-weight:bold;">20% OFF</div>
            <h3 style="color:#FFF; margin-top:5px; font-size:1.3em;">UPGRADE TO PREMIUM PLAN</h3>
            <ul style="color:#FFF; margin:10px 0; padding-left:20px;">
                <li>14 hours/day ad display time</li>
                <li>Priority placement in high-traffic areas</li>
                <li>Advanced analytics dashboard</li>
            </ul>
            <div style="text-align:center; margin-top:10px;">
                <span style="background:#FFF; color:#FF416C; font-weight:bold; padding:5px 15px; border-radius:20px; display:inline-block; font-size:0.9em;">Rs.18,000/month</span>
            </div>
        </div>
        
        <!-- Banner 2: Basic Plan Offer -->
        <div style="background: linear-gradient(135deg, #0052D4, #4364F7); padding:15px; border-radius:10px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); position:relative; overflow:hidden;">
            <div style="position:absolute; top:-10px; right:-10px; background:#7CFC00; color:#000; padding:5px 20px; transform:rotate(45deg); font-size:0.7em; font-weight:bold;">NEW</div>
            <h3 style="color:#FFF; margin-top:5px; font-size:1.3em;">BASIC STARTER PACKAGE</h3>
            <ul style="color:#FFF; margin:10px 0; padding-left:20px;">
                <li>8 hours/day ad display time</li>
                <li>Rotation in standard traffic areas</li>
                <li>Weekly performance reports</li>
            </ul>
            <div style="text-align:center; margin-top:10px;">
                <span style="background:#FFF; color:#4364F7; font-weight:bold; padding:5px 15px; border-radius:20px; display:inline-block; font-size:0.9em;">Rs.12,000/month</span>
            </div>
        </div>
    </div>
    
    <!-- Special Limited Time Offers Row -->
    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin:15px 0 30px 0;">
        <!-- Offer 1 -->
        <div style="background:linear-gradient(135deg, #00b09b, #96c93d); padding:10px; border-radius:8px; text-align:center;">
            <h4 style="color:#FFF; margin:5px 0; font-size:1em;">WEEKEND SPECIAL</h4>
            <p style="color:#FFF; margin:0; font-size:0.8em;">Book Fri-Sun at 25% OFF</p>
        </div>
        
        <!-- Offer 2 -->
        <div style="background:linear-gradient(135deg, #8E2DE2, #4A00E0); padding:10px; border-radius:8px; text-align:center;">
            <h4 style="color:#FFF; margin:5px 0; font-size:1em;">GROUP BOOKING</h4>
            <p style="color:#FFF; margin:0; font-size:0.8em;">10 taxis for price of 8</p>
        </div>
        
        <!-- Offer 3 -->
        <div style="background:linear-gradient(135deg, #F76B1C, #FAD961); padding:10px; border-radius:8px; text-align:center;">
            <h4 style="color:#FFF; margin:5px 0; font-size:1em;">FOOD DELIVERY ADS</h4>
            <p style="color:#FFF; margin:0; font-size:0.8em;">30% OFF first month</p>
        </div>
    </div>
    """
    , unsafe_allow_html=True)

    # Activity Cards Row
    col1, col2, col3 = st.columns(3)

    # Active campaigns, customers, and insights stats
    with col1:
        active_campaigns_html = """
        <div style='background:linear-gradient(45deg, #1e3c72, #2a5298); padding:20px; border-radius:10px; height:100%; box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
            <h3 style='color:#FFF; margin-top:0; font-size:1.3em;'>Active Campaigns</h3>
            <p style='color:#FFF; font-size:2.5em; font-weight:700; margin:15px 0 5px 0;'>12</p>
            <p style='color:rgba(255,255,255,0.7); margin:0;'>&uarr; 3 new this week</p>
        </div>
        """
        st.markdown(active_campaigns_html, unsafe_allow_html=True)

    with col2:
        active_customers_html = """
        <div style='background:linear-gradient(45deg, #11998e, #38ef7d); padding:20px; border-radius:10px; height:100%; box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
            <h3 style='color:#FFF; margin-top:0; font-size:1.3em;'>Active Customers</h3>
            <p style='color:#FFF; font-size:2.5em; font-weight:700; margin:15px 0 5px 0;'>28</p>
            <p style='color:rgba(255,255,255,0.7); margin:0;'>&uarr; 5 new this month</p>
        </div>
        """
        st.markdown(active_customers_html, unsafe_allow_html=True)

    with col3:
        total_views_html = """
        <div style='background:linear-gradient(45deg, #6a11cb, #2575fc); padding:20px; border-radius:10px; height:100%; box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
            <h3 style='color:#FFF; margin-top:0; font-size:1.3em;'>Total Views</h3>
            <p style='color:#FFF; font-size:2.5em; font-weight:700; margin:15px 0 5px 0;'>45.2K</p>
            <p style='color:rgba(255,255,255,0.7); margin:0;'>&uarr; 12% from last week</p>
        </div>
        """
        st.markdown(total_views_html, unsafe_allow_html=True)

    # Display role-specific dashboard content
    if st.session_state.user_role == "advertiser":
        display_advertiser_summary()
    elif st.session_state.user_role == "driver":
        display_driver_summary()
    elif st.session_state.user_role == "admin":
        display_admin_summary()

    # Logout button
    if st.sidebar.button("Logout", key="sidebar_logout_btn"):
        for key in list(st.session_state.keys()):
            if key in ["active_campaigns", "drivers", "ad_templates", "high_viewership_locations", 
                      "notifications", "help_tickets", "payment_records", "invoices"]:
                continue  
            del st.session_state[key]
        st.session_state.logged_in = False
        st.rerun()

def display_advertiser_summary():
    st.subheader("Your Campaign Summary")

    # Create two columns for metrics and map
    col1, col2 = st.columns([3, 2])

    with col1:
        # Filter campaigns for this advertiser (using email as identifier)
        advertiser_campaigns = [c for c in st.session_state.active_campaigns 
                               if c.get("advertiser", "").lower() == st.session_state.user_name.lower()]

        if advertiser_campaigns:
            # Calculate metrics
            total_active = sum(1 for c in advertiser_campaigns if c.get("status") == "Active")
            total_impressions = sum(c.get("impressions", 0) for c in advertiser_campaigns)
            total_views = sum(c.get("views", 0) for c in advertiser_campaigns)
            total_spent = sum(c.get("spent", 0) for c in advertiser_campaigns)

            # Display metrics
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

            with metric_col1:
                st.metric("Active Campaigns", total_active)

            with metric_col2:
                st.metric("Total Impressions", f"{total_impressions:,}")

            with metric_col3:
                st.metric("Total Views", f"{total_views:,}")

            with metric_col4:
                st.metric("Total Spent", f"Rs.{total_spent:,}")

            # Display campaign list
            st.write("##### Your Campaigns")
            for campaign in advertiser_campaigns:
                with st.container():
                    status_color = '#28a745' if campaign['status'] == 'Active' else '#ffc107' if campaign['status'] == 'Scheduled' else '#6c757d'
                    advertiser_campaign_html = f"""
                    <div style="padding:15px; border-radius:5px; background-color:#f8f9fa; margin-bottom:10px; border-left:3px solid {status_color}">
                        <h5>{campaign['name']}</h5>
                        <p><strong>Status:</strong> {campaign['status']} | <strong>Budget:</strong> Rs.{campaign['budget']:,} | <strong>Spent:</strong> Rs.{campaign['spent']:,}</p>
                        <p><strong>Views:</strong> {campaign['views']:,} | <strong>Impressions:</strong> {campaign['impressions']:,}</p>
                    </div>
                    """
                    st.markdown(advertiser_campaign_html, unsafe_allow_html=True)
        else:
            st.info("You don't have any campaigns yet. Create your first campaign from the Campaigns page.")
            st.button("Create Your First Campaign")

    with col2:
        st.write("##### Campaign Performance Metrics")

        # Create performance chart
        if advertiser_campaigns:
            # Get campaign names and performance metrics
            campaign_names = [c['name'] for c in advertiser_campaigns[:3]]
            campaign_views = [c['views'] for c in advertiser_campaigns[:3]]
            campaign_impressions = [c['impressions'] for c in advertiser_campaigns[:3]]

            # Create a bar chart using Plotly
            fig = go.Figure()

            # Add bars for views
            fig.add_trace(go.Bar(
                x=campaign_names,
                y=campaign_views,
                name='Views',
                marker_color='#4A6FE3',
                hovertemplate='Campaign: %{x}<br>Views: %{y:,}<extra></extra>'
            ))

            # Add bars for impressions
            fig.add_trace(go.Bar(
                x=campaign_names,
                y=campaign_impressions,
                name='Impressions',
                marker_color='#52D726',
                hovertemplate='Campaign: %{x}<br>Impressions: %{y:,}<extra></extra>'
            ))

            # Update layout
            fig.update_layout(
                title="Campaign Performance",
                xaxis_title="",
                yaxis_title="Count",
                barmode='group',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )

            # Display the chart
            st.plotly_chart(fig, use_container_width=True)

            # Add text explanation
            explanation_html = """
            <div style='background-color: #f8f9fa; padding: 10px; border-radius:5px;'>
                <p style='margin:0; font-size:0.9em;'><strong>Views</strong>: Number of times your ad was viewed by passengers</p>
                <p style='margin:0; font-size:0.9em;'><strong>Impressions</strong>: Total ad displays, including repeat views</p>
            </div>
            """
            st.markdown(explanation_html, unsafe_allow_html=True)
        else:
            st.info("Create your first campaign to see performance metrics.")

def display_driver_summary():
    st.subheader("Driver Dashboard Summary")

    # Find driver data (using email as identifier)
    driver = None
    for d in st.session_state.drivers:
        if d.get("name", "").lower() == st.session_state.user_name.lower():
            driver = d
            break

    if not driver:
        # If driver not found, create a mock driver for demonstration
        driver = {
            "id": len(st.session_state.drivers) + 1,
            "name": st.session_state.user_name,
            "status": "Active",
            "current_location": {
                "area": "Vijay Nagar",
                "lat": 22.7533,
                "lon": 75.8937
            },
            "kms_today": 45,
            "hours_active": 3,
            "earnings": {
                "today": 96,
                "base": 96,
                "incentives": 0
            },
            "current_ad_displaying": 1
        }
        st.session_state.drivers.append(driver)

    # Create columns for metrics and map
    col1, col2 = st.columns([3, 2])

    with col1:
        # Display driver metrics
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            st.metric("Status", driver.get("status", "Inactive"))

        with metric_col2:
            st.metric("Today's Distance", f"{driver.get('kms_today', 0)} km")

        with metric_col3:
            st.metric("Hours Active", f"{driver.get('hours_active', 0)} hrs")

        with metric_col4:
            st.metric("Today's Earnings", f"Rs.{driver.get('earnings', {}).get('today', 0)}")

        # Display current ad information
        current_ad_id = driver.get("current_ad_displaying")
        current_ad = None

        for campaign in st.session_state.active_campaigns:
            if campaign.get("id") == current_ad_id:
                current_ad = campaign
                break

        if current_ad:
            st.write("##### Currently Displaying Advertisement")
            current_ad_html = f"""
            <div style="padding:15px; border-radius:5px; background-color:#f8f9fa; margin-bottom:10px; border-left:3px solid #0098DA">
                <h5>{current_ad['name']}</h5>
                <p><strong>Advertiser:</strong> {current_ad['advertiser']}</p>
                <p><strong>Type:</strong> {current_ad['ad_type'].title()} Ad | <strong>Regions:</strong> {', '.join(current_ad['regions'][:2])}{' and more' if len(current_ad['regions']) > 2 else ''}</p>
            </div>
            """
            st.markdown(current_ad_html, unsafe_allow_html=True)
        else:
            st.info("No advertisement currently assigned for display.")

    with col2:
        st.write("##### Your Current Location")

        # Initialize a map centered on driver location
        driver_lat = driver.get("current_location", {}).get("lat", 22.7196)
        driver_lon = driver.get("current_location", {}).get("lon", 75.8577)

        m = folium.Map(location=[driver_lat, driver_lon], zoom_start=14)

        # Add marker for driver
        folium.Marker(
            [driver_lat, driver_lon],
            tooltip=f"{driver['name']} - {driver.get('current_location', {}).get('area', 'Unknown')}",
            icon=folium.Icon(color='green', icon='car', prefix='fa')
        ).add_to(m)

        # Display the map
        folium_static(m, width=400)

def display_admin_summary():
    st.subheader("Admin Dashboard Summary")

    # Create tabs for different summaries
    tab1, tab2, tab3 = st.tabs(["Campaigns", "Drivers", "Analytics"])

    with tab1:
        # Campaign summary
        active_campaigns = [c for c in st.session_state.active_campaigns if c.get("status") == "Active"]
        scheduled_campaigns = [c for c in st.session_state.active_campaigns if c.get("status") == "Scheduled"]

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("Active Campaigns", len(active_campaigns))

        with metric_col2:
            st.metric("Scheduled Campaigns", len(scheduled_campaigns))

        with metric_col3:
            total_budget = sum(c.get("budget", 0) for c in st.session_state.active_campaigns)
            st.metric("Total Campaign Budget", f"Rs.{total_budget:,}")

        # List active campaigns
        st.write("##### Active Campaigns")
        for campaign in active_campaigns[:3]:  # Show top 3
            campaign_html = f"""
            <div style="padding:10px; border-radius:5px; background-color:#f8f9fa; margin-bottom:8px; border-left:3px solid #28a745">
                <h6>{campaign['name']}</h6>
                <p><strong>Advertiser:</strong> {campaign['advertiser']} | <strong>Budget:</strong> Rs.{campaign['budget']:,} | <strong>Views:</strong> {campaign['views']:,}</p>
            </div>
            """
            st.markdown(campaign_html, unsafe_allow_html=True)

    with tab2:
        # Driver summary
        active_drivers = [d for d in st.session_state.drivers if d.get("status") == "Active"]
        inactive_drivers = [d for d in st.session_state.drivers if d.get("status") != "Active"]

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("Active Drivers", len(active_drivers))

        with metric_col2:
            st.metric("Inactive Drivers", len(inactive_drivers))

        with metric_col3:
            avg_distance = sum(d.get("kms_today", 0) for d in active_drivers) / max(len(active_drivers), 1)
            st.metric("Avg. Distance Today", f"{avg_distance:.1f} km")

        # List active drivers
        st.write("##### Active Drivers")
        driver_cols = st.columns(3)

        for i, driver in enumerate(active_drivers[:3]):  # Show top 3
            with driver_cols[i % 3]:
                driver_html = f"""
                <div style="padding:10px; border-radius:5px; background-color:#f8f9fa; margin-bottom:8px;">
                    <h6>{driver['name']}</h6>
                    <p><strong>Vehicle:</strong> {driver.get('vehicle_model', 'N/A')}</p>
                    <p><strong>Today:</strong> {driver.get('kms_today', 0)} km | Rs.{driver.get('earnings', {}).get('today', 0)}</p>
                </div>
                """
                st.markdown(driver_html, unsafe_allow_html=True)

    with tab3:
        # Quick analytics
        col1, col2 = st.columns(2)

        with col1:
            st.write("##### Campaign Performance")

            # Create sample data for a chart
            campaigns = st.session_state.active_campaigns[:5]  # Top 5 campaigns
            campaign_names = [c['name'] for c in campaigns]
            campaign_views = [c['views'] for c in campaigns]

            # Create a bar chart using Plotly
            fig = go.Figure(go.Bar(
                x=campaign_names, 
                y=campaign_views,
                marker_color='#0098DA',
                hovertemplate='Campaign: %{x}<br>Views: %{y}<extra></extra>'
            ))

            fig.update_layout(
                title="Top Campaign Views",
                xaxis_title="Campaign",
                yaxis_title="Views"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("##### High Viewership Locations")

            locations = st.session_state.high_viewership_locations
            location_names = [loc['location'] for loc in locations]
            location_views = [loc['views'] for loc in locations]

            # Create a bar chart using go.Figure
            fig = go.Figure(go.Bar(
                x=location_names,
                y=location_views,
                marker_color='#FF6B6B',
                hovertemplate='Location: %{x}<br>Views: %{y}<extra></extra>'
            ))

            fig.update_layout(
                title="Views by Location",
                xaxis_title="Location",
                yaxis_title="Views"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

# Configure sidebar
def sidebar():
    st.sidebar.title("Flow Ads Cab")

    if st.session_state.logged_in:
        st.sidebar.markdown(f"**User:** {st.session_state.user_name}")
        st.sidebar.markdown(f"**Role:** {st.session_state.user_role.title()}")

        if st.sidebar.button("Logout", key="dashboard_logout_btn"):
            for key in list(st.session_state.keys()):
                if key not in ["active_campaigns", "drivers", "ad_templates", "high_viewership_locations"]:
                    del st.session_state[key]
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.sidebar.info("Please log in to access the platform features.")

def advertiser_sidebar():
    st.sidebar.markdown("### Advertiser Navigation")
    st.sidebar.page_link("app.py", label="Dashboard")
    st.sidebar.page_link("pages/01_advertiser_dashboard.py", label="Campaign Management")
    st.sidebar.page_link("pages/04_campaigns.py", label="Create Campaign")
    st.sidebar.page_link("pages/06_payments.py", label="Payments & Billing")
    st.sidebar.page_link("pages/05_analytics.py", label="Analytics")
    st.sidebar.page_link("pages/07_locations.py", label="Location Insights")
    st.sidebar.page_link("pages/08_help_support.py", label="Help & Support")

def driver_sidebar():
    st.sidebar.markdown("### Driver Navigation")
    st.sidebar.page_link("app.py", label="Dashboard")
    st.sidebar.page_link("pages/02_driver_dashboard.py", label="My Profile")
    st.sidebar.page_link("pages/06_payments.py", label="Earnings")
    st.sidebar.page_link("pages/08_help_support.py", label="Help & Support")

def admin_sidebar():
    st.sidebar.markdown("### Admin Navigation")
    st.sidebar.page_link("app.py", label="Dashboard")
    st.sidebar.page_link("pages/03_admin_dashboard.py", label="Admin Panel")
    st.sidebar.page_link("pages/01_advertiser_dashboard.py", label="Advertisers")
    st.sidebar.page_link("pages/02_driver_dashboard.py", label="Drivers")
    st.sidebar.page_link("pages/04_campaigns.py", label="Campaigns")
    st.sidebar.page_link("pages/05_analytics.py", label="Analytics")
    st.sidebar.page_link("pages/06_payments.py", label="Payments")
    st.sidebar.page_link("pages/07_locations.py", label="Locations")
    st.sidebar.page_link("pages/08_help_support.py", label="Support Tickets")

# Run the app
sidebar()
display_home()