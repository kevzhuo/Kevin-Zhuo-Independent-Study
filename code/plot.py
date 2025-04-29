import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('code/data.csv')

# Ensure numerical type for Comparisons column
df['Comparisons'] = pd.to_numeric(df['Comparisons'], errors='coerce')

# Extract unique graphs
graphs = df['Graph'].unique()

# Define hatching patterns (adjust as needed)
hatches = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']

for g in graphs:
    # Filter the data for the current graph
    sub_df = df[df['Graph'] == g]
    
    # Create a subplot for Time vs FASSize
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Pivot the data for Time
    time_data = sub_df.pivot(index='Graph', columns='Method', values='Time')
    time_plot = time_data.plot(kind='bar', ax=ax1)
    ax1.set_title('Time Taken')
    ax1.title.set_size(25)
    ax1.set_ylabel('Time (s)')
    # Remove the graph name from the x-axis
    ax1.set_xlabel('')
    ax1.set_xticks([])  # Removes the tick labels
    
    # Pivot the data for FASSize
    fas_data = sub_df.pivot(index='Graph', columns='Method', values='FASSize')
    fas_plot = fas_data.plot(kind='bar', ax=ax2)
    ax2.set_title('FAS Size')
    ax2.title.set_size(25)
    ax2.set_ylabel('FAS Size')
    # Remove the graph name from the x-axis
    ax2.set_xlabel('')
    ax2.set_xticks([])  # Removes the tick labels
    
    # Apply hatches to the bars in the Time plot
    for i, bar in enumerate(ax1.patches):
        bar.set_hatch(hatches[i % len(hatches)])
    
    # Apply hatches to the bars in the FASSize plot
    for i, bar in enumerate(ax2.patches):
        bar.set_hatch(hatches[i % len(hatches)])
        
    # Set legends
    ax1.legend(title='Method', fontsize=17)
    ax2.legend(title='Method', fontsize=17)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(f'{g}-graph.png', dpi=300)
    plt.close()
