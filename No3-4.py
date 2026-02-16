import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Load Original Individual Data (3.1) ---
file_path = r'RAW_3-4.csv'
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

# --- 2. Load and Process the "Right Data" (3.2, 4.1, 4.2) ---
# Load the new summary data you provided
df_summary = pd.read_csv(r'RAW_3.csv')

# Calculate the combined Final Heads/Tails for the summary graphs (4.1/4.2)
# We handle the case for Class 2 where Tiles is 0.00
def get_final_avg(row):
    # Average of Tiles and Wood (ignoring 0 values where data doesn't exist)
    h_vals = [h for h in [row['H Tiles'], row['H Wood']] if h > 0]
    t_vals = [t for t in [row['T Tiles'], row['T Wood']] if t > 0]
    return pd.Series([np.mean(h_vals), np.mean(t_vals)])

df_summary[['Final Heads', 'Final Tails']] = df_summary.apply(get_final_avg, axis=1)

avg_curves = {}
for _, row in df_summary.iterrows():
    # We display Tiles and Wood as two points to show the comparison
    avg_curves[row['Coin Class']] = pd.DataFrame({
        'Avg Heads': [row['H Tiles'], row['H Wood']],
        'Avg Tails': [row['T Tiles'], row['T Wood']]
    }, index=['Tiles', 'Wood'])

df_final = df_summary[['Coin Class', 'Final Heads', 'Final Tails']].rename(columns={'Coin Class': 'Class'})

# --- Updated Plotting Logic ---
def plot_in_chunks(data_dict, title_prefix, color_h='orange', color_t='blue', is_avg=False):
    items = list(data_dict.items())
    for i in range(0, len(items), 4):
        chunk = items[i:i+4]
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        axs = axs.flatten()
        
        for j, (key, data) in enumerate(chunk):
            if is_avg:
                # For the Average data (3.2), we use a Bar Chart to compare Surfaces
                x_labels = data.index
                x_pos = np.arange(len(x_labels))
                width = 0.35
                axs[j].bar(x_pos - width/2, data['Avg Heads'], width, label='Heads', color=color_h)
                axs[j].bar(x_pos + width/2, data['Avg Tails'], width, label='Tails', color=color_t)
                axs[j].set_xticks(x_pos)
                axs[j].set_xticklabels(x_labels)
                axs[j].set_title(f'Class {key} Average')
                axs[j].set_ylabel("Percentage (%)")
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

# Graph 1: Individual Coin Progressions
plot_in_chunks(coins_data, "3.1 | Individual Coin Progressions")

# Graph 2: Average Progression by Coin Class (Using the new percentage data)
plot_in_chunks(avg_curves, "3.2 | Average Progression by Coin Class", is_avg=True)

# Graph 3: Line Graph (Progression Across Coin Classes)
plt.figure(figsize=(10, 6))
plt.plot(df_final['Class'], df_final['Final Heads'], marker='o', label='Heads', color='orange', linewidth=2)
plt.plot(df_final['Class'], df_final['Final Tails'], marker='o', label='Tails', color='blue', linewidth=2)
plt.title("Graph 3.3 | Final Progression Across Coin Classes (Line Graph)")
plt.xlabel("Coin Class")
plt.ylabel("Average Final Percentage (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Graph 4: Bar Graph (Average H&T Across Coin Classes)
x = np.arange(len(df_final))
width = 0.35
plt.figure(figsize=(10, 6))
plt.bar(x - width/2, df_final['Final Heads'], width, label='Heads', color='orange')
plt.bar(x + width/2, df_final['Final Tails'], width, label='Tails', color='blue')
plt.xlabel('Coin Class')
plt.ylabel('Average Final Percentage (%)')
plt.title('Graph 4.1 | Average Heads & Tails by Coin Class (Bar Graph)')
plt.xticks(x, df_final['Class'], rotation=45)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.show()