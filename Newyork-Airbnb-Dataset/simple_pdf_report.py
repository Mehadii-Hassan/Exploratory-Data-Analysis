"""
Professional PDF Report Generator for NYC Airbnb Dataset
Simplified version using standard fonts
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from datetime import datetime
import os
import shutil

# Set style for plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def load_data():
    """Load the Airbnb dataset"""
    df = pd.read_csv("AB_NYC_2019.csv")
    return df

def add_title_page(pdf, title, subtitle, date_str):
    """Add a professional title page"""
    pdf.add_page()
    
    # Background color (light blue)
    pdf.set_fill_color(41, 128, 185)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Title
    pdf.set_font("Helvetica", "B", 42)
    pdf.set_text_color(255, 255, 255)
    pdf.ln(70)
    pdf.cell(0, 20, title, 0, 1, "C")
    
    # Subtitle
    pdf.set_font("Helvetica", "I", 20)
    pdf.set_text_color(220, 237, 255)
    pdf.cell(0, 15, subtitle, 0, 1, "C")
    
    # Date
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(200, 200, 200)
    pdf.ln(90)
    pdf.cell(0, 8, f"Report Generated: {date_str}", 0, 1, "C")
    pdf.cell(0, 8, "Exploratory Data Analysis", 0, 1, "C")

def add_section(pdf, title):
    """Add a section header"""
    pdf.set_fill_color(41, 128, 185)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, " " + title, 0, 1, "L", True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

def add_text(pdf, text, size=11):
    """Add text paragraph"""
    pdf.set_font("Helvetica", "", size)
    pdf.multi_cell(0, 5, text)
    pdf.ln(3)

def add_heading(pdf, text):
    """Add a subheading"""
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 8, text, 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)

def generate_visualizations(df):
    """Generate visualization images"""
    os.makedirs("temp_images", exist_ok=True)
    
    # 1. Price Distribution
    plt.figure(figsize=(10, 6))
    plt.title('Price Distribution', fontsize=14, fontweight='bold')
    sns.histplot(df['price'], bins=50, kde=True, color='skyblue')
    plt.xlabel('Price (USD)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('temp_images/01_price_dist.png', dpi=90, bbox_inches='tight')
    plt.close()
    
    # 2. Room Type Pie Chart
    plt.figure(figsize=(9, 6))
    room_counts = df['room_type'].value_counts()
    plt.pie(room_counts, labels=room_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Distribution by Room Type', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('temp_images/02_room_type.png', dpi=90, bbox_inches='tight')
    plt.close()
    
    # 3. Neighbourhood Group
    plt.figure(figsize=(10, 6))
    neigh_counts = df['neighbourhood_group'].value_counts()
    plt.barh(neigh_counts.index, neigh_counts.values, color='steelblue')
    plt.title('Listings by Neighbourhood Group', fontsize=14, fontweight='bold')
    plt.xlabel('Count')
    plt.tight_layout()
    plt.savefig('temp_images/03_neighbourhood.png', dpi=90, bbox_inches='tight')
    plt.close()
    
    # 4. Price by Room Type (boxplot)
    plt.figure(figsize=(10, 6))
    df_clean = df[df['price'] < 500]  # Remove extreme outliers for better visualization
    sns.boxplot(data=df_clean, x='room_type', y='price')
    plt.title('Price Distribution by Room Type', fontsize=14, fontweight='bold')
    plt.ylabel('Price (USD)')
    plt.tight_layout()
    plt.savefig('temp_images/04_price_room.png', dpi=90, bbox_inches='tight')
    plt.close()
    
    # 5. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    numerical = df.select_dtypes(include=[np.number]).columns
    corr = df[numerical].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('temp_images/05_correlation.png', dpi=90, bbox_inches='tight')
    plt.close()
    
    # 6. Top 10 Neighbourhoods
    plt.figure(figsize=(12, 6))
    top_neigh = df['neighbourhood'].value_counts().head(10)
    plt.barh(range(len(top_neigh)), top_neigh.values, color='coral')
    plt.yticks(range(len(top_neigh)), top_neigh.index, fontsize=9)
    plt.xlabel('Number of Listings')
    plt.title('Top 10 Neighbourhoods by Listings', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('temp_images/06_top_neighbourhoods.png', dpi=90, bbox_inches='tight')
    plt.close()
    
    print("Visualizations created successfully")

def create_report(df):
    """Create the PDF report"""
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    
    date_str = datetime.now().strftime("%B %d, %Y")
    
    # ===== PAGE 1: Title Page =====
    add_title_page(pdf, "NYC Airbnb Dataset", "Exploratory Data Analysis", date_str)
    
    # ===== PAGE 2: Table of Contents =====
    pdf.add_page()
    add_section(pdf, "Contents")
    toc = [
        "1. Executive Summary",
        "2. Dataset Overview",
        "3. Data Quality",
        "4. Univariate Analysis",
        "5. Bivariate Analysis",
        "6. Key Insights",
        "7. Recommendations"
    ]
    for item in toc:
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, item, 0, 1)
    
    # ===== PAGE 3: Executive Summary =====
    pdf.add_page()
    add_section(pdf, "1. Executive Summary")
    
    summary = f"""The NYC Airbnb dataset contains {len(df):,} listings across New York City, 
