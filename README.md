# MathGPT

## Install

~~~
//python version 3.11.5
git clone https://github.com/ZenoCoding/MathGPT.git
cd MathGPT
python -m venv venv
source venv/bin/activate
pip install aiohttp==3.8.5 openai==0.28.1 discord==2.3.2 sympy==1.12 jsonlines==4.0.0
pip install git+https://github.com/Pycord-Development/pycord


export OPENAI_API_KEY="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"
export DISCORD_ID="945903743319293992"
~~~

## Abstract
Large language models are remarkable in many ways, especially when emulating many aspects of human-like speech and writing. However, a field that large language models such as GPT-3 or OPTT struggle in is the field of mathematics. LLMs (also know as Large Language Models) were never intended to be precise in mathematical calculations, but rather to understand concepts and relationships between words. We aim to improve upon this; through the combination of CAS (Computer Algebra System) and an LLM. We can transform the more complex humanlike language used to denote many mathematical problems into an expression the CAS is able to interpret, solving problems that CAS nor GPT-3 are able to understand alone.

Read the full paper here -> [MathGPT - An Exploration Into the Field of Mathematics with LLMs](https://docs.google.com/document/d/1JSRx4ArHnNyaepVnzyYovBO3OSKnY3CnBVWS2KlXrAw/edit?usp=sharing)