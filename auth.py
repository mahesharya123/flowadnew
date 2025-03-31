
import streamlit as st

st.title("Flow Ads Cab - Login")

# Quick Demo Login Section
st.markdown("""
<div style='display: flex; justify-content: center; gap: 20px; margin: 20px 0;'>
    <div style='text-align: center; padding: 20px; background: #f0f8ff; border-radius: 10px; width: 250px;'>
        <h3>Admin Demo</h3>
        <p>Email: admin@flowadscab.com</p>
        <p>Password: admin123</p>
    </div>
    <div style='text-align: center; padding: 20px; background: #fff8f0; border-radius: 10px; width: 250px;'>
        <h3>Driver Demo</h3>
        <p>Email: driver@flowadscab.com</p>
        <p>Password: driver123</p>
    </div>
    <div style='text-align: center; padding: 20px; background: #fff0f8; border-radius: 10px; width: 250px;'>
        <h3>Advertiser Demo</h3>
        <p>Email: advertiser@flowadscab.com</p>
        <p>Password: advertiser123</p>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Login as Admin", use_container_width=True, key="admin_demo"):
        st.session_state.logged_in = True
        st.session_state.user_role = "admin"
        st.session_state.user_name = "Admin"
        st.session_state.user_email = "admin@flowadscab.com"
        # Set up admin access to all pages
        st.session_state.pages_access = {
            "dashboard": True,
            "admin_panel": True,
            "advertiser_dashboard": True,
            "driver_dashboard": True,
            "campaigns": True,
            "analytics": True,
            "payments": True,
            "locations": True,
            "help_support": True
        }
        st.rerun()

with col2:
    if st.button("Login as Driver", use_container_width=True, key="driver_demo"):
        st.session_state.logged_in = True
        st.session_state.user_role = "driver"
        st.session_state.user_name = "Driver"
        st.session_state.user_email = "driver@flowadscab.com"
        # Set up driver access pages
        st.session_state.pages_access = {
            "dashboard": True,
            "driver_dashboard": True,
            "payments": True,
            "help_support": True
        }
        st.rerun()

with col3:
    if st.button("Login as Advertiser", use_container_width=True, key="advertiser_demo"):
        st.session_state.logged_in = True
        st.session_state.user_role = "advertiser"
        st.session_state.user_name = "Advertiser"
        st.session_state.user_email = "advertiser@flowadscab.com"
        # Set up advertiser access pages
        st.session_state.pages_access = {
            "dashboard": True,
            "advertiser_dashboard": True,
            "campaigns": True,
            "analytics": True,
            "payments": True,
            "locations": True,
            "help_support": True
        }
        st.rerun()

# Display welcome message and access info when logged in
if 'logged_in' in st.session_state and st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.user_name}! You are logged in as {st.session_state.user_role}")
    if 'pages_access' in st.session_state:
        st.write("You have access to the following pages:")
        for page, has_access in st.session_state.pages_access.items():
            if has_access:
                st.write(f"✓ {page.replace('_', ' ').title()}")
