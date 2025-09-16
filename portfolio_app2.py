"""
Complete Interactive Data Science Portfolio
A comprehensive Streamlit application showcasing data science projects,
dashboards, and analytical capabilities.

Author: Your Name
Date: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import re

# Page configuration
st.set_page_config(
    page_title="Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        text-align: center;
        border-radius: 0 0 20px 20px;
    }
    
    .project-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Utility Functions
@st.cache_data
def load_sample_data(data_type):
    """Load sample data for demonstrations"""
    np.random.seed(42)
    
    if data_type == "sales":
        dates = pd.date_range('2023-01-01', periods=365, freq='D')
        return pd.DataFrame({
            'date': dates,
            'product': np.random.choice(['Product A', 'Product B', 'Product C'], 365),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 365),
            'sales_amount': np.random.normal(1000, 300, 365).clip(min=100),
            'quantity_sold': np.random.poisson(20, 365),
            'customer_id': np.random.choice(range(1, 1001), 365)
        })
    
    elif data_type == "web_analytics":
        dates = pd.date_range('2024-01-01', periods=90, freq='D')
        return pd.DataFrame({
            'date': dates,
            'page_views': np.random.poisson(1500, 90) + np.random.normal(0, 200, 90),
            'unique_visitors': np.random.poisson(800, 90) + np.random.normal(0, 100, 90),
            'bounce_rate': np.random.normal(0.35, 0.1, 90).clip(0, 1),
            'conversion_rate': np.random.normal(0.05, 0.02, 90).clip(0, 1)
        })

def main():
    """Main application"""
    
    # Sidebar Navigation
    st.sidebar.title("🚀 Portfolio Navigation")
    
    pages = {
        "🏠 Home": "home",
        "📊 Dashboards": "dashboards",
        "🔧 Data Projects": "data_projects",
        "🌐 Web Applications": "webapps",
        "📋 Documentation": "docs",
        "📞 Contact": "contact"
    }
    
    selected_page = st.sidebar.selectbox("Choose Section:", list(pages.keys()))
    page_key = pages[selected_page]
    
    # Route to pages
    if page_key == "home":
        show_home_page()
    elif page_key == "dashboards":
        show_dashboards_page()
    elif page_key == "data_projects":
        show_data_projects_page()
    elif page_key == "webapps":
        show_webapps_page()
    elif page_key == "docs":
        show_documentation_page()
    elif page_key == "contact":
        show_contact_page()

def show_home_page():
    """Home page with portfolio overview"""
    
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">
            📊 Data Science Portfolio
        </h1>
        <h2 style="font-size: 1.8rem; margin: 0; opacity: 0.9;">
            Transforming Data into Actionable Business Intelligence
        </h2>
        <p style="font-size: 1.3rem; margin-top: 1.5rem; opacity: 0.8;">
            Interactive Dashboards • Advanced Analytics • Full-Stack Solutions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #667eea; margin: 0; font-size: 2.5rem;">25+</h2>
            <p style="margin: 0.5rem 0; font-weight: 600;">Interactive Dashboards</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #667eea; margin: 0; font-size: 2.5rem;">1M+</h2>
            <p style="margin: 0.5rem 0; font-weight: 600;">Records Processed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #667eea; margin: 0; font-size: 2.5rem;">99.9%</h2>
            <p style="margin: 0.5rem 0; font-weight: 600;">System Uptime</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #667eea; margin: 0; font-size: 2.5rem;">5+</h2>
            <p style="margin: 0.5rem 0; font-weight: 600;">Years Experience</p>
        </div>
        """, unsafe_allow_html=True)
    
    # About Section
    st.markdown("## 👨‍💻 About Me")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        I'm a **Senior Data Scientist & Analytics Engineer** specializing in transforming 
        complex data into actionable business insights. My expertise spans the entire data 
        lifecycle, from raw data ingestion to advanced analytics and interactive visualization.
        
        ### 🎯 Core Expertise:
        
        **📊 Business Intelligence & Dashboards**
        - Advanced Power BI development with DAX calculations
        - Grafana infrastructure monitoring and alerting
        - Custom Streamlit applications for real-time analytics
        
        **🔧 Data Engineering & ETL**
        - Python-based ETL pipelines for large-scale data processing
        - SQL optimization and database performance tuning
        - Cloud data architecture (AWS, Azure, GCP)
        
        **🤖 Machine Learning & Analytics**
        - Predictive modeling and forecasting algorithms
        - Customer segmentation and behavioral analysis
        - A/B testing frameworks and statistical analysis
        """)
    
    with col2:
        st.markdown("""
        ### 🏆 Achievements:
        - 🚀 Reduced processing time by **85%**
        - 📈 Improved forecasting accuracy by **40%**
        - 💰 Generated **$5M+** in cost savings
        - 👥 Led teams of **10+** data professionals
        
        ### 🎓 Certifications:
        - Microsoft Certified: Power BI Data Analyst
        - AWS Certified Solutions Architect
        - Google Cloud Professional Data Engineer
        """)
    
    # Featured Projects
    st.markdown("## 🌟 Featured Projects")
    
    tab1, tab2, tab3 = st.tabs(["📊 Dashboards", "🔧 ETL Pipelines", "🌐 Web Apps"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="project-card">
                <h3>🏢 Grafana Infrastructure Monitoring</h3>
                <p>Real-time monitoring dashboard with automated alerting and anomaly detection.</p>
                <div class="success-box">
                    <strong>Impact:</strong> 80% faster incident response, 99.9% uptime
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="project-card">
                <h3>📈 Power BI Sales Analytics</h3>
                <p>Executive dashboard with KPI tracking and sales forecasting.</p>
                <div class="success-box">
                    <strong>Impact:</strong> 40% faster reporting, $500K savings
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="project-card">
                <h3>⚡ High-Performance ETL Pipeline</h3>
                <p>Processing 1M+ records daily with 99.8% accuracy.</p>
                <div class="success-box">
                    <strong>Impact:</strong> 90% reduction in processing time
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="project-card">
                <h3>🔍 Intelligent Log Parser</h3>
                <p>Automated log analysis with pattern recognition.</p>
                <div class="success-box">
                    <strong>Impact:</strong> 95% faster issue detection
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="project-card">
                <h3>📊 CSV Insight Tool</h3>
                <p>Drag-and-drop analysis with automatic chart generation.</p>
                <div class="success-box">
                    <strong>Impact:</strong> Used by 200+ analysts daily
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="project-card">
                <h3>📈 Real-time Log Visualizer</h3>
                <p>Interactive web app for log monitoring and analysis.</p>
                <div class="success-box">
                    <strong>Impact:</strong> Real-time insights, improved reliability
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_dashboards_page():
    """Dashboard projects and demos"""
    
    st.title("📊 Interactive Dashboards Portfolio")
    
    dashboard_tabs = st.tabs(["🏢 Grafana Infrastructure", "📈 Power BI Analytics", "🌐 Traffic Analytics"])
    
    with dashboard_tabs[0]:
        show_grafana_demo()
    
    with dashboard_tabs[1]:
        show_powerbi_demo()
    
    with dashboard_tabs[2]:
        show_traffic_demo()

def show_grafana_demo():
    """Grafana Infrastructure Demo"""
    
    st.markdown("## 🏢 Grafana Infrastructure Monitoring")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Project Overview
        Comprehensive infrastructure monitoring solution with real-time metrics, 
        automated alerting, and predictive analytics for proactive maintenance.
        
        ### Key Features
        - **Real-time Metrics**: CPU, memory, disk, and network monitoring
        - **Automated Alerting**: Smart thresholds with escalation policies
        - **Custom Dashboards**: Role-based views for different teams
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📊 Project Details</h4>
            <p><strong>Duration:</strong> 6 weeks</p>
            <p><strong>Systems Monitored:</strong> 50+ servers</p>
            <p><strong>Metrics/minute:</strong> 10K+</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Live metrics demo
    st.markdown("### 📊 Live Infrastructure Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cpu_usage = np.random.normal(45, 15)
        st.metric("CPU Usage", f"{cpu_usage:.1f}%", f"{np.random.uniform(-2, 2):.1f}%")
    
    with col2:
        memory_usage = np.random.normal(60, 20)
        st.metric("Memory Usage", f"{memory_usage:.1f}%", f"{np.random.uniform(-1, 3):.1f}%")
    
    with col3:
        requests_per_min = np.random.poisson(100)
        st.metric("Requests/min", f"{requests_per_min:,}", f"{np.random.randint(-20, 50)}")
    
    with col4:
        response_time = np.random.exponential(100)
        st.metric("Response Time", f"{response_time:.0f}ms", f"{np.random.randint(-30, 20)}ms")
    
    # Sample infrastructure chart
    dates = pd.date_range('2024-01-01', periods=48, freq='H')
    metrics_data = pd.DataFrame({
        'timestamp': dates,
        'cpu_usage': np.random.normal(45, 15, 48).clip(0, 100),
        'memory_usage': np.random.normal(60, 20, 48).clip(0, 100),
        'response_time': np.random.exponential(100, 48)
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.line(metrics_data, x='timestamp', y=['cpu_usage', 'memory_usage'],
                      title='System Performance - Last 48 Hours')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.line(metrics_data, x='timestamp', y='response_time',
                      title='Response Time Trend')
        st.plotly_chart(fig2, use_container_width=True)

def show_powerbi_demo():
    """Power BI Analytics Demo"""
    
    st.markdown("## 📈 Power BI Sales Analytics")
    
    # Load sales data
    sales_data = load_sample_data("sales")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = sales_data['sales_amount'].sum()
    avg_order = sales_data['sales_amount'].mean()
    total_customers = sales_data['customer_id'].nunique()
    
    with col1:
        st.metric("Total Sales", f"${total_sales:,.0f}", "+12.5%")
    
    with col2:
        st.metric("Average Order", f"${avg_order:.0f}", "+5.2%")
    
    with col3:
        st.metric("Unique Customers", f"{total_customers:,}", "+8.7%")
    
    with col4:
        conversion_rate = 0.045
        st.metric("Conversion Rate", f"{conversion_rate:.1%}", "+1.3%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly sales trend
        monthly_sales = sales_data.groupby(sales_data['date'].dt.to_period('M'))['sales_amount'].sum()
        fig1 = px.line(x=monthly_sales.index.astype(str), y=monthly_sales.values,
                      title='Monthly Sales Trend')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Sales by region
        region_sales = sales_data.groupby('region')['sales_amount'].sum()
        fig2 = px.pie(values=region_sales.values, names=region_sales.index,
                     title='Sales by Region')
        st.plotly_chart(fig2, use_container_width=True)

def show_traffic_demo():
    """Traffic Analytics Demo"""
    
    st.markdown("## 🌐 Traffic Analytics Dashboard")
    
    # Load web analytics data
    traffic_data = load_sample_data("web_analytics")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_views = traffic_data['page_views'].sum()
        st.metric("Total Page Views", f"{total_views:,.0f}", "+15.2%")
    
    with col2:
        avg_bounce = traffic_data['bounce_rate'].mean()
        st.metric("Avg Bounce Rate", f"{avg_bounce:.1%}", "-2.3%")
    
    with col3:
        total_visitors = traffic_data['unique_visitors'].sum()
        st.metric("Total Visitors", f"{total_visitors:,.0f}", "+8.9%")
    
    with col4:
        avg_conversion = traffic_data['conversion_rate'].mean()
        st.metric("Avg Conversion", f"{avg_conversion:.2%}", "+0.8%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.line(traffic_data, x='date', y=['page_views', 'unique_visitors'],
                      title='Traffic Trends')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.scatter(traffic_data, x='bounce_rate', y='conversion_rate',
                         size='unique_visitors', title='Bounce Rate vs Conversion')
        st.plotly_chart(fig2, use_container_width=True)

def show_data_projects_page():
    """Data engineering projects"""
    
    st.title("🔧 Data Engineering Projects")
    
    project_tabs = st.tabs(["⚡ ETL Pipeline", "📝 Log Parser", "🗄️ SQL Optimization"])
    
    with project_tabs[0]:
        show_etl_demo()
    
    with project_tabs[1]:
        show_log_parser_demo()
    
    with project_tabs[2]:
        show_sql_demo()

def show_etl_demo():
    """ETL Pipeline Demo"""
    
    st.markdown("## ⚡ Excel/CSV ETL Pipeline")
    
    st.markdown("""
    ### High-Performance Data Processing System
    Automated ETL pipeline processing 500K+ records per hour with comprehensive 
    data validation and error handling.
    """)
    
    # File upload demo
    uploaded_file = st.file_uploader("Upload CSV for processing", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ Successfully loaded {len(df)} rows, {len(df.columns)} columns")
            
            # Data preview
            st.markdown("### 📊 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Data quality metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Missing Values", f"{df.isnull().sum().sum():,}")
            with col2:
                st.metric("Duplicate Rows", f"{df.duplicated().sum():,}")
            with col3:
                memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
                st.metric("Memory Usage", f"{memory_mb:.1f} MB")
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    else:
        # Show sample processing with generated data
        if st.button("🎲 Demo with Sample Data"):
            sample_data = load_sample_data("sales")
            
            st.success("✅ Processing sample sales data...")
            
            # Processing steps simulation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = [
                "Loading data...",
                "Validating schema...", 
                "Cleaning missing values...",
                "Removing duplicates...",
                "Applying transformations...",
                "Loading to database..."
            ]
            
            for i, step in enumerate(steps):
                status_text.text(step)
                time.sleep(0.5)
                progress_bar.progress((i + 1) * 100 // len(steps))
            
            st.success("✅ ETL pipeline completed successfully!")
            
            # Show results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Records Processed", f"{len(sample_data):,}")
            with col2:
                st.metric("Processing Time", "2.3 seconds")
            with col3:
                st.metric("Data Quality Score", "98.5%")

def show_log_parser_demo():
    """Log Parser Demo"""
    
    st.markdown("## 📝 Intelligent Log Parser")
    
    st.markdown("""
    ### Multi-Format Log Analysis System
    Parse and analyze logs from various sources with pattern recognition and anomaly detection.
    """)
    
    # Sample log formats
    log_formats = {
        "Apache Common": '127.0.0.1 - - [10/Oct/2024:13:55:36 +0000] "GET /index.html HTTP/1.0" 200 2326',
        "Application Log": '2024-10-10 13:55:36,123 INFO [main] com.app.Service - Processing request',
        "JSON Log": '{"timestamp":"2024-10-10T13:55:36Z","level":"ERROR","service":"auth","message":"Login failed"}'
    }
    
    selected_format = st.selectbox("Select log format:", list(log_formats.keys()))
    
    log_input = st.text_area("Enter log entries:", 
                            value=log_formats[selected_format], 
                            height=100)
    
    if st.button("🔍 Parse Logs"):
        st.success("✅ Logs parsed successfully!")
        
        # Simulated parsing results
        parsed_data = pd.DataFrame({
            'Timestamp': ['2024-10-10 13:55:36', '2024-10-10 13:55:37', '2024-10-10 13:55:38'],
            'Level': ['INFO', 'WARNING', 'ERROR'],
            'Source': ['auth', 'api', 'database'],
            'Message': ['User login successful', 'High response time detected', 'Connection failed']
        })
        
        st.dataframe(parsed_data, use_container_width=True)
        
        # Log level distribution
        level_counts = parsed_data['Level'].value_counts()
        fig = px.pie(values=level_counts.values, names=level_counts.index,
                    title='Log Level Distribution')
        st.plotly_chart(fig, use_container_width=True)

def show_sql_demo():
    """SQL Optimization Demo"""
    
    st.markdown("## 🗄️ SQL Data Cleaning & Optimization")
    
    st.markdown("""
    ### Advanced SQL Operations
    Database optimization, query tuning, and automated reporting solutions.
    """)
    
    # Sample SQL queries
    sql_examples = {
        "Data Quality Check": """
