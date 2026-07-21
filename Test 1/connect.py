import matplotlib.pyplot as plt
from collections import defaultdict

def plot_connectivity(data_file="relaxed_gel.data"):
    bond_counts = defaultdict(int)
    
    with open(data_file, 'r') as f:
        lines = f.readlines()
        
    reading_bonds = False
    for line in lines:
        line = line.strip()
        
        # Detect the start of the Bonds section
        if line == "Bonds":
            reading_bonds = True
            continue
        # Stop if we hit a blank line or a new section after Bonds
        elif reading_bonds and (line == "Velocities" or line == "Masses"):
            reading_bonds = False
            
        if reading_bonds and len(line.split()) == 4:
            parts = line.split()
            atom1 = int(parts[2])
            atom2 = int(parts[3])
            
            # Count the bond for both atoms involved
            bond_counts[atom1] += 1
            bond_counts[atom2] += 1
            
    # Tally up how many atoms have 1, 2, 3, etc. bonds
    connectivity_distribution = defaultdict(int)
    for atom, count in bond_counts.items():
        connectivity_distribution[count] += 1
        
    # Prepare data for plotting
    x = sorted(connectivity_distribution.keys())
    y = [connectivity_distribution[k] for k in x]
    
    # Create the Bar Chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x, y, color='tab:blue', edgecolor='black')
    
    # Add numbers on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 10, int(yval), ha='center', va='bottom', fontsize=12)

    plt.title('Connectivity Distribution of Crosslinked Polymer Network', fontsize=14)
    plt.xlabel('Number of Bonds Connected to a Bead', fontsize=12)
    plt.ylabel('Number of Beads', fontsize=12)
    plt.xticks(x)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.show()

# Run the function
plot_connectivity("relaxed_gel.data")