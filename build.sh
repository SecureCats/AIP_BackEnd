# build front end resources and copy them to django site

# set -e

cd frontend
yarn run build

rm  -r ../aipsite/static/login/{js,css,img}

cp dist/index.html ../aipsite/templates/login/index.html

cp_all () {
    for var in $@;
    do
        cp -r dist/$var ../aipsite/static/login/$var
    done
}

cp_all css js img

cp dist/favicon.ico ../aipsite/static/login/
