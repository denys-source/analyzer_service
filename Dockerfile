FROM python:3.11.0

ENV PYTHONUNBUFFERED=1

WORKDIR /code/

COPY pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install uv

RUN uv venv .venv
ENV PATH="/code/.venv/bin:${PATH}"

COPY app/ ./app/

RUN uv pip install -e .

RUN python -m spacy download en_core_web_lg

ARG DEV=false
RUN if [ "$DEV" = "true" ] ; then uv pip install -e .[dev] ; fi

ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
