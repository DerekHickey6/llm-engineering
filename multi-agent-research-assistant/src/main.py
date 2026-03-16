from graph import app

result = app.invoke({"topic": "Data Mining"})

print(result['summary'])
