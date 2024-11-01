#! /bin/bash

source ../bin/activate

if [ $1 == "deploy" ]; then
    echo "Deploying..."
    python -m mkdocs gh-deploy --theme mkdocs
else
    echo "Local build"
    python -m mkdocs build --theme mkdocs
fi
