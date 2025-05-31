import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Stock Split Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 1rem;
        color: #808495;
    }
    h1 {
        text-align: center;
        color: #1f2937;
        padding: 20px 0;
    }
    .stAlert {
        background-color: #e8f4f8;
        border-left: 4px solid #3498db;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    # Read the CSV file - make sure to update the path
    df = pd.read_csv("Updated_Stock_Split_Analysis.csv")
    return df

# Main app
def main():
    # Title
    st.markdown("<h1>📊 Stock Split Analysis Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280; font-size: 1.2rem;'>Analysis of 5 S&P 500 Companies</p>", unsafe_allow_html=True)
    
    # Load data
    try:
        data = load_data()
    except FileNotFoundError:
        st.error("⚠️ Please ensure 'Updated_Stock_Split_Analysis.csv' is in the same directory as this script.")
        st.stop()
    
    # KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Companies Analyzed</div>
            <div class="metric-value" style="color: #3498db;">5</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        recommend_count = len(data[data['Split_Recommendation'] == 'YES'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Recommend Split</div>
            <div class="metric-value" style="color: #27ae60;">{recommend_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_price = data['Price_USD'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Price</div>
            <div class="metric-value" style="color: #f39c12;">${avg_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        max_price = data['Price_USD'].max()
        max_ticker = data.loc[data['Price_USD'].idxmax(), 'Ticker']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Highest Price ({max_ticker})</div>
            <div class="metric-value" style="color: #e74c3c;">${max_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        # Current Stock Prices Bar Chart
        st.subheader("📈 Current Stock Prices")
        
        # Sort data by price
        data_sorted = data.sort_values('Price_USD', ascending=True)
        
        # Create color map
        colors = ['#27ae60' if x == 'YES' else '#3498db' for x in data_sorted['Split_Recommendation']]
        
        fig1 = go.Figure(data=[
            go.Bar(
                x=data_sorted['Price_USD'],
                y=data_sorted['Ticker'],
                orientation='h',
                marker_color=colors,
                text=[f"${x:,.0f}" for x in data_sorted['Price_USD']],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Price: $%{x:,.2f}<extra></extra>'
            )
        ])
        
        fig1.update_layout(
            xaxis_title="Price (USD)",
            yaxis_title="",
            showlegend=False,
            height=400,
            margin=dict(l=0, r=50, t=0, b=0),
            xaxis=dict(tickformat="$,.0f"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Price Comparison Chart
        st.subheader("💹 Price Comparison: Split Scenarios")
        
        # Prepare comparison data
        comparison_data = []
        for _, row in data.iterrows():
            comparison_data.extend([
                {'Company': row['Company'], 'Scenario': 'Current', 'Price': row['Price_USD']},
                {'Company': row['Company'], 'Scenario': '10:1 Split', 'Price': row['Price_After_10to1']},
                {'Company': row['Company'], 'Scenario': '20:1 Split', 'Price': row['Price_After_20to1']}
            ])
        
        comp_df = pd.DataFrame(comparison_data)
        
        fig2 = px.bar(
            comp_df, 
            x='Company', 
            y='Price', 
            color='Scenario',
            barmode='group',
            color_discrete_map={
                'Current': '#3498db',
                '10:1 Split': '#27ae60',
                '20:1 Split': '#f39c12'
            },
            hover_data={'Price': ':$,.2f'}
        )
        
        fig2.update_layout(
            xaxis_title="",
            yaxis_title="Price (USD)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(tickformat="$,.0f"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Key Insights Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔍 Key Insights")
    
    insights_html = """
    <div style="background-color: #e8f4f8; border-left: 4px solid #3498db; padding: 20px; border-radius: 8px;">
        <ul style="margin: 0; padding-left: 20px; line-height: 1.8;">
            <li><strong>Amazon ($3,584)</strong> and <strong>Netflix ($485)</strong> are prime candidates for stock splits</li>
            <li>Amazon's price is <strong>5.7x higher</strong> than our portfolio average</li>
            <li>JPMorgan, Coca-Cola, and J&J have accessible price points (all under $175)</li>
            <li>A 10:1 split would bring Amazon to <strong>$358.40</strong> and Netflix to <strong>$48.50</strong></li>
            <li>Companies with PE ratios >30 tend to benefit more from splits</li>
        </ul>
    </div>
    """
    st.markdown(insights_html, unsafe_allow_html=True)
    
    # Company Cards
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🏢 Individual Company Analysis")
    
    # Create two columns for company cards
    col1, col2 = st.columns(2)
    
    for idx, row in data.iterrows():
        with col1 if idx % 2 == 0 else col2:
            color = "#27ae60" if row['Split_Recommendation'] == 'YES' else "#e74c3c"
            recommendation_text = "✅ SPLIT: YES" if row['Split_Recommendation'] == 'YES' else "❌ SPLIT: NO"
            
            card_html = f"""
            <div style="background-color: white; border-left: 5px solid {color}; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 10px 0;">{row['Company']} ({row['Ticker']})</h4>
                <p style="margin: 5px 0;"><strong>Current Price:</strong> ${row['Price_USD']:,.2f}</p>
                <p style="margin: 5px 0;"><strong>PE Ratio:</strong> {row['PE_Ratio']:.1f} | <strong>Market Cap:</strong> ${row['Market_Cap_Billions']:.1f}B</p>
                <p style="margin: 10px 0 0 0; color: {color}; font-weight: bold;">{recommendation_text}</p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
    
    # Detailed Data Table
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Detailed Stock Analysis")
    
    # Format the dataframe for display
    display_df = data.copy()
    
    # Format currency columns
    currency_cols = ['Price_USD', 'Price_After_10to1', 'Price_After_20to1']
    for col in currency_cols:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
    
    # Format other numeric columns
    display_df['Market_Cap_Billions'] = display_df['Market_Cap_Billions'].apply(lambda x: f"${x:.1f}B")
    display_df['PE_Ratio'] = display_df['PE_Ratio'].apply(lambda x: f"{x:.1f}")
    display_df['Dividend_Yield'] = display_df['Dividend_Yield'].apply(lambda x: f"{x:.2f}%")
    
    # Apply styling to the recommendation column
    def highlight_recommendation(val):
        if val == 'YES':
            return 'background-color: #d4edda; color: #155724; font-weight: bold;'
        else:
            return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    
    styled_df = display_df.style.applymap(highlight_recommendation, subset=['Split_Recommendation'])
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Footer
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280;'>Stock Split Analysis Dashboard | Data as of Latest Update</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()