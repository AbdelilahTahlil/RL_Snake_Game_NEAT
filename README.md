# Snake game using NeuroEvolution of Augmenting Topologies (NEAT)
*Project in development..*

## Overview

This is a Reinforcement Learning project. The environment is the famous classic 90's "Snake Game".

The purpose of this project is to create an AI agent capable of playing the game using a [genetic algorithm (GA)](https://www.sciencedirect.com/topics/engineering/genetic-algorithm) called NEAT (NeuroEvolution of Augmenting Topologies). This method is developed by [Kenneth O. Stanley](http://www.cs.ucf.edu/~kstanley/). 

In traditional Reinforcement Learning approaches, a topology (or structure) is chosen for the neural network beforehand. It is usually a NN with a single hidden layer. The number of nodes (or neurons) in the hidden layer, the activation functions and the connections structure is a trial-and-error process. Thus, in fixed-topology approaches, the learning stage is to only optimize the connection weights.

However, connection weights are not the only aspect of neural networks that con-
tribute to their behavior. The topology, or structure, of neural networks also affects
their functionality. Thus the purpose of evolving topologies along with weights that NEAT is based on. 

For further informations about the algorithm, see the following papers [1](http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf), [2](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf) and [NEAT-Python documentation page](https://neat-python.readthedocs.io/en/latest/index.html) 


**Note:** I have previously implemented an AI agent able to play the Snake Game which is based on the [Q-Learning algorithm](https://en.wikipedia.org/wiki/Q-learning). See my [Github repository](https://github.com/AbdelilahTahlil/Reinforcement_Learning_Snake_Game) for further details.


## Installation

1. Clone the repository in your target location.
2. Install the requirements.
```
pip install -r requirements.txt
```
3. Run the game. The arguments are optional.
```
python run_game.py
