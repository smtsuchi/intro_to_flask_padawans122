from flask import render_template
from app import app


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

@app.route('/test')
def test_page():
    return {
        'test': 'testing'
    }

@app.route('/test2')
def test_page2():
    return {
        'test': 'testing'
    }