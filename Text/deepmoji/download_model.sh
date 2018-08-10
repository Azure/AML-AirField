set -e

if [ ! -d ./torchmoji ]; then
    echo ""
    echo Downloading Model
    echo ""

    # Clone torchMoji repo
    git clone https://github.com/huggingface/torchMoji.git ./torchmoji_repo

    # Copy model related files over to the model directory
    mkdir -p torchmoji
    cp ./torchmoji_repo/torchmoji/attlayer.py ./torchmoji/
    cp ./torchmoji_repo/torchmoji/create_vocab.py ./torchmoji/
    cp ./torchmoji_repo/torchmoji/filter_utils.py ./torchmoji/
    cp ./torchmoji_repo/torchmoji/global_variables.py ./torchmoji/
    cp ./torchmoji_repo/torchmoji/lstm.py ./torchmoji/
    cp ./torchmoji_repo/torchmoji/model_def.py ./torchmoji/
    cp ./torchmoji_repo/torchmoji/sentence_tokenizer.py ./torchmoji/
    cp ./torchmoji_repo/torchmoji/tokenizer.py ./torchmoji/
    cp ./torchmoji_repo/torchmoji/word_generator.py ./torchmoji/
    cp ./torchmoji_repo/LICENSE ./torchmoji/

    mkdir -p data
    cp ./torchmoji_repo/data/emoji_codes.json ./data/
    cp ./torchmoji_repo/data/filtering/wanted_emojis.csv ./data/

    mkdir -p model
    cp ./torchmoji_repo/model/vocabulary.json ./model/

    echo ""
    cat legal.notice
    echo ""
    read -n1 -s -r -p "Press any key to continue . . ."
    echo ""
fi

if [ ! -f model/pytorch_model.bin ]; then
    # Download model weights
    wget -nc https://www.dropbox.com/s/q8lax9ary32c7t9/pytorch_model.bin?dl=0# -O model/pytorch_model.bin
fi
