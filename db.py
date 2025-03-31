import os
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

# Get database credentials from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

def initialize_database():
    """Create tables if they don't exist"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # Create users table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(100) NOT NULL,
                        role VARCHAR(20) NOT NULL,
                        phone VARCHAR(20),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create drivers table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS drivers (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id),
                        vehicle_model VARCHAR(100),
                        vehicle_number VARCHAR(50),
                        vehicle_color VARCHAR(50),
                        license_number VARCHAR(50),
                        status VARCHAR(20) DEFAULT 'Inactive',
                        current_location_area VARCHAR(100),
                        current_location_lat DECIMAL(10, 7),
                        current_location_lon DECIMAL(10, 7),
                        kms_today INTEGER DEFAULT 0,
                        hours_active DECIMAL(5, 2) DEFAULT 0,
                        current_ad_displaying INTEGER
                    )
                """)
                
                # Create campaigns table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS campaigns (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        advertiser_id INTEGER REFERENCES users(id),
                        status VARCHAR(20) DEFAULT 'Draft',
                        ad_type VARCHAR(20),
                        budget INTEGER,
                        spent INTEGER DEFAULT 0,
                        views INTEGER DEFAULT 0,
                        impressions INTEGER DEFAULT 0,
                        start_date DATE,
                        end_date DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create campaign_regions table (for many-to-many relation)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS campaign_regions (
                        id SERIAL PRIMARY KEY,
                        campaign_id INTEGER REFERENCES campaigns(id),
                        region_name VARCHAR(100) NOT NULL
                    )
                """)
                
                # Create payments table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS payments (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id),
                        payment_type VARCHAR(50) NOT NULL,
                        amount DECIMAL(10, 2) NOT NULL,
                        status VARCHAR(20) DEFAULT 'pending',
                        description TEXT,
                        payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create locations table (for high viewership locations)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS locations (
                        id SERIAL PRIMARY KEY,
                        location_name VARCHAR(100) NOT NULL,
                        lat DECIMAL(10, 7) NOT NULL,
                        lon DECIMAL(10, 7) NOT NULL,
                        views INTEGER DEFAULT 0,
                        importance INTEGER DEFAULT 1
                    )
                """)
                
                conn.commit()
                st.success("Database initialized successfully")
                
                # Check if we need to add demo data
                cur.execute("SELECT COUNT(*) FROM users")
                user_count = cur.fetchone()['count']
                
                if user_count == 0:
                    add_demo_data(conn)
                
        except Exception as e:
            conn.rollback()
            st.error(f"Database initialization error: {e}")
        finally:
            conn.close()

