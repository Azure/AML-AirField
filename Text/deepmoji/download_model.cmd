@echo off

if not exist .\torchmoji\ (
    echo.
    echo Downloading Model
    echo.

    REM Clone torchMoji repo
    git clone https://github.com/huggingface/torchMoji.git ./torchmoji_repo

    REM Copy model related files over to the model directory
    if not exist .\torchmoji\ mkdir torchmoji
    copy .\torchmoji_repo\torchmoji\attlayer.py .\torchmoji\
    copy .\torchmoji_repo\torchmoji\create_vocab.py .\torchmoji\
    copy .\torchmoji_repo\torchmoji\filter_utils.py .\torchmoji\
    copy .\torchmoji_repo\torchmoji\global_variables.py .\torchmoji\
    copy .\torchmoji_repo\torchmoji\lstm.py .\torchmoji\
    copy .\torchmoji_repo\torchmoji\model_def.py .\torchmoji\
    copy .\torchmoji_repo\torchmoji\sentence_tokenizer.py .\torchmoji\
    copy .\torchmoji_repo\torchmoji\tokenizer.py .\torchmoji\
    copy .\torchmoji_repo\torchmoji\word_generator.py .\torchmoji\
    copy .\torchmoji_repo\LICENSE .\torchmoji\

    if not exist .\data\ mkdir data
    copy .\torchmoji_repo\data\emoji_codes.json .\data\
    copy .\torchmoji_repo\data\filtering\wanted_emojis.csv .\data\

    if not exist .\model\ mkdir model
    copy .\torchmoji_repo\model\vocabulary.json .\model\
    
    if not exist model\pytorch_model.bin (
        REM Download model weights
        powershell $ProgressPreference = 'SilentlyContinue' ; Invoke-WebRequest -OutFile model\pytorch_model.bin https://www.dropbox.com/s/q8lax9ary32c7t9/pytorch_model.bin?raw=1
    )

    echo.
    type legal.notice
    echo.
    pause    
) else (
    exit /b 0
)
