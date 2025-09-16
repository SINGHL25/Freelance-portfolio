# Process uploaded or sample data
    if uploaded_file or 'demo_data' in st.session_state:
        try:
            # Load data
            if uploaded_file == "sample_data" or 'demo_data' in st.session_state:
                df = st.session_state.demo_data if 'demo_data' in st.session_state else load_sample_data("sales")
                data_source = "Sample Sales Data"
            else:
                df = pd.read_csv(uploaded_file)
                data_source = uploaded_file.name
            
            st.success(f"✅ Successfully loaded {data_source}")
            
            # Data Overview Section
            st.markdown("### 📋 Data Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Rows", f"{len(df):,}")
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Missing Values", f"{df.isnull().sum().sum():,}")
            with col4:
                memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024
                st.metric("Memory Usage", f"{memory_usage:.1f} MB")
            
            # Data Sample
            st.markdown("### 👀 Data Sample")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Data Profiling
            st.markdown("### 🔍 Automated Data Profiling")
            
            profiling_tabs = st.tabs(["📊 Statistical Summary", "📈 Data Quality", "🎯 Column Analysis", "📉 Distributions"])
            
            with profiling_tabs[0]:
                # Statistical summary
                st.markdown("#### Statistical Summary")
                
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if not numeric_cols.empty:
                    summary_stats = df[numeric_cols].describe()
                    st.dataframe(summary_stats, use_container_width=True)
                else:
                    st.info("No numeric columns found for statistical analysis")
                
                # Categorical summary
                categorical_cols = df.select_dtypes(include=['object']).columns
                if not categorical_cols.empty:
                    st.markdown("#### Categorical Data Summary")
                    
                    cat_summary = []
                    for col in categorical_cols[:5]:  # Limit to first 5 categorical columns
                        cat_summary.append({
                            'Column': col,
                            'Unique Values': df[col].nunique(),
                            'Most Frequent': df[col].mode().iloc[0] if not df[col].empty else 'N/A',
                            'Missing Count': df[col].isnull().sum()
                        })
                    
                    cat_df = pd.DataFrame(cat_summary)
                    st.dataframe(cat_df, use_container_width=True)
            
            with profiling_tabs[1]:
                # Data Quality Assessment
                st.markdown("#### Data Quality Assessment")
                
                quality_metrics = []
                for col in df.columns:
                    missing_pct = (df[col].isnull().sum() / len(df)) * 100
                    unique_pct = (df[col].nunique() / len(df)) * 100
                    
                    if df[col].dtype in ['object']:
                        # For text columns, check for consistency
                        consistency_score = 100 - (df[col].str.len().std() / df[col].str.len().mean() * 100) if df[col].str.len().mean() > 0 else 100
                    else:
                        # For numeric columns, check for outliers
                        Q1 = df[col].quantile(0.25)
                        Q3 = df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))][col].count()
                        consistency_score = 100 - (outliers / len(df) * 100)
                    
                    quality_metrics.append({
                        'Column': col,
                        'Data Type': str(df[col].dtype),
                        'Completeness (%)': round(100 - missing_pct, 1),
                        'Uniqueness (%)': round(unique_pct, 1),
                        'Consistency (%)': round(max(0, consistency_score), 1),
                        'Overall Score': round((100 - missing_pct + unique_pct + max(0, consistency_score)) / 3, 1)
                    })
                
                quality_df = pd.DataFrame(quality_metrics)
                
                # Color coding for quality scores
                def color_quality_score(val):
                    if val >= 80:
                        return 'background-color: #d4edda'  # Green
                    elif val >= 60:
                        return 'background-color: #fff3cd'  # Yellow
                    else:
                        return 'background-color: #f8d7da'  # Red
                
                styled_quality = quality_df.style.applymap(
                    color_quality_score, 
                    subset=['Completeness (%)', 'Uniqueness (%)', 'Consistency (%)', 'Overall Score']
                )
                
                st.dataframe(styled_quality, use_container_width=True)
            
            with profiling_tabs[2]:
                # Column Analysis
                st.markdown("#### Individual Column Analysis")
                
                selected_column = st.selectbox("Select column to analyze:", df.columns)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Basic statistics for selected column
                    st.markdown(f"**{selected_column} - Basic Statistics**")
                    
                    col_info = {
                        'Data Type': str(df[selected_column].dtype),
                        'Non-null Count': f"{df[selected_column].count():,}",
                        'Null Count': f"{df[selected_column].isnull().sum():,}",
                        'Unique Values': f"{df[selected_column].nunique():,}",
                        'Memory Usage': f"{df[selected_column].memory_usage(deep=True) / 1024:.1f} KB"
                    }
                    
                    for key, value in col_info.items():
                        st.write(f"**{key}:** {value}")
                
                with col2:
                    # Value distribution
                    if df[selected_column].dtype in ['object']:
                        value_counts = df[selected_column].value_counts().head(10)
                        fig = px.bar(x=value_counts.values, y=value_counts.index, 
                                   orientation='h', title=f'Top 10 Values in {selected_column}')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = px.histogram(df, x=selected_column, 
                                         title=f'Distribution of {selected_column}')
                        st.plotly_chart(fig, use_container_width=True)
            
            with profiling_tabs[3]:
                # Data Distributions
                st.markdown("#### Data Distributions")
                
                numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if numeric_columns:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Correlation heatmap
                        if len(numeric_columns) > 1:
                            correlation_matrix = df[numeric_columns].corr()
                            fig_corr = px.imshow(correlation_matrix, 
                                               title='Correlation Matrix',
                                               color_continuous_scale='RdBu')
                            st.plotly_chart(fig_corr, use_container_width=True)
                    
                    with col2:
                        # Distribution comparison
                        if len(numeric_columns) >= 2:
                            x_col = st.selectbox("X-axis:", numeric_columns, key="dist_x")
                            y_col = st.selectbox("Y-axis:", numeric_columns, key="dist_y", 
                                               index=1 if len(numeric_columns) > 1 else 0)
                            
                            fig_scatter = px.scatter(df, x=x_col, y=y_col,
                                                   title=f'{x_col} vs {y_col}')
                            st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.info("No numeric columns available for distribution analysis")
            
            # Interactive Visualizations
            st.markdown("### 📊 Interactive Visualizations")
            
            viz_type = st.selectbox(
                "Choose visualization type:",
                ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot", "Histogram", "Pie Chart"]
            )
            
            # Dynamic chart creation based on data types
            if viz_type == "Bar Chart":
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if categorical_cols and numeric_cols:
                    x_col = st.selectbox("Category (X-axis):", categorical_cols)
                    y_col = st.selectbox("Value (Y-axis):", numeric_cols)
                    
                    # Aggregate data for bar chart
                    agg_data = df.groupby(x_col)[y_col].sum().reset_index()
                    fig = px.bar(agg_data, x=x_col, y=y_col,
                               title=f'{y_col} by {x_col}')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Bar chart requires both categorical and numeric columns")
            
            elif viz_type == "Scatter Plot":
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if len(numeric_cols) >= 2:
                    x_col = st.selectbox("X-axis:", numeric_cols, key="scatter_x")
                    y_col = st.selectbox("Y-axis:", numeric_cols, key="scatter_y", index=1)
                    
                    color_col = None
                    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                    if categorical_cols:
                        color_col = st.selectbox("Color by (optional):", 
                                               ["None"] + categorical_cols)
                        color_col = None if color_col == "None" else color_col
                    
                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                                   title=f'{x_col} vs {y_col}')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Scatter plot requires at least 2 numeric columns")
            
            # Export and Download Options
            st.markdown("### 📥 Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Download cleaned data
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📄 Download as CSV",
                    data=csv_data,
                    file_name=f"analyzed_{data_source}",
                    mime="text/csv"
                )
            
            with col2:
                # Download data profile report
                profile_report = generate_profile_report(df)
                st.download_button(
                    label="📊 Download Profile Report",
                    data=profile_report,
                    file_name="data_profile_report.txt",
                    mime="text/plain"
                )
            
            with col3:
                if st.button("🔄 Reset Analysis"):
                    st.rerun()
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.error("Please ensure your CSV file is properly formatted and try again.")

def generate_profile_report(df):
    """Generate a text-based data profile report"""
    report = []
    report.append("DATA PROFILE REPORT")
    report.append("=" * 50)
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Basic info
    report.append("BASIC INFORMATION:")
    report.append(f"  Rows: {len(df):,}")
    report.append(f"  Columns: {len(df.columns)}")
    report.append(f"  Memory Usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")
    report.append("")
    
    # Column details
    report.append("COLUMN DETAILS:")
    for col in df.columns:
        report.append(f"  {col}:")
        report.append(f"    Data Type: {df[col].dtype}")
        report.append(f"    Non-null: {df[col].count():,}")
        report.append(f"    Null: {df[col].isnull().sum():,}")
        report.append(f"    Unique: {df[col].nunique():,}")
        report.append("")
    
    return "\n".join(report)

def show_log_visualizer():
    """Log Visualizer Web App Demo"""
    
    st.markdown("## 📈 Real-time Log Visualizer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Interactive Log Monitoring Platform
        
        Real-time log visualization and analysis platform built with Flask and WebSockets, 
        providing instant insights into application performance, error tracking, and 
        system health monitoring.
        
        ### Core Features
        - **Real-time Streaming**: Live log ingestion and processing
        - **Multi-format Support**: JSON, plain text, structured logs
        - **Interactive Dashboards**: Customizable charts and metrics
        - **Alerting System**: Configurable thresholds and notifications
        - **Search & Filter**: Advanced log querying capabilities
        - **Export Functions**: Data export and report generation
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📊 Platform Stats</h4>
            <p><strong>Logs/Second:</strong> 10K+</p>
            <p><strong>Data Retention:</strong> 30 days</p>
            <p><strong>Response Time:</strong> <100ms</p>
            <p><strong>Uptime:</strong> 99.9%</p>
        </div>
        
        <div class="success-box">
            <h4>🎯 Performance</h4>
            <p><strong>Issue Detection:</strong> 95% faster</p>
            <p><strong>Mean Time to Recovery:</strong> 60% improvement</p>
            <p><strong>False Alerts:</strong> 80% reduction</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Live Log Visualizer Demo
    st.markdown("### 📊 Live Log Analytics Demo")
    
    # Simulated real-time controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        log_level_filter = st.multiselect(
            "Filter by Log Level:",
            ["DEBUG", "INFO", "WARNING", "ERROR"],
            default=["INFO", "WARNING", "ERROR"]
        )
    
    with col2:
        service_filter = st.multiselect(
            "Filter by Service:",
            ["auth", "api", "database", "frontend"],
            default=["auth", "api", "database", "frontend"]
        )
    
    with col3:
        auto_refresh = st.checkbox("Auto-refresh (5s)", value=False)
    
    if auto_refresh:
        time.sleep(5)
        st.rerun()
    
    # Load and filter log data
    log_data = load_sample_data("logs")
    
    # Apply filters
    filtered_logs = log_data[
        (log_data['log_level'].isin(log_level_filter)) &
        (log_data['service'].isin(service_filter))
    ]
    
    # Real-time metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        error_count = len(filtered_logs[filtered_logs['log_level'] == 'ERROR'])
        st.metric("Errors (Last Hour)", error_count, f"+{np.random.randint(0, 15)}")
    
    with col2:
        warning_count = len(filtered_logs[filtered_logs['log_level'] == 'WARNING'])
        st.metric("Warnings", warning_count, f"+{np.random.randint(0, 30)}")
    
    with col3:
        avg_response = filtered_logs['response_time'].mean()
        st.metric("Avg Response", f"{avg_response:.0f}ms", f"+{np.random.randint(-20, 50)}ms")
    
    with col4:
        unique_ips = filtered_logs['ip_address'].nunique()
        st.metric("Unique IPs", unique_ips, f"+{np.random.randint(0, 25)}")
    
    # Log visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Log level distribution over time
        hourly_logs = filtered_logs.groupby([
            filtered_logs['timestamp'].dt.hour, 
            'log_level'
        ]).size().reset_index(name='count')
        
        fig1 = px.bar(hourly_logs, x='timestamp', y='count', color='log_level',
                     title='Log Distribution by Hour')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Response time by service
        service_metrics = filtered_logs.groupby('service').agg({
            'response_time': 'mean',
            'status_code': lambda x: (x != 200).sum()  # Error count
        }).reset_index()
        
        fig2 = px.scatter(service_metrics, x='response_time', y='status_code', 
                         size='response_time', color='service',
                         title='Service Performance Matrix')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Recent log entries
    st.markdown("### 📝 Recent Log Entries")
    
    recent_logs = filtered_logs.tail(20).sort_values('timestamp', ascending=False)
    
    # Format logs for display
    display_logs = recent_logs[['timestamp', 'log_level', 'service', 'response_time', 'status_code']].copy()
    display_logs['timestamp'] = display_logs['timestamp'].dt.strftime('%H:%M:%S')
    
    st.dataframe(display_logs, use_container_width=True)

