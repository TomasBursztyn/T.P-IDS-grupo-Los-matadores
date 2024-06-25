# instrucciones para correr el front (un boceto inicial)

FRONT_FOLDER=./Front
FRONTEND_PORT=5000

# o algo por el estilo si el usuario no tiene pip instalado
sudo apt install python3-pip

# instala pipenv por si acaso
pip install pipenv --user

# se mueve a la carpeta front
cd $FRONT_FOLDER

# instalo las dependencias del proyecto administrado por pipenv
pipenv install

# entro a la shell del proyecto
pipenv shell

# esto hay que pegarlo manualmente porque "pipenv shell" crea una sub shell
# corro el front con el --debug activado para actualizar los cambios
# ojo esto solo para desarrollo (no meter en produccion con --debug activado)
pipenv run flask run --debug -p $FRONTEND_PORT