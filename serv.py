from flask import Flask, render_template_string, request
from movesPMD import queryName

app = Flask(__name__)

# HTML Template with a simple CSS style for the table
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PMDTTRPG moves</title>
    <style>
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>Search moves by pokemon name</h2>
    <form method="POST">
        <input type="text" name="user_text" placeholder="Pokemon name" required>
        <input type="checkbox" name="evolutions" value="yes"> Use evolutions
        <button type="submit">Search moves</button>
    </form>
    {% if query_names %}
        <h3>Matches:</h3>
            {% for el in query_names %}
                {{ el }}{% if not loop.last %} - {% endif %} 
            {% endfor %}
    {% endif %}

    {% if table_data %}
        <h3>Results:</h3>
        <table>
            {% for row in table_data %}
                <tr>
                    {% for cell in row %}
                        <td>{{ cell }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </table>
    {% else %}
        {% if user_text %} <h3>Pokemon not found</h3> {% endif %}
    {% endif %}
<br>
<br>
<p>Source code available at <a href='https://github.com/teo3300/PMDTTRPG-showdown-grabber'>PMDTTRPG-showdown-grabber</a> (couldn't come up with a shorter name)</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    table_data = None
    query_names = None
    user_text = None
    if request.method == "POST":
        user_text = request.form.get("user_text")
        evoLine = request.form.get("evolutions")
        # Triggering your hook function
        query_names, table_data = queryName(user_text, True if evoLine else False)
    
    return render_template_string(HTML_TEMPLATE, table_data=table_data, query_names=query_names, user_text=user_text)

if __name__ == "__main__":
    app.run(debug=True)
