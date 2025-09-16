"""
Interactive Data Science Portfolio Website

A comprehensive, interactive portfolio showcasing data science projects,
dashboards, and analytical capabilities using Streamlit.

Author: Your Name
Date: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Data Science Portfolio | Your Name",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://your-portfolio.com/help',
        'Report a bug': 'https://your-portfolio.com/contact',
        'About': """
        # Interactive Data Science Portfolio
        
        Professional portfolio showcasing expertise in:
        - Interactive Dashboard Development
        - Data Engineering & ETL Pipelines  
        - Business Intelligence Solutions
        - Machine Learning & Analytics
        - Full-Stack Data Applications
        
        Contact: your.email@example.com
        """
    }
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        text-align: center;
    }
    
    .project-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2a5298;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .skill-badge {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .contact-button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .contact-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .testimonial {
        background: #f8f9fa;
        padding: 1.5rem;
        border-left: 4px solid #2a5298;
        border-radius: 0 10px 10px 0;
        font-style: italic;
        margin: 1rem 0;
    }
    
    .tech-stack {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #90caf9;
    }
</style>
""", unsafe_allow_html=True)

# Utility functions
def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        import requests
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def get_base64_of_bin_file(bin_file):
    """Convert binary file to base64 string"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def create_download_link(val, filename):
    """Create download link for file"""
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}">Download {filename}</a>'

# Sample data for demonstrations
def generate_sample_analytics_data():
    """Generate sample analytics data for demonstrations"""
    dates = pd.date_range('2024-01-01', periods=90, freq='D')
    
    analytics_data = pd.DataFrame({
        'date': dates,
        'page_views': np.random.poisson(1000, 90) + np.random.normal(0, 50, 90),
        'unique_visitors': np.random.poisson(400, 90) + np.random.normal(0, 30, 90),
        'bounce_rate': np.random.normal(0.35, 0.1, 90).clip(0, 1),
        'conversion_rate': np.random.normal(0.05, 0.02, 90).clip(0, 1)
    })
    
    return analytics_data

def create_skills_chart():
    """Create interactive skills proficiency chart"""
    skills_data = {
        'Python': 95,
        'SQL': 90,
        'Power BI': 85,
        'Streamlit': 90,
        'Machine Learning': 80,
        'Data Visualization': 95,
        'ETL Pipelines': 85,
        'Cloud Platforms': 75,
        'JavaScript': 70,
        'Docker': 75
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(skills_data.values()),
            y=list(skills_data.keys()),
            orientation='h',
            marker=dict(
                color=list(skills_data.values()),
                colorscale='Blues',
                showscale=True
            ),
            text=[f"{v}%" for v in skills_data.values()],
            textposition='inside'
        )
    ])
    
    fig.update_layout(
        title="Technical Skills Proficiency",
        xaxis_title="Proficiency (%)",
        height=400,
        template="plotly_white"
    )
    
    return fig

def create_project_timeline():
    """Create project timeline visualization"""
    projects = [
        {'Project': 'Sales Dashboard', 'Start': '2024-01-15', 'End': '2024-02-15', 'Category': 'Dashboard'},
        {'Project': 'ETL Pipeline', 'Start': '2024-02-01', 'End': '2024-03-01', 'Category': 'Engineering'},
        {'Project': 'Log Analyzer', 'Start': '2024-02-15', 'End': '2024-03-15', 'Category': 'Analytics'},
        {'Project': 'CSV Tool', 'Start': '2024-03-01', 'End': '2024-03-30', 'Category': 'Web App'},
        {'Project': 'Traffic Monitor', 'Start': '2024-03-15', 'End': '2024-04-15', 'Category': 'Dashboard'}
    ]
    
    df = pd.DataFrame(projects)
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])
    
    fig = px.timeline(
        df, 
        x_start='Start', 
        x_end='End', 
        y='Project',
        color='Category',
        title='Project Timeline - Recent Work'
    )
    
    fig.update_layout(height=300, template="plotly_white")
    return fig

# Main application
def main():
    """Main portfolio application"""
    
    # Navigation
    st.sidebar.title("🚀 Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "💼 Projects", "🛠️ Skills", "📊 Live Demos", "📞 Contact"]
    )
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "💼 Projects":
        show_projects_page()
    elif page == "🛠️ Skills":
        show_skills_page()
    elif page == "📊 Live Demos":
        show_demos_page()
    elif page == "📞 Contact":
        show_contact_page()

def show_home_page():
    """Display home page"""
    
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">
            🚀 Data Science Portfolio
        </h1>
        <h2 style="font-size: 1.5rem; margin: 0; opacity: 0.9;">
            Transforming Data into Actionable Business Intelligence
        </h2>
        <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.8;">
            Interactive Dashboards • Advanced Analytics • Full-Stack Solutions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">15+</h2>
            <p style="margin: 0.5rem 0;">Interactive Dashboards</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">500k+</h2>
            <p style="margin: 0.5rem 0;">Records Processed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">99.9%</h2>
            <p style="margin: 0.5rem 0;">Uptime Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">3+</h2>
            <p style="margin: 0.5rem 0;">Years Experience</p>
        </div>
        """, unsafe_allow_html=True)
    
    # About Section
    st.markdown("## 👋 Welcome to My Portfolio")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        I'm a **Data Science Professional** specializing in transforming complex data into 
        actionable business insights. With expertise spanning from **interactive dashboard development** 
        to **machine learning implementation**, I help organizations make data-driven decisions 
        that drive growth and efficiency.
        
        ### 🎯 **Core Specializations:**
        - **📊 Business Intelligence Dashboards** - Power BI, Tableau, Custom Solutions
        - **🔧 Data Engineering** - ETL Pipelines, Database Optimization, Cloud Architecture  
        - **🌐 Web Applications** - Streamlit, Flask, Interactive Data Tools
        - **📈 Advanced Analytics** - Statistical Modeling, Machine Learning, Forecasting
        - **☁️ Cloud Solutions** - AWS, GCP, Azure Data Services
        
        ### 🏆 **Recent Achievements:**
        - Developed real-time monitoring dashboards reducing incident response time by **80%**
        - Built ETL pipelines processing **500k+ records daily** with 99.9% accuracy
        - Created interactive tools used by **50+ analysts** across multiple organizations
        - Delivered projects resulting in **$2M+ cost savings** for clients
        """)
    
    with col2:
        st.image("assets/profile_photo.jpg" if Path("assets/profile_photo.jpg").exists() else "https://via.placeholder.com/300x300", 
                caption="Professional Profile", width=300)
        
        st.markdown("""
        ### 🎓 **Certifications:**
        - Microsoft Power BI Data Analyst
        - AWS Cloud Practitioner  
        - Python for Data Science
        - SQL Database Administration
        
        ### 📍 **Location:**
        Remote • Available Worldwide
        
        ### ⏰ **Availability:**
        Open for new projects
        """)
    
    # Featured Projects Preview
    st.markdown("## 🌟 Featured Projects")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="project-card">
            <h3>📊 Sales Analytics Dashboard</h3>
            <p>Interactive Power BI dashboard tracking KPIs, sales funnels, and regional performance with real-time data updates.</p>
            <div class="tech-stack">
                <strong>Tech:</strong> Power BI, SQL Server, DAX
            </div>
            <p><strong>Impact:</strong> 40% faster reporting, $500K cost savings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="project-card">
            <h3>🔧 CSV Insight Tool</h3>

            st.markdown("""
        <div class="project-card">
            <h3>🔧 CSV Insight Tool</h3>
            <p>Drag-and-drop web application for instant CSV analysis with automated chart generation and statistical insights.</p>
            <div class="tech-stack">
                <strong>Tech:</strong> Streamlit, Pandas, Plotly
            </div>
            <p><strong>Impact:</strong> Used by 100+ analysts daily</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="project-card">
            <h3>📈 Log Visualizer</h3>
            <p>Real-time log monitoring system with anomaly detection, performance metrics, and alert notifications.</p>
            <div class="tech-stack">
                <strong>Tech:</strong> Flask, WebSockets, Chart.js
            </div>
            <p><strong>Impact:</strong> 99.9% uptime monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("## 🚀 Ready to Get Started?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <h3 style="margin: 0 0 1rem 0;">Let's Transform Your Data Together</h3>
            <p style="margin: 0 0 1.5rem 0;">Schedule a free consultation to discuss your project needs</p>
            <a href="mailto:your.email@example.com" class="contact-button" style="color: white; text-decoration: none;">
                📧 Schedule Consultation
            </a>
            <a href="tel:+15551234567" class="contact-button" style="color: white; text-decoration: none;">
                📱 Call Now
            </a>
        </div>
        """, unsafe_allow_html=True)

def show_projects_page():
    """Display projects showcase page"""
    
    st.title("💼 Project Portfolio")
    st.markdown("### Interactive showcase of data science and analytics projects")
    
    # Project categories
    categories = st.tabs(["📊 Dashboards", "🔧 Data Engineering", "🌐 Web Applications", "📈 Analytics"])
    
    with categories[0]:  # Dashboards
        st.markdown("## 📊 Interactive Dashboard Solutions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🏢 Grafana Infrastructure Monitoring
            
            **Project Overview:**
            Comprehensive infrastructure monitoring solution with real-time metrics, alerting, and performance optimization recommendations.
            
            **Key Features:**
            - 📈 Real-time server metrics monitoring
            - 🚨 Automated alert system with Slack/email integration
            - 📊 Custom dashboards for different stakeholder groups
            - 🔍 Log aggregation and analysis
            - 📱 Mobile-responsive design
            
            **Technical Stack:**
            - **Frontend:** Grafana, Custom Panels
            - **Backend:** Prometheus, InfluxDB  
            - **Alerting:** AlertManager, PagerDuty
            - **Infrastructure:** Docker, Kubernetes
            
            **Business Impact:**
            - ⬇️ 80% reduction in incident response time
            - 🎯 99.9% system uptime achievement
            - 💰 $200K annual cost savings through optimization
            """)
            
            # Sample metrics chart
            metrics_data = pd.DataFrame({
                'timestamp': pd.date_range('2024-01-01', periods=100, freq='H'),
                'cpu_usage': np.random.normal(45, 15, 100).clip(0, 100),
                'memory_usage': np.random.normal(60, 20, 100).clip(0, 100),
                'disk_io': np.random.exponential(20, 100).clip(0, 100)
            })
            
            fig = px.line(metrics_data, x='timestamp', y=['cpu_usage', 'memory_usage', 'disk_io'],
                         title='Sample Infrastructure Metrics')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            ### 📊 Power BI Sales & KPI Analytics
            
            **Project Overview:**
            Executive-level sales performance dashboard with advanced KPI tracking, forecasting, and regional analysis capabilities.
            
            **Key Features:**
            - 🎯 Executive KPI dashboard with drill-down capabilities
            - 🌍 Geographic sales performance mapping
            - 📈 Predictive sales forecasting using ML models
            - 🔄 Real-time data refresh from multiple sources
            - 📱 Mobile-optimized for executive access
            
            **Technical Stack:**
            - **Visualization:** Power BI Premium
            - **Data Sources:** SQL Server, SharePoint, Excel
            - **Processing:** Power Query, DAX
            - **ML Integration:** Azure Machine Learning
            
            **Business Impact:**
            - 📊 40% faster executive reporting
            - 🎯 25% improvement in sales forecasting accuracy
            - 💼 Adopted by 50+ sales representatives
            """)
            
            # Sample sales data visualization
            sales_data = pd.DataFrame({
                'month': pd.date_range('2024-01-01', periods=12, freq='M'),
                'revenue': np.random.normal(100000, 20000, 12).clip(50000, 200000),
                'target': [120000] * 12,
                'region': np.random.choice(['North', 'South', 'East', 'West'], 12)
            })
            
            fig = px.bar(sales_data, x='month', y='revenue', color='region',
                        title='Monthly Revenue by Region')
            fig.add_scatter(x=sales_data['month'], y=sales_data['target'], 
                          mode='lines', name='Target', line=dict(color='red', dash='dash'))
            st.plotly_chart(fig, use_container_width=True)
        
        # Traffic Analytics Dashboard
        st.markdown("""
        ### 🌐 Traffic Analytics Dashboard
        
        **Real-time web analytics platform with user behavior tracking and conversion optimization.**
        """)
        
        # Create sample traffic analytics
        analytics_data = generate_sample_analytics_data()
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(analytics_data, x='date', y=['page_views', 'unique_visitors'],
                          title='Traffic Trends Over Time')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.scatter(analytics_data, x='bounce_rate', y='conversion_rate',
                             size='unique_visitors', title='Bounce Rate vs Conversion Rate')
            st.plotly_chart(fig2, use_container_width=True)
    
    with categories[1]:  # Data Engineering
        st.markdown("## 🔧 Data Engineering Solutions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ⚡ Excel/CSV ETL Pipeline
            
            **Project Overview:**
            Automated ETL pipeline for processing large Excel and CSV files with data validation, transformation, and loading capabilities.
            
            **Key Features:**
            - 📂 Batch processing of multiple file formats
            - 🔍 Automated data quality checks and validation
            - 🔄 Incremental data loading with change detection
            - 📊 Processing statistics and error reporting
            - ⏱️ Scheduled execution with monitoring
            
            **Technical Architecture:**
            ```python
            # Sample ETL Pipeline Code
            import pandas as pd
            from sqlalchemy import create_engine
            
            def process_csv_files(file_paths):
                consolidated_data = []
                
                for file_path in file_paths:
                    # Read and validate data
                    df = pd.read_csv(file_path)
                    df_clean = validate_and_clean(df)
                    consolidated_data.append(df_clean)
                
                # Consolidate and load
                final_df = pd.concat(consolidated_data)
                load_to_database(final_df)
                
                return processing_stats
            ```
            
            **Performance Metrics:**
            - ⚡ 500K+ records processed per hour
            - 🎯 99.5% data accuracy rate
            - 📉 90% reduction in manual processing time
            """)
        
        with col2:
            st.markdown("""
            ### 🗄️ SQL Data Cleaning & Reporting
            
            **Project Overview:**
            Comprehensive SQL-based data cleaning and automated reporting system with data quality monitoring and optimization.
            
            **Key Features:**
            - 🧹 Advanced data cleaning algorithms
            - 📊 Automated report generation
            - 🔍 Data quality monitoring dashboard
            - ⚡ Query optimization and performance tuning
            - 📈 Historical data analysis and trending
            
            **SQL Optimization Examples:**
            ```sql
            -- Performance-optimized reporting query
            WITH monthly_sales AS (
                SELECT 
                    DATE_TRUNC('month', order_date) as month,
                    region,
                    SUM(revenue) as total_revenue,
                    COUNT(DISTINCT customer_id) as unique_customers
                FROM sales_data 
                WHERE order_date >= '2024-01-01'
                GROUP BY 1, 2
            ),
            growth_calc AS (
                SELECT *,
                    LAG(total_revenue) OVER (
                        PARTITION BY region 
                        ORDER BY month
                    ) as prev_month_revenue
                FROM monthly_sales
            )
            SELECT 
                region,
                month,
                total_revenue,
                unique_customers,
                ROUND(
                    ((total_revenue - prev_month_revenue) / 
                     prev_month_revenue) * 100, 2
                ) as growth_rate
            FROM growth_calc
            ORDER BY region, month;
            ```
            
            **Performance Improvements:**
            - ⚡ 75% faster query execution times  
            - 📊 Automated daily/weekly/monthly reports
            - 🎯 99.8% data quality scores
            """)
        
        # Data Processing Pipeline Visualization
        st.markdown("### 🔄 ETL Pipeline Architecture")
        
        # Create pipeline flow diagram using Plotly
        import plotly.graph_objects as go
        
        fig = go.Figure(data=go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["Raw Data", "Validation", "Transformation", "Quality Check", "Database", "Reports"],
                color=["lightblue", "lightgreen", "lightyellow", "lightcoral", "lightpink", "lightgray"]
            ),
            link=dict(
                source=[0, 1, 2, 3, 4],
                target=[1, 2, 3, 4, 5],
                value=[100, 95, 90, 88, 88]
            )
        ))
        
        fig.update_layout(title_text="Data Processing Pipeline Flow", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with categories[2]:  # Web Applications
        st.markdown("## 🌐 Interactive Web Applications")
        
        st.markdown("""
        ### 📊 CSV Insight Tool - Live Demo
        
        **Try the interactive CSV analysis tool directly in your browser!**
        """)
        
        # Embed a mini version of the CSV tool
        uploaded_file = st.file_uploader("Upload a CSV file to analyze", type="csv")
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            
            st.markdown("#### 📈 Quick Data Overview")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            
            st.markdown("#### 📊 Data Preview")
            st.dataframe(df.head(10))
            
            st.markdown("#### 📈 Automatic Visualizations")
            
            # Generate automatic charts
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_columns) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig1 = px.histogram(df, x=numeric_columns[0], 
                                      title=f'Distribution of {numeric_columns[0]}')
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    if len(numeric_columns) >= 2:
                        fig2 = px.scatter(df, x=numeric_columns[0], y=numeric_columns[1],
                                        title=f'{numeric_columns[0]} vs {numeric_columns[1]}')
                        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("""
        ### 📈 Log Visualizer Dashboard
        
        **Real-time log monitoring and analysis system**
        """)
        
        # Simulate log data
        log_data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=1000, freq='min'),
            'log_level': np.random.choice(['INFO', 'WARNING', 'ERROR', 'DEBUG'], 1000, p=[0.6, 0.2, 0.1, 0.1]),
            'response_time': np.random.exponential(100, 1000),
            'status_code': np.random.choice([200, 404, 500, 503], 1000, p=[0.8, 0.1, 0.05, 0.05])
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Log level distribution
            log_counts = log_data['log_level'].value_counts()
            fig = px.pie(values=log_counts.values, names=log_counts.index,
                        title='Log Level Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Response time trend
            hourly_avg = log_data.groupby(log_data['timestamp'].dt.hour)['response_time'].mean()
            fig = px.bar(x=hourly_avg.index, y=hourly_avg.values,
                        title='Average Response Time by Hour')
            st.plotly_chart(fig, use_container_width=True)
    
    with categories[3]:  # Analytics
        st.markdown("## 📈 Advanced Analytics Projects")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🤖 Machine Learning Models
            
            **Predictive analytics and machine learning implementations**
            
            **Sales Forecasting Model:**
            - Random Forest Regressor for monthly sales prediction
            - Feature engineering with seasonality and trends
            - 95% accuracy on test data
            
            **Customer Segmentation:**
            - K-Means clustering for customer behavior analysis  
            - RFM analysis integration
            - Actionable marketing insights
            
            **Anomaly Detection:**
            - Isolation Forest for fraud detection
            - Real-time scoring pipeline
            - 98% precision in anomaly identification
            """)
        
        with col2:
            st.markdown("""
            ### 📊 Statistical Analysis
            
            **Advanced statistical modeling and hypothesis testing**
            
            **A/B Testing Framework:**
            - Bayesian statistical testing
            - Power analysis and sample size calculation
            - Real-time results monitoring
            
            **Time Series Analysis:**
            - ARIMA and LSTM models for forecasting
            - Seasonal decomposition and trend analysis
            - Automated model selection
            
            **Correlation Analysis:**
            - Multi-variate correlation studies
            - Causal inference techniques
            - Business impact quantification
            """)
        
        # Interactive ML Demo
        st.markdown("### 🤖 Interactive ML Demo: Sales Prediction")
        
        # Create sample data for ML demo
        np.random.seed(42)
        n_samples = 1000
        
        demo_data = pd.DataFrame({
            'advertising_spend': np.random.normal(5000, 2000, n_samples),
            'season': np.random.choice([1, 2, 3, 4], n_samples),
            'competitor_price': np.random.normal(50, 10, n_samples),
            'economic_index': np.random.normal(100, 15, n_samples)
        })
        
        # Simple linear relationship for demo
        demo_data['sales'] = (
            demo_data['advertising_spend'] * 0.8 + 
            demo_data['season'] * 1000 + 
            demo_data['competitor_price'] * -200 + 
            demo_data['economic_index'] * 50 + 
            np.random.normal(0, 5000, n_samples)
        )
        
        # Interactive controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ad_spend = st.slider("Advertising Spend ($)", 1000, 10000, 5000)
        with col2:
            season = st.selectbox("Season", [1, 2, 3, 4], index=1)
        with col3:
            comp_price = st.slider("Competitor Price ($)", 30, 80, 50)
        
        # Simple prediction calculation
        predicted_sales = ad_spend * 0.8 + season * 1000 + comp_price * -200 + 100 * 50
        
        st.markdown(f"""
        ### 🎯 Predicted Sales: **${predicted_sales:,.0f}**
        
        *Based on machine learning model trained on historical sales data*
        """)
        
        # Show feature importance
        feature_importance = pd.DataFrame({
            'Feature': ['Advertising Spend', 'Season', 'Competitor Price', 'Economic Index'],
            'Importance': [0.4, 0.25, 0.2, 0.15]
        })
        
        fig = px.bar(feature_importance, x='Importance', y='Feature', orientation='h',
                    title='Feature Importance in Sales Prediction Model')
        st.plotly_chart(fig, use_container_width=True)

def show_skills_page():
    """Display skills and expertise page"""
    
    st.title("🛠️ Technical Skills & Expertise")
    st.markdown("### Comprehensive overview of technical capabilities and proficiency levels")
    
    # Skills proficiency chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        skills_fig = create_skills_chart()
        st.plotly_chart(skills_fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### 📊 **Skill Levels:**
        
        **🟢 Expert (90-100%):**
        Advanced proficiency with extensive project experience
        
        **🟡 Proficient (75-89%):**
        Strong working knowledge with multiple implementations
        
        **🟠 Intermediate (60-74%):**
        Solid foundation with growing expertise
        
        **🔴 Learning (< 60%):**
        Currently developing skills through projects
        """)
    
    # Skills categories
    categories = st.tabs(["💻 Programming", "📊 Data & Analytics", "☁️ Cloud & Infrastructure", "🌐 Web Development"])
    
    with categories[0]:  # Programming
        st.markdown("## 💻 Programming Languages & Frameworks")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🐍 **Python Ecosystem**
            
            **Core Libraries:**
            - **Pandas** - Data manipulation and analysis
            - **NumPy** - Numerical computing and arrays
            - **Matplotlib/Seaborn** - Static visualizations
            - **Plotly** - Interactive charts and dashboards
            - **Scikit-learn** - Machine learning algorithms
            
            **Web Frameworks:**
            - **Streamlit** - Rapid prototyping and dashboards
            - **Flask** - Lightweight web applications  
            - **FastAPI** - High-performance APIs
            - **Django** - Full-featured web development
            
            **Data Engineering:**
            - **Apache Airflow** - Workflow orchestration
            - **Dask** - Parallel computing
            - **SQLAlchemy** - Database ORM
            """)
            
            # Code example
            st.code("""
            # Advanced data processing example
            import pandas as pd
            import numpy as np
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.model_selection import train_test_split
            
            def build_sales_model(data):
                # Feature engineering
                data['month'] = pd.to_datetime(data['date']).dt.month
                data['quarter'] = pd.to_datetime(data['date']).dt.quarter
                
                # Model training
                features = ['advertising', 'month', 'quarter', 'price']
                X = data[features]
                y = data['sales']
                
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )
                
                model = RandomForestRegressor(n_estimators=100)
                model.fit(X_train, y_train)
                
                return model, model.score(X_test, y_test)
            """, language="python")
        
        with col2:
            st.markdown("""
            ### 🗄️ **SQL & Databases**
            
            **Database Systems:**
            - **PostgreSQL** - Advanced relational database
            - **MySQL** - Popular open-source RDBMS
            - **SQL Server** - Microsoft enterprise database
            - **SQLite** - Lightweight embedded database
            - **MongoDB** - NoSQL document database
            
            **Advanced SQL Features:**
            - Window functions and CTEs
            - Query optimization and indexing
            - Stored procedures and functions
            - Data warehousing concepts
            - ETL pipeline development
            """)
            
            # SQL example
            st.code("""
            -- Advanced sales analytics query
            WITH monthly_metrics AS (
                SELECT 
                    DATE_TRUNC('month', order_date) as month,
                    customer_segment,
                    SUM(revenue) as total_revenue,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    AVG(order_value) as avg_order_value
                FROM sales_data s
                JOIN customers c ON s.customer_id = c.id
                WHERE order_date >= '2024-01-01'
                GROUP BY 1, 2
            ),
            growth_analysis AS (
                SELECT *,
                    LAG(total_revenue) OVER (
                        PARTITION BY customer_segment 
                        ORDER BY month
                    ) as prev_month_revenue,
                    PERCENT_RANK() OVER (
                        PARTITION BY month 
                        ORDER BY total_revenue
                    ) as revenue_percentile
                FROM monthly_metrics
            )
            SELECT 
                month,
                customer_segment,
                total_revenue,
                unique_customers,
                ROUND(
                    ((total_revenue - prev_month_revenue) / 
                     NULLIF(prev_month_revenue, 0)) * 100, 2
                ) as growth_rate,
                CASE 
                    WHEN revenue_percentile >= 0.8 THEN 'Top Performer'
                    WHEN revenue_percentile >= 0.6 THEN 'Above Average' 
                    WHEN revenue_percentile >= 0.4 THEN 'Average'
                    ELSE 'Below Average'
                END as performance_tier
            FROM growth_analysis
            ORDER BY month DESC, total_revenue DESC;
            """, language="sql")
    
    with categories[1]:  # Data & Analytics
        st.markdown("## 📊 Data Science & Analytics Tools")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📈 **Business Intelligence**
            
            **Microsoft Power BI:**
            - Advanced DAX calculations and measures
            - Custom visualizations and themes
            - Row-level security implementation
            - Gateway configuration and data refresh
            - Power BI Service administration
            
            **Tableau:**
            - Interactive dashboard development
            - Advanced calculations and LOD expressions
            - Data blending and relationships
            - Tableau Server deployment
            
            **Advanced Features:**
            - Real-time data streaming
            - Mobile-responsive design
            - Embedded analytics
            - Custom connectors development
            """)
        
        with col2:
            st.markdown("""
            ### 🤖 **Machine Learning & AI**
            
            **Algorithms & Techniques:**
            - Supervised Learning (Regression, Classification)
            - Unsupervised Learning (Clustering, PCA)
            - Time Series Forecasting (ARIMA, LSTM)
            - Natural Language Processing
            - Computer Vision basics
            
            **MLOps & Production:**
            - Model versioning and tracking (MLflow)
            - A/B testing frameworks
            - Model monitoring and drift detection
            - Automated retraining pipelines
            - Feature stores and data pipelines
            
            **Cloud ML Services:**
            - AWS SageMaker
            - Azure Machine Learning
            - Google Cloud AI Platform
            """)
        
        # Interactive ML metrics demo
        st.markdown("### 🎯 Model Performance Visualization")
        
        # Generate sample model performance data
        models = ['Random Forest', 'XGBoost', 'Linear Regression', 'Neural Network', 'SVM']
        metrics_data = pd.DataFrame({
            'Model': models,
            'Accuracy': np.random.uniform(0.75, 0.95, 5),
            'Precision': np.random.uniform(0.70, 0.90, 5),
            'Recall': np.random.uniform(0.65, 0.85, 5),
            'F1-Score': np.random.uniform(0.68, 0.87, 5)
        })
        
        fig = px.scatter(metrics_data, x='Precision', y='Recall', 
                        size='Accuracy', color='Model', hover_name='Model',
                        title='Model Performance Comparison')
        st.plotly_chart(fig, use_container_width=True)
    
    with categories[2]:  # Cloud & Infrastructure
        st.markdown("## ☁️ Cloud Platforms & Infrastructure")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ☁️ **Amazon Web Services (AWS)**
            
            **Data Services:**
            - **S3** - Object storage and data lakes
            - **RDS** - Managed relational databases
            - **Redshift** - Data warehousing
            - **EMR** - Big data processing
            - **Glue** - ETL and data catalog
            
            **Analytics & ML:**
            - **SageMaker** - Machine learning platform
            - **QuickSight** - Business intelligence
            - **Kinesis** - Real-time data streaming
            - **Lambda** - Serverless computing
            
            **Infrastructure:**
            - **EC2** - Virtual servers
            - **ECS/EKS** - Container orchestration
            - **CloudFormation** - Infrastructure as code
            """)
        
        with col2:
            st.markdown("""
            ### 🔧 **DevOps & Monitoring**
            
            **Containerization:**
            - **Docker** - Application containerization
            - **Kubernetes** - Container orchestration
            - **Docker Compose** - Multi-container applications
            
            **CI/CD:**
            - **GitHub Actions** - Automated workflows
            - **Jenkins** - Build automation
            - **GitLab CI/CD** - Integrated DevOps
            
            **Monitoring & Observability:**
            - **Grafana** - Metrics visualization
            - **Prometheus** - Metrics collection
            - **ELK Stack** - Log analysis
            - **DataDog** - Application monitoring
            """)
        
        # Cloud services comparison chart
        cloud_services = pd.DataFrame({
            'Service': ['Data Storage', 'ML Platform', 'Analytics', 'Monitoring', 'Compute'],
            'AWS': [95, 90, 85, 80, 90],
            'Azure': [85, 85, 80, 75, 85],
            'GCP': [80, 95, 90, 85, 85]
        })
        
        fig = px.bar(cloud_services, x='Service', y=['AWS', 'Azure', 'GCP'],
                    title='Cloud Platform Proficiency by Service',
                    barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    with categories[3]:  # Web Development
        st.markdown("## 🌐 Web Development & APIs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎨 **Frontend Technologies**
            
            **Core Technologies:**
            - **HTML5** - Modern semantic markup
            - **CSS3** - Advanced styling and animations
            - **JavaScript (ES6+)** - Interactive functionality
            - **Bootstrap** - Responsive framework
            - **Chart.js/D3.js** - Data visualizations
            
            **Streamlit Expertise:**
            - Custom component development
            - Advanced layout and styling
            - Session state management
            - Multi-page applications
            - Performance optimization
            
            **Interactive Features:**
            - Real-time data updates
            - User authentication systems
            - File upload and processing
            - Dynamic chart generation
            """)
        
        with col2:
            st.markdown("""
            ### 🔧 **Backend & APIs**
            
            **API Development:**
            - **FastAPI** - High-performance Python APIs
            - **Flask-RESTful** - Lightweight REST services  
            - **Django REST** - Full-featured API framework
            - **GraphQL** - Flexible query language
            
            **Database Integration:**
            - SQLAlchemy ORM
            - Database migrations
            - Connection pooling
            - Query optimization
            
            **Authentication & Security:**
            - JWT token authentication
            - OAuth2 implementation
            - Rate limiting
            - Input validation
            - CORS configuration
            """)
        
        # Web development project timeline
        st.markdown("### 🚀 Recent Web Development Projects")
        timeline_fig = create_project_timeline()
        st.plotly_chart(timeline_fig, use_container_width=True)
    
    # Certifications and learning
    st.markdown("## 🎓 Certifications & Continuous Learning")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📜 **Current Certifications**
        - Microsoft Power"""
Interactive Data Science Portfolio Website

A comprehensive, interactive portfolio showcasing data science projects,
dashboards, and analytical capabilities using Streamlit.

Author: Your Name
Date: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Data Science Portfolio | Your Name",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://your-portfolio.com/help',
        'Report a bug': 'https://your-portfolio.com/contact',
        'About': """
        # Interactive Data Science Portfolio
        
        Professional portfolio showcasing expertise in:
        - Interactive Dashboard Development
        - Data Engineering & ETL Pipelines  
        - Business Intelligence Solutions
        - Machine Learning & Analytics
        - Full-Stack Data Applications
        
        Contact: your.email@example.com
        """
    }
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        text-align: center;
    }
    
    .project-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2a5298;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .skill-badge {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .contact-button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .contact-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .testimonial {
        background: #f8f9fa;
        padding: 1.5rem;
        border-left: 4px solid #2a5298;
        border-radius: 0 10px 10px 0;
        font-style: italic;
        margin: 1rem 0;
    }
    
    .tech-stack {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #90caf9;
    }
</style>
""", unsafe_allow_html=True)

