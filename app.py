from flask import Flask, render_template, request
from retrieve_route_data import (get_coordinates_from_place_name as dist_dur_coords,
                                 calculate_fastest_cheapest as calc_fast_cheap,
                                 get_walking_data,
                                 get_cycling_data,
                                 get_transit_data,
                                 AddressIncorrectFormError)
from retrieve_car_data import get_car_data
from retrieve_taxi_data import get_taxi_prices as get_taxi_data
import stats_compile
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main_ex.html')

@app.route('/stats')
def stats():
    hours_data = [stats_compile.Day('bolt').output, stats_compile.Day('uklon').output]
    days_data = [stats_compile.Week('bolt').output, stats_compile.Week('uklon').output]
    print(days_data)
    return render_template("stats.html", hours=hours_data, days=days_data)

@app.route('/result', methods=["POST"])
def result():

    final_data = {}

    origin = request.form.get("origin")
    origin_coords = dist_dur_coords(origin)
    destination = request.form.get("destination")
    destination_coords = dist_dur_coords(destination)
    map_coords = (origin_coords, destination_coords)

    selected_modes = request.form.getlist("mode")

    modes = {'select_taxi' : get_taxi_data,
             'select_cycling' : get_cycling_data,
             'select_walking' : get_walking_data,
             'select_transit' : get_transit_data}

    for mode in selected_modes:
        final_data.update(modes[mode](origin, destination))
    if request.form.get("spec_list"):
        car_id = request.form.get("spec_list")
        selected_modes.append("select_driving")
        final_data.update(get_car_data(origin, destination, car_id))

    cheapest_fastest_data = calc_fast_cheap(final_data)
    #print(cheapest_fastest_data)
    #print(final_data)

    return render_template("secondary.html",
                           result=final_data, selected_modes=selected_modes,
                           map_coords=map_coords, cheapest_fastest=cheapest_fastest_data)

    # except AddressIncorrectFormError as e:
    #     error_msg = e.args[0]
    #     return render_template("error.html", error_msg=error_msg)
    # except:
    #     error_msg = "something went wrong"
    #     return render_template("error.html", error_msg=error_msg)


if __name__ == "__main__":

    app.run(host='0.0.0.0',port=8001)