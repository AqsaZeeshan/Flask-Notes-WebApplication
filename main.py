from Website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # the line debug = true just means that whenevr a changeis made to app its going to run servr again
