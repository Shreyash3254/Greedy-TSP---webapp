import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend suitable for Flask


from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)

# Distance function
def distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Greedy TSP algorithm
def greedy_tsp(cities):
    city_names = list(cities.keys())
    start_city = city_names[0]
    unvisited = set(city_names)
    path = [start_city]
    unvisited.remove(start_city)
    total_distance = 0
    current_city = start_city

    while unvisited:
        nearest_city = min(unvisited, key=lambda city: distance(cities[current_city], cities[city]))
        total_distance += distance(cities[current_city], cities[nearest_city])
        path.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city

    total_distance += distance(cities[current_city], cities[start_city])
    path.append(start_city)
    return path, total_distance

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city_names = request.form.getlist("city_name")
        x_coords = request.form.getlist("x_coord")
        y_coords = request.form.getlist("y_coord")

        cities = {name: (float(x), float(y)) for name, x, y in zip(city_names, x_coords, y_coords)}
        path, total_dist = greedy_tsp(cities)

        # Plot path
        x = [cities[city][0] for city in path]
        y = [cities[city][1] for city in path]
        plt.figure(figsize=(6,6))
        plt.plot(x, y, marker='o', color='blue')
        for i, city in enumerate(path):
            plt.text(x[i]+0.1, y[i]+0.1, city)
        plt.title("Greedy TSP Path")

        # Convert plot to PNG
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_data = base64.b64encode(buf.getvalue()).decode()
        plt.close()

        return render_template("index.html", path=path, total_dist=total_dist, plot_url=img_data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
