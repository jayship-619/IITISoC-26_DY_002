import numpy as np

from src.network.polymer_chain import PolymerChain


class NetworkBuilder:

    def __init__(
        self,
        box_size=100,
        n_chains=200,
        beads_per_chain=30,
        bond_length=1.0,
        persistence_length=0.8,
        seed=42,
    ):

        np.random.seed(seed)

        self.box=box_size
        self.nchains=n_chains
        self.nbeads=beads_per_chain
        self.bond=bond_length
        self.persist=persistence_length

    def random_vec(self):

        v=np.random.normal(size=3)

        return v/np.linalg.norm(v)

    def generate_chain(self,cid):

        chain=PolymerChain(cid)

        unwrap=np.random.rand(3)*self.box

        direction=self.random_vec()

        image=np.array([0,0,0],dtype=int)

        wrapped=unwrap.copy()

        chain.add_bead(
            wrapped.copy(),
            unwrap.copy(),
            image.copy()
        )

        for _ in range(self.nbeads-1):

            direction+=self.persist*self.random_vec()

            direction/=np.linalg.norm(direction)

            unwrap+=self.bond*direction

            wrapped=unwrap.copy()

            for k in range(3):

                while wrapped[k]<0:

                    wrapped[k]+=self.box

                    image[k]-=1

                while wrapped[k]>=self.box:

                    wrapped[k]-=self.box

                    image[k]+=1

            chain.add_bead(
                wrapped.copy(),
                unwrap.copy(),
                image.copy()
            )

        return chain

    def build(self):

        return [
            self.generate_chain(i)
            for i in range(self.nchains)
        ]