# Use an official Python runtime as a parent image
FROM python:3.10.2

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV production

# Set working directory
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /code/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /code/

# Run database migrations
RUN python manage.py migrate

# Run the test suite
RUN python manage.py test

# Expose the default Django port
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
