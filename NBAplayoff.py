import pygsheets
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# Authenticate and load data from Google Sheets
gc = pygsheets.authorize(service_file='C:\\Users\\yourb\\OneDrive\\Desktop\\Genetic Algorithim\\Gernetic-algorithims-Proj\\genetic-alg-db30145480cf.json')
sh = gc.open('NBAGA')
wks = sh[0]
df = wks.get_as_df()

# Playoff averages used for fitness function
playoff_averages = {'PPG': 116.6, 'APG': 26.8, 'OREB': 10.4, 'BLKS': 4.7, 'STLS': 7.3, 'DREB': 33.6}

# Fitness function definition
def fitness(team_stats, playoff_averages):
    total_difference = sum(abs(team_stats[stat] - playoff_averages[stat]) for stat in playoff_averages)
    fitness_score = 1 / (1 + total_difference)
    return fitness_score

# Adjustments for crossover and mutation
def crossover_mutation(selected_teams_df):
    for _ in range(len(selected_teams_df) // 2):
        team_a, team_b = random.sample(selected_teams_df.index.tolist(), 2)
        stat_to_swap = random.choice(['PPG', 'APG', 'OREB', 'BLKS', 'STLS', 'DREB'])
        selected_teams_df.at[team_a, stat_to_swap], selected_teams_df.at[team_b, stat_to_swap] = selected_teams_df.at[team_b, stat_to_swap], selected_teams_df.at[team_a, stat_to_swap]
    
    team_to_mutate = random.choice(selected_teams_df.index.tolist())
    stat_to_modify = random.choice(['PPG', 'APG', 'OREB', 'BLKS', 'STLS', 'DREB'])
    mutation_amount = np.random.normal(0, 1)
    selected_teams_df.at[team_to_mutate, stat_to_modify] += mutation_amount
    if selected_teams_df.at[team_to_mutate, stat_to_modify] < 0:
        selected_teams_df.at[team_to_mutate, stat_to_modify] = 0

    return selected_teams_df

def simulate_generations(df, num_generations=200):
    avg_fitness_scores = []  # List to store average fitness scores for each generation
    
    for generation in range(num_generations):
        df['Fitness Score'] = df.apply(lambda row: fitness(row.to_dict(), playoff_averages), axis=1)
        avg_fitness = df['Fitness Score'].mean()
        avg_fitness_scores.append(avg_fitness)  # Append average fitness score to list
        
        selected_teams_df = df.nlargest(8, 'Fitness Score').copy()
        
        selected_teams_df = crossover_mutation(selected_teams_df)
        
        for idx in selected_teams_df.index:
            df.loc[idx] = selected_teams_df.loc[idx]
        
        # Print only the top 3 generations
        if generation >= num_generations - 3:
            print(f"Generation {generation + 1}")
            display_df = selected_teams_df[['Team', 'Fitness Score']].reset_index(drop=True)
            display_df.index += 1  # Adjust index to start from 1 for team numbering
            print(display_df, "\n")
    
    # Plot average fitness scores
    plt.plot(range(1, num_generations + 1), avg_fitness_scores)
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness Score')
    plt.title('Average Fitness Score per Generation')
    plt.grid(True)
    plt.show()

# Call the simulation function
simulate_generations(df)