def show_data_processing_tools():
    """Additional Data Processing Tools"""
    
    st.markdown("## 🔧 Data Processing Tools Suite")
    
    tool_tabs = st.tabs(["🔄 Data Converter", "🧹 Data Cleaner", "📊 Quick Analytics"])
    
    with tool_tabs[0]:
        st.markdown("### 🔄 Universal Data Converter")
        
        st.markdown("""
        Convert between various data formats with automatic schema detection and validation.
        """)
        
        # File conversion tool
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Input Format:**")
            input_format = st.selectbox("Select input format:", ["CSV", "JSON", "XML", "Excel"])
            
            uploaded_convert_file = st.file_uploader(
                "Upload file to convert:",
                type=['csv', 'json', 'xml', 'xlsx']
            )
        
        with col2:
            st.markdown("**Output Format:**")
            output_format = st.selectbox("Select output format:", ["CSV", "JSON", "XML", "Excel"])
            
            if st.button("🔄 Convert File") and uploaded_convert_file:
                st.info(f"Converting from {input_format} to {output_format}...")
                st.success("✅ Conversion completed! Download link generated.")
    
    with tool_tabs[1]:
        st.markdown("### 🧹 Automated Data Cleaner")
        
        cleaning_options = st.multiselect(
            "Select cleaning operations:",
            [
                "Remove duplicates",
                "Fill missing values", 
                "Standardize text formatting",
                "Remove outliers",
                "Validate email formats",
                "Normalize phone numbers",
                "Convert data types"
            ]
        )
        
        if cleaning_options:
            st.markdown("**Selected Operations:**")
            for option in cleaning_options:
                st.write(f"✅ {option}")
    
    with tool_tabs[2]:
        st.markdown("### 📊 Quick Analytics Engine")
        
        if st.button("🎲 Generate Sample Report"):
            # Create sample analytics
            sample_metrics = {
                'Metric': ['Total Records', 'Data Quality Score', 'Processing Time', 'Error Rate'],
                'Value': ['1,234,567', '94.5%', '2.3 seconds', '0.02%'],
                'Status': ['✅ Good', '✅ Excellent', '✅ Fast', '✅ Low']
            }
            
            metrics_df = pd.DataFrame(sample_metrics)
            st.dataframe(metrics_df, use_container_width=True)
            
            # Quick visualization
            fig = px.bar(x=['Quality', 'Performance', 'Reliability'], 
                        y=[94.5, 88.2, 99.1],
                        title='System Health Metrics')
            st.plotly_chart(fig, use_container_width=True)

# Documentation Page
def show_documentation_page():
    """Display documentation and resources"""
    
    st.title("📋 Documentation & Resources")
    st.markdown("### Technical guides, API documentation, and project resources")
    
    doc_tabs = st.tabs(["📖 Technical Guides", "💰 Services & Pricing", "📁 Project Files", "🔗 Resources"])
    
    with doc_tabs[0]:
        st.markdown("## 📖 Technical Documentation")
        
        # Documentation sections
        doc_sections = st.selectbox(
            "Select documentation section:",
            [
                "Getting Started Guide",
                "Dashboard Development",
                "ETL Pipeline Setup", 
                "API Integration",
                "Deployment Guide",
                "Troubleshooting"
            ]
        )
        
        if doc_sections == "Getting Started Guide":
            st.markdown("""
            ### 🚀 Getting Started Guide
            
            #### Prerequisites
            - Python 3.8 or higher
            - Database access (PostgreSQL recommended)
            - Basic knowledge of SQL and data analysis
            
            #### Installation Steps
            
            1. **Clone the repository:**
            ```bash
            git clone https://github.com/yourname/data-science-portfolio
            cd data-science-portfolio
            ```
            
            2. **Create virtual environment:**
            ```bash
            python -m venv venv
            source venv/bin/activate  # On Windows: venv\\Scripts\\activate
            ```
            
            3. **Install dependencies:**
            ```bash
            pip install -r requirements.txt
            ```
            
            4. **Configure environment variables:**
            ```bash
            cp .env.example .env
            # Edit .env with your database credentials and API keys
            ```
            
            5. **Run the application:**
            ```bash
            streamlit run app.py
            ```
            
            #### Quick Start Example
            ```python
            import pandas as pd
            import plotly.express as px
            from portfolio_tools import DataProcessor
            
            # Load and process data
            processor = DataProcessor()
            df = processor.load_csv('your_data.csv')
            
            # Generate insights
            insights = processor.analyze(df)
            print(insights)
            ```
            """)
        
        elif doc_sections == "Dashboard Development":
            st.markdown("""
            ### 📊 Dashboard Development Guide
            
            #### Architecture Overview
            Our dashboard system uses a modular architecture with the following components:
            
            - **Data Layer**: Database connections and data processing
            - **Logic Layer**: Business logic and calculations  
            - **Presentation Layer**: Streamlit UI components
            - **Caching Layer**: Redis for performance optimization
            
            #### Creating Custom Dashboards
            
            1. **Define your data model:**
            ```python
            class SalesDashboard:
                def __init__(self, data_source):
                    self.data = data_source
                    self.metrics = self.calculate_metrics()
                
                def calculate_metrics(self):
                    return {
                        'total_sales': self.data['amount'].sum(),
                        'order_count': len(self.data),
                        'avg_order_value': self.data['amount'].mean()
                    }
            ```
            
            2. **Build visualizations:**
            ```python
            def create_sales_chart(data):
                fig = px.line(data, x='date', y='sales',
                             title='Sales Trend Over Time')
                return fig
            ```
            
            3. **Add interactivity:**
            ```python
            # Filters and controls
            date_range = st.date_input("Select date range")
            region_filter = st.multiselect("Select regions", regions)
            
            # Dynamic updates
            filtered_data = filter_data(data, date_range, region_filter)
            st.plotly_chart(create_sales_chart(filtered_data))
            ```
            """)
    
    with doc_tabs[1]:
        st.markdown("## 💰 Services & Pricing")
        
        # Pricing table
        pricing_data = {
            'Service': [
                'Dashboard Development',
                'ETL Pipeline Setup', 
                'Data Analysis & Reporting',
                'Web Application Development',
                'Database Optimization',
                'Training & Consultation'
            ],
            'Duration': ['2-4 weeks', '3-6 weeks', '1-3 weeks', '4-8 weeks', '1-2 weeks', 'Hourly'],
            'Starting Price': ['$2,500', '$4,000', '$1,500', '$5,000', '$2,000', '$150/hour'],
            'Includes': [
                'Custom dashboard, documentation, training',
                'Full pipeline, monitoring, documentation', 
                'Analysis, reports, recommendations',
                'Full-stack app, deployment, support',
                'Performance tuning, query optimization',
                'Expert guidance, best practices'
            ]
        }
        
        pricing_df = pd.DataFrame(pricing_data)
        st.dataframe(pricing_df, use_container_width=True)
        
        st.markdown("""
        ### 📋 What's Included
        
        **All projects include:**
        - ✅ Comprehensive documentation
        - ✅ Source code and deployment guides
        - ✅ 30 days post-launch support
        - ✅ Training session for your team
        - ✅ Performance optimization
        - ✅ Security best practices
        
        **Enterprise packages available with:**
        - 🏢 Dedicated project manager
        - 📞 Priority support (24/7)
        - 🔒 Advanced security features
        - 📈 Custom SLA agreements
        - 🎓 Extended training programs
        """)
    
    with doc_tabs[2]:
        st.markdown("## 📁 Project Resources")
        
        # File downloads simulation
        st.markdown("### 📥 Downloadable Resources")
        
        resources = [
            ("Portfolio Slide Deck", "portfolio_presentation.pdf", "Comprehensive overview of projects and capabilities"),
            ("Technical Architecture", "system_architecture.pdf", "Detailed technical documentation"),
            ("Sample Datasets", "sample_data.zip", "Example datasets for testing and development"),
            ("Code Templates", "code_templates.zip", "Reusable code snippets and templates"),
            ("Best Practices Guide", "best_practices.pdf", "Industry best practices and guidelines")
        ]
        
        for title, filename, description in resources:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{title}**")
                st.write(description)
            
            with col2:
                st.write(filename)
            
            with col3:
                st.button(f"📥 Download", key=filename)
        
        # GitHub repository
        st.markdown("### 💻 Source Code")
        st.markdown("""
        **GitHub Repository:** [github.com/yourname/data-portfolio](https://github.com/yourname/data-portfolio)
        
        The complete source code for all projects is available on GitHub, including:
        - Dashboard implementations
        - ETL pipeline code
        - Web application source
        - Database scripts
        - Documentation and examples
        """)
    
    with doc_tabs[3]:
        st.markdown("## 🔗 Additional Resources")
        
        st.markdown("""
        ### 📚 Learning Resources
        
        **Recommended Reading:**
        - [Python for Data Analysis](https://wes.mckinney.com/book/) by Wes McKinney
        - [The Data Warehouse Toolkit](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/books/) by Ralph Kimball
        - [Streamlit Documentation](https://docs.streamlit.io/)
        
        **Online Courses:**
        - [Advanced SQL for Data Scientists](https://www.coursera.org/learn/sql-for-data-science)
        - [Data Visualization with Python](https://www.datacamp.com/courses/data-visualization-with-python)
        - [Building Dashboards with Plotly](https://plotly.com/python/)
        
        ### 🛠️ Tools & Technologies
        
        **Development Stack:**
        - **Languages:** Python, SQL, JavaScript
        - **Databases:** PostgreSQL, MongoDB, Redis
        - **Visualization:** Plotly, Streamlit, Power BI
        - **Cloud:** AWS, Azure, Google Cloud
        - **DevOps:** Docker, GitHub Actions
        
        **Useful Libraries:**
        ```python
        # Data processing
        import pandas as pd
        import numpy as np
        
        # Visualization
        import plotly.express as px
        import plotly.graph_objects as go
        
        # Web framework
        import streamlit as st
        
        # Database
        from sqlalchemy import create_engine
        ```
        """)