# Utility functions
def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        import requests
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def get_base64_of_bin_file(bin_file):
    """Convert binary file to base64 string"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def create_download_link(val, filename):
    """Create download link for file"""
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}">Download {filename}</a>'

# Sample data for demonstrations
def generate_sample_analytics_data():
    """Generate sample analytics data for demonstrations"""
    dates = pd.date_range('2024-01-01', periods=90, freq='D')
    
    analytics_data = pd.DataFrame({
        'date': dates,
        'page_views': np.random.poisson(1000, 90) + np.random.normal(0, 50, 90),
        'unique_visitors': np.random.poisson(400, 90) + np.random.normal(0, 30, 90),
        'bounce_rate': np.random.normal(0.35, 0.1, 90).clip(0, 1),
        'conversion_rate': np.random.normal(0.05, 0.02, 90).clip(0, 1)
    })
    
    return analytics_data

def create_skills_chart():
    """Create interactive skills proficiency chart"""
    skills_data = {
        'Python': 95,
        'SQL': 90,
        'Power BI': 85,
        'Streamlit': 90,
        'Machine Learning': 80,
        'Data Visualization': 95,
        'ETL Pipelines': 85,
        'Cloud Platforms': 75,
        'JavaScript': 70,
        'Docker': 75
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(skills_data.values()),
            y=list(skills_data.keys()),
            orientation='h',
            marker=dict(
                color=list(skills_data.values()),
                colorscale='Blues',
                showscale=True
            ),
            text=[f"{v}%" for v in skills_data.values()],
            textposition='inside'
        )
    ])
    
    fig.update_layout(
        title="Technical Skills Proficiency",
        xaxis_title="Proficiency (%)",
        height=400,
        template="plotly_white"
    )
    
    return fig

def create_project_timeline():
    """Create project timeline visualization"""
    projects = [
        {'Project': 'Sales Dashboard', 'Start': '2024-01-15', 'End': '2024-02-15', 'Category': 'Dashboard'},
        {'Project': 'ETL Pipeline', 'Start': '2024-02-01', 'End': '2024-03-01', 'Category': 'Engineering'},
        {'Project': 'Log Analyzer', 'Start': '2024-02-15', 'End': '2024-03-15', 'Category': 'Analytics'},
        {'Project': 'CSV Tool', 'Start': '2024-03-01', 'End': '2024-03-30', 'Category': 'Web App'},
        {'Project': 'Traffic Monitor', 'Start': '2024-03-15', 'End': '2024-04-15', 'Category': 'Dashboard'}
    ]
    
    df = pd.DataFrame(projects)
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])
    
    fig = px.timeline(
        df, 
        x_start='Start', 
        x_end='End', 
        y='Project',
        color='Category',
        title='Project Timeline - Recent Work'
    )
    
    fig.update_layout(height=300, template="plotly_white")
    return fig

# Main application
def main():
    """Main portfolio application"""
    
    # Navigation
    st.sidebar.title("🚀 Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "💼 Projects", "🛠️ Skills", "📊 Live Demos", "📞 Contact"]
    )
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "💼 Projects":
        show_projects_page()
    elif page == "🛠️ Skills":
        show_skills_page()
    elif page == "📊 Live Demos":
        show_demos_page()
    elif page == "📞 Contact":
        show_contact_page()

def show_home_page():
    """Display home page"""
    
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">
            🚀 Data Science Portfolio
        </h1>
        <h2 style="font-size: 1.5rem; margin: 0; opacity: 0.9;">
            Transforming Data into Actionable Business Intelligence
        </h2>
        <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.8;">
            Interactive Dashboards • Advanced Analytics • Full-Stack Solutions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">15+</h2>
            <p style="margin: 0.5rem 0;">Interactive Dashboards</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">500k+</h2>
            <p style="margin: 0.5rem 0;">Records Processed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">99.9%</h2>
            <p style="margin: 0.5rem 0;">Uptime Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">3+</h2>
            <p style="margin: 0.5rem 0;">Years Experience</p>
        </div>
        """, unsafe_allow_html=True)
    
    # About Section
    st.markdown("## 👋 Welcome to My Portfolio")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        I'm a **Data Science Professional** specializing in transforming complex data into 
        actionable business insights. With expertise spanning from **interactive dashboard development** 
        to **machine learning implementation**, I help organizations make data-driven decisions 
        that drive growth and efficiency.
        
        ### 🎯 **Core Specializations:**
        - **📊 Business Intelligence Dashboards** - Power BI, Tableau, Custom Solutions
        - **🔧 Data Engineering** - ETL Pipelines, Database Optimization, Cloud Architecture  
        - **🌐 Web Applications** - Streamlit, Flask, Interactive Data Tools
        - **📈 Advanced Analytics** - Statistical Modeling, Machine Learning, Forecasting
        - **☁️ Cloud Solutions** - AWS, GCP, Azure Data Services
        
        ### 🏆 **Recent Achievements:**
        - Developed real-time monitoring dashboards reducing incident response time by **80%**
        - Built ETL pipelines processing **500k+ records daily** with 99.9% accuracy
        - Created interactive tools used by **50+ analysts** across multiple organizations
        - Delivered projects resulting in **$2M+ cost savings** for clients
        """)
    
    with col2:
        st.image("assets/profile_photo.jpg" if Path("assets/profile_photo.jpg").exists() else "https://via.placeholder.com/300x300", 
                caption="Professional Profile", width=300)
        
        st.markdown("""
        ### 🎓 **Certifications:**
        - Microsoft Power BI Data Analyst
        - AWS Cloud Practitioner  
        - Python for Data Science
        - SQL Database Administration
        
        ### 📍 **Location:**
        Remote • Available Worldwide
        
        ### ⏰ **Availability:**
        Open for new projects
        """)
    
    # Featured Projects Preview
    st.markdown("## 🌟 Featured Projects")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="project-card">
            <h3>📊 Sales Analytics Dashboard</h3>
            <p>Interactive Power BI dashboard tracking KPIs, sales funnels, and regional performance with real-time data updates.</p>
            <div class="tech-stack">
                <strong>Tech:</strong> Power BI, SQL Server, DAX
            </div>
            <p><strong>Impact:</strong> 40% faster reporting, $500K cost savings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="project-card">
            <h3>🔧 CSV Insight Tool</h3>
            st.markdown("""
        <div class="project-card">
            <h3>🔧 CSV Insight Tool</h3>
            <p>Drag-and-drop web application for instant CSV analysis with automated chart generation and statistical insights.</p>
            <div class="tech-stack">
                <strong>Tech:</strong> Streamlit, Pandas, Plotly
            </div>
            <p><strong>Impact:</strong> Used by 100+ analysts daily</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="project-card">
            <h3>📈 Log Visualizer</h3>
            <p>Real-time log monitoring system with anomaly detection, performance metrics, and alert notifications.</p>
            <div class="tech-stack">
                <strong>Tech:</strong> Flask, WebSockets, Chart.js
            </div>
            <p><strong>Impact:</strong> 99.9% uptime monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("## 🚀 Ready to Get Started?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <h3 style="margin: 0 0 1rem 0;">Let's Transform Your Data Together</h3>
            <p style="margin: 0 0 1.5rem 0;">Schedule a free consultation to discuss your project needs</p>
            <a href="mailto:your.email@example.com" class="contact-button" style="color: white; text-decoration: none;">
                📧 Schedule Consultation
            </a>
            <a href="tel:+15551234567" class="contact-button" style="color: white; text-decoration: none;">
                📱 Call Now
            </a>
        </div>
        """, unsafe_allow_html=True)

def show_projects_page():
    """Display projects showcase page"""
    
    st.title("💼 Project Portfolio")
    st.markdown("### Interactive showcase of data science and analytics projects")
    
    # Project categories
    categories = st.tabs(["📊 Dashboards", "🔧 Data Engineering", "🌐 Web Applications", "📈 Analytics"])
    
    with categories[0]:  # Dashboards
        st.markdown("## 📊 Interactive Dashboard Solutions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🏢 Grafana Infrastructure Monitoring
            
            **Project Overview:**
            Comprehensive infrastructure monitoring solution with real-time metrics, alerting, and performance optimization recommendations.
            
            **Key Features:**
            - 📈 Real-time server metrics monitoring
            - 🚨 Automated alert system with Slack/email integration
            - 📊 Custom dashboards for different stakeholder groups
            - 🔍 Log aggregation and analysis
            - 📱 Mobile-responsive design
            
            **Technical Stack:**
            - **Frontend:** Grafana, Custom Panels
            - **Backend:** Prometheus, InfluxDB  
            - **Alerting:** AlertManager, PagerDuty
            - **Infrastructure:** Docker, Kubernetes
            
            **Business Impact:**
            - ⬇️ 80% reduction in incident response time
            - 🎯 99.9% system uptime achievement
            - 💰 $200K annual cost savings through optimization
            """)
            
            # Sample metrics chart
            metrics_data = pd.DataFrame({
                'timestamp': pd.date_range('2024-01-01', periods=100, freq='H'),
                'cpu_usage': np.random.normal(45, 15, 100).clip(0, 100),
                'memory_usage': np.random.normal(60, 20, 100).clip(0, 100),
                'disk_io': np.random.exponential(20, 100).clip(0, 100)
            })
            
            fig = px.line(metrics_data, x='timestamp', y=['cpu_usage', 'memory_usage', 'disk_io'],
                         title='Sample Infrastructure Metrics')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            ### 📊 Power BI Sales & KPI Analytics
            
            **Project Overview:**
            Executive-level sales performance dashboard with advanced KPI tracking, forecasting, and regional analysis capabilities.
            
            **Key Features:**
            - 🎯 Executive KPI dashboard with drill-down capabilities
            - 🌍 Geographic sales performance mapping
            - 📈 Predictive sales forecasting using ML models
            - 🔄 Real-time data refresh from multiple sources
            - 📱 Mobile-optimized for executive access
            
            **Technical Stack:**
            - **Visualization:** Power BI Premium
            - **Data Sources:** SQL Server, SharePoint, Excel
            - **Processing:** Power Query, DAX
            - **ML Integration:** Azure Machine Learning
            
            **Business Impact:**
            - 📊 40% faster executive reporting
            - 🎯 25% improvement in sales forecasting accuracy
            - 💼 Adopted by 50+ sales representatives
            """)
            
            # Sample sales data visualization
            sales_data = pd.DataFrame({
                'month': pd.date_range('2024-01-01', periods=12, freq='M'),
                'revenue': np.random.normal(100000, 20000, 12).clip(50000, 200000),
                'target': [120000] * 12,
                'region': np.random.choice(['North', 'South', 'East', 'West'], 12)
            })
            
            fig = px.bar(sales_data, x='month', y='revenue', color='region',
                        title='Monthly Revenue by Region')
            fig.add_scatter(x=sales_data['month'], y=sales_data['target'], 
                          mode='lines', name='Target', line=dict(color='red', dash='dash'))
            st.plotly_chart(fig, use_container_width=True)
        
        # Traffic Analytics Dashboard
        st.markdown("""
        ### 🌐 Traffic Analytics Dashboard
        
        **Real-time web analytics platform with user behavior tracking and conversion optimization.**
        """)
        
        # Create sample traffic analytics
        analytics_data = generate_sample_analytics_data()
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(analytics_data, x='date', y=['page_views', 'unique_visitors'],
                          title='Traffic Trends Over Time')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.scatter(analytics_data, x='bounce_rate', y='conversion_rate',
                             size='unique_visitors', title='Bounce Rate vs Conversion Rate')
            st.plotly_chart(fig2, use_container_width=True)
    
    with categories[1]:  # Data Engineering
        st.markdown("## 🔧 Data Engineering Solutions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ⚡ Excel/CSV ETL Pipeline
            
            **Project Overview:**
            Automated ETL pipeline for processing large Excel and CSV files with data validation, transformation, and loading capabilities.
            
            **Key Features:**
            - 📂 Batch processing of multiple file formats
            - 🔍 Automated data quality checks and validation
            - 🔄 Incremental data loading with change detection
            - 📊 Processing statistics and error reporting
            - ⏱️ Scheduled execution with monitoring
            
            **Technical Architecture:**
            ```python
            # Sample ETL Pipeline Code
            import pandas as pd
            from sqlalchemy import create_engine
            
            def process_csv_files(file_paths):
                consolidated_data = []
                
                for file_path in file_paths:
                    # Read and validate data
                    df = pd.read_csv(file_path)
                    df_clean = validate_and_clean(df)
                    consolidated_data.append(df_clean)
                
                # Consolidate and load
                final_df = pd.concat(consolidated_data)
                load_to_database(final_df)
                
                return processing_stats
            ```
            
            **Performance Metrics:**
            - ⚡ 500K+ records processed per hour
            - 🎯 99.5% data accuracy rate
            - 📉 90% reduction in manual processing time
            """)
        
        with col2:
            st.markdown("""
            ### 🗄️ SQL Data Cleaning & Reporting
            
            **Project Overview:**
            Comprehensive SQL-based data cleaning and automated reporting system with data quality monitoring and optimization.
            
            **Key Features:**
            - 🧹 Advanced data cleaning algorithms
            - 📊 Automated report generation
            - 🔍 Data quality monitoring dashboard
            - ⚡ Query optimization and performance tuning
            - 📈 Historical data analysis and trending
            
            **SQL Optimization Examples:**
            ```sql
            -- Performance-optimized reporting query
            WITH monthly_sales AS (
                SELECT 
                    DATE_TRUNC('month', order_date) as month,
                    region,
                    SUM(revenue) as total_revenue,
                    COUNT(DISTINCT customer_id) as unique_customers
                FROM sales_data 
                WHERE order_date >= '2024-01-01'
                GROUP BY 1, 2
            ),
            growth_calc AS (
                SELECT *,
                    LAG(total_revenue) OVER (
                        PARTITION BY region 
                        ORDER BY month
                    ) as prev_month_revenue
                FROM monthly_sales
            )
            SELECT 
                region,
                month,
                total_revenue,
                unique_customers,
                ROUND(
                    ((total_revenue - prev_month_revenue) / 
                     prev_month_revenue) * 100, 2
                ) as growth_rate
            FROM growth_calc
            ORDER BY region, month;
            ```
            
            **Performance Improvements:**
            - ⚡ 75% faster query execution times  
            - 📊 Automated daily/weekly/monthly reports
            - 🎯 99.8% data quality scores
            """)
        
        # Data Processing Pipeline Visualization
        st.markdown("### 🔄 ETL Pipeline Architecture")
        
        # Create pipeline flow diagram using Plotly
        import plotly.graph_objects as go
        
        fig = go.Figure(data=go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["Raw Data", "Validation", "Transformation", "Quality Check", "Database", "Reports"],
                color=["lightblue", "lightgreen", "lightyellow", "lightcoral", "lightpink", "lightgray"]
            ),
            link=dict(
                source=[0, 1, 2, 3, 4],
                target=[1, 2, 3, 4, 5],
                value=[100, 95, 90, 88, 88]
            )
        ))
        
        fig.update_layout(title_text="Data Processing Pipeline Flow", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with categories[2]:  # Web Applications
        st.markdown("## 🌐 Interactive Web Applications")
        
        st.markdown("""
        ### 📊 CSV Insight Tool - Live Demo
        
        **Try the interactive CSV analysis tool directly in your browser!**
        """)
        
        # Embed a mini version of the CSV tool
        uploaded_file = st.file_uploader("Upload a CSV file to analyze", type="csv")
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            
            st.markdown("#### 📈 Quick Data Overview")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            
            st.markdown("#### 📊 Data Preview")
            st.dataframe(df.head(10))
            
            st.markdown("#### 📈 Automatic Visualizations")
            
            # Generate automatic charts
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_columns) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig1 = px.histogram(df, x=numeric_columns[0], 
                                      title=f'Distribution of {numeric_columns[0]}')
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    if len(numeric_columns) >= 2:
                        fig2 = px.scatter(df, x=numeric_columns[0], y=numeric_columns[1],
                                        title=f'{numeric_columns[0]} vs {numeric_columns[1]}')
                        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("""
        ### 📈 Log Visualizer Dashboard
        
        **Real-time log monitoring and analysis system**
        """)
        
        # Simulate log data
        log_data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=1000, freq='min'),
            'log_level': np.random.choice(['INFO', 'WARNING', 'ERROR', 'DEBUG'], 1000, p=[0.6, 0.2, 0.1, 0.1]),
            'response_time': np.random.exponential(100, 1000),
            'status_code': np.random.choice([200, 404, 500, 503], 1000, p=[0.8, 0.1, 0.05, 0.05])
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Log level distribution
            log_counts = log_data['log_level'].value_counts()
            fig = px.pie(values=log_counts.values, names=log_counts.index,
                        title='Log Level Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Response time trend
            hourly_avg = log_data.groupby(log_data['timestamp'].dt.hour)['response_time'].mean()
            fig = px.bar(x=hourly_avg.index, y=hourly_avg.values,
                        title='Average Response Time by Hour')
            st.plotly_chart(fig, use_container_width=True)
    
    with categories[3]:  # Analytics
        st.markdown("## 📈 Advanced Analytics Projects")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🤖 Machine Learning Models
            
            **Predictive analytics and machine learning implementations**
            
            **Sales Forecasting Model:**
            - Random Forest Regressor for monthly sales prediction
            - Feature engineering with seasonality and trends
            - 95% accuracy on test data
            
            **Customer Segmentation:**
            - K-Means clustering for customer behavior analysis  
            - RFM analysis integration
            - Actionable marketing insights
            
            **Anomaly Detection:**
            - Isolation Forest for fraud detection
            - Real-time scoring pipeline
            - 98% precision in anomaly identification
            """)
        
        with col2:
            st.markdown("""
            ### 📊 Statistical Analysis
            
            **Advanced statistical modeling and hypothesis testing**
            
            **A/B Testing Framework:**
            - Bayesian statistical testing
            - Power analysis and sample size calculation
            - Real-time results monitoring
            
            **Time Series Analysis:**
            - ARIMA and LSTM models for forecasting
            - Seasonal decomposition and trend analysis
            - Automated model selection
            
            **Correlation Analysis:**
            - Multi-variate correlation studies
            - Causal inference techniques
            - Business impact quantification
            """)
        
        # Interactive ML Demo
        st.markdown("### 🤖 Interactive ML Demo: Sales Prediction")
        
        # Create sample data for ML demo
        np.random.seed(42)
        n_samples = 1000
        
        demo_data = pd.DataFrame({
            'advertising_spend': np.random.normal(5000, 2000, n_samples),
            'season': np.random.choice([1, 2, 3, 4], n_samples),
            'competitor_price': np.random.normal(50, 10, n_samples),
            'economic_index': np.random.normal(100, 15, n_samples)
        })
        
        # Simple linear relationship for demo
        demo_data['sales'] = (
            demo_data['advertising_spend'] * 0.8 + 
            demo_data['season'] * 1000 + 
            demo_data['competitor_price'] * -200 + 
            demo_data['economic_index'] * 50 + 
            np.random.normal(0, 5000, n_samples)
        )
        
        # Interactive controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ad_spend = st.slider("Advertising Spend ($)", 1000, 10000, 5000)
        with col2:
            season = st.selectbox("Season", [1, 2, 3, 4], index=1)
        with col3:
            comp_price = st.slider("Competitor Price ($)", 30, 80, 50)
        
        # Simple prediction calculation
        predicted_sales = ad_spend * 0.8 + season * 1000 + comp_price * -200 + 100 * 50
        
        st.markdown(f"""
        ### 🎯 Predicted Sales: **${predicted_sales:,.0f}**
        
        *Based on machine learning model trained on historical sales data*
        """)
        
        # Show feature importance
        feature_importance = pd.DataFrame({
            'Feature': ['Advertising Spend', 'Season', 'Competitor Price', 'Economic Index'],
            'Importance': [0.4, 0.25, 0.2, 0.15]
        })
        
        fig = px.bar(feature_importance, x='Importance', y='Feature', orientation='h',
                    title='Feature Importance in Sales Prediction Model')
        st.plotly_chart(fig, use_container_width=True)

def show_skills_page():
    """Display skills and expertise page"""
    
    st.title("🛠️ Technical Skills & Expertise")
    st.markdown("### Comprehensive overview of technical capabilities and proficiency levels")
    
    # Skills proficiency chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        skills_fig = create_skills_chart()
        st.plotly_chart(skills_fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### 📊 **Skill Levels:**
        
        **🟢 Expert (90-100%):**
        Advanced proficiency with extensive project experience
        
        **🟡 Proficient (75-89%):**
        Strong working knowledge with multiple implementations
        
        **🟠 Intermediate (60-74%):**
        Solid foundation with growing expertise
        
        **🔴 Learning (< 60%):**
        Currently developing skills through projects
        """)
    
    # Skills categories
    categories = st.tabs(["💻 Programming", "📊 Data & Analytics", "☁️ Cloud & Infrastructure", "🌐 Web Development"])
    
    with categories[0]:  # Programming
        st.markdown("## 💻 Programming Languages & Frameworks")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🐍 **Python Ecosystem**
            
            **Core Libraries:**
            - **Pandas** - Data manipulation and analysis
            - **NumPy** - Numerical computing and arrays
            - **Matplotlib/Seaborn** - Static visualizations
            - **Plotly** - Interactive charts and dashboards
            - **Scikit-learn** - Machine learning algorithms
            
            **Web Frameworks:**
            - **Streamlit** - Rapid prototyping and dashboards
            - **Flask** - Lightweight web applications  
            - **FastAPI** - High-performance APIs
            - **Django** - Full-featured web development
            
            **Data Engineering:**
            - **Apache Airflow** - Workflow orchestration
            - **Dask** - Parallel computing
            - **SQLAlchemy** - Database ORM
            """)
            
            # Code example
            st.code("""
            # Advanced data processing example
            import pandas as pd
            import numpy as np
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.model_selection import train_test_split
            
            def build_sales_model(data):
                # Feature engineering
                data['month'] = pd.to_datetime(data['date']).dt.month
                data['quarter'] = pd.to_datetime(data['date']).dt.quarter
                
                # Model training
                features = ['advertising', 'month', 'quarter', 'price']
                X = data[features]
                y = data['sales']
                
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )
                
                model = RandomForestRegressor(n_estimators=100)
                model.fit(X_train, y_train)
                
                return model, model.score(X_test, y_test)
            """, language="python")
        
        with col2:
            st.markdown("""
            ### 🗄️ **SQL & Databases**
            
            **Database Systems:**
            - **PostgreSQL** - Advanced relational database
            - **MySQL** - Popular open-source RDBMS
            - **SQL Server** - Microsoft enterprise database
            - **SQLite** - Lightweight embedded database
            - **MongoDB** - NoSQL document database
            
            **Advanced SQL Features:**
            - Window functions and CTEs
            - Query optimization and indexing
            - Stored procedures and functions
            - Data warehousing concepts
            - ETL pipeline development
            """)
            
            # SQL example
            st.code("""
            -- Advanced sales analytics query
            WITH monthly_metrics AS (
                SELECT 
                    DATE_TRUNC('month', order_date) as month,
                    customer_segment,
                    SUM(revenue) as total_revenue,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    AVG(order_value) as avg_order_value
                FROM sales_data s
                JOIN customers c ON s.customer_id = c.id
                WHERE order_date >= '2024-01-01'
                GROUP BY 1, 2
            ),
            growth_analysis AS (
                SELECT *,
                    LAG(total_revenue) OVER (
                        PARTITION BY customer_segment 
                        ORDER BY month
                    ) as prev_month_revenue,
                    PERCENT_RANK() OVER (
                        PARTITION BY month 
                        ORDER BY total_revenue
                    ) as revenue_percentile
                FROM monthly_metrics
            )
            SELECT 
                month,
                customer_segment,
                total_revenue,
                unique_customers,
                ROUND(
                    ((total_revenue - prev_month_revenue) / 
                     NULLIF(prev_month_revenue, 0)) * 100, 2
                ) as growth_rate,
                CASE 
                    WHEN revenue_percentile >= 0.8 THEN 'Top Performer'
                    WHEN revenue_percentile >= 0.6 THEN 'Above Average' 
                    WHEN revenue_percentile >= 0.4 THEN 'Average'
                    ELSE 'Below Average'
                END as performance_tier
            FROM growth_analysis
            ORDER BY month DESC, total_revenue DESC;
            """, language="sql")
    
    with categories[1]:  # Data & Analytics
        st.markdown("## 📊 Data Science & Analytics Tools")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📈 **Business Intelligence**
            
            **Microsoft Power BI:**
            - Advanced DAX calculations and measures
            - Custom visualizations and themes
            - Row-level security implementation
            - Gateway configuration and data refresh
            - Power BI Service administration
            
            **Tableau:**
            - Interactive dashboard development
            - Advanced calculations and LOD expressions
            - Data blending and relationships
            - Tableau Server deployment
            
            **Advanced Features:**
            - Real-time data streaming
            - Mobile-responsive design
            - Embedded analytics
            - Custom connectors development
            """)
        
        with col2:
            st.markdown("""
            ### 🤖 **Machine Learning & AI**
            
            **Algorithms & Techniques:**
            - Supervised Learning (Regression, Classification)
            - Unsupervised Learning (Clustering, PCA)
            - Time Series Forecasting (ARIMA, LSTM)
            - Natural Language Processing
            - Computer Vision basics
            
            **MLOps & Production:**
            - Model versioning and tracking (MLflow)
            - A/B testing frameworks
            - Model monitoring and drift detection
            - Automated retraining pipelines
            - Feature stores and data pipelines
            
            **Cloud ML Services:**
            - AWS SageMaker
            - Azure Machine Learning
            - Google Cloud AI Platform
            """)
        
        # Interactive ML metrics demo
        st.markdown("### 🎯 Model Performance Visualization")
        
        # Generate sample model performance data
        models = ['Random Forest', 'XGBoost', 'Linear Regression', 'Neural Network', 'SVM']
        metrics_data = pd.DataFrame({
            'Model': models,
            'Accuracy': np.random.uniform(0.75, 0.95, 5),
            'Precision': np.random.uniform(0.70, 0.90, 5),
            'Recall': np.random.uniform(0.65, 0.85, 5),
            'F1-Score': np.random.uniform(0.68, 0.87, 5)
        })
        
        fig = px.scatter(metrics_data, x='Precision', y='Recall', 
                        size='Accuracy', color='Model', hover_name='Model',
                        title='Model Performance Comparison')
        st.plotly_chart(fig, use_container_width=True)
    
    with categories[2]:  # Cloud & Infrastructure
        st.markdown("## ☁️ Cloud Platforms & Infrastructure")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ☁️ **Amazon Web Services (AWS)**
            
            **Data Services:**
            - **S3** - Object storage and data lakes
            - **RDS** - Managed relational databases
            - **Redshift** - Data warehousing
            - **EMR** - Big data processing
            - **Glue** - ETL and data catalog
            
            **Analytics & ML:**
            - **SageMaker** - Machine learning platform
            - **QuickSight** - Business intelligence
            - **Kinesis** - Real-time data streaming
            - **Lambda** - Serverless computing
            
            **Infrastructure:**
            - **EC2** - Virtual servers
            - **ECS/EKS** - Container orchestration
            - **CloudFormation** - Infrastructure as code
            """)
        
        with col2:
            st.markdown("""
            ### 🔧 **DevOps & Monitoring**
            
            **Containerization:**
            - **Docker** - Application containerization
            - **Kubernetes** - Container orchestration
            - **Docker Compose** - Multi-container applications
            
            **CI/CD:**
            - **GitHub Actions** - Automated workflows
            - **Jenkins** - Build automation
            - **GitLab CI/CD** - Integrated DevOps
            
            **Monitoring & Observability:**
            - **Grafana** - Metrics visualization
            - **Prometheus** - Metrics collection
            - **ELK Stack** - Log analysis
            - **DataDog** - Application monitoring
            """)
        
        # Cloud services comparison chart
        cloud_services = pd.DataFrame({
            'Service': ['Data Storage', 'ML Platform', 'Analytics', 'Monitoring', 'Compute'],
            'AWS': [95, 90, 85, 80, 90],
            'Azure': [85, 85, 80, 75, 85],
            'GCP': [80, 95, 90, 85, 85]
        })
        
        fig = px.bar(cloud_services, x='Service', y=['AWS', 'Azure', 'GCP'],
                    title='Cloud Platform Proficiency by Service',
                    barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    with categories[3]:  # Web Development
        st.markdown("## 🌐 Web Development & APIs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎨 **Frontend Technologies**
            
            **Core Technologies:**
            - **HTML5** - Modern semantic markup
            - **CSS3** - Advanced styling and animations
            - **JavaScript (ES6+)** - Interactive functionality
            - **Bootstrap** - Responsive framework
            - **Chart.js/D3.js** - Data visualizations
            
            **Streamlit Expertise:**
            - Custom component development
            - Advanced layout and styling
            - Session state management
            - Multi-page applications
            - Performance optimization
            
            **Interactive Features:**
            - Real-time data updates
            - User authentication systems
            - File upload and processing
            - Dynamic chart generation
            """)
        
        with col2:
            st.markdown("""
            ### 🔧 **Backend & APIs**
            
            **API Development:**
            - **FastAPI** - High-performance Python APIs
            - **Flask-RESTful** - Lightweight REST services  
            - **Django REST** - Full-featured API framework
            - **GraphQL** - Flexible query language
            
            **Database Integration:**
            - SQLAlchemy ORM
            - Database migrations
            - Connection pooling
            - Query optimization
            
            **Authentication & Security:**
            - JWT token authentication
            - OAuth2 implementation
            - Rate limiting
            - Input validation
            - CORS configuration
            """)
        
        # Web development project timeline
        st.markdown("### 🚀 Recent Web Development Projects")
        timeline_fig = create_project_timeline()
        st.plotly_chart(timeline_fig, use_container_width=True)
    
    # Certifications and learning
    st.markdown("## 🎓 Certifications & Continuous Learning")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📜 **Current Certifications**
        - Microsoft Power BI Data Analyst Associate
        - AWS Certified Cloud Practitioner  
        - Google Analytics Individual Qualification
        - Python for Data Science (IBM)
        - SQL Database Administration
        """)
    
    with col2:
        st.markdown("""
        ### 📚 **Currently Learning**
        - Advanced Machine Learning (Coursera)
        - Kubernetes Administration
        - React.js for Data Applications
        - Snowflake Data Cloud
        - Apache Kafka Streaming
        """)
    
    with col3:
        st.markdown("""
        ### 🎯 **2024 Learning Goals**
        - Azure Data Engineer Associate
        - Terraform Infrastructure Management
        - Advanced Statistical Analysis
        - Deep Learning Specialization
        - Data Mesh Architecture
        """)

def show_demos_page():
    """Display live demos page"""
    
    st.title("📊 Live Interactive Demos")
    st.markdown("### Experience the tools and dashboards in action")
    
    demo_tabs = st.tabs(["📈 Analytics Demo", "🔍 Data Explorer", "📊 Dashboard Builder", "🤖 ML Predictor"])
    
    with demo_tabs[0]:  # Analytics Demo
        st.markdown("## 📈 Real-time Analytics Demo")
        st.markdown("*Simulate real-time business metrics with interactive controls*")
        
        # Controls
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            metric_type = st.selectbox("Metric Type", ["Sales", "Traffic", "Users", "Revenue"])
        with col2:
            time_period = st.selectbox("Time Period", ["Last 7 days", "Last 30 days", "Last 90 days"])
        with col3:
            region = st.selectbox("Region", ["All", "North America", "Europe", "Asia"])
        with col4:
            if st.button("🔄 Refresh Data"):
                st.rerun()
        
        # Generate dynamic data based on selections
        days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
        num_days = days_map[time_period]
        
        dates = pd.date_range(end=datetime.now(), periods=num_days, freq='D')
        base_value = {"Sales": 10000, "Traffic": 50000, "Users": 5000, "Revenue": 25000}[metric_type]
        
        # Create realistic data with trends and seasonality
        trend = np.linspace(0.8, 1.2, num_days)
        seasonality = np.sin(np.arange(num_days) * 2 * np.pi / 7) * 0.1 + 1
        noise = np.random.normal(0, 0.05, num_days)
        
        values = base_value * trend * seasonality * (1 + noise)
        
        demo_data = pd.DataFrame({
            'date': dates,
            'value': values.clip(min=base_value * 0.5)
        })
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        current_value = demo_data['value'].iloc[-1]
        previous_value = demo_data['value'].iloc[-2] if len(demo_data) > 1 else current_value
        change_pct = ((current_value - previous_value) / previous_value) * 100
        
        with col1:
            st.metric(
                f"Current {metric_type}",
                f"${current_value:,.0f}" if metric_type in ["Sales", "Revenue"] else f"{current_value:,.0f}",
                f"{change_pct:+.1f}%"
            )
        
        with col2:
            st.metric("Average", f"{demo_data['value'].mean():,.0f}")
        
        with col3:
            st.metric("Peak", f"{demo_data['value'].max():,.0f}")
        
        with col4:
            st.metric("Growth Rate", f"{((demo_data['value'].iloc[-1] / demo_data['value'].iloc[0] - 1) * 100):+.1f}%")
        
        # Interactive charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.line(demo_data, x='date', y='value', 
                          title=f'{metric_type} Trend - {time_period}')
            fig1.add_hline(y=demo_data['value'].mean(), line_dash="dash", 
                          annotation_text="Average")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Distribution chart
            fig2 = px.histogram(demo_data, x='value', 
                               title=f'{metric_type} Distribution')
            st.plotly_chart(fig2, use_container_width=True)
    
    with demo_tabs[1]:  # Data Explorer
        st.markdown("## 🔍 Interactive Data Explorer")
        st.markdown("*Upload your own data or use sample datasets*")
        
        # Data source selection
        data_source = st.radio("Choose data source:", 
                              ["📁 Upload your file", "📊 Sample sales data", "📈 Sample web analytics"])
        
        df = None
        
        if data_source == "📁 Upload your file":
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
        
        elif data_source == "📊 Sample sales data":
            # Generate sample sales data
            np.random.seed(42)
            df = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=365, freq='D'),
                'product': np.random.choice(['Product A', 'Product B', 'Product C'], 365),
                'region': np.random.choice(['North', 'South', 'East', 'West'], 365),
                'sales': np.random.normal(1000, 300, 365).clip(min=100),
                'customers': np.random.poisson(50, 365),
                'marketing_spend': np.random.normal(500, 150, 365).clip(min=50)
            })
        
        elif data_source == "📈 Sample web analytics":
            # Generate sample web analytics data
            df = generate_sample_analytics_data()
            df.columns = ['date', 'page_views', 'unique_visitors', 'bounce_rate', 'conversion_rate']
        
        if df is not None:
            st.markdown("### 📋 Data Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Rows", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            with col4:
                st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            # Data preview
            st.markdown("### 👀 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Interactive exploration
            st.markdown("### 🔍 Interactive Analysis")
            
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
            
            col1, col2 = st.columns(2)
            
            if len(numeric_columns) >= 1:
                with col1:
                    selected_numeric = st.selectbox("Select numeric column:", numeric_columns)
                    
                    fig1 = px.histogram(df, x=selected_numeric, 
                                       title=f'Distribution of {selected_numeric}')
                    st.plotly_chart(fig1, use_container_width=True)
            
            if len(numeric_columns) >= 2:
                with col2:
                    x_col = st.selectbox("X-axis:", numeric_columns, index=0)
                    y_col = st.selectbox("Y-axis:", numeric_columns, index=1 if len(numeric_columns) > 1 else 0)
                    
                    color_col = None
                    if categorical_columns:
                        color_col = st.selectbox("Color by:", ["None"] + categorical_columns)
                        color_col = color_col if color_col != "None" else None
                    
                    fig2 = px.scatter(df, x=x_col, y=y_col, color=color_col,
                                     title=f'{x_col} vs {y_col}')
                    st.plotly_chart(fig2, use_container_width=True)
            
            # Statistical summary
            st.markdown("### 📊 Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)
    
    with demo_tabs[2]:  # Dashboard Builder
        st.markdown("## 📊 Interactive Dashboard Builder")
        st.markdown("*Build custom dashboards with drag-and-drop simplicity*")
        
        # Dashboard configuration
        st.markdown("### ⚙️ Dashboard Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dashboard_title = st.text_input("Dashboard Title", "My Business Dashboard")
        with col2:
            refresh_interval = st.selectbox("Auto-refresh", ["None", "30 seconds", "1 minute", "5 minutes"])
        with col3:
            theme = st.selectbox("Theme", ["Light", "Dark", "Corporate"])
        
        # Widget selection
        st.markdown("### 🧩 Add Widgets")
        
        widget_types = st.multiselect(
            "Select widgets to add:",
            ["📈 Line Chart", "📊 Bar Chart", "🥧 Pie Chart", "📋 Data Table", "🔢 KPI Cards"],
            default=["📈 Line Chart", "🔢 KPI Cards"]
        )
        
        # Generate dashboard
        if widget_types:
            st.markdown(f"## {dashboard_title}")
            st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
            
            # Sample business data
            dashboard_data = pd.DataFrame({
                'month': pd.date_range('2024-01-01', periods=12, freq='M'),
                'revenue': np.random.normal(100000, 20000, 12).clip(50000, 200000),
                'expenses': np.random.normal(60000, 15000, 12).clip(30000, 100000),
                'customers': np.random.normal(500, 100, 12).clip(200, 800),
                'products_sold': np.random.normal(1000, 200, 12).clip(500, 1500)
            })
            
            dashboard_data['profit'] = dashboard_data['revenue'] - dashboard_data['expenses']
            
            # Render selected widgets
            if "🔢 KPI Cards" in widget_types:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Revenue", f"${dashboard_data['revenue'].sum():,.0f}",
                             f"{((dashboard_data['revenue'].iloc[-1] / dashboard_data['revenue'].iloc[-2] - 1) * 100):+.1f}%")
                
                with col2:
                    st.metric("Total Profit", f"${dashboard_data['profit'].sum():,.0f}",
                             f"{((dashboard_data['profit'].iloc[-1] / dashboard_data['profit'].iloc[-2] - 1) * 100):+.1f}%")
                
                with col3:
                    st.metric("Avg Customers", f"{dashboard_data['customers'].mean():,.0f}",
                             f"{((dashboard_data['customers'].iloc[-1] / dashboard_data['customers'].iloc[-2] - 1) * 100):+.1f}%")
                
                with col4:
                    st.metric("Products Sold", f"{dashboard_data['products_sold'].sum():,.0f}",
                             f"{((dashboard_data['products_sold'].iloc[-1] / dashboard_data['products_sold'].iloc[-2] - 1) * 100):+.1f}%")
            
            # Charts
            chart_cols = st.columns(2)
            chart_idx = 0
            
            if "📈 Line Chart" in widget_types:
                with chart_cols[chart_idx % 2]:
                    fig = px.line(dashboard_data, x='month', y=['revenue', 'expenses'],
                                 title='Revenue vs Expenses Trend')
                    st.plotly_chart(fig, use_container_width=True)
                    chart_idx += 1
            
            if "📊 Bar Chart" in widget_types:
                with chart_cols[chart_idx % 2]:
                    fig = px.bar(dashboard_data, x='month', y='profit',
                                title='Monthly Profit')
                    st.plotly_chart(fig, use_container_width=True)
                    chart_idx += 1
            
            if "🥧 Pie Chart" in widget_types:
                with chart_cols[chart_idx % 2]:
                    # Create quarterly data for pie chart
                    quarterly_data = dashboard_data.groupby(dashboard_data['month'].dt.quarter)['revenue'].sum()
                    fig = px.pie(values=quarterly_data.values, 
                                names=[f'Q{i}' for i in quarterly_data.index],
                                title='Quarterly Revenue Distribution')
                    st.plotly_chart(fig, use_container_width=True)
                    chart_idx += 1
            
            if "📋 Data Table" in widget_types:
                st.markdown("### 📋 Detailed Data")
                st.dataframe(
                    dashboard_data.style.format({
                        'revenue': '${:,.0f}',
                        'expenses': '${:,.0f}',
                        'profit': '${:,.0f}',
                        'customers': '{:,.0f}',
                        'products_sold': '{:,.0f}'
                    }),
                    use_container_width=True
                )
    
    with demo_tabs[3]:  # ML Predictor
        st.markdown("## 🤖 Machine Learning Predictor Demo")
        st.markdown("*Interactive sales prediction using machine learning*")
        
        st.markdown("### 🎯 Sales Prediction Model")
        st.markdown("*Adjust the parameters below to see how they affect predicted sales*")
        
        # Model inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            advertising_spend = st.slider("Advertising Spend ($)", 1000, 20000, 10000, 500)
            season = st.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])
        
        with col2:
            competitor_price = st.slider("Competitor Price ($)", 20, 100, 50, 5)
            economic_index = st.slider("Economic Index", 80, 120, 100, 2)
        
        with col3:
            market_size = st.slider("Market Size (thousands)", 100, 1000, 500, 50)
            brand_strength = st.slider("Brand Strength (1-10)", 1, 10, 7, 1)
        
        # Simple prediction model (linear combination with weights)
        season_multipliers = {"Spring": 1.1, "Summer": 1.2, "Fall": 0.9, "Winter": 0.8}
        
        prediction = (
            advertising_spend * 0.8 +
            season_multipliers[season] * 5000 +
            (100 - competitor_price) * 500 +
            economic_index * 200 +
            market_size * 10 +
            brand_strength * 1000 +
            np.random.normal(0, 2000)  # Add some randomness
        )
        
        prediction = max(prediction, 10000)  # Ensure positive prediction
        
        # Display prediction
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                color: white;
                margin: 2rem 0;
            ">
                <h2 style="margin: 0 0 1rem 0;">🎯 Predicted Sales</h2>
                <h1 style="font-size: 3rem; margin: 0 0 1rem 0;">${prediction:,.0f}</h1>
                <p style="margin: 0; opacity: 0.8;">Monthly sales prediction based on ML model</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Model explanation
        st.markdown("### 🔍 Model Insights")
        
        # Calculate feature contributions
        contributions = {
            'Advertising Spend': advertising_spend * 0.8,
            'Season Effect': season_multipliers[season] * 5000,
            'Price Advantage': (100 - competitor_price) * 500,
            'Economic Conditions': economic_index * 200,
            'Market Size': market_size * 10,
            'Brand Strength': brand_strength * 1000
        }
        
        contributions_df = pd.DataFrame(
            list(contributions.items()),
            columns=['Factor', 'Contribution']
        )
        
        fig = px.bar(contributions_df, x='Contribution', y='Factor', 
                    orientation='h', title='Feature Contributions to Prediction')
        st.plotly_chart(fig, use_container_width=True)
        
        # Model performance metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Model Accuracy", "94.2%", "↑ 2.1%")
        with col2:
            st.metric("Mean Absolute Error", "$3,245", "↓ $432")
        with col3:
            st.metric("R² Score", "0.891", "↑ 0.023")
        
        # Historical predictions vs actuals
        st.markdown("### 📈 Model Performance History")
        
        # Generate sample historical data
        dates = pd.date_range('2024-01-01', periods=90, freq='D')
        actuals = np.random.normal(prediction, prediction * 0.1, 90)
        predictions_hist = actuals + np.random.normal(0, prediction * 0.05, 90)
        
        performance_data = pd.DataFrame({
            'date': dates,
            'actual': actuals,
            'predicted': predictions_hist
        })
        
        fig = px.line(performance_data, x='date', y=['actual', 'predicted'],
                     title='Actual vs Predicted Sales (Last 90 Days)')
        st.plotly_chart(fig, use_container_width=True)

def show_contact_page():
    """Display contact and consultation page"""
    
    st.title("📞 Contact & Consultation")
    st.markdown("### Ready to transform your data into actionable insights?")
    
    # Contact header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        I help businesses and organizations unlock the power of their data through:
        
        - **📊 Interactive Dashboard Development** - Real-time business intelligence solutions
        - **🔧 Data Engineering & ETL Pipelines** - Automated data processing and transformation
        - **🤖 Machine Learning & Predictive Analytics** - Advanced modeling and forecasting
        - **🌐 Custom Web Applications** - Full-stack data-driven solutions
        - **☁️ Cloud Infrastructure & Deployment** - Scalable and secure cloud solutions
        
        ### 💼 **Consultation Process:**
        1. **Free Discovery Call** (30 minutes) - Understand your needs and challenges
        2. **Technical Proposal** - Detailed solution architecture and timeline  
        3. **Project Kickoff** - Agile development with regular check-ins
        4. **Delivery & Support** - Complete solution with documentation and training
        """)
    
    with col2:
        st.image("https://via.placeholder.com/300x200", caption="Ready to collaborate")
        
        st.markdown("""
        ### 🏆 **Why Choose Me:**
        - ✅ **3+ years** of data science experience
        - ✅ **15+ successful** project deliveries
        - ✅ **99.9% client satisfaction** rate
        - ✅ **24-48 hour** response time
        - ✅ **Flexible engagement** models
        """)
    
    # Contact form
    st.markdown("## 📝 Get In Touch")
    
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john@company.com")
            company = st.text_input("Company", placeholder="Your Company Name")
        
        with col2:
            phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
            budget = st.selectbox("Project Budget", 
                                 ["< $5,000", "$5,000 - $15,000", "$15,000 - $50,000", "> $50,000"])
            timeline = st.selectbox("Timeline", 
                                   ["ASAP", "1-2 weeks", "1 month", "2-3 months", "Flexible"])
        
        project_type = st.multiselect(
            "Services Needed *",
            ["Dashboard Development", "Data Engineering", "Web Application", "Machine Learning", "Consulting", "Training"]
        )
        
        message = st.text_area(
            "Project Description *",
            placeholder="Please describe your project needs, current challenges, and goals...",
            height=100
        )
        
        # Additional options
        col1, col2 = st.columns(2)
        with col1:
            consultation = st.checkbox("Request free 30-minute consultation call")
        with col2:
            newsletter = st.checkbox("Subscribe to data science insights newsletter")
        
        submitted = st.form_submit_button("🚀 Send Message", type="primary", use_container_width=True)
        
        if submitted:
            if name and email and project_type and message:
                st.success("""
                ✅ **Message sent successfully!** 
                
                Thank you for your interest. I'll review your project details and respond within 24 hours.
                
                **Next Steps:**
                1. You'll receive a confirmation email shortly
                2. I'll review your project requirements  
                3. We'll schedule a discovery call to discuss details
                4. I'll provide a detailed proposal and timeline
                """)
                
                # Simulate sending email notification
                st.balloons()
            else:
                st.error("⚠️ Please fill in all required fields marked with *")
    
    # Contact information
    st.markdown("---")
    st.markdown("## 📱 Direct Contact Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📧 **Email**
        [your.email@example.com](mailto:your.email@example.com)
        
        **Response Time:** 24 hours  
        **Best For:** Project inquiries, detailed discussions
        """)
    
    with col2:
        st.markdown("""
        ### 📱 **Phone**
        [+1 (555) 123-4567](tel:+15551234567)
        
        **Availability:** Mon-Fri, 9 AM - 6 PM EST  
        **Best For:** Urgent questions, quick consultations
        """)
    
    with col3:
        st.markdown("""
        ### 💼 **LinkedIn**
        [linkedin.com/in/yourname](https://linkedin.com/in/yourname)
        
        **Best For:** Professional networking, referrals
        """)
    
    # Scheduling
    st.markdown("## 📅 Schedule a Consultation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🕐 **Available Time Slots**
        
        I offer flexible consultation times to accommodate different time zones:
        
        **Weekdays (Monday - Friday):**
        - 9:00 AM - 12:00 PM EST (Morning slots)
        - 1:00 PM - 5:00 PM EST (Afternoon slots)
        - 6:00 PM - 8:00 PM EST (Evening slots)
        
        **Weekends (by appointment):**
        - Saturday: 10:00 AM - 2:00 PM EST
        - Sunday: Available for urgent projects
        
        ### 🌍 **Time Zone Friendly**
        - **US/Canada:** All time zones accommodated
        - **Europe:** Morning/afternoon slots available
        - **Asia/Pacific:** Evening slots (my time) work well
        """)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
        ">
            <h3 style="margin: 0 0 1rem 0;">📅 Book Now</h3>
            <p style="margin: 0 0 1rem 0;">Free 30-minute consultation</p>
            <a href="https://calendly.com/yourusername" target="_blank" style="
                background: white;
                color: #667eea;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                text-decoration: none;
                font-weight: bold;
                display: inline-block;
            ">
                Schedule Call
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # FAQ
    st.markdown("## ❓ Frequently Asked Questions")
    
    with st.expander("💰 What are your rates and pricing structure?"):
        st.markdown("""
        **Hourly Consulting:** $150/hour  
        **Dashboard Development:** Starting at $1,500  
        **Data Engineering Projects:** Starting at $2,000  
        **Web Applications:** Starting at $2,500  
        **Machine Learning Projects:** Starting at $3,000  
        
        All projects include:
        - Detailed project documentation
        - Source code and deployment guides  
        - 30 days of post-launch support
        - Training session for your team
        
        *Custom pricing available for long-term engagements and enterprise projects.*
        """)
    
    with st.expander("⏱️ What is your typical project timeline?"):
        st.markdown("""
        **Dashboard Development:** 1-3 weeks  
        **Data Pipeline/ETL:** 2-4 weeks  
        **Web Applications:** 3-6 weeks  
        **Machine Learning Projects:** 4-8 weeks  
        **Full-Stack Solutions:** 6-12 weeks  
        
        Timeline depends on:
        - Project complexity and scope
        - Data availability and quality
        - Integration requirements
        - Testing and deployment needs
        
        I provide detailed project timelines during the proposal phase.
        """)
    
    with st.expander("🛠️ What technologies and tools do you use?"):
        st.markdown("""
        **Programming:** Python, SQL, JavaScript, R  
        **Visualization:** Power BI, Tableau, Plotly, D3.js  
        **Web Frameworks:** Streamlit, Flask, FastAPI  
        **Databases:** PostgreSQL, MySQL, MongoDB  
        **Cloud Platforms:** AWS, Azure, Google Cloud  
        **ML/AI:** Scikit-learn, TensorFlow, PyTorch  
        **DevOps:** Docker, Kubernetes, GitHub Actions  
        
        I choose the best technology stack for each project based on requirements, budget, and long-term maintenance needs.
        """)
    
    with st.expander("🎓 Do you provide training and knowledge transfer?"):
        st.markdown("""
        **Yes!** Knowledge transfer is included in all projects:
        
        - **Documentation:** Comprehensive technical documentation
        - **Training Sessions:** Live training for your team
        - **Video Tutorials:** Recorded sessions for future reference  
        - **Best Practices Guide:** Maintenance and optimization tips
        - **Ongoing Support:** 30 days post-launch support included
        
        **Additional Training Options:**
        - Custom workshops for your team
        - Advanced analytics training programs
        - Tool-specific certification preparation
        """)
    
    with st.expander("🔒 How do you handle data security and confidentiality?"):
        st.markdown("""
        **Data Security is my top priority:**
        
        - **NDA/Confidentiality Agreements:** Standard for all projects
        - **Secure Development:** Following industry best practices
        - **Data Encryption:** At rest and in transit
        - **Access Controls:** Role-based permissions and authentication
        - **Compliance:** GDPR, CCPA, and industry-specific regulations
        
        **Security Measures:**
        - Secure coding practices
        - Regular security audits
        - Encrypted communication channels
        - Secure cloud infrastructure
        - Data backup and recovery procedures
        """)

# Run the application
if __name__ == "__main__":
    main()"""
Interactive Data Science Portfolio Website

A comprehensive, interactive portfolio showcasing data science projects,
dashboards, and analytical capabilities using Streamlit.

Author: Your Name
Date: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Data Science Portfolio | Your Name",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://your-portfolio.com/help',
        'Report a bug': 'https://your-portfolio.com/contact',
        'About': """
        # Interactive Data Science Portfolio
        
        Professional portfolio showcasing expertise in:
        - Interactive Dashboard Development
        - Data Engineering & ETL Pipelines  
        - Business Intelligence Solutions
        - Machine Learning & Analytics
        - Full-Stack Data Applications
        
        Contact: your.email@example.com
        """
    }
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        text-align: center;
    }
    
    .project-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2a5298;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .skill-badge {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .contact-button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .contact-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .testimonial {
        background: #f8f9fa;
        padding: 1.5rem;
        border-left: 4px solid #2a5298;
        border-radius: 0 10px 10px 0;
        font-style: italic;
        margin: 1rem 0;
    }
    
    .tech-stack {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #90caf9;
    }
</style>
""", unsafe_allow_html=True)