def add_demo_data(conn):
    """Add demo data to the database"""
    try:
        with conn.cursor() as cur:
            # Add demo users
            cur.execute("""
                INSERT INTO users (name, email, password, role, phone) VALUES
                ('Demo Admin', 'demo_admin@flowadscab.com', 'password', 'admin', '9876543210'),
                ('Demo Advertiser', 'demo_advertiser@flowadscab.com', 'password', 'advertiser', '9876543211'),
                ('Demo Driver', 'demo_driver@flowadscab.com', 'password', 'driver', '9876543212')
                RETURNING id
            """)
            user_ids = cur.fetchall()
            
            # Get the user IDs
            admin_id = user_ids[0]['id']
            advertiser_id = user_ids[1]['id']
            driver_id = user_ids[2]['id']
            
            # Add demo driver
            cur.execute("""
                INSERT INTO drivers (user_id, vehicle_model, vehicle_number, vehicle_color, license_number, 
                                    status, current_location_area, current_location_lat, current_location_lon,
                                    kms_today, hours_active)
                VALUES (%s, 'Swift Dzire', 'MP-09-AB-1234', 'White', 'DL9876543210',
                       'Active', 'Vijay Nagar', 22.7533, 75.8937, 45, 3)
            """, (driver_id,))
            
            # Add demo campaigns
            cur.execute("""
                INSERT INTO campaigns (name, advertiser_id, status, ad_type, budget, spent, views, impressions, 
                                      start_date, end_date)
                VALUES 
                ('Summer Sale Promotion', %s, 'Active', 'image', 50000, 12500, 8750, 15000, 
                CURRENT_DATE - INTERVAL '5 days', CURRENT_DATE + INTERVAL '25 days'),
                ('New Product Launch', %s, 'Scheduled', 'video', 75000, 0, 0, 0, 
                CURRENT_DATE + INTERVAL '3 days', CURRENT_DATE + INTERVAL '33 days'),
                ('Brand Awareness Campaign', %s, 'Active', 'image', 40000, 18000, 12000, 20000, 
                CURRENT_DATE - INTERVAL '10 days', CURRENT_DATE + INTERVAL '20 days')
                RETURNING id
            """, (advertiser_id, advertiser_id, advertiser_id))
            
            campaign_ids = cur.fetchall()
            
            # Add regions for campaigns
            regions = ['Vijay Nagar', 'Palasia', 'South Tukoganj', 'New Palasia', 'MG Road', 'AB Road']
            
            for campaign in campaign_ids:
                # Add 3-4 random regions per campaign
                import random
                campaign_regions = random.sample(regions, random.randint(3, 4))
                
                for region in campaign_regions:
                    cur.execute("""
                        INSERT INTO campaign_regions (campaign_id, region_name)
                        VALUES (%s, %s)
                    """, (campaign['id'], region))
            
            # Add high viewership locations
            cur.execute("""
                INSERT INTO locations (location_name, lat, lon, views, importance)
                VALUES
                ('Palasia Square', 22.7244, 75.8839, 45000, 5),
                ('Vijay Nagar Square', 22.7533, 75.8937, 38000, 4),
                ('Malwa Mall', 22.7229, 75.8874, 32000, 4),
                ('C21 Mall', 22.7607, 75.8940, 29000, 3),
                ('MG Road', 22.7183, 75.8720, 26000, 3),
                ('Treasure Island Mall', 22.7248, 75.8876, 35000, 4)
            """)
            
            # Add some payments
            cur.execute("""
                INSERT INTO payments (user_id, payment_type, amount, status, description)
                VALUES
                (%s, 'driver_payment', 2500.00, 'completed', 'Weekly payment for March 22'),
                (%s, 'driver_payment', 2300.00, 'completed', 'Weekly payment for March 15'),
                (%s, 'advertiser_payment', 12500.00, 'completed', 'Summer Sale Promotion - Initial payment'),
                (%s, 'advertiser_payment', 18000.00, 'completed', 'Brand Awareness Campaign - Initial payment')
            """, (driver_id, driver_id, advertiser_id, advertiser_id))
            
            conn.commit()
            st.success("Demo data added successfully")
            
    except Exception as e:
        conn.rollback()
        st.error(f"Error adding demo data: {e}")

def get_users():
    """Get all users from the database"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users")
                users = cur.fetchall()
                return users
        except Exception as e:
            st.error(f"Error retrieving users: {e}")
            return []
        finally:
            conn.close()
    return []

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cur.fetchone()
                return user
        except Exception as e:
            st.error(f"Error retrieving user: {e}")
            return None
        finally:
            conn.close()
    return None

def get_drivers():
    """Get all drivers with user information"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT d.*, u.name, u.email, u.phone 
                    FROM drivers d
                    JOIN users u ON d.user_id = u.id
                """)
                drivers = cur.fetchall()
                return drivers
        except Exception as e:
            st.error(f"Error retrieving drivers: {e}")
            return []
        finally:
            conn.close()
    return []

def get_campaigns(advertiser_id=None):
    """Get campaigns with optional advertiser filter"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                if advertiser_id:
                    cur.execute("""
                        SELECT c.*, u.name as advertiser 
                        FROM campaigns c
                        JOIN users u ON c.advertiser_id = u.id
                        WHERE c.advertiser_id = %s
                    """, (advertiser_id,))
                else:
                    cur.execute("""
                        SELECT c.*, u.name as advertiser 
                        FROM campaigns c
                        JOIN users u ON c.advertiser_id = u.id
                    """)
                campaigns = cur.fetchall()
                
                # Get regions for each campaign
                for campaign in campaigns:
                    cur.execute("""
                        SELECT region_name FROM campaign_regions 
                        WHERE campaign_id = %s
                    """, (campaign['id'],))
                    regions = cur.fetchall()
                    campaign['regions'] = [r['region_name'] for r in regions]
                
                return campaigns
        except Exception as e:
            st.error(f"Error retrieving campaigns: {e}")
            return []
        finally:
            conn.close()
    return []

def get_high_viewership_locations():
    """Get high viewership locations"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM locations ORDER BY views DESC")
                locations = cur.fetchall()
                return locations
        except Exception as e:
            st.error(f"Error retrieving locations: {e}")
            return []
        finally:
            conn.close()
    return []

def get_payments(user_id=None, payment_type=None):
    """Get payments with optional filters"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                query = "SELECT p.*, u.name, u.email FROM payments p JOIN users u ON p.user_id = u.id WHERE 1=1"
                params = []
                
                if user_id:
                    query += " AND p.user_id = %s"
                    params.append(user_id)
                
                if payment_type:
                    query += " AND p.payment_type = %s"
                    params.append(payment_type)
                
                query += " ORDER BY p.payment_date DESC"
                
                cur.execute(query, params)
                payments = cur.fetchall()
                return payments
        except Exception as e:
            st.error(f"Error retrieving payments: {e}")
            return []
        finally:
            conn.close()
    return []

