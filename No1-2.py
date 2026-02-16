import pandas as pd
import matplotlib.pyplot as plt


file_path = r'RAW_1-2.csv'
df = pd.read_csv(file_path)

data_limit = 100 
df_subset = df.head(data_limit)
toss_counts = df_subset['Toss #']

# Coin 1 Variables
c1_tails = df_subset['Coin 1 Cumulative Tails']
c1_heads = df_subset['Coin 1 Cumulative Heads']

# Coin 2 Variables
c2_tails = df_subset['Coin 2 Cumulative Tails']
c2_heads = df_subset['Coin 2 Cumulative Heads']

# Combined Variables
combined_tails = df_subset['Combined Cumulative Formula (Tails)']
combined_heads = df_subset['Combined Cumulative Formula (Heads)']



# Visual Graphs
plt.figure(figsize=(12, 8))

# Graph 1: Coin 1 Performance (Top Left)
plt.subplot(2, 2, 1) 
plt.plot(toss_counts, c1_tails, label='C1 Tails', color='blue')
plt.plot(toss_counts, c1_heads, label='C1 Heads', color='orange')
plt.title('Graph 1.1 | Coin 1: Heads vs Tails')
plt.xlabel('Toss #')
plt.ylabel('Count')
plt.legend()
plt.grid(True)

# Graph 2: Coin 2 Performance (Top Right)
plt.subplot(2, 2, 2) 
plt.plot(toss_counts, c2_tails, label='C2 Tails', color='green')
plt.plot(toss_counts, c2_heads, label='C2 Heads', color='red')
plt.title('Graph 1.2 | Coin 2: Heads vs Tails')
plt.xlabel('Toss #')
plt.ylabel('Count')
plt.legend()
plt.grid(True)

# Graph 3: Combined Totals (Bottom)
plt.subplot(2, 1, 2) 
plt.plot(toss_counts, combined_tails, label='Combined Tails', color='purple', linewidth=2)
plt.plot(toss_counts, combined_heads, label='Combined Heads', color='cyan', linewidth=2)
plt.title('Graph 2.1 | Combined Cumulative Results')
plt.xlabel('Toss #')
plt.ylabel('Total Count')
plt.legend()
plt.grid(True)

# Show the graphs
plt.tight_layout()
plt.show()