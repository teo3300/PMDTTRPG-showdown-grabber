from flask import Flask, render_template, request
from movesPMD import queryName

app = Flask(__name__)

# Clean output
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.route("/", methods=["GET", "POST"])
def index():
    table_data = None
    query_names = None
    user_text = None
    type_column_idx = None
    category_column_idx = None
    if request.method == "POST":
        user_text = request.form.get("user_text")
        evoLine = request.form.get("evolutions")
        query_names, table_data = queryName(user_text, True if evoLine else False)
        if table_data:
            type_column_idx = table_data[0].index("[Type]")
            category_column_idx = table_data[0].index("[Category]")
    
    return render_template('index.html',
                                  table_data            =   table_data,
                                  query_names           =   query_names,
                                  user_text             =   user_text,
                                  type_column_idx       =   type_column_idx,
                                  category_column_idx   =   category_column_idx)

if __name__ == "__main__":
    app.run(debug=True)