def create_user(user_data):
    """Create a new user"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (name, email, password, role, phone)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    user_data['name'], 
                    user_data['email'], 
                    user_data['password'], 
                    user_data['role'], 
                    user_data.get('phone', '')
                ))
                user_id = cur.fetchone()['id']
                conn.commit()
                return user_id
        except Exception as e:
            conn.rollback()
            st.error(f"Error creating user: {e}")
            return None
        finally:
            conn.close()
    return None

def create_driver(driver_data, user_id):
    """Create a new driver for an existing user"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO drivers (
                        user_id, vehicle_model, vehicle_number, vehicle_color, 
                        license_number, status, current_location_area, 
                        current_location_lat, current_location_lon
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    user_id,
                    driver_data.get('vehicle_model', ''),
                    driver_data.get('vehicle_number', ''),
                    driver_data.get('vehicle_color', ''),
                    driver_data.get('license_number', ''),
                    driver_data.get('status', 'Inactive'),
                    driver_data.get('current_location_area', 'Indore'),
                    driver_data.get('current_location_lat', 22.7196),
                    driver_data.get('current_location_lon', 75.8577)
                ))
                driver_id = cur.fetchone()['id']
                conn.commit()
                return driver_id
        except Exception as e:
            conn.rollback()
            st.error(f"Error creating driver: {e}")
            return None
        finally:
            conn.close()
    return None

def create_campaign(campaign_data):
    """Create a new campaign"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO campaigns (
                        name, advertiser_id, status, ad_type, budget, 
                        start_date, end_date
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    campaign_data['name'],
                    campaign_data['advertiser_id'],
                    campaign_data.get('status', 'Draft'),
                    campaign_data.get('ad_type', 'image'),
                    campaign_data.get('budget', 0),
                    campaign_data.get('start_date'),
                    campaign_data.get('end_date')
                ))
                campaign_id = cur.fetchone()['id']
                
                # Add regions if provided
                if 'regions' in campaign_data and campaign_data['regions']:
                    for region in campaign_data['regions']:
                        cur.execute("""
                            INSERT INTO campaign_regions (campaign_id, region_name)
                            VALUES (%s, %s)
                        """, (campaign_id, region))
                
                conn.commit()
                return campaign_id
        except Exception as e:
            conn.rollback()
            st.error(f"Error creating campaign: {e}")
            return None
        finally:
            conn.close()
    return None

def create_payment(payment_data):
    """Create a new payment record"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO payments (
                        user_id, payment_type, amount, status, description
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    payment_data['user_id'],
                    payment_data['payment_type'],
                    payment_data['amount'],
                    payment_data.get('status', 'pending'),
                    payment_data.get('description', '')
                ))
                payment_id = cur.fetchone()['id']
                conn.commit()
                return payment_id
        except Exception as e:
            conn.rollback()
            st.error(f"Error creating payment: {e}")
            return None
        finally:
            conn.close()
    return None

def update_driver_location(driver_id, location_data):
    """Update a driver's location"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE drivers SET 
                    current_location_area = %s,
                    current_location_lat = %s,
                    current_location_lon = %s
                    WHERE id = %s
                """, (
                    location_data['area'],
                    location_data['lat'],
                    location_data['lon'],
                    driver_id
                ))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            st.error(f"Error updating driver location: {e}")
            return False
        finally:
            conn.close()
    return False

def update_campaign_status(campaign_id, status):
    """Update a campaign's status"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE campaigns SET status = %s
                    WHERE id = %s
                """, (status, campaign_id))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            st.error(f"Error updating campaign status: {e}")
            return False
        finally:
            conn.close()
    return False

def update_campaign_metrics(campaign_id, views, impressions, spent):
    """Update a campaign's metrics"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE campaigns SET 
                    views = views + %s,
                    impressions = impressions + %s,
                    spent = spent + %s
                    WHERE id = %s
                """, (views, impressions, spent, campaign_id))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            st.error(f"Error updating campaign metrics: {e}")
            return False
        finally:
            conn.close()
    return False

# Initialize the database when the module is imported
if 'db_initialized' not in st.session_state:
    initialize_database()
    st.session_state.db_initialized = True