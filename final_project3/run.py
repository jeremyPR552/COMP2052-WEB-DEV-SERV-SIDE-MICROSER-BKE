from app import create_app

try:
    app = create_app()
except Exception as e:
    print("Error creando la app:", e)
    raise

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

