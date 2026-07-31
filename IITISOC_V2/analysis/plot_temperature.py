import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("Results/Tables/thermo.csv")

plt.figure(figsize=(8,5))

plt.plot(df.Step,df.PE,lw=2)

plt.xlabel("Step")

plt.ylabel("Potential Energy")

plt.title("Potential Energy Relaxation")

plt.grid()

plt.tight_layout()

plt.savefig("Results/Plots/potential_energy.png",dpi=300)

plt.show()
