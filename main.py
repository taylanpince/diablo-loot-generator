from flask import request, render_template, Flask

from database import generate_random_weapon, generate_random_armor

app = Flask(__name__)

@app.route('/')
def generate_loot():
    weapon = generate_random_weapon()
    return render_template('loot.html', items=[weapon])
