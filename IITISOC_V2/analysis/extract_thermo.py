import pandas as pd

rows=[]

capture=False

with open("log.lammps") as f:

    for line in f:

        if line.startswith("Step"):

            capture=True

            continue

        if capture:

            if line.startswith("Loop"):

                break

            s=line.split()

            if len(s)==10:

                rows.append(s)

columns=[
"Step",
"Temp",
"Press",
"PE",
"KE",
"Etotal",
"Ebond",
"Eangle",
"Evdwl",
"Density"
]

df=pd.DataFrame(rows,columns=columns)

df=df.astype(float)

df.to_csv("Results/Tables/thermo.csv",index=False)

print(df.head())

print(df.tail())