-- Comprehensive data quality assessment
SELECT 
    'customers' as table_name,
    COUNT(*) as total_records,
    SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) as null_names,
    SUM(CASE WHEN email NOT LIKE '%@%' THEN 1 ELSE 0 END) as invalid_emails,
    COUNT(DISTINCT customer_id) as unique_customers
FROM customers;
        """,
        "Performance Optimization": """
-- Optimized sales report with proper indexing
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total_sales,
        COUNT(*) as order_count
    FROM orders 
    WHERE order_date >= '2024-01-01'
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    month,
    total_sales,
    order_count,
    LAG(total_sales) OVER (ORDER BY month) as prev_month_sales
FROM monthly_sales
ORDER BY month;
        """,
        "Data Cleaning": """
-- Remove duplicates and standardize data
DELETE FROM customers 
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM customers 
    GROUP BY email, name
);

UPDATE customers 
SET name = INITCAP(TRIM(name)),
    email = LOWER(TRIM(email))
WHERE name != INITCAP(TRIM(name)) 
   OR email != LOWER(TRIM(email));
        """
    }
    
    selected_query = st.selectbox("Select SQL example:", list(sql_examples.keys()))
    
    st.code(sql_examples[selected_query], language='sql')
    
    if st.button("📊 Show Query Results"):
        # Simulated query results
        if selected_query == "Data Quality Check":
            results = pd.DataFrame({
                'table_name': ['customers'],
                'total_records': [5000],
                'null_names': [25],
                'invalid_emails': [15],
                'unique_customers': [4950]
            })
        else:
            results = pd.DataFrame({
                'month': ['2024-01', '2024-02', '2024-03'],
                'total_sales': [125000, 138000, 142000],
                'order_count': [1250, 1380, 1420]
            })
        
        st.dataframe(results, use_container_width=True)

def show_webapps_page():
    """Web applications demos"""
    
    st.title("🌐 Web Applications Portfolio")
    
    webapp_tabs = st.tabs(["📊 CSV Insight Tool", "📈 Log Visualizer"])
    
    with webapp_tabs[0]:
        show_csv_tool()
    
    with webapp_tabs[1]:
        show_log_visualizer()

def show_csv_tool():
    """CSV Analysis Tool Demo"""
    
    st.markdown("## 📊 CSV Insight Tool")
    
    st.markdown("""
    ### Intelligent Data Analysis Platform
    Drag-and-drop CSV analysis with automated insights and interactive visualizations.
    """)
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    # Demo with sample data if no file uploaded
    if not uploaded_file:
        if st.button("🎲 Try with Sample Data"):
            st.session_state.demo_data = load_sample_data("sales")
    
    # Process data
    if uploaded_file or 'demo_data' in st.session_state:
        try:
            # Load data
            if 'demo_data' in st.session_state:
                df = st.session_state.demo_data
                data_source = "Sample Sales Data"
            else:
                df = pd.read_csv(uploaded_file)
                data_source = uploaded_file.name
            
            st.success(f"✅ Loaded {data_source}")
            
            # Quick stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Rows", f"{len(df):,}")
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Missing", f"{df.isnull().sum().sum():,}")
            with col4:
                memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
                st.metric("Size", f"{memory_mb:.1f} MB")
            
            # Data preview
            st.markdown("### 📋 Data Sample")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Automatic visualizations
            st.markdown("### 📊 Auto-Generated Insights")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Distribution of first numeric column
                    fig1 = px.histogram(df, x=numeric_cols[0],
                                      title=f'Distribution of {numeric_cols[0]}')
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Correlation if multiple numeric columns
                    if len(numeric_cols) > 1:
                        fig2 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                                        title=f'{numeric_cols[0]} vs {numeric_cols[1]}')
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        # Show summary stats
                        summary = df[numeric_cols[0]].describe()
                        st.dataframe(summary, use_container_width=True)
            
            # Download options
            st.markdown("### 📥 Export Options")
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = df.to_csv(index=False)
                st.download_button(
                    "📄 Download CSV",
                    data=csv_data,
                    file_name="analyzed_data.csv",
                    mime="text/csv"
                )
            
            with col2:
                if st.button("🔄 Reset Analysis"):
                    if 'demo_data' in st.session_state:
                        del st.session_state.demo_data
                    st.rerun()
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def show_log_visualizer():
    """Log Visualizer Demo"""
    
    st.markdown("## 📈 Real-time Log Visualizer")
    
    st.markdown("""
    ### Interactive Log Monitoring Platform
    Real-time log analysis with filtering, alerting, and performance monitoring.
    """)
    
    # Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        log_levels = st.multiselect(
            "Filter Log Levels:",
            ["DEBUG", "INFO", "WARNING", "ERROR"],
            default=["INFO", "WARNING", "ERROR"]
        )
    
    with col2:
        services = st.multiselect(
            "Filter Services:",
            ["auth", "api", "database", "frontend"],
            default=["auth", "api", "database", "frontend"]
        )
    
    with col3:
        auto_refresh = st.checkbox("Auto-refresh (5s)")
    
    if auto_refresh:
        time.sleep(1)  # Reduced for demo
        st.rerun()
    
    # Generate sample log data
    log_data = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=1000, freq='min'),
        'level': np.random.choice(log_levels if log_levels else ["INFO"], 1000),
        'service': np.random.choice(services if services else ["api"], 1000),
        'response_time': np.random.exponential(100, 1000),
        'status_code': np.random.choice([200, 404, 500], 1000, p=[0.8, 0.15, 0.05])
    })
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        error_count = len(log_data[log_data['level'] == 'ERROR'])
        st.metric("Errors", error_count, f"+{np.random.randint(0, 10)}")
    
    with col2:
        avg_response = log_data['response_time'].mean()
        st.metric("Avg Response", f"{avg_response:.0f}ms", f"+{np.random.randint(-20, 30)}ms")
    
    with col3:
        success_rate = (log_data['status_code'] == 200).mean()
        st.metric("Success Rate", f"{success_rate:.1%}", "+0.5%")
    
    with col4:
        total_requests = len(log_data)
        st.metric("Total Requests", f"{total_requests:,}", f"+{np.random.randint(50, 200)}")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Log levels over time
        hourly_logs = log_data.groupby([log_data['timestamp'].dt.hour, 'level']).size().reset_index(name='count')
        fig1 = px.bar(hourly_logs, x='timestamp', y='count', color='level',
                     title='Log Distribution by Hour')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Response time by service
        service_response = log_data.groupby('service')['response_time'].mean()
        fig2 = px.bar(x=service_response.index, y=service_response.values,
                     title='Average Response Time by Service')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Recent logs table
    st.markdown("### 📝 Recent Log Entries")
    recent_logs = log_data.tail(10)[['timestamp', 'level', 'service', 'response_time', 'status_code']]
    recent_logs['timestamp'] = recent_logs['timestamp'].dt.strftime('%H:%M:%S')
    st.dataframe(recent_logs, use_container_width=True)

def show_documentation_page():
    """Documentation and resources"""
    
    st.title("📋 Documentation & Resources")
    
    doc_tabs = st.tabs(["📖 Technical Guides", "💰 Services & Pricing", "📁 Resources"])
    
    with doc_tabs[0]:
        st.markdown("## 📖 Technical Documentation")
        
        guide_sections = st.selectbox(
            "Select documentation:",
            ["Getting Started", "Dashboard Development", "ETL Setup", "API Integration"]
        )
        
        if guide_sections == "Getting Started":
            st.markdown("""
            ### 🚀 Getting Started Guide
            
            #### Prerequisites
            - Python 3.8 or higher
            - Basic knowledge of data analysis
            
            #### Installation
            ```bash
            # Clone repository
            git clone https://github.com/yourname/portfolio
            
            # Install dependencies
            pip install -r requirements.txt
            
            # Run application
            streamlit run portfolio_app.py
            ```
            
            #### Quick Example
            ```python
            import pandas as pd
            import plotly.express as px
            
            # Load data
            df = pd.read_csv('data.csv')
            
            # Create visualization
            fig = px.scatter(df, x='x', y='y')
            fig.show()
            ```
            """)
        
        elif guide_sections == "Dashboard Development":
            st.markdown("""
            ### 📊 Dashboard Development Guide
            
            #### Architecture
            - **Data Layer**: Database connections and processing
            - **Logic Layer**: Business calculations and metrics
            - **UI Layer**: Streamlit components and visualizations
            
            #### Best Practices
            - Use caching for expensive operations
            - Implement proper error handling
            - Design for mobile responsiveness
            - Follow consistent styling patterns
            """)
    
    with doc_tabs[1]:
        st.markdown("## 💰 Services & Pricing")
        
        pricing_data = {
            'Service': [
                'Dashboard Development',
                'ETL Pipeline Setup',
                'Data Analysis',
                'Web Application',
                'Consultation'
            ],
            'Duration': ['2-4 weeks', '3-6 weeks', '1-3 weeks', '4-8 weeks', 'Hourly'],
            'Starting Price': ['$2,500', '$4,000', '$1,500', '$5,000', '$150/hour'],
            'Deliverables': [
                'Custom dashboard + training',
                'Full pipeline + monitoring',
                'Reports + recommendations',
                'Complete app + deployment',
                'Expert guidance'
            ]
        }
        
        pricing_df = pd.DataFrame(pricing_data)
        st.dataframe(pricing_df, use_container_width=True)
        
        st.markdown("""
        ### 📋 What's Included
        - ✅ Complete documentation
        - ✅ Source code access
        - ✅ 30-day support
        - ✅ Team training
        - ✅ Performance optimization
        """)
    
    with doc_tabs[2]:
        st.markdown("## 📁 Project Resources")
        
        st.markdown("### 📥 Available Downloads")
        
        resources = [
            ("Portfolio Presentation", "Comprehensive project overview"),
            ("Technical Documentation", "Detailed implementation guides"),
            ("Sample Code Templates", "Reusable code snippets"),
            ("Best Practices Guide", "Industry standards and guidelines")
        ]
        
        for title, description in resources:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{title}**")
                st.write(description)
            with col2:
                st.button("📥 Download", key=title)

def show_contact_page():
    """Contact form and information"""
    
    st.title("📞 Contact & Consultation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Let's Transform Your Data Together
        
        Ready to unlock the power of your data? I specialize in creating custom solutions 
        that drive business value and operational efficiency.
        
        **What I Offer:**
        - 📊 Interactive dashboard development
        - 🔧 ETL pipeline design and implementation
        - 🌐 Custom web application development
        - 📈 Advanced analytics and reporting
        - ☁️ Cloud architecture and optimization
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📊 Quick Facts</h4>
            <p><strong>Response Time:</strong> <24 hours</p>
            <p><strong>Project Success Rate:</strong> 98%</p>
            <p><strong>Client Satisfaction:</strong> 4.9/5</p>
            <p><strong>Years Experience:</strong> 5+</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Contact Form
    st.markdown("### 📝 Get In Touch")
    
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            company = st.text_input("Company")
        
        with col2:
            phone = st.text_input("Phone")
            budget = st.selectbox("Budget Range", 
                                 ["< $5K", "$5K-$15K", "$15K-$50K", "> $50K"])
            timeline = st.selectbox("Timeline", 
                                   ["ASAP", "1 month", "2-3 months", "Flexible"])
        
        services = st.multiselect(
            "Services Needed *",
            ["Dashboard", "ETL Pipeline", "Web App", "Analysis", "Consultation"]
        )
        
        message = st.text_area("Project Description *", height=100)
        
        submitted = st.form_submit_button("🚀 Send Inquiry", type="primary")
        
        if submitted:
            if name and email and services and message:
                st.success("""
                ✅ **Thank you for your inquiry!**
                
                I'll respond within 24 hours with:
                - Initial project assessment
                - Proposed timeline and approach
                - Detailed cost estimate
                - Next steps for consultation
                """)
                st.balloons()
            else:
                st.error("Please fill in all required fields (*)")
    
    # Contact Options
    st.markdown("### 📱 Direct Contact")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📧 Email**  
        your.email@example.com  
        *Response: 24 hours*
        """)
    
    with col2:
        st.markdown("""
        **📱 Phone**  
        +1 (555) 123-4567  
        *Hours: 9 AM - 6 PM EST*
        """)
    
    with col3:
        st.markdown("""
        **💼 LinkedIn**  
        linkedin.com/in/yourname  
        *Professional networking*
        """)
    
    # FAQ
    st.markdown("### ❓ Frequently Asked Questions")
    
    with st.expander("What's your typical project timeline?"):
        st.write("""
        Project timelines depend on complexity:
        - **Dashboards:** 2-4 weeks
        - **ETL Pipelines:** 3-6 weeks  
        - **Web Applications:** 4-8 weeks
        - **Data Analysis:** 1-3 weeks
        """)
    
    with st.expander("Do you offer fixed-price or hourly billing?"):
        st.write("""
        I offer both options:
        - **Fixed-price** for well-defined projects
        - **Hourly consulting** at $150/hour
        - **Hybrid approach** with milestones
        """)
    
    with st.expander("What technologies do you work with?"):
        st.write("""
        Core technologies include:
        - **Languages:** Python, SQL, JavaScript
        - **Databases:** PostgreSQL, MySQL, MongoDB
        - **Visualization:** Plotly, Power BI, Tableau
        - **Cloud:** AWS, Azure, Google Cloud
        """)

# Run the application
if __name__ == "__main__":
    main()
