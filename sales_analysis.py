import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── DATASET ──
data = {
    'Order_ID': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112],
    'Customer': ['Priya', 'Rahul', 'Sneha', 'Arjun', 'Meena', 'Kiran',
                 'Pooja', 'Vikram', 'Ananya', 'Rohit', 'Divya', 'Suresh'],
    'Product':  ['Laptop', 'Phone', 'Laptop', 'Tablet', 'Phone', 'Laptop',
                 'Tablet', 'Phone', 'Laptop', 'Phone', 'Tablet', 'Laptop'],
    'City':     ['Delhi', 'Mumbai', 'Delhi', 'Chennai', 'Delhi', 'Mumbai',
                 'Delhi', 'Chennai', 'Bangalore', 'Bangalore', 'Mumbai', 'Chennai'],
    'Amount':   [55000, 22000, 55000, 18000, 22000, 55000,
                 18000, 22000, 55000, 22000, 18000, 55000],
    'Month':    ['January', 'January', 'February', 'February', 'February', 'March',
                 'March', 'March', 'April', 'April', 'April', 'May']
}

df = pd.DataFrame(data)

# ── DATA CLEANING ──
df['Customer'] = df['Customer'].str.strip().str.title()
df['City'] = df['City'].str.strip().str.title()
df['Product'] = df['Product'].str.strip().str.title()

# ── ORDER TYPE ──
df['Order_Type'] = df['Amount'].apply(
    lambda x: 'Premium' if x >= 55000 else ('Standard' if x >= 20000 else 'Budget')
)

# ── EMOJIS / ICONS as text for products ──
product_icons = {'Laptop': '💻', 'Phone': '📱', 'Tablet': '📟'}
df['Product_Icon'] = df['Product'].map(product_icons)

# ── COLORS ──
NAVY = '#0D1B2A'
BLUE1 = '#1B3A5C'
BLUE2 = '#2E6BAD'
BLUE3 = '#5BA4CF'
BLUE4 = '#A8D1F0'
GOLD = '#E8A838'
WHITE = '#FFFFFF'
BG = '#F0F4F8'

product_colors = {'Laptop': BLUE1, 'Phone': BLUE2, 'Tablet': BLUE3}
city_colors = ['#0D1B2A', '#1B3A5C', '#2E6BAD', '#5BA4CF', '#A8D1F0']

# ── FIGURE ──
fig = plt.figure(figsize=(20, 24), facecolor=BG)
fig.suptitle('', fontsize=1)

# Title Banner
ax_title = fig.add_axes([0, 0.95, 1, 0.05])
ax_title.set_facecolor(NAVY)
ax_title.text(0.5, 0.5, '📊  RETAIL SALES PERFORMANCE ANALYSIS  📊',
              ha='center', va='center', fontsize=22, fontweight='bold',
              color=GOLD, transform=ax_title.transAxes)
ax_title.axis('off')

# Subtitle
ax_sub = fig.add_axes([0, 0.92, 1, 0.03])
ax_sub.set_facecolor(BLUE1)
ax_sub.text(0.5, 0.5, 'Multi-City Sales Dashboard  |  Excel · SQL · Python  |  G. Sweekrith Kumar',
            ha='center', va='center', fontsize=13, color=BLUE4,
            transform=ax_sub.transAxes)
ax_sub.axis('off')

# ── KPI CARDS ──
kpis = [
    ('💰 Total Revenue', f'₹{df["Amount"].sum():,}', NAVY),
    ('📦 Total Orders', str(len(df)), BLUE1),
    ('📈 Avg Order Value', f'₹{int(df["Amount"].mean()):,}', BLUE2),
    ('🏆 Top City', df.groupby("City")["Amount"].sum().idxmax(), NAVY),
    ('⭐ Top Product', df.groupby("Product")["Amount"].sum().idxmax(), BLUE1),
]