# Contact Page
def show_contact_page():
    """Display contact information and consultation form"""
    
    st.title("📞 Contact & Consultation")
    st.markdown("### Let's discuss your data science and analytics needs")
    
    # Contact header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Ready to transform your data into actionable insights? I specialize in creating 
        custom data solutions that drive business value and operational efficiency.
        
        ### 🎯 What I Offer:
        
        **📊 Dashboard Development**
        - Executive KPI dashboards
        - Real-time monitoring systems
        - Interactive business intelligence solutions
        - Mobile-responsive designs
        
        **🔧 Data Engineering**
        - ETL pipeline development
        - Database optimization
        - Data quality frameworks
        - Cloud architecture design
        
        **🌐 Web Applications**
        - Custom data applications
        - API development and integration
        - User-friendly interfaces
        - Scalable architectures
        
        **📈 Analytics & Insights**
        - Statistical analysis
        - Machine learning models
        - Predictive analytics
        - Business intelligence consulting
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📊 Project Stats</h4>
            <p><strong>Projects Completed:</strong> 50+</p>
            <p><strong>Client Satisfaction:</strong> 98%</p>
            <p><strong>Average ROI:</strong> 300%</p>
            <p><strong>Response Time:</strong> <24 hours</p>
        </div>
        
        <div class="success-box">
            <h4>🎯 Why Choose Me</h4>
            <p><strong>✅ Proven Results:</strong> Delivered $5M+ in value</p>
            <p><strong>✅ Fast Delivery:</strong> Agile development approach</p>
            <p><strong>✅ Full Support:</strong> 30-day post-launch support</p>
            <p><strong>✅ Transparent:</strong> Fixed pricing, no surprises</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Contact form
    st.markdown("## 📝 Get Started Today")
    
    with st.form("contact_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john@company.com")
            company = st.text_input("Company/Organization", placeholder="Your Company")
        
        with col2:
            phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
            budget = st.selectbox("Project Budget Range", 
                                 ["< $5,000", "$5,000 - $15,000", "$15,000 - $50,000", "> $50,000"])
            timeline = st.selectbox("Desired Timeline", 
                                   ["ASAP", "Within 2 weeks", "1 month", "2-3 months", "Flexible"])
        
        project_type = st.multiselect(
            "Services Needed *",
            ["Dashboard Development", "ETL Pipeline", "Web Application", 
             "Data Analysis", "Database Optimization", "Consultation"]
        )
        
        message = st.text_area(
            "Project Description *",
            placeholder="Please describe your project requirements, current challenges, data sources, and expected outcomes...",
            height=120
        )
        
        col1, col2 = st.columns(2)
        with col1:
            free_consultation = st.checkbox("Request free 30-minute consultation call")
        with col2:
            newsletter = st.checkbox("Subscribe to data insights newsletter")
        
        submitted = st.form_submit_button("🚀 Send Project Inquiry", type="primary", use_container_width=True)
        
        if submitted:
            if name and email and project_type and message:
                st.success("""
                ✅ **Thank you for your inquiry!** 
                
                Your project request has been received and I'll respond within 24 hours with:
                
                - Initial project assessment
                - Proposed timeline and approach  
                - Detailed cost estimate
                - Next steps and consultation scheduling
                
                **What happens next:**
                1. I'll review your requirements and send a detailed response
                2. We'll schedule a free consultation call to discuss specifics
                3. I'll provide a comprehensive project proposal
                4. Upon agreement, we'll kick off the project
                """)
                
                # Show fake processing animation
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                st.balloons()
            else:
                st.error("⚠️ Please fill in all required fields marked with *")
    
    # Direct contact options
    st.markdown("---")
    st.markdown("## 📱 Direct Contact Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="project-card">
            <h3>📧 Email</h3>
            <p><strong>your.email@example.com</strong></p>
            <p><strong>Response Time:</strong> Within 24 hours</p>
            <p><strong>Best For:</strong> Detailed project discussions, file sharing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="project-card">
            <h3>📱 Phone/WhatsApp</h3>
            <p><strong>+1 (555) 123-4567</strong></p>
            <p><strong>Hours:</strong> Mon-Fri 9 AM - 6 PM EST</p>
            <p><strong>Best For:</strong> Urgent questions, quick consultations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="project-card">
            <h3>💼 LinkedIn</h3>
            <p><strong>linkedin.com/in/yourname</strong></p>
            <p><strong>Response Time:</strong> 1-2 business days</p>
            <p><strong>Best For:</strong> Professional networking, referrals</p>
        </div>
        """, unsafe_allow_html=True)
    
    # FAQ Section
    st.markdown("## ❓ Frequently Asked Questions")
    
    faq_items = [
        {
            "question": "What's your typical project timeline?",
            "answer": "Project timelines vary based on complexity:\n\n- **Dashboards:** 2-4 weeks\n- **ETL Pipelines:** 3-6 weeks\n- **Web Applications:** 4-8 weeks\n- **Data Analysis:** 1-3 weeks\n\nI provide detailed timelines during the consultation phase."
        },
        {
            "question": "Do you offer fixed-price or hourly billing?",
            "answer": "I offer both options:\n\n- **Fixed-price projects** for well-defined scopes with clear deliverables\n- **Hourly consulting** at $150/hour for ongoing support or exploratory work\n- **Hybrid approach** with fixed milestones and hourly adjustments\n\nAll pricing is transparent with no hidden fees."
        },
        {
            "question": "What technologies do you specialize in?",
            "answer": "My core technology stack includes:\n\n- **Languages:** Python, SQL, JavaScript\n- **Databases:** PostgreSQL, MySQL, MongoDB\n- **Visualization:** Plotly, Streamlit, Power BI, Tableau\n- **Cloud:** AWS, Azure, Google Cloud Platform\n- **Tools:** Docker, Git, Apache Airflow\n\nI'm always learning new technologies to meet client needs."
        },
        {
            "question": "Do you provide training and documentation?",
            "answer": "Yes! Every project includes:\n\n- **Comprehensive documentation** with setup and usage guides\n- **Live training session** for your team\n- **Video tutorials** for complex features\n- **30 days of post-launch support** at no extra cost\n- **Best practices guide** for maintenance\n\nAdditional training sessions are available at $150/hour."
        },
        {
            "question": "Can you work with our existing systems?",
            "answer": "Absolutely! I have extensive experience integrating with:\n\n- **Legacy databases** and data warehouses\n- **Cloud platforms** (AWS, Azure, GCP)\n- **Business systems** (CRM, ERP, accounting software)\n- **APIs and web services**\n- **File systems and data lakes**\n\nI always assess your current infrastructure first to ensure seamless integration."
        }
    ]
    
    for i, item in enumerate(faq_items):
        with st.expander(f"💡 {item['question']}"):
            st.markdown(item['answer'])
    
    # Testimonials section
    st.markdown("## 👥 Client Testimonials")
    
    testimonials = [
        {
            "text": "The dashboard delivered exceeded our expectations. Response times improved by 80% and our team can now make data-driven decisions in real-time.",
            "author": "Sarah Johnson, VP of Operations",
            "company": "TechCorp Solutions"
        },
        {
            "text": "The ETL pipeline transformed our data processing capabilities. What used to take days now completes in hours with 99.8% accuracy.",
            "author": "Michael Chen, Data Director", 
            "company": "Global Analytics Inc"
        },
        {
            "text": "Exceptional technical expertise combined with clear communication. The project was delivered on time and within budget.",
            "author": "Emma Rodriguez, CTO",
            "company": "DataFlow Systems"
        }
    ]
    
    for testimonial in testimonials:
        st.markdown(f"""
        <div class="project-card">
            <p style="font-style: italic; font-size: 1.1rem; margin-bottom: 1rem;">
                "{testimonial['text']}"
            </p>
            <p style="margin: 0; font-weight: bold;">
                {testimonial['author']}
            </p>
            <p style="margin: 0; color: #666;">
                {testimonial['company']}
            </p>
        </div>
        """, unsafe_allow_html=True)

# Run the main application
if __name__ == "__main__":
    main()
# Web Applications Page
def show_webapps_page():
    """Display web applications and interactive tools"""
    
    st.title("🌐 Web Applications Portfolio")
    st.markdown("### Interactive web tools and full-stack data applications")
    
    webapp_tabs = st.tabs(["📊 CSV Insight Tool", "📈 Log Visualizer", "🔧 Data Processing Tools"])
    
    with webapp_tabs[0]:
        show_csv_insight_tool()
    
    with webapp_tabs[1]:
        show_log_visualizer()
    
    with webapp_tabs[2]:
        show_data_processing_tools()

def show_csv_insight_tool():
    """CSV Insight Tool Demo"""
    
    st.markdown("## 📊 CSV Insight Tool")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Intelligent CSV Analysis Platform
        
        Advanced web application for instant CSV analysis with automated insights, 
        statistical profiling, and interactive visualizations. Built for data analysts 
        who need quick, reliable data exploration capabilities.
        
        ### Key Features
        - **Drag & Drop Interface**: Intuitive file upload with instant processing
        - **Automated Insights**: AI-powered pattern recognition and anomaly detection  
        - **Statistical Profiling**: Comprehensive data quality and distribution analysis
        - **Interactive Charts**: Dynamic visualizations with drill-down capabilities
        - **Export Capabilities**: Download cleaned data and analysis reports
        - **Collaborative Features**: Share insights and annotate findings
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📊 Tool Usage</h4>
            <p><strong>Daily Users:</strong> 500+ analysts</p>
            <p><strong>Files Processed:</strong> 2K+ daily</p>
            <p><strong>Average Session:</strong> 15 minutes</p>
            <p><strong>User Satisfaction:</strong> 4.8/5</p>
        </div>
        
        <div class="success-box">
            <h4>🎯 Impact</h4>
            <p><strong>Analysis Speed:</strong> 10x faster</p>
            <p><strong>Accuracy:</strong> 95% improvement</p>
            <p><strong>Learning Curve:</strong> 80% reduction</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Live CSV Tool Demo
    st.markdown("### 🚀 Live Demo - Try It Now!")
    
    # File upload
    uploaded_file = st.file_uploader(
        "📁 Upload your CSV file for instant analysis",
        type=['csv'],
        help="Supported formats: CSV files up to 200MB"
    )
    
    # Demo with sample data option
    if not uploaded_file:
        st.info("👆 Upload a CSV file above, or use the sample data below to try the tool")
        
        if st.button("🎲 Load Sample Sales Data"):
            sample_data = load_sample_data("sales")
            uploaded_file = "sample_data"  # Flag to use sample data
            st.session_state.demo_data = sample_data
    
    # Process uploaded or sample data
    if uploaded_file or 'demo_data' in st.session_def show_excel_csv_etl():
    """Excel/CSV ETL Pipeline Demo"""
    
    st.markdown("## ⚡ Excel/CSV ETL Pipeline")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### High-Performance ETL System
        
        Automated ETL pipeline designed to process large Excel and CSV files with data validation, 
        transformation, and loading capabilities. Built for scalability and reliability with 
        comprehensive error handling and monitoring.
        
        ### Key Features
        - **Multi-format Support**: Excel (.xlsx, .xls), CSV, TSV file processing
        - **Data Validation**: Schema validation, data type checking, constraint validation
        - **Transformation Engine**: Data cleaning, normalization, enrichment
        - **Error Handling**: Comprehensive logging and error recovery
        - **Incremental Loading**: Change detection and delta processing
        - **Performance Monitoring**: Processing statistics and performance metrics
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📊 Pipeline Metrics</h4>
            <p><strong>Processing Speed:</strong> 500K+ records/hour</p>
            <p><strong>Accuracy Rate:</strong> 99.8%</p>
            <p><strong>Uptime:</strong> 99.5%</p>
            <p><strong>Files Processed:</strong> 10K+ monthly</p>
        </div>
        
        <div class="success-box">
            <h4>🎯 Business Impact</h4>
            <p><strong>Time Savings:</strong> 90% reduction</p>
            <p><strong>Error Reduction:</strong> 85% fewer data issues</p>
            <p><strong>Cost Savings:</strong> $300K annually</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive ETL Demo
    st.markdown("### 📂 Interactive ETL Demo")
    
    # File upload section
    uploaded_files = st.file_uploader(
        "Upload CSV/Excel files for processing",
        accept_multiple_files=True,
        type=['csv', 'xlsx', 'xls']
    )
    
    if uploaded_files:
        st.markdown("#### 📋 File Processing Results")
        
        processing_results = []
        
        for file in uploaded_files:
            try:
                # Determine file type and read
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                
                # Basic data profiling
                profile = {
                    'filename': file.name,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'missing_values': df.isnull().sum().sum(),
                    'duplicate_rows': df.duplicated().sum(),
                    'memory_usage': df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
                    'status': 'Success'
                }
                
                processing_results.append(profile)
                
            except Exception as e:
                processing_results.append({
                    'filename': file.name,
                    'rows': 0,
                    'columns': 0,
                    'missing_values': 0,
                    'duplicate_rows': 0,
                    'memory_usage': 0,
                    'status': f'Error: {str(e)}'
                })
        
        # Display processing results
        results_df = pd.DataFrame(processing_results)
        st.dataframe(results_df, use_container_width=True)
        
        # Show detailed analysis for first successful file
        successful_files = [f for f in uploaded_files if not f.name in results_df[results_df['status'] != 'Success']['filename'].values]
        
        if successful_files:
            selected_file = st.selectbox("Select file for detailed analysis:", 
                                       [f.name for f in successful_files])
            
            # Get the selected file data
            for file in successful_files:
                if file.name == selected_file:
                    if file.name.endswith('.csv'):
                        df = pd.read_csv(file)
                    else:
                        df = pd.read_excel(file)
                    break
            
            # Data quality assessment
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📊 Data Quality Assessment")
                
                quality_metrics = {
                    'Completeness': (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
                    'Uniqueness': (1 - df.duplicated().sum() / len(df)) * 100,
                    'Validity': 95.0,  # Simulated
                    'Consistency': 92.0  # Simulated
                }
                
                quality_df = pd.DataFrame(list(quality_metrics.items()), 
                                        columns=['Metric', 'Score'])
                
                fig_quality = px.bar(quality_df, x='Metric', y='Score',
                                   title='Data Quality Scores')
                fig_quality.update_yaxis(range=[0, 100])
                st.plotly_chart(fig_quality, use_container_width=True)
            
            with col2:
                st.markdown("##### 🔍 Column Analysis")
                
                column_analysis = []
                for col in df.columns:
                    column_analysis.append({
                        'Column': col,
                        'Type': str(df[col].dtype),
                        'Missing %': (df[col].isnull().sum() / len(df)) * 100,
                        'Unique Values': df[col].nunique()
                    })
                
                analysis_df = pd.DataFrame(column_analysis)
                st.dataframe(analysis_df, use_container_width=True)
            
            # ETL Transformations Demo
            st.markdown("##### ⚙️ Available Transformations")
            
            transformations = st.multiselect(
                "Select transformations to apply:",
                ["Remove Duplicates", "Handle Missing Values", "Standardize Formats", 
                 "Data Type Conversion", "Outlier Detection"]
            )
            
            if transformations and st.button("Apply Transformations"):
                transformed_df = df.copy()
                
                for transform in transformations:
                    if transform == "Remove Duplicates":
                        before_count = len(transformed_df)
                        transformed_df = transformed_df.drop_duplicates()
                        st.info(f"Removed {before_count - len(transformed_df)} duplicate rows")
                    
                    elif transform == "Handle Missing Values":
                        numeric_columns = transformed_df.select_dtypes(include=[np.number]).columns
                        transformed_df[numeric_columns] = transformed_df[numeric_columns].fillna(
                            transformed_df[numeric_columns].mean()
                        )
                        categorical_columns = transformed_df.select_dtypes(include=['object']).columns
                        transformed_df[categorical_columns] = transformed_df[categorical_columns].fillna('Unknown')
                        st.info("Filled missing values with mean (numeric) and 'Unknown' (categorical)")
                    
                    elif transform == "Standardize Formats":
                        for col in transformed_df.select_dtypes(include=['object']).columns:
                            transformed_df[col] = transformed_df[col].astype(str).str.strip().str.title()
                        st.info("Standardized text formatting")
                
                # Show before/after comparison
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Before Transformation:**")
                    st.dataframe(df.head(), use_container_width=True)
                
                with col2:
                    st.markdown("**After Transformation:**")
                    st.dataframe(transformed_df.head(), use_container_width=True)
                
                # Download processed data
                csv_data = transformed_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Processed Data",
                    data=csv_data,
                    file_name=f"processed_{selected_file}",
                    mime="text/csv"
                )
    
    # ETL Architecture and Code
    st.markdown("### 💻 ETL Implementation")
    
    etl_tabs = st.tabs(["🐍 Python Code", "🏗️ Architecture", "📊 Monitoring"])
    
    with etl_tabs[0]:
        st.markdown("#### ETL Pipeline Implementation")
        
        etl_code = '''
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import logging
from typing import List, Dict, Any
import os
from datetime import datetime

class ETLPipeline:
    """High-performance ETL pipeline for Excel/CSV processing"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = self._setup_logging()
        self.engine = create_engine(config['database_url'])
        self.stats = {'processed': 0, 'errors': 0, 'warnings': 0}
    
    def _setup_logging(self) -> logging.Logger:
        """Configure comprehensive logging"""
        logger = logging.getLogger('ETL_Pipeline')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(f"etl_pipeline_{datetime.now().strftime('%Y%m%d')}.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def extract_data(self, file_path: str) -> pd.DataFrame:
        """Extract data from various file formats"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.csv':
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            self.logger.info(f"Extracted {len(df)} rows from {file_path}")
            return df
            
        except Exception as e:
            self.logger.error(f"Extraction failed for {file_path}: {str(e)}")
            self.stats['errors'] += 1
            raise
    
    def validate_data(self, df: pd.DataFrame, schema: Dict[str, Any]) -> pd.DataFrame:
        """Comprehensive data validation"""
        validation_errors = []
        
        # Check required columns
        missing_columns = set(schema['required_columns']) - set(df.columns)
        if missing_columns:
            validation_errors.append(f"Missing required columns: {missing_columns}")
        
        # Data type validation
        for column, expected_type in schema['column_types'].items():
            if column in df.columns:
                try:
                    if expected_type == 'datetime':
                        df[column] = pd.to_datetime(df[column])
                    elif expected_type == 'numeric':
                        df[column] = pd.to_numeric(df[column], errors='coerce')
                    elif expected_type == 'string':
                        df[column] = df[column].astype(str)
                except Exception as e:
                    validation_errors.append(f"Type conversion failed for {column}: {str(e)}")
        
        # Business rule validation
        if 'validation_rules' in schema:
            for rule in schema['validation_rules']:
                try:
                    mask = df.eval(rule['condition'])
                    invalid_count = (~mask).sum()
                    if invalid_count > 0:
                        self.logger.warning(f"Validation rule '{rule['name']}' failed for {invalid_count} records")
                        self.stats['warnings'] += invalid_count
                except Exception as e:
                    validation_errors.append(f"Validation rule '{rule['name']}' execution failed: {str(e)}")
        
        if validation_errors:
            raise ValueError(f"Data validation failed: {'; '.join(validation_errors)}")
        
        self.logger.info(f"Data validation completed successfully")
        return df
    
    def transform_data(self, df: pd.DataFrame, transformations: List[Dict[str, Any]]) -> pd.DataFrame:
        """Apply data transformations"""
        for transform in transformations:
            try:
                if transform['type'] == 'remove_duplicates':
                    before_count = len(df)
                    df = df.drop_duplicates(subset=transform.get('columns'))
                    removed_count = before_count - len(df)
                    self.logger.info(f"Removed {removed_count} duplicate records")
                
                elif transform['type'] == 'fill_missing':
                    for column, method in transform['methods'].items():
                        if column in df.columns:
                            if method == 'mean':
                                df[column].fillna(df[column].mean(), inplace=True)
                            elif method == 'median':
                                df[column].fillna(df[column].median(), inplace=True)
                            elif method == 'mode':
                                df[column].fillna(df[column].mode().iloc[0], inplace=True)
                            elif isinstance(method, (str, int, float)):
                                df[column].fillna(method, inplace=True)
                
                elif transform['type'] == 'standardize_text':
                    text_columns = df.select_dtypes(include=['object']).columns
                    for col in text_columns:
                        df[col] = df[col].astype(str).str.strip().str.title()
                
                elif transform['type'] == 'outlier_removal':
                    numeric_columns = df.select_dtypes(include=[np.number]).columns
                    for col in numeric_columns:
                        Q1 = df[col].quantile(0.25)
                        Q3 = df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        before_count = len(df)
                        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
                        removed_count = before_count - len(df)
                        if removed_count > 0:
                            self.logger.info(f"Removed {removed_count} outliers from {col}")
                
                elif transform['type'] == 'custom_calculation':
                    df[transform['target_column']] = df.eval(transform['expression'])
                
            except Exception as e:
                self.logger.error(f"Transformation '{transform['type']}' failed: {str(e)}")
                self.stats['errors'] += 1
        
        return df
    
    def load_data(self, df: pd.DataFrame, table_name: str, load_method: str = 'append') -> None:
        """Load data to target database"""
        try:
            if load_method == 'replace':
                df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            elif load_method == 'append':
                df.to_sql(table_name, self.engine, if_exists='append', index=False)
            elif load_method == 'upsert':
                # Implement upsert logic based on primary key
                self._upsert_data(df, table_name)
            
            self.logger.info(f"Loaded {len(df)} records to {table_name}")
            self.stats['processed'] += len(df)
            
        except Exception as e:
            self.logger.error(f"Loading failed for {table_name}: {str(e)}")
            self.stats['errors'] += 1
            raise
    
    def run_pipeline(self, file_paths: List[str], schema: Dict[str, Any], 
                    transformations: List[Dict[str, Any]], target_table: str) -> Dict[str, Any]:
        """Execute complete ETL pipeline"""
        start_time = datetime.now()
        
        try:
            all_data = []
            
            for file_path in file_paths:
                # Extract
                df = self.extract_data(file_path)
                
                # Validate
                df = self.validate_data(df, schema)
                
                # Transform
                df = self.transform_data(df, transformations)
                
                all_data.append(df)
            
            # Combine all data
            if all_data:
                combined_df = pd.concat(all_data, ignore_index=True)
                
                # Load
                self.load_data(combined_df, target_table)
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            results = {
                'status': 'success',
                'records_processed': self.stats['processed'],
                'processing_time_seconds': processing_time,
                'errors': self.stats['errors'],
                'warnings': self.stats['warnings']
            }
            
            self.logger.info(f"Pipeline completed successfully: {results}")
            return results
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'records_processed': self.stats['processed'],
                'errors': self.stats['errors'],
                'warnings': self.stats['warnings']
            }

# Usage Example
if __name__ == "__main__":
    config = {
        'database_url': 'postgresql://user:pass@localhost/datawarehouse'
    }
    
    schema = {
        'required_columns': ['id', 'date', 'amount'],
        'column_types': {
            'id': 'numeric',
            'date': 'datetime',
            'amount': 'numeric',
            'description': 'string'
        },
        'validation_rules': [
            {
                'name': 'amount_positive',
                'condition': 'amount > 0'
            },
            {
                'name': 'date_recent',
                'condition': 'date >= "2020-01-01"'
            }
        ]
    }
    
    transformations = [
        {'type': 'remove_duplicates', 'columns': ['id']},
        {'type': 'fill_missing', 'methods': {'amount': 'mean', 'description': 'Unknown'}},
        {'type': 'standardize_text'},
        {'type': 'outlier_removal'}
    ]
    
    pipeline = ETLPipeline(config)
    results = pipeline.run_pipeline(
        file_paths=['sales_data.csv', 'customer_data.xlsx'],
        schema=schema,
        transformations=transformations,
        target_table='processed_sales_data'
    )
    
    print(f"Pipeline Results: {results}")
        '''
        
        st.code(etl_code, language='python')
    
    with etl_tabs[1]:
        st.markdown("#### ETL Architecture Overview")
        
        # Architecture diagram using Plotly
        fig_arch = go.Figure()
        
        # Define components
        components = {
            'Data Sources': (1, 4, ['CSV Files', 'Excel Files', 'Database', 'APIs']),
            'Extract Layer': (2, 3, ['File Readers', 'Data Connectors', 'Format Parsers']),
            'Validation Layer': (3, 3, ['Schema Validation', 'Data Quality', 'Business Rules']),
            'Transform Layer': (4, 4, ['Data Cleaning', 'Normalization', 'Enrichment', 'Calculations']),
            'Load Layer': (5, 2, ['Database Writer', 'File Output']),
            'Monitoring': (6, 2, ['Logging', 'Metrics'])
        }
        
        # Create architecture visualization
        st.markdown("""
        **ETL Pipeline Architecture:**
        
        ```
        📁 Data Sources (CSV, Excel, DB) 
              ↓
        🔍 Extract Layer (File Readers, Parsers)
              ↓  
        ✅ Validation Layer (Schema, Quality, Rules)
              ↓
        ⚙️ Transform Layer (Clean, Normalize, Enrich)
              ↓
        📊 Load Layer (Database, Files)
              ↓
        📈 Monitoring (Logs, Metrics)
        ```
        
        **Key Architecture Principles:**
        
        - **Modularity**: Each layer is independently testable and maintainable
        - **Scalability**: Horizontal scaling support with parallel processing
        - **Reliability**: Comprehensive error handling and retry mechanisms  
        - **Observability**: Detailed logging and monitoring at each stage
        - **Flexibility**: Configurable transformations and validation rules
        - **Performance**: Optimized for large-scale data processing
        """)
        
        # Performance metrics
        perf_data = {
            'File Size': ['1MB', '10MB', '100MB', '1GB', '10GB'],
            'Processing Time (min)': [0.5, 2.0, 15.0, 45.0, 180.0],
            'Memory Usage (GB)': [0.1, 0.5, 2.0, 8.0, 24.0],
            'Records/Second': [50000, 45000, 35000, 25000, 15000]
        }
        
        perf_df = pd.DataFrame(perf_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.line(perf_df, x='File Size', y='Processing Time (min)',
                          title='Processing Time vs File Size')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.line(perf_df, x='File Size', y='Records/Second',
                          title='Throughput vs File Size')
            st.plotly_chart(fig2, use_container_width=True)
    
    with etl_tabs[2]:
        st.markdown("#### Pipeline Monitoring & Metrics")
        
        # Generate sample monitoring data
        monitoring_data = {
            'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
            'Files Processed': np.random.poisson(25, 30),
            'Records Processed': np.random.normal(50000, 10000, 30).astype(int),
            'Success Rate': np.random.uniform(0.95, 1.0, 30),
            'Avg Processing Time': np.random.normal(15, 5, 30),
            'Errors': np.random.poisson(2, 30)
        }
        
        monitoring_df = pd.DataFrame(monitoring_data)
        
        # Monitoring dashboard
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_files = monitoring_df['Files Processed'].sum()
            st.metric("Files Processed", f"{total_files:,}", "+12%")
        
        with col2:
            total_records = monitoring_df['Records Processed'].sum()
            st.metric("Records Processed", f"{total_records:,}", "+8%")
        
        with col3:
            avg_success_rate = monitoring_df['Success Rate'].mean()
            st.metric("Success Rate", f"{avg_success_rate:.1%}", "+0.5%")
        
        with col4:
            avg_proc_time = monitoring_df['Avg Processing Time'].mean()
            st.metric("Avg Proc Time", f"{avg_proc_time:.1f}min", "-2.3min")
        
        # Monitoring charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.line(monitoring_df, x='Date', y=['Files Processed', 'Errors'],
                          title='Daily Processing Volume & Errors')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.line(monitoring_df, x='Date', y='Success Rate',
                          title='Success Rate Trend')
            fig2.update_yaxis(range=[0.9, 1.0])
            st.plotly_chart(fig2, use_container_width=True)

def show_log_file_parser():
    """Log File Parser Demo"""
    
    st.markdown("## 📝 Intelligent Log File Parser")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Advanced Log Analysis System
        
        Intelligent log parsing and analysis tool that automatically detects log formats, 
        extracts key information, and provides actionable insights through interactive 
        visualizations and alerting mechanisms.
        
        ### Core Capabilities
        - **Multi-format Support**: Apache, Nginx, IIS, custom application logs
        - **Pattern Recognition**: Automatic log format detection and parsing
        - **Real-time Analysis**: Stream processing for live log monitoring  
        - **Anomaly Detection**: ML-powered unusual pattern identification
        - **Interactive Dashboards**: Drill-down analysis and filtering
        - **Alerting System**: Configurable thresholds and notifications
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📊 Parser Metrics</h4>
            <p><strong>Logs Processed:</strong> 10M+ daily</p>
            <p><strong>Parse Accuracy:</strong> 99.7%</p>
            <p><strong>Response Time:</strong> <50ms</p>
            <p><strong>Formats Supported:</strong> 15+</p>
        </div>
        
        <div class="success-box">
            <h4>🎯 Impact</h4>
            <p><strong>Issue Detection:</strong> 95% faster</p>
            <p><strong>False Positives:</strong> 80% reduction</p>
            <p><strong>MTTR:</strong> 60% improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive Log Parser Demo
    st.markdown("### 🔍 Interactive Log Parser Demo")
    
    # Sample log formats
    log_formats = {
        "Apache Common": '127.0.0.1 - - [10/Oct/2024:13:55:36 +0000] "GET /index.html HTTP/1.0" 200 2326',
        "Nginx": '192.168.1.1 - - [10/Oct/2024:13:55:36 +0000] "POST /api/users HTTP/1.1" 201 1024 "-" "Mozilla/5.0"',
        "Application Log": '2024-10-10 13:55:36,123 INFO [main] com.app.Service - Processing user request for ID: 12345',
        "JSON Log": '{"timestamp":"2024-10-10T13:55:36.123Z","level":"ERROR","service":"auth","message":"Login failed","user_id":67890}',
        "Custom Format": '[ERROR] 2024-10-10 13:55:36 | UserService | Authentication failed for user: admin | IP: 192.168.1.100'
    }
    
    selected_format = st.selectbox("Select log format to analyze:", list(log_formats.keys()))
    
    # Text area for log input
    sample_log = log_formats[selected_format]
    log_input = st.text_area("Enter log entries (one per line):", value=sample_log, height=150)
    
    if st.button("🔍 Parse Logs"):
        if log_input.strip():
            log_lines = log_input.strip().split('\n')
            parsed_results = []
            
            for i, line in enumerate(log_lines):
                try:
                    # Parse different log formats
                    if selected_format == "Apache Common":
                        parsed = parse_apache_log(line)
                    elif selected_format == "Nginx":
                        parsed = parse_nginx_log(line)
                    elif selected_format == "Application Log":
                        parsed = parse_application_log(line)
                    elif selected_format == "JSON Log":
                        parsed = parse_json_log(line)
                    else:
                        parsed = parse_custom_log(line)
                    
                    parsed['line_number'] = i + 1
                    parsed['raw_log'] = line
                    parsed_results.append(parsed)
                    
                except Exception as e:
                    st.error(f"Failed to parse line {i+1}: {str(e)}")
            
            if parsed_results:
                # Display parsed results
                results_df = pd.DataFrame(parsed_results)
                st.markdown("#### 📋 Parsed Log Data")
                st.dataframe(results_df, use_container_width=True)
                
                # Log analysis visualizations
                if len(results_df) > 1:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if 'status_code' in results_df.columns:
                            status_counts = results_df['status_code'].value_counts()
                            fig1 = px.pie(values=status_counts.values, names=status_counts.index,
                                        title='HTTP Status Code Distribution')
                            st.plotly_chart(fig1, use_container_width=True)
                        elif 'level' in results_df.columns:
                            level_counts = results_df['level'].value_counts()
                            fig1 = px.bar(x=level_counts.index, y=level_counts.values,
                                        title='Log Level Distribution')
                            st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        if 'ip_address' in results_df.columns:
                            ip_counts = results_df['ip_address'].value_counts().head(10)
                            fig2 = px.bar(x=ip_counts.values, y=ip_counts.index, orientation='h',
                                        title='Top 10 IP Addresses')
                            st.plotly_chart(fig2, use_container_width=True)
                        elif 'service' in results_df.columns:
                            service_counts = results_df['service'].value_counts()
                            fig2 = px.bar(x=service_counts.index, y=service_counts.values,
                                        title='Messages by Service')
                            st.plotly_chart(fig2, use_container_width=True)
    
    # Generate sample log analysis
    st.markdown("### 📊 Live Log Analysis Demo")
    
    # Load sample log data
    log_data = load_sample_data("logs")
    
    # Log analysis metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        error_rate = (log_data['log_level'] == 'ERROR').mean()
        st.metric("Error Rate", f"{error_rate:.2%}", "-0.5%")
    
    with col2:
        avg_response = log_data['response_time'].mean()
        st.metric("Avg Response Time", f"{avg_response:.0f}ms", "+15ms")
    
    with col3:
        total_requests = len(log_data)
        st.metric("Total Requests", f"{total_requests:,}", "+1.2K")
    
    with col4:
        unique_ips = log_data['ip_address'].nunique()
        st.metric("Unique IPs", f"{unique_ips:,}", "+45")
    
    # Log analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Log level distribution over time
        hourly_logs = log_data.groupby([
            log_data['timestamp'].dt.hour, 
            'log_level'
        ]).size().reset_index(name='count')
        
        fig1 = px.bar(hourly_logs, x='timestamp', y='count', color='log_level',
                     title='Log Levels by Hour of Day')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Response time by service
        service_response = log_data.groupby('service')['response_time'].mean().sort_values(ascending=True)
        fig2 = px.bar(x=service_response.values, y=service_response.index, orientation='h',
                     title='Average Response Time by Service')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Error analysis
    st.markdown("#### 🚨 Error Analysis")
    
    error_logs = log_data[log_data['log_level'] == 'ERROR']
    
    if not error_logs.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            error_by_service = error_logs['service'].value_counts()
            fig3 = px.pie(values=error_by_service.values, names=error_by_service.index,
                         title='Errors by Service')
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Error timeline
            error_timeline = error_logs.groupby(error_logs['timestamp'].dt.hour).size()
            fig4 = px.line(x=error_timeline.index, y=error_timeline.values,
                          title='Error Count by Hour')
            st.plotly_chart(fig4, use_container_width=True)
    
    # Log parsing functions (helper functions for the demo)
    
def parse_apache_log(line):
    """Parse Apache Common Log Format"""
    import re
    pattern = r'(\S+) \S+ \S+ \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+|-)'
    match = re.match(pattern, line)
    if match:
        return {
            'ip_address': match.group(1),
            'timestamp': match.group(2),
            'method': match.group(3),
            'url': match.group(4),
            'protocol': match.group(5),
            'status_code': int(match.group(6)),
            'response_size': match.group(7)
        }
    return {'error': 'Failed to parse Apache log format'}

def parse_nginx_log(line):
    """Parse Nginx log format"""
    import re
    pattern = r'(\S+) - - \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+) "([^"]*)" "([^"]*)"'
    match = re.match(pattern, line)
    if match:
        return {
            'ip_address': match.group(1),
            'timestamp': match.group(2),
            'method': match.group(3),
            'url': match.group(4),
            'protocol': match.group(5),
            'status_code': int(match.group(6)),
            'response_size': int(match.group(7)),
            'referrer': match.group(8),
            'user_agent': match.group(9)
        }
    return {'error': 'Failed to parse Nginx log format'}

def parse_application_log(line):
    """Parse application log format"""
    import re
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ (\w+) \[([^\]]+)\] ([^-]+) - (.+)'
    match = re.match(pattern, line)
    if match:
        return {
            'timestamp': match.group(1),
            'level': match.group(2),
            'thread': match.group(3),
            'class': match.group(4),
            'message': match.group(5)
        }
    return {'error': 'Failed to parse application log format'}

def parse_json_log(line):
    """Parse JSON log format"""
    import json
    try:
        data = json.loads(line)
        return data
    except json.JSONDecodeError:
        return {'error': 'Invalid JSON format'}

def parse_custom_log(line):
    """Parse custom log format"""
    import re
    pattern = r'\[(\w+)\] (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \| (\w+) \| ([^|]+) \| ([^|]+)'
    match = re.match(pattern, line)
    if match:
        return {
            'level': match.group(1),
            'timestamp': match.group(2),
            'service': match.group(3),
            'message': match.group(4),
            'metadata': match.group(5)
        }
    return {'error': 'Failed to parse custom log format'}

def show_sql_cleaning_reporting():
    """SQL Data Cleaning & Reporting Demo"""
    
    st.markdown("## 🗄️ SQL Data Cleaning & Reporting")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Advanced SQL Data Processing
        
        Comprehensive SQL-based data cleaning, validation, and automated reporting system 
        with performance optimization and data quality monitoring capabilities.
        
        ### Key Features
        - **Data Quality Assessment**: Automated data profiling and quality scoring
        - **Advanced Cleaning**: Deduplication, standardization, outlier detection
        - **Performance Optimization**: Query tuning and index recommendations
        - **Automated Reporting**: Scheduled report generation and distribution
        - **Data Lineage**: Track data transformations and dependencies
        - **Compliance Monitoring**: GDPR, SOX, and industry compliance checks
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📊 Processing Stats</h4>
            <p><strong>Records Cleaned:</strong> 5M+ daily</p>
            <p><strong>Query Performance:</strong> 75% improvement</p>
            <p><strong>Data Quality:</strong> 99.8% accuracy</p>
            <p><strong>Report Automation:</strong> 150+ reports</p>
        </div>
        
        <div class="success-box">
            <h4>🎯 Business Value</h4>
            <p><strong>Manual Effort:</strong> 90% reduction</p>
            <p><strong>Data Errors:</strong> 85% fewer issues</p>
            <p><strong>Reporting Speed:</strong> 10x faster</p>
        </div>
        """, unsafe_allow_html=True)
    
    # SQL Demo Interface
    st.markdown("### 💻 Interactive SQL Demo")
    
    # Create sample data
    if 'sample_db_created' not in st.session_state:
        create_sample_database()
        st.session_state.sample_db_created = True
    
    sql_tabs = st.tabs(["📊 Data Exploration", "🧹 Data Cleaning", "📈 Reporting Queries", "⚡ Performance Tuning"])
    
    with sql_tabs[0]:
        st.markdown("#### Data Exploration & Profiling")
        
        # Sample exploration queries
        exploration_queries = {
            "Data Overview": """
-- Get basic table statistics
SELECT 
    'customers' as table_name,
    COUNT(*) as total_records,
    COUNT(DISTINCT customer_id) as unique_customers,
    MIN(registration_date) as earliest_date,
    MAX(registration_date) as latest_date
FROM customers
UNION ALL
SELECT 
    'orders' as table_name,
    COUNT(*) as total_records,
    COUNT(DISTINCT order_id) as unique_orders,
    MIN(order_date) as earliest_date,
    MAX(order_date) as latest_date
FROM orders;
            """,
            "Data Quality Assessment": """
-- Assess data quality across key tables
WITH quality_metrics AS (
    SELECT 
        'customers' as table_name,
        COUNT(*) as total_records,
        SUM(CASE WHEN customer_name IS NULL OR customer_name = '' THEN 1 ELSE 0 END) as null_names,
        SUM(CASE WHEN email IS NULL OR email NOT LIKE '%@%.%' THEN 1 ELSE 0 END) as invalid_emails,
        SUM(CASE WHEN phone IS NULL OR LENGTH(phone) < 10 THEN 1 ELSE 0 END) as invalid_phones
    FROM customers
    
    UNION ALL
    
    SELECT 
        'orders' as table_name,
        COUNT(*) as total_records,
        SUM(CASE WHEN order_amount IS NULL OR order_amount <= 0 THEN 1 ELSE 0 END) as invalid_amounts,
        SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END) as null_dates,
        SUM(CASE WHEN customer_id NOT IN (SELECT customer_id FROM customers) THEN 1 ELSE 0 END) as orphaned_records
    FROM orders
)
SELECT 
    table_name,
    total_records,
    ROUND(100.0 * (total_records - COALESCE(null_names, 0) - COALESCE(invalid_emails, 0) - COALESCE(invalid_phones, 0) - COALESCE(invalid_amounts, 0) - COALESCE(null_dates, 0) - COALESCE(orphaned_records, 0)) / total_records, 2) as data_quality_score
FROM quality_metrics;
            """,
            "Duplicate Analysis": """
-- Find potential duplicates in customer data
SELECT 
    customer_name,
    email,
    COUNT(*) as duplicate_count,
    STRING_AGG(CAST(customer_id AS VARCHAR), ', ') as customer_ids
FROM customers
GROUP BY customer_name, email
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
            """
        }
        
        selected_exploration = st.selectbox("Select exploration query:", list(exploration_queries.keys()))
        
        if st.button("🔍 Execute Query"):
            query = exploration_queries[selected_exploration]
            st.code(query, language='sql')
            
            # Execute query and show results
            try:
                results = execute_sample_query(query)
                st.markdown("**Query Results:**")
                st.dataframe(results, use_container_width=True)
            except Exception as e:
                st.error(f"Query execution failed: {str(e)}")
    
    with sql_tabs[1]:
        st.markdown("#### Data Cleaning Operations")
        
        cleaning_queries = {
            "Standardize Customer Names": """
-- Clean and standardize customer names
UPDATE customers 
SET customer_name = TRIM(UPPER(SUBSTRING(customer_name, 1, 1)) || LOWER(SUBSTRING(customer_name, 2)))
WHERE customer_name IS NOT NULL;

-- Remove extra whitespace
UPDATE customers 
SET customer_name = REGEXP_REPLACE(customer_name, '\\s+', ' ', 'g')
WHERE customer_name LIKE '%  %';

-- Show results
SELECT 
    customer_id,
    customer_name,
    email
FROM customers 
WHERE customer_name IS NOT NULL
LIMIT 10;
            """,
            "Email Validation & Cleaning": """
-- Identify and fix common email issues
WITH email_fixes AS (
    SELECT 
        customer_id,
        email,
        CASE 
            WHEN email LIKE '% %' THEN REPLACE(email, ' ', '')
            WHEN email LIKE '%..%' THEN REPLACE(email, '..', '.')
            WHEN email NOT LIKE '%@%' THEN NULL
            ELSE LOWER(TRIM(email))
        END as cleaned_email
    FROM customers
    WHERE email IS NOT NULL
)
SELECT 
    customer_id,
    email as original_email,
    cleaned_email,
    CASE 
        WHEN cleaned_email IS NULL THEN 'Invalid'
        WHEN email != cleaned_email THEN 'Fixed'
        ELSE 'Valid'
    END as status
FROM email_fixes
WHERE email != cleaned_email OR cleaned_email IS NULL
LIMIT 20;
            """,
            "Remove Duplicates": """
-- Identify and handle duplicate customer records
WITH ranked_customers AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_name, email 
            ORDER BY registration_date DESC
        ) as rn
    FROM customers
    WHERE customer_name IS NOT NULL 
    AND email IS NOT NULL
),
duplicates AS (
    SELECT 
        customer_name,
        email,
        COUNT(*) as duplicate_count,
        MIN(customer_id) as keep_id,
        STRING_AGG(
            CASE WHEN rn > 1 THEN CAST(customer_id AS VARCHAR) END, 
            ', '
        ) as remove_ids
    FROM ranked_customers
    GROUP BY customer_name, email
    HAVING COUNT(*) > 1
)
SELECT 
    customer_name,
    email,
    duplicate_count,
    keep_id,
    remove_ids
FROM duplicates
ORDER BY duplicate_count DESC;
            """
        }
        
        selected_cleaning = st.selectbox("Select cleaning operation:", list(cleaning_queries.keys()))
        
        if st.button("🧹 Execute Cleaning Query"):
            query = cleaning_queries[selected_cleaning]
            st.code(query, language='sql')
            
            try:
                results = execute_sample_query(query)
                st.markdown("**Cleaning Results:**")
                st.dataframe(results, use_container_width=True)
                st.success("✅ Data cleaning operation completed successfully!")
            except Exception as e:
                st.error(f"Cleaning operation failed: {str(e)}")
    
    with sql_tabs[2]:
        st.markdown("#### Automated Reporting Queries")
        
        reporting_queries = {
            "Sales Performance Report": """
-- Comprehensive sales performance analysis
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', o.order_date) as month,
        COUNT(DISTINCT o.order_id) as total_orders,
        COUNT(DISTINCT o.customer_id) as unique_customers,
        SUM(o.order_amount) as total_revenue,
        AVG(o.order_amount) as avg_order_value,
        SUM(oi.quantity) as total_items_sold
    FROM orders o
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY DATE_TRUNC('month', o.order_date)
),
growth_calc AS (
    SELECT 
        *,
        LAG(total_revenue) OVER (ORDER BY month) as prev_month_revenue,
        LAG(total_orders) OVER (ORDER BY month) as prev_month_orders
    FROM monthly_sales
)
SELECT 
    TO_CHAR(month, 'YYYY-MM') as month,
    total_orders,
    unique_customers,
    total_revenue,
    avg_order_value,
    total_items_sold,
    ROUND(
        ((total_revenue - prev_month_revenue) / NULLIF(prev_month_revenue, 0)) * 100, 2
    ) as revenue_growth_pct,
    ROUND(
        ((total_orders - prev_month_orders) / NULLIF(prev_month_orders, 0)) * 100, 2
    ) as order_growth_pct
FROM growth_calc
ORDER BY month;
            """,
            "Customer Analytics Report": """
-- Customer behavior and segmentation analysis
WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.registration_date,
        COUNT(o.order_id) as total_orders,
        SUM(o.order_amount) as total_spent,
        AVG(o.order_amount) as avg_order_value,
        MAX(o.order_date) as last_order_date,
        CURRENT_DATE - MAX(o.order_date) as days_since_last_order
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.registration_date
),
customer_segments AS (
    SELECT 
        *,
        CASE 
            WHEN total_orders >= 10 AND total_spent >= 1000 THEN 'VIP'
            WHEN total_orders >= 5 AND total_spent >= 500 THEN 'Loyal'
            WHEN total_orders >= 2 THEN 'Regular'
            WHEN total_orders = 1 THEN 'One-time'
            ELSE 'Inactive'
        END as customer_segment,
        CASE 
            WHEN days_since_last_order <= 30 THEN 'Active'
            WHEN days_since_last_order <= 90 THEN 'At Risk'
            ELSE 'Churned'
        END as activity_status
    FROM customer_metrics
)
SELECT 
    customer_segment,
    activity_status,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_lifetime_value,
    AVG(total_orders) as avg_orders_per_customer,
    AVG(days_since_last_order) as avg_days_since_last_order
FROM customer_segments
GROUP BY customer_segment, activity_status
ORDER BY customer_segment, activity_status;
            """,
            "Product Performance Report": """
-- Product sales analysis and ranking
WITH product_performance AS (
    SELECT 
        p.product_name,
        p.category,
        COUNT(oi.order_item_id) as times_ordered,
        SUM(oi.quantity) as total_quantity_sold,
        SUM(oi.quantity * oi.unit_price) as total_revenue,
        AVG(oi.unit_price) as avg_selling_price,
        COUNT(DISTINCT oi.order_id) as unique_orders
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '6 months'
    GROUP BY p.product_id, p.product_name, p.category
),
ranked_products AS (
    SELECT 
        *,
        RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank,
        RANK() OVER (ORDER BY total_quantity_sold DESC) as quantity_rank,
        RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) as category_rank
    FROM product_performance
    WHERE total_revenue > 0
)
SELECT 
    product_name,
    category,
    times_ordered,
    total_quantity_sold,
    total_revenue,
    avg_selling_price,
    revenue_rank,
    quantity_rank,
    category_rank
FROM ranked_products
WHERE revenue_rank <= 20
ORDER BY revenue_rank;
            """
        }
        
        selected_report = st.selectbox("Select report to generate:", list(reporting_queries.keys()))
        
        if st.button("📊 Generate Report"):
            query = reporting_queries[selected_report]
            st.code(query, language='sql')
            
            try:
                results = execute_sample_query(query)
                st.markdown(f"**{selected_report} Results:**")
                st.dataframe(results, use_container_width=True)
                
                # Add download button for report
                csv_data = results.to_csv(index=False)
                st.download_button(
                    label="📥 Download Report as CSV",
                    data=csv_data,
                    file_name=f"{selected_report.lower().replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Report generation failed: {str(e)}")
    
    with sql_tabs[3]:
        st.markdown("#### Query Performance Optimization")
        
        st.markdown("""
        **Performance Optimization Techniques:**
        
        1. **Index Analysis and Recommendations**
        2. **Query Execution Plan Review** 
        3. **Statistics and Cardinality Estimation**
        4. **Partitioning Strategies**
        5. **Query Rewriting and Optimization**
        """)
        
        optimization_examples = {
            "Slow Query Analysis": """
-- Identify slow-running queries and their performance metrics
SELECT 
    query_text,
    total_exec_time,
    mean_exec_time,
    calls,
    rows_returned,
    temp_blks_read,
    temp_blks_written
FROM pg_stat_statements 
WHERE mean_exec_time > 1000  -- queries taking more than 1 second
ORDER BY total_exec_time DESC
LIMIT 10;

-- Query execution plan analysis
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT 
    c.customer_name,
    COUNT(o.order_id) as order_count,
    SUM(o.order_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.registration_date >= '2023-01-01'
GROUP BY c.customer_id, c.customer_name
HAVING COUNT(o.order_id) > 5;
            """,
            "Index Recommendations": """
-- Analyze table usage and suggest indexes
WITH table_stats AS (
    SELECT 
        schemaname,
        tablename,
        seq_scan,
        seq_tup_read,
        idx_scan,
        idx_tup_fetch,
        n_tup_ins + n_tup_upd + n_tup_del as total_writes
    FROM pg_stat_user_tables
),
index_usage AS (
    SELECT 
        schemaname,
        tablename,
        indexname,
        idx_scan,
        idx_tup_read,
        idx_tup_fetch
    FROM pg_stat_user_indexes
)
-- Tables with high sequential scans (need indexes)
SELECT 
    'High Sequential Scans' as issue_type,
    tablename,
    seq_scan,
    seq_tup_read,
    CASE 
        WHEN idx_scan = 0 THEN 'No index usage detected'
        ELSE 'Consider adding indexes on frequently filtered columns'
    END as recommendation
FROM table_stats
WHERE seq_scan > 1000 AND (idx_scan = 0 OR seq_scan > idx_scan * 10)
ORDER BY seq_scan DESC;
            """,
            "Query Optimization": """
-- Before: Inefficient query with subqueries
-- SELECT * FROM customers WHERE customer_id IN 
--   (SELECT customer_id FROM orders WHERE order_amount > 1000);

-- After: Optimized with EXISTS and proper indexing
SELECT DISTINCT c.*
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_amount > 1000
);

-- Before: Inefficient aggregation
-- SELECT customer_id, 
--        (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count
-- FROM customers c;

-- After: Efficient JOIN with aggregation
SELECT 
    c.customer_id,
    c.customer_name,
    COALESCE(order_stats.order_count, 0) as order_count,
    COALESCE(order_stats.total_spent, 0) as total_spent
FROM customers c
LEFT JOIN (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_amount) as total_spent
    FROM orders
    GROUP BY customer_id
) order_stats ON c.customer_id = order_stats.customer_id;
            """
        }
        
        selected_optimization = st.selectbox("Select optimization example:", list(optimization_examples.keys()))
        
        st.code(optimization_examples[selected_optimization], language='sql')
        
        # Performance metrics simulation
        st.markdown("#### Performance Metrics")
        
        perf_metrics = {
            'Metric': ['Query Execution Time', 'Index Hit Ratio', 'Cache Hit Rate', 'Temp Files Created', 'Locks Acquired'],
            'Before Optimization': ['2.5s', '65%', '78%', '150/day', '850/day'],
            'After Optimization': ['0.3s', '95%', '94%', '12/day', '120/day'],
            'Improvement': ['88% faster', '+30%', '+16%', '92% reduction', '86% reduction']
        }
        
        perf_df = pd.DataFrame(perf_metrics)
        st.dataframe(perf_df, use_container_width=True)

def create_sample_database():
    """Create sample database for SQL demos"""
    # This is a simulation - in a real app, you'd connect to an actual database
    pass

def execute_sample_query(query):
    """Execute sample SQL query and return results"""
    # Simulate query execution with sample data
    if "customers" in query.lower() and "orders" in query.lower():
        return pd.DataFrame({
            'table_name': ['customers', 'orders'],
            'total_records': [5000, 12000],
            'unique_customers': [5000, 4800],
            'earliest_date': ['2020-01-15', '2020-02-01'],
            'latest_date': ['2024-10-10', '2024-10-10']
        })
    elif "quality" in query.lower():
        return pd.DataFrame({
            'table_name': ['customers', 'orders'],
            'total_records': [5000, 12000],
            'data_quality_score': [94.5, 97.2]
        })
    elif "duplicate" in query.lower():
        return pd.DataFrame({
            'customer_name': ['John Smith', 'Jane Doe', 'Bob Johnson'],
            'email': ['john@email.com', 'jane@email.com', 'bob@email.com'],
            'duplicate_count': [3, 2, 2],
            'customer_ids': ['101,205,309', '150,287', '89,156']
        })
    else:
        # Return sample sales/reporting data
        return pd.DataFrame({
            'month': ['2024-01', '2024-02', '2024-03'],
            'total_orders': [1250, 1380, 1420],
            'total_revenue': [125000, 138000, 142000],
            'revenue_growth_pct': [None, 10.4, 2.9]
        })
# Data Projects Page  
def show_data_projects_page():
    """Display data engineering and processing projects"""
    
    st.title("🔧 Data Projects Portfolio")
    st.markdown("### Advanced data engineering, ETL pipelines, and processing solutions")
    
    project_tabs = st.tabs(["⚡ Excel/CSV ETL", "📝 Log File Parser", "🗄️ SQL Cleaning & Reporting"])
    
    with project_tabs[0]:
        show_excel_csv_etl()
    
    with project_tabs[1]:
        show_log_file_parser()
    
    with project_tabs[2]:
        show_sql_cleaning_reporting()

def show_excel_csv_etl():
    """Excel/CSV ETL Pipeline Demo"""
    
    st.markdown("## """
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
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import base64
import io
import sqlite3
from pathlib import Path
import re
import time

# Page configuration
st.set_page_config(
    page_title="Data Science Portfolio | Professional Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:your.email@example.com',
        'Report a bug': 'mailto:your.email@example.com',
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
        border: 1px solid #e0e0e0;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border-left-color: #764ba2;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .demo-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .tech-stack {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #90caf9;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0px 20px;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0px 0px;
        color: #262730;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Utility Functions
@st.cache_data
def load_sample_data(data_type):
    """Load various types of sample data for demonstrations"""
    np.random.seed(42)
    
    if data_type == "sales":
        dates = pd.date_range('2023-01-01', periods=365, freq='D')
        return pd.DataFrame({
            'date': dates,
            'product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], 365),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 365),
            'sales_amount': np.random.normal(1000, 300, 365).clip(min=100),
            'quantity_sold': np.random.poisson(20, 365),
            'customer_id': np.random.choice(range(1, 1001), 365),
            'sales_rep': np.random.choice(['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'], 365)
        })
    
    elif data_type == "web_analytics":
        dates = pd.date_range('2024-01-01', periods=90, freq='D')
        return pd.DataFrame({
            'date': dates,
            'page_views': np.random.poisson(1500, 90) + np.random.normal(0, 200, 90),
            'unique_visitors': np.random.poisson(800, 90) + np.random.normal(0, 100, 90),
            'bounce_rate': np.random.normal(0.35, 0.1, 90).clip(0, 1),
            'conversion_rate': np.random.normal(0.05, 0.02, 90).clip(0, 1),
            'avg_session_duration': np.random.normal(180, 60, 90).clip(30, 600),
            'mobile_traffic': np.random.normal(0.6, 0.15, 90).clip(0, 1)
        })
    
    elif data_type == "infrastructure":
        timestamps = pd.date_range('2024-01-01', periods=1000, freq='H')
        return pd.DataFrame({
            'timestamp': timestamps,
            'cpu_usage': np.random.normal(45, 15, 1000).clip(0, 100),
            'memory_usage': np.random.normal(60, 20, 1000).clip(0, 100),
            'disk_io': np.random.exponential(20, 1000).clip(0, 100),
            'network_in': np.random.exponential(50, 1000),
            'network_out': np.random.exponential(30, 1000),
            'response_time': np.random.exponential(100, 1000),
            'error_count': np.random.poisson(2, 1000)
        })
    
    elif data_type == "logs":
        timestamps = pd.date_range('2024-01-01', periods=10000, freq='min')
        return pd.DataFrame({
            'timestamp': timestamps,
            'log_level': np.random.choice(['INFO', 'WARNING', 'ERROR', 'DEBUG'], 10000, p=[0.6, 0.2, 0.1, 0.1]),
            'service': np.random.choice(['auth', 'api', 'database', 'frontend'], 10000),
            'response_time': np.random.exponential(150, 10000),
            'status_code': np.random.choice([200, 404, 500, 503], 10000, p=[0.8, 0.1, 0.05, 0.05]),
            'user_agent': np.random.choice(['Chrome', 'Firefox', 'Safari', 'Edge'], 10000),
            'ip_address': [f"192.168.{np.random.randint(1,255)}.{np.random.randint(1,255)}" for _ in range(10000)]
        })

def create_download_link(data, filename, file_type="csv"):
    """Create download link for data"""
    if file_type == "csv":
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download {filename}</a>'
    return href

def simulate_realtime_data():
    """Simulate real-time data updates"""
    return {
        'cpu': np.random.normal(45, 15),
        'memory': np.random.normal(60, 20),
        'requests': np.random.poisson(100),
        'errors': np.random.poisson(5),
        'response_time': np.random.exponential(100)
    }

# Main Navigation
def main():
    """Main application with navigation"""
    
    # Sidebar Navigation
    st.sidebar.title("🚀 Portfolio Navigation")
    
    # Main sections
    main_pages = {
        "🏠 Home": "home",
        "📊 Dashboards": "dashboards", 
        "🔧 Data Projects": "data_projects",
        "🌐 Web Applications": "webapps",
        "📋 Documentation": "docs",
        "📞 Contact": "contact"
    }
    
    selected_page = st.sidebar.selectbox("Choose Section:", list(main_pages.keys()))
    page_key = main_pages[selected_page]
    
    # Route to appropriate page
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

# Home Page
def show_home_page():
    """Display home page with portfolio overview"""
    
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3.5rem; margin-bottom: 1rem; font-weight: 700;">
            📊 Data Science Portfolio
        </h1>
        <h2 style="font-size: 1.8rem; margin: 0; opacity: 0.9; font-weight: 400;">
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
        I'm a **Senior Data Scientist & Analytics Engineer** specializing in transforming complex data 
        into actionable business insights. My expertise spans the entire data lifecycle, from raw data 
        ingestion and processing to advanced analytics and interactive visualization.
        
        ### 🎯 Core Expertise:
        
        **📊 Business Intelligence & Dashboards**
        - Advanced Power BI development with DAX calculations
        - Grafana infrastructure monitoring and alerting
        - Custom Streamlit applications for real-time analytics
        - Tableau dashboard design and optimization
        
        **🔧 Data Engineering & ETL**
        - Python-based ETL pipelines for large-scale data processing
        - SQL optimization and database performance tuning  
        - Cloud data architecture (AWS, Azure, GCP)
        - Real-time streaming data processing
        
        **🤖 Machine Learning & Advanced Analytics**
        - Predictive modeling and forecasting algorithms
        - Customer segmentation and behavioral analysis
        - Anomaly detection and fraud prevention
        - A/B testing frameworks and statistical analysis
        
        **🌐 Full-Stack Development**
        - Interactive web applications using Flask and Streamlit
        - RESTful API development and integration
        - Database design and optimization
        - DevOps and CI/CD pipeline implementation
        """)
    
    with col2:
        st.image("https://via.placeholder.com/300x400/667eea/ffffff?text=Professional+Photo", 
                caption="Data Science Professional")
        
        st.markdown("""
        ### 🏆 Achievements:
        - 🚀 Reduced data processing time by **85%**
        - 📈 Improved forecasting accuracy by **40%**
        - 💰 Generated **$5M+** in cost savings
        - 👥 Led teams of **10+** data professionals
        
        ### 🎓 Certifications:
        - Microsoft Certified: Power BI Data Analyst
        - AWS Certified Solutions Architect  
        - Google Cloud Professional Data Engineer
        - Certified Analytics Professional (CAP)
        """)
    
    # Featured Projects
    st.markdown("## 🌟 Featured Projects")
    
    project_tabs = st.tabs(["📊 Dashboards", "🔧 Data Engineering", "🌐 Web Apps", "🤖 ML Models"])
    
    with project_tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="project-card">
                <h3>🏢 Grafana Infrastructure Monitoring</h3>
                <p>Real-time monitoring dashboard for infrastructure metrics with automated alerting and anomaly detection.</p>
                <div class="tech-stack">
                    <strong>Tech Stack:</strong> Grafana, Prometheus, InfluxDB, Docker
                </div>
                <div class="success-box">
                    <strong>Impact:</strong> 80% faster incident response, 99.9% uptime achieved
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="project-card">
                <h3>📈 Power BI Sales Analytics</h3>
                <p>Executive dashboard with KPI tracking, sales forecasting, and regional performance analysis.</p>
                <div class="tech-stack">
                    <strong>Tech Stack:</strong> Power BI, SQL Server, DAX, Power Query
                </div>
                <div class="success-box">
                    <strong>Impact:</strong> 40% faster reporting, $500K cost savings annually
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with project_tabs[1]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="project-card">
                <h3>⚡ High-Performance ETL Pipeline</h3>
                <p>Scalable ETL system processing 1M+ records daily with data validation and error handling.</p>
                <div class="tech-stack">
                    <strong>Tech Stack:</strong> Python, Apache Airflow, PostgreSQL, Redis
                </div>
                <div class="success-box">
                    <strong>Impact:</strong> 90% reduction in processing time, 99.8% accuracy
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="project-card">
                <h3>🔍 Intelligent Log Parser</h3>
                <p>Automated log analysis system with pattern recognition and anomaly detection.</p>
                <div class="tech-stack">
                    <strong>Tech Stack:</strong> Python, RegEx, Streamlit, Plotly
                </div>
                <div class="success-box">
                    <strong>Impact:</strong> 95% faster issue detection, proactive monitoring
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with project_tabs[2]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="project-card">
                <h3>📊 CSV Insight Tool</h3>
                <p>Drag-and-drop CSV analysis tool with automatic chart generation and statistical insights.</p>
                <div class="tech-stack">
                    <strong>Tech Stack:</strong> Streamlit, Pandas, Plotly, NumPy
                </div>
                <div class="success-box">
                    <strong>Impact:</strong> Used by 200+ analysts, 75% time savings
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="project-card">
                <h3>📈 Real-time Log Visualizer</h3>
                <p>Interactive web application for real-time log monitoring and visualization.</p>
                <div class="tech-stack">
                    <strong>Tech Stack:</strong> Flask, WebSockets, Chart.js, SQLite
                </div>
                <div class="success-box">
                    <strong>Impact:</strong> Real-time insights, improved system reliability
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with project_tabs[3]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="project-card">
                <h3>🎯 Sales Prediction Engine</h3>
                <p>Machine learning model for sales forecasting with 95% accuracy using ensemble methods.</p>
                <div class="tech-stack">
                    <strong>Tech Stack:</strong> Python, Scikit-learn, XGBoost, MLflow
                </div>
                <div class="success-box">
                    <strong>Impact:</strong> 40% improvement in forecast accuracy
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="project-card">
                <h3>🔒 Fraud Detection System</h3>
                <p>Real-time anomaly detection system using isolation forests and neural networks.</p>
                <div class="tech-stack">
                    <strong>Tech Stack:</strong> Python, TensorFlow, Apache Kafka, Docker
                </div>
                <div class="success-box">
                    <strong>Impact:</strong> 98% fraud detection rate, $2M+ losses prevented
                </div>
            </div>
            """, unsafe_allow_html=True)

# Dashboards Page
def show_dashboards_page():
    """Display dashboard projects and demos"""
    
    st.title("📊 Interactive Dashboards Portfolio")
    st.markdown("### Professional dashboard solutions for business intelligence and monitoring")
    
    dashboard_tabs = st.tabs(["🏢 Grafana Infrastructure", "📈 Power BI Sales Analytics", "🌐 Traffic Analytics", "⚡ Real-time Demos"])
    
    with dashboard_tabs[0]:
        show_grafana_dashboard()
    
    with dashboard_tabs[1]:
        show_powerbi_dashboard()
    
    with dashboard_tabs[2]:
        show_traffic_dashboard()
    
    with dashboard_tabs[3]:
        show_realtime_demos()

def show_grafana_dashboard():
    """Grafana Infrastructure Monitoring Dashboard"""
    
    st.markdown("## 🏢 Grafana Infrastructure Monitoring Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Project Overview
        Comprehensive infrastructure monitoring solution built with Grafana, providing real-time visibility 
        into system performance, automated alerting, and predictive analytics for proactive maintenance.
        
        ### Key Features
        - **Real-time Metrics**: CPU, memory, disk, and network monitoring
        - **Automated Alerting**: Smart thresholds with escalation policies  
        - **Predictive Analytics**: Anomaly detection and capacity planning
        - **Custom Dashboards**: Role-based views for different stakeholders
        - **Integration Ready**: APIs for external systems and notifications
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📋 Project Details</h4>
            <p><strong>Duration:</strong> 8 weeks</p>
            <p><strong>Team Size:</strong> 2 BI developers</p>
            <p><strong>Data Sources:</strong> 5 systems integrated</p>
            <p><strong>Report Users:</strong> 150+ executives</p>
        </div>
        
        <div class="success-box">
            <h4>🎯 Business Impact</h4>
            <p><strong>Reporting Speed:</strong> 60% faster</p>
            <p><strong>Decision Making:</strong> Real-time insights</p>
            <p><strong>ROI Achieved:</strong> $750K annually</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Live Infrastructure Demo
    st.markdown("### 📊 Live Infrastructure Metrics Demo")
    
    # Create infrastructure monitoring demo
    infra_data = load_sample_data("infrastructure")
    
    # Real-time metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    current_metrics = simulate_realtime_data()
    
    with col1:
        st.metric("CPU Usage", f"{current_metrics['cpu']:.1f}%", 
                 f"{np.random.choice(['+', '-'])}{np.random.uniform(0.1, 2.0):.1f}%")
    
    with col2:
        st.metric("Memory Usage", f"{current_metrics['memory']:.1f}%",
                 f"{np.random.choice(['+', '-'])}{np.random.uniform(0.5, 3.0):.1f}%")
    
    with col3:
        st.metric("Requests/min", f"{current_metrics['requests']:,}",
                 f"{np.random.choice(['+', '-'])}{np.random.randint(5, 50)}")
    
    with col4:
        st.metric("Avg Response", f"{current_metrics['response_time']:.0f}ms",
                 f"{np.random.choice(['+', '-'])}{np.random.randint(5, 30)}ms")
    
    # Infrastructure charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.line(infra_data.tail(168), x='timestamp', y=['cpu_usage', 'memory_usage'],
                      title='System Performance - Last 7 Days')
        fig1.add_hline(y=80, line_dash="dash", line_color="red", 
                      annotation_text="Critical Threshold")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.scatter(infra_data.tail(168), x='cpu_usage', y='response_time',
                         size='error_count', color='memory_usage',
                         title='Performance Correlation Analysis')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Network traffic analysis
    col1, col2 = st.columns(2)
    
    with col1:
        fig3 = px.area(infra_data.tail(72), x='timestamp', y=['network_in', 'network_out'],
                      title='Network Traffic - Last 3 Days')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Error rate analysis
        hourly_errors = infra_data.tail(168).groupby(infra_data.tail(168)['timestamp'].dt.hour)['error_count'].mean()
        fig4 = px.bar(x=hourly_errors.index, y=hourly_errors.values,
                     title='Average Errors by Hour of Day')
        fig4.update_xaxis(title='Hour of Day')
        fig4.update_yaxis(title='Average Error Count')
        st.plotly_chart(fig4, use_container_width=True)
    
    # Configuration and Documentation
    st.markdown("### ⚙️ Grafana Configuration")
    
    config_tabs = st.tabs(["📋 Dashboard Config", "🚨 Alert Rules", "📖 Documentation"])
    
    with config_tabs[0]:
        st.markdown("#### Grafana Dashboard JSON Configuration")
        
        grafana_config = {
            "dashboard": {
                "title": "Infrastructure Monitoring",
                "panels": [
                    {
                        "title": "CPU Usage",
                        "type": "stat",
                        "targets": [{"expr": "cpu_usage_percent"}],
                        "thresholds": [{"value": 80, "color": "red"}]
                    },
                    {
                        "title": "Memory Usage", 
                        "type": "stat",
                        "targets": [{"expr": "memory_usage_percent"}],
                        "thresholds": [{"value": 85, "color": "red"}]
                    },
                    {
                        "title": "System Performance",
                        "type": "graph",
                        "targets": [
                            {"expr": "cpu_usage_percent", "legend": "CPU %"},
                            {"expr": "memory_usage_percent", "legend": "Memory %"}
                        ]
                    }
                ]
            }
        }
        
        st.code(json.dumps(grafana_config, indent=2), language="json")
    
    with config_tabs[1]:
        st.markdown("#### Alert Configuration Rules")
        
        alert_rules = """
# High CPU Usage Alert
alert: HighCPUUsage
expr: cpu_usage_percent > 80
for: 5m
labels:
  severity: warning
annotations:
  summary: "High CPU usage detected"
  description: "CPU usage is above 80% for more than 5 minutes"

# Memory Usage Critical
alert: MemoryUsageCritical  
expr: memory_usage_percent > 90
for: 2m
labels:
  severity: critical
annotations:
  summary: "Critical memory usage"
  description: "Memory usage is above 90%"

# High Error Rate
alert: HighErrorRate
expr: rate(error_count[5m]) > 0.1
for: 3m
labels:
  severity: warning
annotations:
  summary: "High error rate detected"
  description: "Error rate is above 10% over the last 5 minutes"
        """
        
        st.code(alert_rules, language="yaml")
    
    with config_tabs[2]:
        st.markdown("""
        #### 📖 Implementation Documentation
        
        **Setup Requirements:**
        - Grafana 9.0+ with authentication enabled
        - Prometheus for metrics collection
        - InfluxDB for time-series storage
        - Docker containers for easy deployment
        
        **Installation Steps:**
        
        1. **Deploy Infrastructure:**
        ```bash
        docker-compose up -d grafana prometheus influxdb
        ```
        
        2. **Configure Data Sources:**
        ```yaml
        apiVersion: 1
        datasources:
          - name: Prometheus
            type: prometheus
            url: http://prometheus:9090
          - name: InfluxDB
            type: influxdb
            url: http://influxdb:8086
        ```
        
        3. **Import Dashboard:**
        ```bash
        curl -X POST http://grafana:3000/api/dashboards/db \
             -H "Content-Type: application/json" \
             -d @dashboard-config.json
        ```
        
        **Key Metrics Monitored:**
        - System: CPU, Memory, Disk I/O, Network
        - Application: Response times, Error rates, Throughput  
        - Business: User sessions, Transaction volumes
        - Infrastructure: Container health, Service availability
        
        **Best Practices:**
        - Set appropriate alert thresholds based on historical data
        - Use tags for better organization and filtering
        - Implement dashboard permissions for security
        - Regular backup of dashboard configurations
        - Monitor Grafana itself for high availability
        """)

def show_powerbi_dashboard():
    """Power BI Sales Analytics Dashboard"""
    
    st.markdown("## 📈 Power BI Sales & KPI Analytics Dashboard")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        ### Executive Sales Performance Dashboard
        
        Advanced Power BI solution providing comprehensive sales analytics, KPI tracking, and predictive 
        insights for executive decision-making. Features real-time data integration, interactive 
        visualizations, and automated reporting capabilities.
        
        ### Key Dashboard Features
        - **Executive KPI Overview**: Revenue, profit margins, customer acquisition costs
        - **Sales Performance Tracking**: Individual and team performance metrics
        - **Geographic Analysis**: Regional sales mapping with drill-down capabilities
        - **Predictive Analytics**: ML-powered sales forecasting and trend analysis  
        - **Customer Analytics**: Segmentation, lifetime value, and churn prediction
        - **Mobile Optimization**: Responsive design for executive mobile access
        
        ### Technical Implementation
        - **Data Sources**: SQL Server, Excel, SharePoint, Salesforce CRM
        - **Refresh Schedule**: Real-time for critical metrics, hourly for detailed reports
        - **Security**: Row-level security with role-based access control
        - **Performance**: Optimized DAX calculations and data model design
