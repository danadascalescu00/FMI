# The-Shootout
This game is a zero-player game, meaning that its evolution is determinated by its initial state, requiring no further input. One interacts with 'The Shootout' by creating an initial configuration and observing how it evolves.

## Description
We have a map on which a number of agents(players, enemies or wizards) are placed. Each agent has an area of visibility in which he can see other agents and a weapon that can fire in a certain way, depending on its type, as well as an armor that can protect the agent or/and influence the way its weapon fire. If the agent has no other agent in his visibility area, then it can change position(the move is made with a distance less than the area of visibility). Some characters, like the wizards, have the power to revive.

The whole action takes place in rounds. In each round, each agent can use the weapon or move on another title, depending on the context in which it is. The game ends when either all enemies are dead, which means the player wins, or the player has no life.
