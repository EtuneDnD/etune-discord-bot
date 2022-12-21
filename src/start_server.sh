cd $ETUNE_PATH/src
export PYTHONPATH="$PYTHONPATH:$ETUNE_PATH"
source ../bin/activate
python3.11 main/main_server.py