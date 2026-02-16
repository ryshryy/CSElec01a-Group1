import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Load the data (Same as original) ---
file_floor = r'RAW_5-6.csv'
df_floor = pd.read_csv(file_floor, header=[0, 1])

file_materials = r'RAW_5.csv'
df_materials = pd.read_csv(file_materials)

# --- 2. Data Processing (Same as original) ---
wood_data = df_floor.iloc[:, [2, 3]].dropna()
wood_data.columns = ['Cum Tails', 'Cum Heads']
wood_data['Toss Number'] = range(1, len(wood_data) + 1)

tiles_data = df_floor.iloc[:, [7, 8]].dropna()
tiles_data.columns = ['Cum Tails', 'Cum Heads']
tiles_data['Toss Number'] = range(1, len(tiles_data) + 1)

all_data = df_floor.iloc[:, [17, 18]].dropna()
all_data.columns = ['Cum Tails', 'Cum Heads']
all_data['Toss Number'] = range(1, len(all_data) + 1)

min_len = min(len(wood_data), len(tiles_data))
wood_comp = wood_data.iloc[:min_len]
tiles_comp = tiles_data.iloc[:min_len]

df_clean = df_materials.dropna(subset=['Final Heads', 'Final Tails'])
pivot_data = df_clean.groupby(['Coin Class', 'Surface'])[['Final Heads', 'Final Tails']].sum().unstack('Surface')
pivot_data.columns = [f'{col[0]} {col[1]}' for col in pivot_data.columns]

group_data = df_clean.groupby(['Surface', 'Coin Class'])[['Final Heads', 'Final Tails']].sum()
group_data.index = group_data.index.map(lambda x: f"{x[0]} - {x[1]}")
stacked_data = group_data.transpose()

# --- WINDOW 1: Time Series Progressions (Graphs 1a - 1d) ---
fig1, axs1 = plt.subplots(2, 2, figsize=(14, 10))
axs1 = axs1.flatten()

# 1a. Progression on Wood
axs1[0].plot(wood_data['Toss Number'], wood_data['Cum Heads'], label='Heads', color='orange')
axs1[0].plot(wood_data['Toss Number'], wood_data['Cum Tails'], label='Tails', color='blue')
axs1[0].set_title('5.1 | H&T: Progression on Wood')
axs1[0].set_ylabel('Count')
axs1[0].legend()
axs1[0].grid(True, alpha=0.3)

# 1b. Tiles Progression
axs1[1].plot(tiles_data['Toss Number'], tiles_data['Cum Heads'], label='Heads', color='orange')
axs1[1].plot(tiles_data['Toss Number'], tiles_data['Cum Tails'], label='Tails', color='blue')
axs1[1].set_title('5.2 | H&T: Progression on Tiles')
axs1[1].legend()
axs1[1].grid(True, alpha=0.3)

# 1c. Heads Comparison (Wood vs Tiles)
axs1[2].plot(wood_comp['Toss Number'], wood_comp['Cum Heads'], label='Wood Heads', color='brown')
axs1[2].plot(tiles_comp['Toss Number'], tiles_comp['Cum Heads'], label='Tiles Heads', color='orange')
axs1[2].set_title('5.3 | Heads Comparison: Wood vs Tiles')
axs1[2].set_ylabel('Count')
axs1[2].legend()
axs1[2].grid(True, alpha=0.3)

# 1d. Tails Comparison (Wood vs Tiles)
axs1[3].plot(wood_comp['Toss Number'], wood_comp['Cum Tails'], label='Wood Tails', color='darkblue')
axs1[3].plot(tiles_comp['Toss Number'], tiles_comp['Cum Tails'], label='Tiles Tails', color='cyan')
axs1[3].set_title('5.4 | Tails Comparison: Wood vs Tiles')
axs1[3].legend()
axs1[3].grid(True, alpha=0.3)

fig1.suptitle("5.0 | Surface Comparison Progressions", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# --- WINDOW 2: Summary and Categorical Data (Graphs 2 - 4) ---
fig2 = plt.figure(figsize=(14, 10))

# 2. Heads & Tails by Coin Class (4 Lines) - Taking the top half
ax5 = fig2.add_subplot(2, 1, 1)
ax5.plot(pivot_data.index, pivot_data.get('Final Heads Wood', 0), marker='o', label='Heads (Wood)', color='brown', linewidth=2)
ax5.plot(pivot_data.index, pivot_data.get('Final Tails Wood', 0), marker='o', label='Tails (Wood)', color='darkblue', linewidth=2)
ax5.plot(pivot_data.index, pivot_data.get('Final Heads Tiles', 0), marker='s', label='Heads (Tiles)', color='orange', linewidth=2, linestyle='--')
ax5.plot(pivot_data.index, pivot_data.get('Final Tails Tiles', 0), marker='s', label='Tails (Tiles)', color='cyan', linewidth=2, linestyle='--')
ax5.set_title('5.5 | Heads & Tails by Coin Class (4 Lines)')
ax5.set_xlabel('Coin Class')
ax5.set_ylabel('Final Count')
ax5.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax5.grid(True, alpha=0.3)

# 3. Progression Across All Surfaces - Bottom Left
ax6 = fig2.add_subplot(2, 2, 3)
ax6.plot(all_data['Toss Number'], all_data['Cum Heads'], label='Total Heads', color='orange', linewidth=2)
ax6.plot(all_data['Toss Number'], all_data['Cum Tails'], label='Total Tails', color='blue', linewidth=2)
ax6.set_title('6.1 | Progression Across All Surfaces')
ax6.set_ylabel('Cumulative Count')
ax6.legend()
ax6.grid(True, alpha=0.3)

# 4. Stacked Bar - Bottom Right
ax7 = fig2.add_subplot(2, 2, 4)
stacked_data.plot(kind='bar', stacked=True, ax=ax7, colormap='tab20')
ax7.set_title('6.2 | Total Heads & Tails (Stacked)')
ax7.tick_params(axis='x', rotation=45) # Rotated for better fit
ax7.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small')
ax7.grid(axis='y', alpha=0.3)

fig2.suptitle("Part 2: Categorical and Total Summaries", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()