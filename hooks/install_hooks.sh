#!/bin/bash

cd ../.git/hooks/

ln -s -f ../../hooks/commit-msg.py ./commit-msg
ln -s -f ../../hooks/pre-commit.py ./pre-commit
ln -s -f ../../hooks/pre-push.py ./pre-push

chmod +x commit-msg
chmod +x pre-commit
chmod +x pre-push

echo "Install done!"