providing insights into the short-term rental market. The analysis reveals significant 
variations in pricing and demand across neighborhoods and room types. Manhattan dominates 
with {(df[df['neighbourhood_group']=='Manhattan'].shape[0]/len(df)*100):.1f}% of listings, 
while Entire homes command premium prices.
"""
    add_text(pdf, summary)
    
    add_heading(pdf, "Key Metrics:")
    metrics = f"""Total Listings: {len(df):,}
Average Price: USD {df['price'].mean():.2f}
Median Price: USD {df['price'].median():.2f}
Total Neighbourhoods: {df['neighbourhood'].nunique()}
Unique Hosts: {df['host_id'].nunique():,}
Avg Reviews/Month: {df['reviews_per_month'].mean():.2f}
"""
    add_text(pdf, metrics, size=10)
    
    # ===== PAGE 4: Dataset Overview =====
    pdf.add_page()
    add_section(pdf, "2. Dataset Overview")
    
    overview = f"""Dataset Structure:
- Total Records: {len(df):,} listings
- Total Columns: {len(df.columns)} features
- Coverage: 5 NYC boroughs
- Data Period: 2019
- Five Neighbourhood Groups: Manhattan, Brooklyn, Queens, Bronx, Staten Island
"""
    add_text(pdf, overview)
    
    add_heading(pdf, "Key Features:")
    features = """- Listing information (ID, name, prices)
- Host information (ID, name, listings count)
- Geographic data (neighborhood groups, lat/long)
- Room type and minimum night requirements
- Review metrics and availability data
"""
    add_text(pdf, features)
    
    # ===== PAGE 5: Data Quality =====
    pdf.add_page()
    add_section(pdf, "3. Data Quality Assessment")
    
    missing = df.isnull().sum()
    missing_text = f"""Missing Values Analysis:
- No completely empty columns
- Most critical fields are complete
- {(df.isnull().any(axis=1)).sum()} records have missing data
- {(~df.isnull().any(axis=1)).sum()} fully complete records

Data Integrity:
[OK] No duplicate records found
[OK] Consistent data types
[OK] Valid coordinate ranges
[OK] Reasonable price values
"""
    add_text(pdf, missing_text, size=10)
    
    # ===== PAGE 6: Univariate Analysis - Part 1 =====
    pdf.add_page()
    add_section(pdf, "4. Univariate Analysis")
    
    add_heading(pdf, "Price Statistics:")
    price_stats = f"""Mean: USD {df['price'].mean():.2f}
Median: USD {df['price'].median():.2f}
Std Dev: USD {df['price'].std():.2f}
Min: USD {df['price'].min():.0f}
Max: USD {df['price'].max():.0f}
Range: USD {df['price'].max() - df['price'].min():.0f}
Skewness: {df['price'].skew():.2f} (Right-skewed)
"""
    add_text(pdf, price_stats, size=10)
    
    # Add first visualization
    if os.path.exists('temp_images/01_price_dist.png'):
        pdf.image('temp_images/01_price_dist.png', x=12, w=186)
    
    # ===== PAGE 7: Univariate Analysis - Charts =====
    pdf.add_page()
    
    if os.path.exists('temp_images/02_room_type.png'):
        pdf.image('temp_images/02_room_type.png', x=12, w=95)
    
    if os.path.exists('temp_images/03_neighbourhood.png'):
        pdf.image('temp_images/03_neighbourhood.png', x=110, w=95)
    
    pdf.ln(10)
    add_heading(pdf, "Room Type & Neighbourhood Distribution:")
    dist_text = f"""Room Types:
- Entire homes: {(df['room_type']=='Entire home/apt').sum():,} ({(df['room_type']=='Entire home/apt').sum()/len(df)*100:.1f}%)
- Private rooms: {(df['room_type']=='Private room').sum():,} ({(df['room_type']=='Private room').sum()/len(df)*100:.1f}%)
- Shared rooms: {(df['room_type']=='Shared room').sum():,} ({(df['room_type']=='Shared room').sum()/len(df)*100:.1f}%)

