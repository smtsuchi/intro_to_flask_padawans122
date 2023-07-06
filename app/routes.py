from flask import render_template, request, redirect, url_for
from app import app
from .forms import SignUpForm
from .models import User, Post , db

@app.route('/')
def home_page():

    people = ['Shoha', "Sarah", "Edward", "Renat", "Nick", "Paul", 'Troy', "Ousama"]

    pokemons = [{
        'name': 'Pikachu',
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/25.png'
    },{
        'name': "Ditto",
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/132.png'
    }]

    return render_template('index.html', peeps=people, pokemons = pokemons)

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            #add user to database
            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login_page'))
        

    return render_template('signup.html', form = form)