for i, (label, value, color) in enumerate(kpis):
    ax = fig.add_axes([0.01 + i * 0.196, 0.86, 0.185, 0.055])
    ax.set_facecolor(color)
    ax.text(0.5, 0.7, label, ha='center', va='center', fontsize=11,
            color=BLUE4, transform=ax.transAxes)
    ax.text(0.5, 0.25, value, ha='center', va='center', fontsize=16,
            fontweight='bold', color=GOLD, transform=ax.transAxes)
    for spine in ax.spines.values():
        spine.set_edgecolor(GOLD)
        spine.set_linewidth(1.5)
    ax.set_xticks([])
    ax.set_yticks([])

# ── CHART 1: Sales by Product (Bar with icons) ──
ax1 = fig.add_axes([0.05, 0.62, 0.4, 0.22])
ax1.set_facecolor(WHITE)
product_sales = df.groupby('Product')['Amount'].sum().sort_values(ascending=False)
bars = ax1.bar(
    [f"{product_icons[p]}  {p}" for p in product_sales.index],
    product_sales.values,
    color=[product_colors[p] for p in product_sales.index],
    width=0.5, edgecolor=GOLD, linewidth=1.5
)
for bar, val in zip(bars, product_sales.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
             f'₹{val:,}', ha='center', va='bottom', fontsize=12,
             fontweight='bold', color=NAVY)
pct = product_sales / product_sales.sum() * 100
for i, (bar, p) in enumerate(zip(bars, product_sales.index)):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
             f'{pct[p]:.1f}%', ha='center', va='center', fontsize=11,
             color=WHITE, fontweight='bold')
ax1.set_title('💻 📱 📟  Sales by Product', fontsize=14, fontweight='bold', color=NAVY, pad=10)
ax1.set_ylabel('Revenue (₹)', color=NAVY, fontsize=11)
ax1.tick_params(colors=NAVY, labelsize=11)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_facecolor('#FAFCFF')

# ── CHART 2: Sales by City ──
ax2 = fig.add_axes([0.55, 0.62, 0.4, 0.22])
city_sales = df.groupby('City')['Amount'].sum().sort_values(ascending=False)
bars2 = ax2.barh(
    city_sales.index, city_sales.values,
    color=city_colors[:len(city_sales)],
    edgecolor=GOLD, linewidth=1.2, height=0.5
)
for bar, val in zip(bars2, city_sales.values):
    ax2.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
             f'₹{val:,}', va='center', fontsize=11, fontweight='bold', color=NAVY)
ax2.set_title('🏙️  Sales by City', fontsize=14, fontweight='bold', color=NAVY, pad=10)
ax2.set_xlabel('Revenue (₹)', color=NAVY, fontsize=11)
ax2.tick_params(colors=NAVY, labelsize=11)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_facecolor('#FAFCFF')

# ── CHART 3: Monthly Trend ──
ax3 = fig.add_axes([0.05, 0.36, 0.4, 0.22])
month_order = ['January', 'February', 'March', 'April', 'May']
month_sales = df.groupby('Month')['Amount'].sum().reindex(month_order)
ax3.plot(month_sales.index, month_sales.values, color=GOLD,
         marker='o', linewidth=3, markersize=10, markerfacecolor=NAVY,
         markeredgecolor=GOLD, markeredgewidth=2)
ax3.fill_between(range(len(month_sales)), month_sales.values,
                 alpha=0.15, color=BLUE2)
for i, (month, val) in enumerate(zip(month_sales.index, month_sales.values)):
    ax3.text(i, val + 1500, f'₹{val:,}', ha='center', fontsize=10,
             fontweight='bold', color=NAVY)
ax3.set_xticks(range(len(month_sales)))
ax3.set_xticklabels([m[:3] for m in month_sales.index], color=NAVY, fontsize=11)
ax3.set_title('📈  Monthly Sales Trend', fontsize=14, fontweight='bold', color=NAVY, pad=10)
ax3.set_ylabel('Revenue (₹)', color=NAVY, fontsize=11)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.set_facecolor('#FAFCFF')
ax3.tick_params(colors=NAVY)

# ── CHART 4: Order Type Distribution (Pie) ──
ax4 = fig.add_axes([0.55, 0.36, 0.4, 0.22])
order_dist = df['Order_Type'].value_counts()
pie_colors = [NAVY, BLUE2, BLUE4]
wedges, texts, autotexts = ax4.pie(
    order_dist.values,
    labels=order_dist.index,
    autopct='%1.1f%%',
    colors=pie_colors,
    startangle=90,
    wedgeprops={'edgecolor': WHITE, 'linewidth': 2}
)
for text in texts:
    text.set_fontsize(12)
    text.set_color(NAVY)
    text.set_fontweight('bold')