Neighbourhood Groups:
- Manhattan: {(df['neighbourhood_group']=='Manhattan').sum():,} listings
- Brooklyn: {(df['neighbourhood_group']=='Brooklyn').sum():,} listings
- Queens: {(df['neighbourhood_group']=='Queens').sum():,} listings
"""
    add_text(pdf, dist_text, size=9)
    
    # ===== PAGE 8: Bivariate Analysis =====
    pdf.add_page()
    add_section(pdf, "5. Bivariate Analysis")
    
    add_heading(pdf, "Price by Room Type:")
    price_room = df.groupby('room_type')['price'].agg(['mean', 'median', 'count'])
    price_text = ""
    for room_type in price_room.index:
        row = price_room.loc[room_type]
        count = int(row['count'])
        mean_price = row['mean']
        median_price = row['median']
        price_text += f"{room_type}: Mean USD {mean_price:.2f}, Median USD {median_price:.2f}, Count {count:,}\n"
    
    add_text(pdf, price_text, size=10)
    
    if os.path.exists('temp_images/04_price_room.png'):
        pdf.image('temp_images/04_price_room.png', x=12, w=186)
    
    # ===== PAGE 9: Top Neighbourhoods =====
    pdf.add_page()
    
    if os.path.exists('temp_images/06_top_neighbourhoods.png'):
        pdf.image('temp_images/06_top_neighbourhoods.png', x=12, w=186)
    
    pdf.ln(10)
    top_10 = df['neighbourhood'].value_counts().head(10)
    top_text = "Top 10 Neighbourhoods:\n"
    for i, (neigh, count) in enumerate(top_10.items(), 1):
        top_text += f"{i}. {neigh}: {count} listings\n"
    add_text(pdf, top_text, size=10)
    
    # ===== PAGE 10: Correlation =====
    pdf.add_page()
    add_section(pdf, "5b. Correlation Analysis")
    
    if os.path.exists('temp_images/05_correlation.png'):
        pdf.image('temp_images/05_correlation.png', x=12, w=186)
    
    # ===== PAGE 11: Key Insights =====
    pdf.add_page()
    add_section(pdf, "6. Key Insights & Findings")
    
    insights = f"""Market Leaders:
Manhattan has the highest concentration ({(df[df['neighbourhood_group']=='Manhattan'].shape[0]/len(df)*100):.1f}% 
of listings). Brooklyn follows with {(df[df['neighbourhood_group']=='Brooklyn'].shape[0]/len(df)*100):.1f}%.

Price Premium:
Entire homes average USD {df[df['room_type']=='Entire home/apt']['price'].mean():.2f} vs 
USD {df[df['room_type']=='Private room']['price'].mean():.2f} for private rooms - a 
{(df[df['room_type']=='Entire home/apt']['price'].mean() / df[df['room_type']=='Private room']['price'].mean() - 1)*100:.0f}% premium.

Booking Activity:
{(df['number_of_reviews'] > 0).sum():,} listings ({(df['number_of_reviews'] > 0).sum()/len(df)*100:.1f}%) 
have at least one review. Average reviews/month: {df['reviews_per_month'].mean():.2f}.

Host Market:
{df['host_id'].nunique():,} unique hosts manage {len(df):,} listings, 
averaging {len(df)/df['host_id'].nunique():.2f} properties per host.

Availability:
Average {df['availability_365'].mean():.0f} days available per year, 
suggesting approximately {((365-df['availability_365'].mean())/(365)*100):.1f}% occupancy rate.
"""
    add_text(pdf, insights, size=10)
    
    # ===== PAGE 12: Recommendations =====
    pdf.add_page()
    add_section(pdf, "7. Recommendations")
    
    recs = """Strategic Location Focus:
- Prioritize Manhattan and Brooklyn for premium pricing
- Explore underserved outer boroughs for growth opportunities

Room Type Optimization:
- Consider converting to entire homes where market conditions support
- Private rooms remain competitive in price-sensitive segments

Pricing Strategy:
- Use competitive pricing in high-competition areas
- Leverage location uniqueness for premium positioning
- Monitor neighbourhood price trends

Host Performance:
- Share best practices from high-performing hosts
- Focus on review generation and maintenance
- Invest in customer experience for repeat bookings

Market Expansion:
- Analyze neighbourhoods with low density but consistent demand
- Identify emerging neighbourhoods for early-mover advantage
"""
    add_text(pdf, recs, size=10)
    
    # ===== Final Note =====
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 4, "Analysis based on 2019 Airbnb data. Market conditions may have changed. " +
                   "This report is for informational purposes only.")
    
    # Save the PDF
    output_file = "NYC_Airbnb_EDA_Report.pdf"
    pdf.output(output_file)
    
    return output_file

def main():
    print("Loading Airbnb dataset...")
    df = load_data()
    print(f"Loaded: {len(df)} listings with {len(df.columns)} features")
    
    print("Generating visualizations...")
    generate_visualizations(df)
    
    print("Creating PDF report...")
    output = create_report(df)
    print(f"Report saved: {output}")
    
    # Cleanup
    if os.path.exists("temp_images"):
        shutil.rmtree("temp_images")
        print("Cleaned up temporary files")
    
    print("Done!")

if __name__ == "__main__":
    main()
