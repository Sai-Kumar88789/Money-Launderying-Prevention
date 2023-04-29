# Money-Launderying-Prevention

### Problem Statement
Through machine learning we can identify the patterns for every consumer that may lead to money laundering like transferring money to foreign banks, big deposits, transaction
patterns etc.

### Solution Proposed 
The Project is  designed to help prevent the illegal practice of money laundering using the Bitcoin blockchain transaction data. This project is aimed at providing a solution to the growing concern of illicit activities and financial crimes on the blockchain network.

## Tech Stack Used
1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions

## How to run?
Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.

## Data Collections

Collect the data from the below link
```bash 
https://www.kaggle.com/datasets/ellipticco/elliptic-data-set
```
## User Interface
![image](https://drive.google.com/file/d/1znTNd_ZK2taiXhR3Ybq5HUuXlEXU9rwv/view?usp=sharing )
## Project Archietecture
![image](https://user-images.githubusercontent.com/57321948/193536768-ae704adc-32d9-4c6c-b234-79c152f756c5.png)


## Deployment Archietecture
![image](https://user-images.githubusercontent.com/57321948/193536973-4530fe7d-5509-4609-bfd2-cd702fc82423.png)

### Step 1: Clone the repository
```bash
git clone https://github.com/SaiKumarOfficial/Money-Launderying-Prevention.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n money python=3.7.6 -y
```

```bash
conda activate money
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```
### Step 4 - Export the environment variable
```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

export MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.edjcajk.mongodb.net/?retryWrites=true&w=majority"

```

### Step 5 - Run the application server
```bash
python main.py
```

### Step 6. Train application
```bash
http://localhost:8080/train

```

### Step 7. Prediction application
```bash
http://localhost:8080/predict

```
## Run locally

1. Check if the Dockerfile is available in the project directory

2. Build the Docker image
```
docker build --build-arg AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> --build-arg AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> --build-arg AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION> --build-arg MONGODB_URL=<MONGODB_URL> . 

```

3. Run the Docker image
```
docker run -d -p 8080:8080 <IMAGE_NAME>
```

To run the project  first execute the below commmand.
MONGO DB URL: 
```
mongodb+srv://<username>:<password>@cluster0.edjcajk.mongodb.net/?retryWrites=true&w=majority
```

then run 
```
python main.py
```