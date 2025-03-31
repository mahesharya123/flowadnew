import os
import streamlit as st
from twilio.rest import Client

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

def send_sms_alert(phone_number, message):
    """
    Send an SMS alert to a user using Twilio API
    
    Parameters:
    - phone_number: Recipient's phone number (in E.164 format, e.g., +919876543210)
    - message: SMS message content
    
    Returns:
    - Dictionary containing response status
    """
    # Store sent messages in session state for demonstration regardless of mode
    if "sent_sms" not in st.session_state:
        st.session_state.sent_sms = []
    
    st.session_state.sent_sms.append({
        "phone": phone_number,
        "message": message
    })
    
    # Check if we have Twilio credentials
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER:
        try:
            # Initialize Twilio client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            
            # Send the SMS message
            message = client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            
            print(f"SMS sent with SID: {message.sid}")
            
            return {
                "status": "success",
                "message": "SMS alert sent successfully via Twilio",
                "recipient": phone_number,
                "sid": message.sid
            }
        except Exception as e:
            print(f"Error sending SMS via Twilio: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to send SMS: {str(e)}",
                "recipient": phone_number
            }
    else:
        # Fallback to simulation mode if no Twilio credentials
        print(f"SMS ALERT to {phone_number}: {message} (SIMULATED - Twilio credentials not configured)")
        return {
            "status": "success",
            "message": "SMS alert sent successfully (simulated - Twilio not configured)",
            "recipient": phone_number
        }

def get_viewership_alert_message(campaign_name, views_count, target=None):
    """
    Generate a viewership milestone alert message
    
    Parameters:
    - campaign_name: Name of the campaign
    - views_count: Current view count
    - target: Target view count (optional)
    
    Returns:
    - Formatted message string
    """
    if target and views_count >= target:
        return f"Congratulations! Your '{campaign_name}' campaign has reached its target of {target:,} views. Current views: {views_count:,}."
    else:
        milestones = [1000, 5000, 10000, 25000, 50000, 100000]
        # Find the highest milestone reached
        reached_milestone = None
        for milestone in milestones:
            if views_count >= milestone:
                reached_milestone = milestone
        
        if reached_milestone:
            return f"Milestone alert! Your '{campaign_name}' campaign has reached {reached_milestone:,} views. Keep up the good work!"
        else:
            return f"Update: Your '{campaign_name}' campaign has {views_count:,} views so far."

def get_target_reached_message(area_name, target_type="views"):
    """
    Generate a location target reached message
    
    Parameters:
    - area_name: Name of the location
    - target_type: Type of target (views, impressions)
    
    Returns:
    - Formatted message string
    """
    return f"Location alert: {area_name} has reached high {target_type} engagement. Consider boosting your ad display in this area for maximum impact."

def get_driver_earnings_alert(driver_name, amount, period="today"):
    """
    Generate a driver earnings alert message
    
    Parameters:
    - driver_name: Name of the driver
    - amount: Earnings amount
    - period: Time period (today, this week, etc.)
    
    Returns:
    - Formatted message string
    """
    return f"Hi {driver_name}, you've earned ₹{amount} {period}! Check your Flow Ads Cab driver app for details."

def get_document_expiry_alert(driver_name, document_type, days_remaining):
    """
    Generate a document expiry alert message
    
    Parameters:
    - driver_name: Name of the driver
    - document_type: Type of document (license, insurance, etc.)
    - days_remaining: Number of days until expiry
    
    Returns:
    - Formatted message string
    """
    if days_remaining <= 7:
        urgency = "Urgent: "
    else:
        urgency = ""
    
    return f"{urgency}Hi {driver_name}, your {document_type} will expire in {days_remaining} days. Please renew it soon to continue using Flow Ads Cab services."

def get_payment_confirmation(user_name, amount, purpose=None):
    """
    Generate a payment confirmation message
    
    Parameters:
    - user_name: Name of the user
    - amount: Payment amount
    - purpose: Purpose of the payment (optional)
    
    Returns:
    - Formatted message string
    """
    if purpose:
        return f"Payment confirmed: ₹{amount} for {purpose}. Thank you, {user_name}! Receipt available in your Flow Ads Cab account."
    else:
        return f"Payment confirmed: ₹{amount}. Thank you, {user_name}! Receipt available in your Flow Ads Cab account."

def get_campaign_status_alert(campaign_name, status, start_date=None):
    """
    Generate a campaign status alert message
    
    Parameters:
    - campaign_name: Name of the campaign
    - status: New status of the campaign (Active, Paused, etc.)
    - start_date: Campaign start date (for Scheduled status)
    
    Returns:
    - Formatted message string
    """
    if status == "Active":
        return f"Your campaign '{campaign_name}' is now active and being displayed on Flow Ads Cab taxis!"
    elif status == "Paused":
        return f"Your campaign '{campaign_name}' has been paused. You can resume it anytime from your Flow Ads Cab dashboard."
    elif status == "Scheduled" and start_date:
        return f"Your campaign '{campaign_name}' is scheduled to start on {start_date}. We'll notify you when it goes live."
    elif status == "Completed":
        return f"Your campaign '{campaign_name}' has completed its scheduled run. View the full performance report on your dashboard."
    else:
        return f"Status update: Your campaign '{campaign_name}' status is now '{status}'."