for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_color(WHITE)
    autotext.set_fontweight('bold')
ax4.set_title('🎯  Order Type Distribution', fontsize=14, fontweight='bold', color=NAVY, pad=10)

# ── CHART 5: City x Product Heatmap ──
ax5 = fig.add_axes([0.05, 0.10, 0.55, 0.22])
pivot = df.pivot_table(values='Amount', index='City', columns='Product', aggfunc='sum', fill_value=0)
im = ax5.imshow(pivot.values, cmap='Blues', aspect='auto')
ax5.set_xticks(range(len(pivot.columns)))
ax5.set_yticks(range(len(pivot.index)))
ax5.set_xticklabels([f"{product_icons[c]}  {c}" for c in pivot.columns], fontsize=11, color=NAVY)
ax5.set_yticklabels(pivot.index, fontsize=11, color=NAVY)
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        val = pivot.values[i, j]
        ax5.text(j, i, f'₹{val:,}' if val > 0 else '—',
                ha='center', va='center', fontsize=11,
                color=WHITE if val > 30000 else NAVY, fontweight='bold')
ax5.set_title('🗺️  City × Product Revenue Heatmap', fontsize=14, fontweight='bold', color=NAVY, pad=10)
plt.colorbar(im, ax=ax5, shrink=0.8)

# ── CHART 6: Top Customers ──
ax6 = fig.add_axes([0.65, 0.10, 0.3, 0.22])
customer_sales = df.groupby('Customer')['Amount'].sum().sort_values(ascending=True).tail(6)
bars6 = ax6.barh(customer_sales.index, customer_sales.values,
                  color=[BLUE1 if v == customer_sales.max() else BLUE3 for v in customer_sales.values],
                  edgecolor=GOLD, linewidth=1.2, height=0.5)
for bar, val in zip(bars6, customer_sales.values):
    ax6.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
             f'₹{val:,}', va='center', fontsize=10, color=NAVY, fontweight='bold')
ax6.set_title('👑  Top Customers', fontsize=14, fontweight='bold', color=NAVY, pad=10)
ax6.spines['top'].set_visible(False)
ax6.spines['right'].set_visible(False)
ax6.set_facecolor('#FAFCFF')
ax6.tick_params(colors=NAVY, labelsize=10)

# Footer
ax_foot = fig.add_axes([0, 0, 1, 0.025])
ax_foot.set_facecolor(NAVY)
ax_foot.text(0.5, 0.5, 'Project by G. Sweekrith Kumar  |  Tools: Python · SQL · Excel · Power BI  |  github.com/sweekrithkumar08-cmd',
             ha='center', va='center', fontsize=11, color=BLUE4,
             transform=ax_foot.transAxes)
ax_foot.axis('off')

plt.savefig('/mnt/user-data/outputs/Sales_Analysis_Dashboard.png',
            dpi=150, bbox_inches='tight', facecolor=BG)
print("Sales Dashboard saved!")
plt.close()

# ── INSIGHTS ──
print("\n" + "="*50)
print("KEY BUSINESS INSIGHTS")
print("="*50)
print(f"Total Revenue: ₹{df['Amount'].sum():,}")
print(f"Total Orders: {len(df)}")
print(f"Average Order Value: ₹{int(df['Amount'].mean()):,}")
print(f"\nTop Product: {df.groupby('Product')['Amount'].sum().idxmax()}")
print(f"Top City: {df.groupby('City')['Amount'].sum().idxmax()}")
print(f"Best Month: {df.groupby('Month')['Amount'].sum().idxmax()}")
print(f"\nProduct Revenue Share:")
for prod, amt in df.groupby('Product')['Amount'].sum().items():
    pct = amt/df['Amount'].sum()*100
    print(f"  {product_icons[prod]} {prod}: ₹{amt:,} ({pct:.1f}%)")
