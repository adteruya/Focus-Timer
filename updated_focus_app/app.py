from flask import Flask, render_template, request, redirect
import requests
import json

app = Flask(__name__)

# Global values
focus_options = [15, 25, 50]
break_options = [3, 5, 10]
focus_time = 25
break_time = 5
focus_remaining = None
break_remaining = None
image_list = []


def get_image():
    # Microservice Function - calls microservice and stores the images retrieved
    global image_list
    url = 'https://image-microservice-us.herokuapp.com/background'
    for i in range(5):
        data = requests.get(url=url)
        image_url = data.text
        image_list.append(image_url)


@app.route('/', methods=['GET', 'POST'])
def home():
    # Variable that will be accessed and modified
    global focus_time, break_time
    # Updates the focus and/or break times based on the buttons clicked on the front-end
    if request.method == 'POST':
        focus_value = request.form.get('set-focus')
        break_value = request.form.get('set-break')
        if focus_value is not None:
            focus_time = int(focus_value)
            return redirect('/')
        if break_value is not None:
            break_time = int(break_value)
            return redirect('/')
    return render_template('index.html', focus_options=focus_options, break_options=break_options,
                           current_focus=focus_time, current_break=break_time)


@app.route('/timer', methods=['GET', 'POST'])
def timer():
    global focus_remaining, break_remaining, image_list
    # Add images using the image microservice
    get_image()
    focus_remaining = focus_time * 60 * 1000
    break_remaining = break_time * 60 * 1000
    return render_template('timer.html', focus_time=json.dumps(focus_remaining),
                           break_time=json.dumps(break_remaining), images=json.dumps(image_list))


if __name__ == '__main__':
    app.run(debug=True)
