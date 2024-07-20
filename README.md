# PORTFOLIO_py_sabia_api

An Maritaca.AI interface to execute Sabiá API models.

Implements the methods:

**set_maritacaai_key()**

Set openai key using environment variable MARITACAAI_API_KEY inside .env file

**get_completion(prompt, model, temperature)**

Get models response using MaritacaAI API

Parameters:
- prompt: prompt to send to MaritacaAI
- model: MaritacaAI model to use
- temperature: degree of randomness/creativity of the model's output (0= no randomness, 1=super-random)

Returns
- message: is the response message or the exception code
- finish_reason: is the reason why the message was returned



## Installing

~~~
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt 
~~~

## Running

Create a file named '.env' setting the you MARITACAAI_API_KEY license. i.e.:

~~~bash
MARITACAAI_API_KEY=112........................
~~~
Then:
~~~
export PYTHONPATH=./:$PYTHONPATH
python tests/test_openai_api.py
~~~

