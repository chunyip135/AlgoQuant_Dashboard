import pygsheets


client = pygsheets.authorize(service_file='algoquant-351309-ae021cd7392e.json')

sh = client.open_by_key('1hPxsuwdDvpZpQYG2yi_djwcDG1RDAw1RcS-QZ5prUPo')

wk1 = sh[0] # open first worksheet of spreadsheet or sh.sheet1


