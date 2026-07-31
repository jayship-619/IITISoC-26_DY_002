import numpy as np


class NetworkValidator:

    def __init__(self, network, crosslinks):

        self.network = network
        self.crosslinks = crosslinks

    def validate(self):

        print()
        print("="*50)
        print("NETWORK VALIDATION")
        print("="*50)

        maxbond = 0.0
        minbond = 1e9

        for chain in self.network:

            for i in range(chain.n_beads-1):

                d = np.linalg.norm(
                    chain.unwrapped_positions[i+1] -
                    chain.unwrapped_positions[i]
                )

                maxbond = max(maxbond,d)
                minbond = min(minbond,d)

        print("Minimum backbone bond :",minbond)
        print("Maximum backbone bond :",maxbond)

        duplicates = len(self.crosslinks) - len(set(self.crosslinks))

        print("Duplicate crosslinks :",duplicates)

        selfcheck = 0

        for c1,b1,c2,b2 in self.crosslinks:

            if c1==c2 and abs(b1-b2)<=2:

                selfcheck += 1

        print("Invalid local crosslinks :",selfcheck)