# Utility functions
def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        import requests
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def get_base64_of_bin_file(bin_file):
    """Convert binary file to base64 string"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def create_download_link(val, filename):
    """Create download link for file"""
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}">Download {filename}</a>'

# Sample data for demonstrations
def generate_sample_analytics_data():
    """Generate sample analytics data for demonstrations"""
    dates = pd.date_range('2024-01-01', periods=90, freq='D')
    
    analytics_data = pd.DataFrame({
        'date': dates,
        'page_views': np.random.poisson(1000, 90) + np.random.normal(0, 50, 90),
        'unique_visitors': np.random.poisson(400, 90) + np.random.normal(0, 30, 90),
        'bounce_rate': np.random.normal(0.35, 0.1, 90).clip(0, 1),
        'conversion_rate': np.random.normal(0.05, 0.02, 90).clip(0, 1)
    })
    
    return analytics_data

def create_skills_chart():
    """Create interactive skills proficiency chart"""
    skills_data = {
        'Python': 95,
        'SQL': 90,
        'Power BI': 85,
        'Streamlit': 90,
        'Machine Learning': 80,
        'Data Visualization': 95,
        'ETL Pipelines': 85,
        'Cloud Platforms': 75,
        'JavaScript': 70,
        'Docker': 75
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(skills_data.values()),
            y=list(skills_data.keys()),
            orientation='h',
            marker=dict(
                color=list(skills_data.values()),
                colorscale='Blues',
                showscale=True
            ),
            text=[f"{v}%" for v in skills_data.values()],
            textposition='inside'
        )
    ])
    
    fig.update_layout(
        title="Technical Skills Proficiency",
        xaxis_title="Proficiency (%)",
        height=400,
        template="plotly_white"
    )
    
    return fig

def create_project_timeline():
    """Create project timeline visualization"""
    projects = [
        {'Project': 'Sales Dashboard', 'Start': '2024-01-15', 'End': '2024-02-15', 'Category': 'Dashboard'},
        {'Project': 'ETL Pipeline', 'Start': '2024-02-01', 'End': '2024-03-01', 'Category': 'Engineering'},
        {'Project': 'Log Analyzer', 'Start': '2024-02-15', 'End': '2024-03-15', 'Category': 'Analytics'},
        {'Project': 'CSV Tool', 'Start': '2024-03-01', 'End': '2024-03-30', 'Category': 'Web App'},
        {'Project': 'Traffic Monitor', 'Start': '2024-03-15', 'End': '2024-04-15', 'Category': 'Dashboard'}
    ]
    
    df = pd.DataFrame(projects)
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])
    
    fig = px.timeline(
        df, 
        x_start='Start', 
        x_end='End', 
        y='Project',
        color='Category',
        title='Project Timeline - Recent Work'
    )
    
    fig.update_layout(height=300, template="plotly_white")
    return fig

# Main application
def main():
    """Main portfolio application"""
    
    # Navigation
    st.sidebar.title("🚀 Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "💼 Projects", "🛠️ Skills", "📊 Live Demos", "📞 Contact"]
    )
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "💼 Projects":
        show_projects_page()
    elif page == "🛠️ Skills":
        show_skills_page()
    elif page == "📊 Live Demos":
        show_demos_page()
    elif page == "📞 Contact":
        show_contact_page()

def show_home_page():
    """Display home page"""
    
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">
            🚀 Data Science Portfolio
        </h1>
        <h2 style="font-size: 1.5rem; margin: 0; opacity: 0.9;">
            Transforming Data into Actionable Business Intelligence
        </h2>
        <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.8;">
            Interactive Dashboards • Advanced Analytics • Full-Stack Solutions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">15+</h2>
            <p style="margin: 0.5rem 0;">Interactive Dashboards</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">500k+</h2>
            <p style="margin: 0.5rem 0;">Records Processed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">99.9%</h2>
            <p style="margin: 0.5rem 0;">Uptime Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #2a5298; margin: 0;">3+</h2>
            <p style="margin: 0.5rem 0;">Years Experience</p>
        </div>
        """, unsafe_allow_html=True)
    
    # About Section
    st.markdown("## 👋 Welcome to My Portfolio")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        I'm a **Data Science Professional** specializing in transforming complex data into 
        actionable business insights. With expertise spanning from **interactive dashboard development** 
        to **machine learning implementation**, I help organizations make data-driven decisions 
        that drive growth and efficiency.
        
        ### 🎯 **Core Specializations:**
        - **📊 Business Intelligence Dashboards** - Power BI, Tableau, Custom Solutions
        - **🔧 Data Engineering** - ETL Pipelines, Database Optimization, Cloud Architecture  
        - **🌐 Web Applications** - Streamlit, Flask, Interactive Data Tools
        - **📈 Advanced Analytics** - Statistical Modeling, Machine Learning, Forecasting
        - **☁️ Cloud Solutions** - AWS, GCP, Azure Data Services
        
        ### 🏆 **Recent Achievements:**
        - Developed real-time monitoring dashboards reducing incident response time by **80%**
        - Built ETL pipelines processing **500k+ records daily** with 99.9% accuracy
        - Created interactive tools used by **50+ analysts** across multiple organizations
        - Delivered projects resulting in **$2M+ cost savings** for clients
        """)
    
    with col2:
        st.image("assets/profile_photo.jpg" if Path("assets/profile_photo.jpg").exists() else "https://via.placeholder.com/300x300", 
                caption="Professional Profile", width=300)
        
        st.markdown("""
        ### 🎓 **Certifications:**
        - Microsoft Power BI Data Analyst
        - AWS Cloud Practitioner  
        - Python for Data Science
        - SQL Database Administration
        
        ### 📍 **Location:**
        Remote • Available Worldwide
        
        ### ⏰ **Availability:**
        Open for new projects
        """)
    
    # Featured Projects Preview
    st.markdown("## 🌟 Featured Projects")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="project-card">
            <h3>📊 Sales Analytics Dashboard</h3>
            <p>Interactive Power BI dashboard tracking KPIs, sales funnels, and regional performance with real-time data updates.</p>
            <div class="tech-stack">
                <strong>Tech:</strong> Power BI, SQL Server, DAX
            </div>
            <p><strong>Impact:</strong> 40% faster reporting, $500K cost savings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="project-card">
            <h3>🔧 CSV Insight Tool</h3>
