# Dashboard README.md

Status: In progress

# AlgoQuant Dashboard

# Motivation

The dashboard is hosted on Google Data Studio to display the key metrics and figures of a trading portfolio account. A bot is running 24/7 on cloud and the performance of the bot can be accessed and evaluated through the dashboard.

# Demo / Screenshots

- [Dashboard link](https://datastudio.google.com/s/olg3z5e2JEI)
- [Database link](https://docs.google.com/spreadsheets/d/1hPxsuwdDvpZpQYG2yi_djwcDG1RDAw1RcS-QZ5prUPo/edit?usp=sharing)
- Screenshot
    - Google Data Studio
        
        ![Untitled](Screenshots/Untitled.png)
        
        ![Untitled](Screenshots/Untitled%201.png)
        
    - Google Sheets
        
        ![Untitled](Screenshots/Untitled%202.png)
        
        ![Untitled](Screenshots/Untitled%203.png)
        
        ![Untitled](Screenshots/Untitled%204.png)
        

# Built with

- Python
- Google Sheets
- Google Data Studio
- Cron

# Features

- Auto updates every 30minutes (requires local machine to be on)
- ETL workflow adapted
- Seamless workflow from extracting data, transforming data and loading data into Google Sheets as temporary database before visualizing it using Google Data Studio
- Monitor the cron job using Cronitor and alerts will be sent to the email if the automation fails.

# Installation?

Clone the source locally:

```sql
$ git clone 
$ cd AlgoQuant_dashboard
```

Install project dependencies:

```sql
pip install requirements.txt
```

Start the project:

```sql
$ python src/main.py
```

# License

MIT ©️  [Samuel](https://github.com/chunyip135)