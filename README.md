# NBA_data_stats

### Description

This project was created with the aim to analyze and format data from an NBA basketball game contained in a CSV file.

### The process

---

- Open and access the CSV file, separating each column by the delimiter "|".
- Determine if the current team is the away team.
- Use regular expressions to fetch data for each acronym that is not a formula.
- Count the occurrences of each acronym from the regex data and identify the player's name.
- Return a hash of data for each player in each team, organized by team.
- Using the dictionary with player names and data, return the data in a formatted manner.
