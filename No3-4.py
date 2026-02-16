import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Load Original Individual Data (3.1) ---
# This part tracks the "live" progression for each of the 8 coins
file_path = r'RAW_3-4.csv' 
try:
    df = pd.read_csv(file_path, header=[0, 1])
    coin_map = {
        '1A': '1', '1B': '1',
        '2': '2',
        '5A': '5', '5B': '5',
        '10A': '10', '10B': '10',
        '20': '20'
    }

    coins_data = {}
    for i, coin_id in enumerate(coin_map.keys()):
        start_col = i * 4
        temp_df = df.iloc[:, start_col:start_col+4].copy()
        temp_df.columns = ['G', 'T', 'Cum Tails', 'Cum Heads']
        temp_df['Cum Tails'] = pd.to_numeric(temp_df['Cum Tails'], errors='coerce')
        temp_df['Cum Heads'] = pd.to_numeric(temp_df['Cum Heads'], errors='coerce')
        temp_df = temp_df.dropna(subset=['Cum Tails', 'Cum Heads'])
        temp_df['Toss Number'] = range(1, len(temp_df) + 1)
        coins_data[coin_id] = temp_df
except FileNotFoundError:
    print("Individual toss file (RAW_3-4.csv) not found. Skipping Graph 3.1.")
    coins_data = {}

# --- 2. Load and Process the "Right Data" (3.2, 3.3, 4.1) ---
# This uses the specific summary percentages you provided
df_summary = pd.read_csv(r'RAW_3.csv')

# Calculate the combined Final Heads/Tails for the summary graphs
# We average Tiles and Wood percentages (ignoring 0 values like Class 2 on Tiles)
def get_final_avg(row):
    h_vals = [h for h in [row['H Tiles'], row['H Wood']] if h > 0]
    t_vals = [t for t in [row['T Tiles'], row['T Wood']] if t > 0]
    return pd.Series([np.mean(h_vals), np.mean(t_vals)])

df_summary[['Final Heads', 'Final Tails']] = df_summary.apply(get_final_avg, axis=1)

# Format for the plot_in_chunks function (3.2)
avg_curves = {}
for _, row in df_summary.iterrows():
    avg_curves[row['Coin Class']] = pd.DataFrame({
        'Avg Heads': [row['H Tiles'], row['H Wood']],
        'Avg Tails': [row['T Tiles'], row['T Wood']]
    }, index=['Tiles', 'Wood'])

df_final = df_summary[['Coin Class', 'Final Heads', 'Final Tails']].rename(columns={'Coin Class': 'Class'})

# --- Updated Plotting Logic ---

def plot_in_chunks(data_dict, title_prefix, color_h='orange', color_t='blue', is_avg=False):
    """Helper function to plot items in chunks of 4 (2x2 grid)"""
    items = list(data_dict.items())
    for i in range(0, len(items), 4):
        chunk = items[i:i+4]
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        axs = axs.flatten()
        
        for j, (key, data) in enumerate(chunk):
            if is_avg:
                # For 3.2, we compare Wood vs Tiles percentages for each class
                x_labels = data.index
                x_pos = np.arange(len(x_labels))
                width = 0.35
                axs[j].bar(x_pos - width/2, data['Avg Heads'], width, label='Heads', color=color_h)
                axs[j].bar(x_pos + width/2, data['Avg Tails'], width, label='Tails', color=color_t)
                axs[j].set_xticks(x_pos)
                axs[j].set_xticklabels(x_labels)
                axs[j].set_title(f'Class {key} Average')
                axs[j].set_ylabel("Percentage (%)")
                axs[j].set_ylim(0, 100)
            else:
                axs[j].plot(data['Toss Number'], data['Cum Heads'], label='Heads', color=color_h)
                axs[j].plot(data['Toss Number'], data['Cum Tails'], label='Tails', color=color_t)
                axs[j].set_title(f'Coin {key}')
                axs[j].set_xlabel("Tosses")
                axs[j].set_ylabel("Count")
            
            axs[j].legend()
            axs[j].grid(True, alpha=0.3)

        for k in range(len(chunk), 4):
            axs[k].axis('off')
            
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.suptitle(f"{title_prefix} (Part {i//4 + 1})", fontsize=16)
        plt.show()

# Graph 3.1: Individual Coin Progressions
if coins_data:
    plot_in_chunks(coins_data, "3.1 | Individual Coin Progressions")

# Graph 3.2: Average Progression by Coin Class
plot_in_chunks(avg_curves, "3.2 | Average Progression by Coin Class", is_avg=True)

# Graph 3.3: Line Graph (Progression Across Coin Classes)
plt.figure(figsize=(10, 6))
plt.plot(df_final['Class'], df_final['Final Heads'], marker='o', label='Heads', color='orange', linewidth=2)
plt.plot(df_final['Class'], df_final['Final Tails'], marker='o', label='Tails', color='blue', linewidth=2)
plt.title("Graph 3.3 | Final Progression Across Coin Classes (Line Graph)")
plt.xlabel("Coin Class")
plt.ylabel("Average Final Percentage (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Graph 4.1: Bar Graph (Overall Average H&T Across ALL Coin Classes)
# CHANGED: Now shows only two bars for the entire experiment's average
overall_h = df_final['Final Heads'].mean()
overall_t = df_final['Final Tails'].mean()

plt.figure(figsize=(8, 6))
bars = plt.bar(['Overall Heads', 'Overall Tails'], [overall_h, overall_t], color=['orange', 'blue'], width=0.6)
plt.ylabel('Average Final Percentage (%)')
plt.title('Graph 4.1 | Overall Average Heads & Tails (%)')
plt.ylim(0, 100) 
plt.grid(axis='y', alpha=0.3)

# Adding percentage labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.show()